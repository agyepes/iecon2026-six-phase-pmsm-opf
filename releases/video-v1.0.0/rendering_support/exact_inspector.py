"""Probe and fully decode an MP4, checking timing, fidelity and frame order."""
import argparse, hashlib, json, math, os, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from PIL import Image

def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p, value): Path(p).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()
def mse(a,b):
    diff = np.subtract(a,b,dtype=np.float32)
    return float(np.mean(np.square(diff),dtype=np.float64))
def psnr(error): return 100.0 if error == 0 else 10*math.log10(255**2/error)

parser=argparse.ArgumentParser()
parser.add_argument('--recording-folder',required=True)
parser.add_argument('--selection')
args=parser.parse_args()
OUT=Path(args.recording_folder).resolve(strict=True)
assert 'onedrive' not in str(OUT).lower()
R=read(OUT/'recording_review.json')
movie=Path(R['encoded_file']).resolve(strict=True)
assert sha(movie)==R['encoded_file_SHA256']
count=R['frame_count']; width,height=R['image_dimensions_px']
ffprobe=shutil.which('ffprobe');ffmpeg=shutil.which('ffmpeg')
hidden=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
def invoke(command):
    p=subprocess.run(command,capture_output=True,creationflags=hidden,timeout=86400,check=False)
    assert p.returncode==0,p.stderr.decode('utf-8',errors='replace')
    return p.stdout
