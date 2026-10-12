"""Private Python support embedded into the single MATLAB entry file."""
import argparse,csv,hashlib,importlib.util,json,os,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
from scipy.io import loadmat
from PIL import Image
from threadpoolctl import threadpool_limits

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def write(p,v):Path(p).write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def module(p):
    spec=importlib.util.spec_from_file_location('packaged_exact_layout',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def run(command,stdout=None,stderr=None):
    return subprocess.run(command,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0,timeout=86400)
parser=argparse.ArgumentParser()
parser.add_argument('--job',required=True)
a=parser.parse_args()
J=read(a.job);P=Path(J['package_folder']).resolve(strict=True);O=Path(J['output_folder']).resolve(strict=True)
assert 'onedrive' not in str(O).lower()
D=read(O/'runtime_definition.json')
strict=bool(J['strict_reference'])
threadpool_limits(limits=1)
support=O/'support';C=D['layout_config']
renderer=module(support/'exact_layout.py')
if J['action']=='preflight':
    from importlib.metadata import version
    actual={'python':sys.version.split()[0],**{name:version(dist) for name,dist in [
        ('numpy','numpy'),('scipy','scipy'),('matplotlib','matplotlib'),('pillow','Pillow'),('threadpoolctl','threadpoolctl')]}}
    if strict:assert actual==D['reference_runtime']['python_packages'],(actual,D['reference_runtime']['python_packages'])
    renderer.configure_style(C,O)
    fp=renderer.matplotlib.font_manager.findfont(renderer.matplotlib.font_manager.FontProperties(family=C['font_family']),fallback_to_default=False)
    if strict:assert sha(fp)==D['reference_runtime']['regular_font_sha256'],'Reference font differs'
    executables={}
    for key in ['ffmpeg','ffprobe']:
        explicit=J.get(key+'_path','')
        actual_path=Path(explicit).resolve(strict=True) if explicit else Path(shutil.which(key) or '')
        assert actual_path.is_file(),key+' is unavailable; supply an executable or add its folder to PATH'
        executables[key]=str(actual_path.resolve())
    for key,path in list(executables.items()):
        result=subprocess.run([path,'-version'],capture_output=True,creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0,timeout=3600)
        assert result.returncode==0
        first=result.stdout.decode('utf-8').splitlines()[0]
        if strict:assert first==D['reference_runtime'][key+'_version_line'],first
        executables[key+'_version_line']=first
    write(O/'dependency_preflight.json',{'result':'PASS_PACKAGE_DEPENDENCIES','python_packages':actual,
        'python_executable':sys.executable,'regular_font_path':fp,'regular_font_sha256':sha(fp),**executables,
        'strict_reference':strict,'no_visible_window_or_GUI_backend':True})
    print('PASS: Python, reference font, FFmpeg and FFprobe preflight.',flush=True)
elif J['action']=='batch':
    renderer.configure_style(C,O)
    data=loadmat(O/'rebuilt_plot_context.mat',simplify_cells=True)['frame_data']
    assert data['configuration_id']==D['configuration_id']
    A={'plot_data':data['plot_data'],'configuration_id':D['configuration_id']}
    gold={int(r['frame_1based']):r for r in D['gold_frames']}
    native=O/'native_batch';frames=O/'rendered_frames';frames.mkdir(exist_ok=True)
    details=O/'frame_verification';details.mkdir(exist_ok=True)
    ids=np.asarray(J['frame_ids'],dtype=int).reshape(-1).tolist()
    expected=[]
    for k in ids:
        source=int(D['selection']['source_indices_1based'][k-1])
        f=loadmat(native/('cycle_%04d.mat'%k),simplify_cells=True)['video_frame']
        assert int(f['source_index_1based'])==source
        fig,entry=renderer.build_frame(A,f,k,600,C)
        png=frames/('frame_%04d.png'%k)
        fig.savefig(png,dpi=C['dpi']);renderer.plt.close(fig)
        with Image.open(png) as im:assert im.size==(2560,1440)
        actual_png=sha(png)
        equals=actual_png==gold[k]['original_PNG_sha256']
        if strict:assert equals,'Rebuilt raster differs from reference at frame %d'%k
        W=f['W']
        entry.update(encoded_frame_1based=k,planned_full_frame_1based=k,
            playback_time_seconds=(k-1)/30,image_SHA256=actual_png,
            exact_reference_PNG_sha256=gold[k]['original_PNG_sha256'],
            exact_reference_PNG_bytes_match=equals,native_cycle_SHA256=sha(native/('cycle_%04d.mat'%k)),
            neutral_peak_A=float(abs(np.asarray(W['currents_A']).sum(axis=1)).max()))
        write(details/('frame_%04d.json'%k),entry)
        expected.append({'frame_1based':k,'image_sha256':actual_png,'all_artist_checks_passed':True,
            'exact_reference_PNG_bytes_match':equals})
        print('PASS package raster %d/600, original sample %d.'%(k,source),flush=True)
    write(O/'last_batch_review.json',{'result':'PASS_PACKAGE_RENDERED_BATCH','frame_ids':ids,'records':expected})
elif J['action']=='encode':
    dep=read(O/'dependency_preflight.json');ffmpeg=dep['ffmpeg'];ffprobe=dep['ffprobe']
    E=D['selection']['encoding'];records=[]
    for k in range(1,601):
        entry=read(O/'frame_verification'/('frame_%04d.json'%k))
        assert entry['encoded_frame_1based']==k and entry['planned_full_frame_1based']==k
        assert entry['source_index_1based']==D['selection']['source_indices_1based'][k-1]
        assert entry['image_SHA256']==sha(O/'rendered_frames'/('frame_%04d.png'%k))
        assert all(q['pass'] for q in entry['layout_checks'])
        if strict:assert entry['exact_reference_PNG_bytes_match']
        records.append(entry)
    movie=O/'IECON2026_OPFa_H21_speed_ramp_video.mp4'
    assert not movie.exists(),'Output movie already exists; choose a new output folder'
    command=[ffmpeg,'-hide_banner','-nostdin','-y','-loglevel','warning',
        '-framerate','30','-start_number','1','-i',str(O/'rendered_frames/frame_%04d.png'),
        '-frames:v','600','-an','-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709',
        '-c:v','libx264','-preset',E['preset'],'-crf',str(E['quality_CRF']),
        '-threads',str(E['threads']),'-profile:v','high','-pix_fmt','yuv420p',
        '-color_range','tv','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
        '-bsf:v','h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1',
        '-r','30','-fps_mode','cfr','-video_track_timescale','30000','-movflags','+faststart',
        '-metadata','title=IECON 2026: phase a open, H21, zero cogging',
        '-progress',str(O/'encode_progress.txt'),'-nostats',str(movie)]
    with (O/'encode_stdout.log').open('wb') as out,(O/'encode_stderr.log').open('wb') as err:
        process=run(command,out,err)
    assert process.returncode==0,(O/'encode_stderr.log').read_text(encoding='utf-8')
    R={'result':'PASS_PACKAGED_NATIVE_CYCLES_RENDERED_AND_ENCODED_AWAITING_DECODE','stage':'full',
        'encoded_file':str(movie),'encoded_file_SHA256':sha(movie),'frame_count':600,
        'image_dimensions_px':[2560,1440],'records':records,
        'scientific_limit_compliance':'FAIL_CURRENT_AND_VOLTAGE','recording_ready_with_all_limits_claim':False,
        'encoder_command_arguments':command,'encoder_exit_code':0}
    write(O/'recording_review.json',R)
    # The compact-layout inspector is restored from the MATLAB entry.
    # Its PATH is bound to the explicit executable directories before dispatch.
    os.environ['PATH']=str(Path(ffmpeg).parent)+os.pathsep+str(Path(ffprobe).parent)+os.pathsep+os.environ.get('PATH','')
    assert Path(shutil.which('ffmpeg')).resolve()==Path(ffmpeg).resolve()
    assert Path(shutil.which('ffprobe')).resolve()==Path(ffprobe).resolve()
    write(O/'video_selection.json',D['selection'])
    with (O/'inspect_stdout.log').open('wb') as out,(O/'inspect_stderr.log').open('wb') as err:
        process=run([sys.executable,'-B',str(support/'exact_inspector.py'),
            '--recording-folder',str(O),'--selection',str(O/'video_selection.json')],out,err)
    assert process.returncode==0,(O/'inspect_stderr.log').read_text(encoding='utf-8')
    V=read(O/'encoded_verification.json')
    assert V['result']=='PASS_ENCODED_FORMAT_TIMING_COMPLETE_DECODE_AND_FRAME_IDENTITIES'
    actual_pixels=[r['decoded_RGB_SHA256'] for r in V['quality_and_identity_per_frame']]
    reference_pixels=[r['original_decoded_RGB_sha256'] for r in D['gold_frames']]
    decoded_match=actual_pixels==reference_pixels
    encoded_match=sha(movie)==D['reference_MP4_sha256']
    if strict:assert decoded_match,'Rebuilt decoded pixels differ from original video'
    report={'result':'PASS_PACKAGE_REBUILT_FULL_REFERENCE_VIDEO','created_utc':datetime.now(timezone.utc).isoformat(),
        'strict_reference':strict,'frame_count':600,'frames_per_second':30,'duration_seconds':20,'dimensions_px':[2560,1440],
        'all_600_raster_checks_passed':True,'all_600_rebuilt_PNG_bytes_match_reference':all(r['exact_reference_PNG_bytes_match'] for r in records),
        'all_600_decoded_RGB_frames_match_original':decoded_match,
        'encoded_MP4_bytes_match_original':encoded_match,'rebuilt_MP4_sha256':sha(movie),
        'original_MP4_sha256':D['reference_MP4_sha256'],'full_decode_verification':V,
        'native_verification':read(O/'native_verification.json'),'dependency_preflight':dep,
        'artist_checks_passed':sum(r['layout_checks_passed'] for r in records),
        'scientific_limit_compliance':'FAIL_CURRENT_AND_VOLTAGE','recording_ready_with_all_limits_claim':False,
        'original_inputs_modified':False,'external_project_files_required':False,'working_storage_outside_OneDrive':str(O)}
    write(O/'reproduction_review.json',report)
    print(json.dumps({k:v for k,v in report.items() if k not in ['full_decode_verification','native_verification','dependency_preflight']},indent=2),flush=True)
else:raise ValueError(J['action'])