probe=json.loads(invoke([ffprobe,'-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]))
write(OUT/'encoded_probe.json',probe)
checks=[]
def check(name,condition,**evidence):
    assert bool(condition),name
    checks.append({'name':name,'pass':True,**evidence})
streams=probe['streams']
check('exactly one video stream and no audio',len(streams)==1 and streams[0]['codec_type']=='video')
stream=streams[0]
check('H264 MP4 with broadly supported 420 pixel format',stream['codec_name']=='h264' and stream['pix_fmt']=='yuv420p' and 'mp4' in probe['format']['format_name'])
check('fixed dimensions preserved without crop or resize',(stream['width'],stream['height'])==(width,height)==(2560,1440))
check('exactly 30 frames per second',stream['r_frame_rate']==stream['avg_frame_rate']=='30/1')
check('exact frame counts in header and actual decode',int(stream['nb_frames'])==int(stream['nb_read_frames'])==count)
check('exact encoded duration',float(stream['duration'])==float(probe['format']['duration'])==count/30)
check('time base represents every frame exactly',stream['time_base']=='1/30000')
check('colour signalling matches RGB conversion',stream['color_space']==stream['color_primaries']==stream['color_transfer']=='bt709' and stream['color_range']=='tv')
timing=json.loads(invoke([ffprobe,'-v','error','-select_streams','v:0','-show_frames',
    '-show_entries','frame=pts,best_effort_timestamp_time,duration_time,width,height','-of','json',str(movie)]))
write(OUT/'encoded_frame_timestamps.json',timing)
F=timing['frames']
check('every encoded presentation timestamp present',len(F)==count)
check('presentation timestamps start at zero and advance exactly 1/30 s',[f['pts'] for f in F]==[k*1000 for k in range(count)])
check('every decoded frame has the fixed dimensions',all((f['width'],f['height'])==(width,height) for f in F))
check('final frame completes exact playback duration',F[-1]['pts']==(count-1)*1000 and abs(float(F[-1]['duration_time'])-1/30)<5e-7)

records=R['records']
def first_cross(key,limit):
    values=[r['live'][key] for r in records]
    candidates=[i+1 for i,v in enumerate(values) if v>limit]
    assert candidates,key
    return candidates[0]
vfirst=first_cross('peak_line_voltage_V',290)
ifirst=first_cross('peak_phase_current_A',4.34)
lookup=[r['planned_full_frame_1based'] for r in records]
selection=read(args.selection if args.selection else OUT.parent/'prepared_records/IECON2026_OPFa_H21_video_selection.json')
sources=np.array([r['source_index_1based'] for r in records])
points={'start':1,'final':count}
for key,first in [('voltage',vfirst),('current',ifirst)]:
    for delta in [-2,-1,0,1,2]:
        at=first+delta
        if 1<=at<=count:points[key+('_before_%d'%(-delta) if delta<0 else ('_after_%d'%delta if delta>0 else '_first_displayed_excess'))]=at
for key,source in selection['constraint_transition_source_indices'].items():
    points['nearest_'+key]=int(np.argmin(np.abs(sources-source)))+1
for key,source in selection['original_global_peak_source_indices'].items():
    points['nearest_global_'+key+'_peak']=int(np.argmin(np.abs(sources-source)))+1
floor_source=259715
nearest_floor=int(np.searchsorted(sources,floor_source))
for index in [nearest_floor-1,nearest_floor]:
    if 0<=index<count:points['lookup_floor_'+('below' if sources[index]<floor_source else 'above')]=index+1
points['penultimate']=count-1
selected=sorted(set(points.values()))
decoded_dir=OUT/'decoded_inspection';decoded_dir.mkdir(exist_ok=True)
frame_bytes=width*height*3
quality=[];started=time.monotonic()
title_box=(int(width*.20),int(height*.010),int(width*.80),int(height*.051))
identity_box=(int(width*.061),int(height*.07),int(width*.45),int(height*.945))
roi_boxes={
    'title_and_operating_point':title_box,
    'waveforms':(int(width*.505),int(height*.07),int(width*.90),int(height*.945)),
    'progressive_plots_and_labels':(int(width*.005),int(height*.07),int(width*.45),int(height*.995)),
    'outside_measurement_rails':(int(width*.912),int(height*.07),int(width*.998),int(height*.94))
}
command=[ffmpeg,'-hide_banner','-v','error','-nostdin','-threads','4','-i',str(movie),
    '-map','0:v:0','-an','-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
reference_command=[ffmpeg,'-hide_banner','-v','error','-nostdin','-threads','4',
    '-framerate','30','-start_number','1','-i',str(OUT/'rendered_frames/frame_%04d.png'),
    '-frames:v',str(count),'-vf',
    'scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p,scale=in_range=tv:out_range=pc:in_color_matrix=bt709,format=rgb24',
    '-fps_mode','passthrough','-pix_fmt','rgb24','-f','rawvideo','pipe:1']
with (OUT/'full_decode_stderr.log').open('wb') as err,(OUT/'colour_reference_stderr.log').open('wb') as referr:
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=err,creationflags=hidden)
    reference_process=subprocess.Popen(reference_command,stdout=subprocess.PIPE,stderr=referr,creationflags=hidden)
    for k in range(1,count+1):
        raw=process.stdout.read(frame_bytes)
        check('complete decoded frame %d'%k,len(raw)==frame_bytes)
        decoded=np.frombuffer(raw,dtype=np.uint8).reshape(height,width,3)
        reference_raw=reference_process.stdout.read(frame_bytes)
        check('complete lossless format-conversion reference frame %d'%k,len(reference_raw)==frame_bytes)
        reference=np.frombuffer(reference_raw,dtype=np.uint8).reshape(height,width,3)
        source_png=OUT/'rendered_frames'/('frame_%04d.png'%k)
        check('original raster hash bound for frame %d'%k,sha(source_png)==records[k-1]['image_SHA256'])
        with Image.open(source_png) as im:original=np.asarray(im.convert('RGB'))
        global_error=mse(decoded,original)
        compression_error=mse(decoded,reference)
        roi_errors={}
        compression_roi_errors={}
        for key,(x0,y0,x1,y1) in roi_boxes.items():
            roi_errors[key]=mse(decoded[y0:y1,x0:x1],original[y0:y1,x0:x1])
            compression_roi_errors[key]=mse(decoded[y0:y1,x0:x1],reference[y0:y1,x0:x1])
        x0,y0,x1,y1=title_box
        current_error=roi_errors['title_and_operating_point']
        neighbor_errors={}
        identical_neighbor_titles=[]
        ix0,iy0,ix1,iy1=identity_box
        trace_error=mse(decoded[iy0:iy1,ix0:ix1],original[iy0:iy1,ix0:ix1])
        neighbor_trace_errors={}
        for j in [k-1,k+1]:
            if not 1<=j<=count:continue
            with Image.open(OUT/'rendered_frames'/('frame_%04d.png'%j)) as neighbor:
                neighbor_rgb=neighbor.convert('RGB')
                crop=np.asarray(neighbor_rgb.crop(title_box))
                trace_crop=np.asarray(neighbor_rgb.crop(identity_box))
            neighbor_errors[str(j)]=mse(decoded[y0:y1,x0:x1],crop)
            neighbor_trace_errors[str(j)]=mse(decoded[iy0:iy1,ix0:ix1],trace_crop)
            if np.array_equal(crop,original[y0:y1,x0:x1]):identical_neighbor_titles.append(str(j))
        check('encoded heading matches all distinct neighboring headings: %d'%k,
              all(current_error<v for j,v in neighbor_errors.items() if j not in identical_neighbor_titles),
              expected_title_MSE=current_error,neighbor_title_MSE=neighbor_errors,
              identical_neighbor_titles=identical_neighbor_titles)
        check('encoded progress traces identify this frame against both neighbors: %d'%k,
              all(trace_error<v for v in neighbor_trace_errors.values()),
              expected_progressive_trace_MSE=trace_error,neighbor_progressive_trace_MSE=neighbor_trace_errors)
        check('high fidelity relative to lossless standard-colour conversion for frame %d'%k,psnr(compression_error)>45,
              compression_only_full_frame_PSNR_dB=psnr(compression_error),criterion_minimum_dB=45)
        check('legends and numbers retain raster fidelity for frame %d'%k,
              all(psnr(v)>43 for v in compression_roi_errors.values()),
              compression_only_ROI_PSNR_dB={key:psnr(v) for key,v in compression_roi_errors.items()})
        item={'frame_1based':k,'source_index_1based':records[k-1]['source_index_1based'],
            'decoded_RGB_SHA256':hashlib.sha256(raw).hexdigest(),
            'full_frame_PSNR_dB':psnr(global_error),'ROI_PSNR_dB':{key:psnr(v) for key,v in roi_errors.items()},
            'compression_only_full_frame_PSNR_dB':psnr(compression_error),
            'compression_only_ROI_PSNR_dB':{key:psnr(v) for key,v in compression_roi_errors.items()},
            'expected_title_MSE':current_error,'neighbor_title_MSE':neighbor_errors,
            'identical_neighbor_titles':identical_neighbor_titles,
            'expected_progressive_trace_MSE':trace_error,'neighbor_progressive_trace_MSE':neighbor_trace_errors}
        if k in selected:
            filename='encoded_frame_%04d.png'%k
            Image.fromarray(decoded).save(decoded_dir/filename)
            item['decoded_inspection_image']=filename
            item['decoded_inspection_SHA256']=sha(decoded_dir/filename)
        quality.append(item)
        write(OUT/'decode_progress.json',{'completed_frames':k,'frame_count':count,'all_completed_frames_passed':True,
            'elapsed_seconds':time.monotonic()-started})
        if k%30==0 or k==count:print('PASS fully decoded and matched encoded frames %d/%d.'%(k,count),flush=True)
    trailing=process.stdout.read(1);process.stdout.close()
    exit_code=process.wait(timeout=86400)
    reference_trailing=reference_process.stdout.read(1);reference_process.stdout.close()
    reference_exit_code=reference_process.wait(timeout=86400)
check('no extra decoded frames',trailing==b'')
check('full decoder completed without errors',exit_code==0 and (OUT/'full_decode_stderr.log').stat().st_size==0)
check('lossless format-conversion reference completed with exact count',reference_trailing==b'' and reference_exit_code==0 and (OUT/'colour_reference_stderr.log').stat().st_size==0)
tiles=[]
for k in selected:
    with Image.open(decoded_dir/('encoded_frame_%04d.png'%k)) as im:
        tiles.append(im.convert('RGB').resize((1280,720),Image.Resampling.LANCZOS))
sheet=Image.new('RGB',(3840,720*math.ceil(len(tiles)/3)),'white')
for index,tile in enumerate(tiles):sheet.paste(tile,((index%3)*1280,(index//3)*720))
sheet.save(OUT/'encoded_inspection_contact_sheet.png')
review={'result':'PASS_ENCODED_FORMAT_TIMING_COMPLETE_DECODE_AND_FRAME_IDENTITIES',
    'inspector_source_SHA256':sha(__file__),
    'created_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'stage':R['stage'],
    'encoded_file':str(movie),'encoded_file_SHA256':sha(movie),'frame_count':count,
    'dimensions_px':[width,height],'frames_per_second':30,'duration_seconds':count/30,
    'codec':stream['codec_name'],'profile':stream['profile'],'level':stream['level'],
    'pixel_format':stream['pix_fmt'],'colour_space':stream['color_space'],
    'checks_passed':len(checks),'checks':checks,'complete_decode_exit_code':exit_code,
    'decode_command_arguments':command,'quality_and_identity_per_frame':quality,
    'lossless_colour_reference_command_arguments':reference_command,
    'minimum_compression_only_full_frame_PSNR_dB':min(q['compression_only_full_frame_PSNR_dB'] for q in quality),
    'minimum_compression_only_ROI_PSNR_dB':{key:min(q['compression_only_ROI_PSNR_dB'][key] for q in quality) for key in roi_boxes},
    'minimum_full_frame_PSNR_dB':min(q['full_frame_PSNR_dB'] for q in quality),
    'minimum_ROI_PSNR_dB':{key:min(q['ROI_PSNR_dB'][key] for q in quality) for key in roi_boxes},
    'frame_identity_matched_at_every_frame':True,
    'frame_identity_method':'Every decoded frame must match its progressive traces and moving markers more closely than either adjacent reference; distinct headings are checked additionally. Identical shortened headings are recorded explicitly.',
    'first_displayed_voltage_excess_frame_1based':vfirst,'first_displayed_current_excess_frame_1based':ifirst,
    'inspection_points':points,'decoded_inspection_frame_indices_1based':selected,
    'contact_sheet_SHA256':sha(OUT/'encoded_inspection_contact_sheet.png'),
    'scientific_limit_compliance':'FAIL_CURRENT_AND_VOLTAGE','recording_ready_with_all_limits_claim':False,
    'encoded_video_created':True,'visual_inspection_pending':True}
write(OUT/'encoded_verification.json',review)
print(json.dumps({k:v for k,v in review.items() if k not in ['checks','quality_and_identity_per_frame','decode_command_arguments']},indent=2))
