"""Compact scientific layout; reads exact supplied native cycles, never changes them."""
import os,sys,hashlib
sys.dont_write_bytecode=True
from pathlib import Path
import numpy as np

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def configure_style(C,output_folder):
 global matplotlib,plt,MaxNLocator,FormatStrFormatter,WIDTH,HEIGHT,DPI,INK,TEAL,RED,BROWN,GRID,PHASES,PAIRS,PC,LC
 output_folder=Path(output_folder).resolve();assert 'onedrive' not in str(output_folder).lower()
 os.environ['MPLCONFIGDIR']=str(output_folder.parent/'matplotlib_cache')
 import matplotlib
 matplotlib.use('Agg',force=True)
 import matplotlib.pyplot as plt
 from matplotlib.ticker import MaxNLocator,FormatStrFormatter
 WIDTH,HEIGHT=C['image_dimensions_px'];DPI=C['dpi']
 INK,TEAL,RED,BROWN,GRID=[C['semantic_colors'][k] for k in ['text','progressive_trace','physical_limits_only','measurements_and_overshoots','grid']]
 PHASES=C['phase_order'];PAIRS=C['line_pairs'];PC=[C['phase_colors'][p] for p in PHASES];LC=[C['line_colors'][p] for p in PAIRS]
 plt.rcParams.update({'font.family':C['font_family'],'mathtext.fontset':C['mathtext_fontset'],
  'font.size':24,'axes.labelsize':26,'xtick.labelsize':24,'ytick.labelsize':24,'axes.linewidth':.9,
  'path.simplify':False,'savefig.facecolor':'white','axes.unicode_minus':True})
 matplotlib.font_manager.findfont(matplotlib.font_manager.FontProperties(family=C['font_family']),fallback_to_default=False)

def ylim(a,cap=None):
 lo=float(np.min(a));hi=float(np.max(a))
 if cap is not None:lo=min(lo,cap);hi=max(hi,cap)
 delta=hi-lo
 if delta==0:delta=max(abs(hi)*.05,.01)
 return [lo-.10*delta,hi+.10*delta]

def style(ax):
 ax.set_facecolor('white');ax.grid(True,color=GRID,lw=.8);ax.set_axisbelow(True)
 ax.tick_params(direction='in',top=True,right=True,length=4,pad=5)
 for s in ax.spines.values():s.set_color('#788185')

def bracket(ax,lo,hi):
 x=1.023;cap=.011;trans=ax.get_yaxis_transform()
 artists=ax.plot([x,x],[lo,hi],color=BROWN,lw=2,transform=trans,clip_on=False)
 for y in [lo,hi]:artists+=ax.plot([x-cap,x+cap],[y,y],color=BROWN,lw=2,transform=trans,clip_on=False)
 return {'minimum':float(lo),'maximum':float(hi),'length':float(hi-lo)},artists

def build_frame(A,f,ordinal,frame_count,C):
 P=A['plot_data'];W=f['W'];Q=f['Q'];source=int(f['source_index_1based'])
 theta=np.asarray(W['theta_e_rad']);theta_deg=theta*180/np.pi
 current=np.asarray(W['currents_A']);emf=np.asarray(W['back_emf_V']);voltage=np.asarray(W['line_voltage_V']);torque=np.asarray(W['torque_Nm'])
 assert len(theta)==16000 and np.all(current[:,0]==0) and int(W['source_index_1based'])==source
 phi=np.asarray(W['phase_displacements_rad']);alpha=current@np.cos(phi)/3;beta=current@np.sin(phi)/3
 live={'torque_min_Nm':float(torque.min()),'torque_max_Nm':float(torque.max()),'torque_ripple_pp_Nm':float(np.ptp(torque)),
  'peak_phase_current_A':float(np.abs(current[:,1:]).max()),'peak_line_voltage_V':float(np.abs(voltage).max()),
  'mean_torque_Nm':float(torque.mean()),'phase_rms_current_A':np.sqrt(np.mean(current*current,axis=0)).tolist(),
  'copper_loss_W':float(1.4*np.mean(current*current,axis=0).sum())}
 metrics={**live,'speed_rpm':float(W['speed_used_rpm']),
  'id1_A':float(np.mean(-alpha*np.cos(theta)-beta*np.sin(theta))),
  'iq1_A':float(np.mean(alpha*np.sin(theta)-beta*np.cos(theta)))}
 for key in [*live,'id1_A','iq1_A']:assert np.max(np.abs(np.asarray(Q[key])-metrics[key]))<2e-10,key
 ip=int(Q['peak_phase_index_1based'])-1;vp=int(Q['peak_line_pair_index_1based'])-1
 x=np.asarray(P['progress_percent']);progress=(source-1)/(C['original_selected_operating_points']-1)*100
 stop=int(np.searchsorted(P['source_index_1based'],source));prefix_x=np.r_[x[:stop],progress]
 fig=plt.figure(figsize=(WIDTH/DPI,HEIGHT/DPI),dpi=DPI,facecolor='white')
 header=fig.text(.5,.990,C['case_label']+"   |   "+r'$n$'+f" = {W['speed_used_rpm']:.1f} r/min   |   "+r'$T^{\ast}$'+f" = {W['torque_used_Nm']:.3f} Nm",ha='center',va='top',fontsize=32,color=INK)
 bottom,top=.060,.923;left_x,left_w=.064,.383;gap=.008;left_h=(top-bottom-8*gap)/9
 rows=[('speed_rpm',r'$n$ (r/min)',None),('mean_torque_Nm',r'$\overline{T}$ (Nm)',None),
  ('torque_ripple_pp_Nm',r'$\tau$ (Nm)',2.),('peak_line_voltage_V',r'$v_{\mathrm{pk}}$ (V)',290.),
  ('peak_phase_current_A',r'$i_{\mathrm{pk}}$ (A)',4.34),('phase_rms_current_A',r'$i_{\mathrm{rms},k}$ (A)',None),
  ('id1_A',r'$\overline{i}_{d_1}$ (A)',None),('iq1_A',r'$\overline{i}_{q_1}$ (A)',None),('copper_loss_W','SCL (W)',None)]
 left=[];groups={};limit_lines=[];limit_texts=[];rms_legend=None
 for row,(key,label,cap) in enumerate(rows):
  ax=fig.add_axes([left_x,top-(row+1)*left_h-row*gap,left_w,left_h]);style(ax);left.append(ax)
  values=np.asarray(P[key]);mv=np.asarray(metrics[key]);groups[key]=[]
  if key=='phase_rms_current_A':values=values[:,1:];mv=mv[1:]
  for j in range(5 if values.ndim==2 else 1):
   v=values[:,j] if values.ndim==2 else values;value=float(mv[j] if values.ndim==2 else mv)
   color=PC[j+1] if values.ndim==2 else TEAL
   context=ax.plot(x,v,color=color,lw=C['left_future_context_width_pt'],alpha=C['left_future_context_alpha'])[0]
   trace=ax.plot(prefix_x,np.r_[v[:stop],value],color=color,lw=C['left_progressive_trace_width_pt'],label=PHASES[j+1] if values.ndim==2 else key)[0]
   marker=ax.plot(progress,value,'o',color=color,ms=C['left_marker_size_pt'])[0];groups[key].append((context,trace,marker))
  if key=='mean_torque_Nm':ax.plot(x,P['torque_requested_Nm'],color='#71797d',ls='--',lw=C['left_requested_torque_width_pt'],alpha=.4,zorder=1.8)
  if key=='phase_rms_current_A':
   handles=[g[1] for g in groups[key]]
   rms_legend=ax.legend(handles,PHASES[1:],ncol=5,loc='upper left',frameon=False,fontsize=24,handlelength=1.0,columnspacing=.9,borderpad=.1,borderaxespad=.25)
  if cap is not None:
   limit_lines.append(ax.axhline(cap,color=RED,ls=(0,(5,4)),lw=1.25,gid='physical_limit_line'))
   limit_texts.append(ax.text(*C['left_limit_symbol_position_axes'],C['left_limit_symbols'][key],ha='left',va='center',transform=ax.transAxes,color=RED,fontsize=C['left_limit_symbol_font_pt'],gid='physical_limit_label',bbox={'facecolor':'white','edgecolor':'none','alpha':.94,'pad':.4}))
  ax.set_xlim(0,100);ax.set_ylim(ylim(values,cap));ax.set_xticks([0,20,40,60,80,100])
  loc=MaxNLocator(nbins=2,steps=[1,2,2.5,5,10]);ticks=loc.tick_values(*ax.get_ylim());ax.set_yticks(ticks[(ticks>=ax.get_ylim()[0])&(ticks<=ax.get_ylim()[1])])
  ax.set_ylabel(label,labelpad=8,fontsize=26)
  if row<8:ax.set_xticklabels([])
  else:ax.set_xlabel('Trajectory progress (%)',labelpad=4,fontsize=26)
 rx,rw=.505,.395;right_gaps=[.043,.043,.054];rh=(top-bottom-sum(right_gaps))/4
 axes=[];heads=[];rails=[];measurement_labels={};brackets={};bracket_artists={}
 titles=[r'Torque $T$ (Nm)',r'Back-EMF $e_k$ (V)',r'Current $i_k$ (A)',r'Line voltage $v^{\prime}_{r}$ (V)']
 for row,title in enumerate(titles):
  pos=[rx,top-(row+1)*rh-sum(right_gaps[:row]),rw,rh];ax=fig.add_axes(pos);style(ax);axes.append(ax)
  ax.set_xlim(0,360);ax.set_xticks([0,90,180,270,360])
  heads.append(ax.text(0,1.025,title,transform=ax.transAxes,ha='left',va='bottom',fontsize=26,color=INK))
  if row<3:ax.set_xticklabels([])
  else:ax.set_xlabel(r'Electrical angle $\theta_{\mathrm{r}}$ ($^\circ$)',labelpad=4,fontsize=26)
  rail=fig.add_axes([.920,pos[1],.075,pos[3]]);rail.set_axis_off();rails.append(rail)
 torque_line=axes[0].plot(theta_deg,torque,color='#262c2e',lw=1.5)[0]
 axes[0].axhline(live['mean_torque_Nm'],color=TEAL,lw=1.0,ls='--')
 axes[0].set_ylim(ylim(torque))
 torque_ticks=MaxNLocator(nbins=3).tick_values(*axes[0].get_ylim())
 axes[0].set_yticks(torque_ticks[(torque_ticks>=axes[0].get_ylim()[0])&(torque_ticks<=axes[0].get_ylim()[1])])
 axes[0].yaxis.set_major_formatter(FormatStrFormatter('%.3f'))
 phases={'back_emf':[],'current':[]}
 for k in range(6):
  phases['back_emf'].append(axes[1].plot(theta_deg,emf[:,k],color=PC[k],lw=1.55,ls='--' if k==0 else '-',label='a (open)' if k==0 else PHASES[k])[0])
  phases['current'].append(axes[2].plot(theta_deg,current[:,k],color=PC[k],lw=2.0 if k in [0,ip] else 1.45,ls='--' if k==0 else '-',zorder=7 if k==0 else 2,label=r'$a:\,i_a=0$' if k==0 else PHASES[k])[0])
 legends=[]
 for row in [1,2]:
  legends.append(axes[row].legend(ncol=6,loc='lower right',bbox_to_anchor=(1,1.015),borderaxespad=0,fontsize=24,frameon=False,handlelength=1.2,columnspacing=.70,handletextpad=.35,borderpad=.05))
 line_curves=[]
 for k in range(10):line_curves.append(axes[3].plot(theta_deg,voltage[:,k],color=LC[k],lw=2.0 if k==vp else 1.35,alpha=1,label=PAIRS[k])[0])
 order=[0,5,1,6,2,7,3,8,4,9]
 legends.append(axes[3].legend([line_curves[k] for k in order],[PAIRS[k] for k in order],ncol=5,loc='lower right',bbox_to_anchor=(1,1.015),borderaxespad=0,fontsize=24,frameon=False,handlelength=1.25,columnspacing=.85,handletextpad=.35,labelspacing=.12,borderpad=.05))
 for row,key in [(1,'back_emf_V'),(2,'phase_current_A'),(3,'healthy_line_voltage_V')]:
  axes[row].set_ylim(C['waveform_y_limits'][key]);axes[row].set_yticks(C['waveform_y_ticks'][key])
 for row,cap in [(2,4.34),(3,290)]:
  for sign in [-1,1]:limit_lines.append(axes[row].axhline(sign*cap,color=RED,ls=(0,(5,4)),lw=1.25,gid='physical_limit_line'))
  for tick,label in zip(axes[row].get_yticks(),axes[row].get_yticklabels()):
   if abs(tick)==cap:label.set_color(RED);label.set_gid('physical_limit_label')
 for row,key,symbol,digits,unit in [(0,'torque_ripple_pp_Nm',r'$\tau$',4,'Nm'),(2,'peak_phase_current_A',r'$i_{\mathrm{pk}}$',4,'A'),(3,'peak_line_voltage_V',r'$v_{\mathrm{pk}}$',2,'V')]:
  lo=live['torque_min_Nm'] if row==0 else 0.;hi=live['torque_max_Nm'] if row==0 else live[key]
  brackets[key],bracket_artists[key]=bracket(axes[row],lo,hi)
  yl=axes[row].get_ylim();yc=((lo+hi)/2-yl[0])/(yl[1]-yl[0])
  measurement_labels[key]=rails[row].text(.04,yc,symbol+'\n'+f'{live[key]:.{digits}f} {unit}',ha='left',va='center',fontsize=28,color=BROWN,linespacing=1.15)
 fig.canvas.draw();rr=fig.canvas.get_renderer();checks=[]
 def test(name,condition,**evidence):
  assert bool(condition),(name,evidence)
  checks.append({'name':name,'pass':True,**evidence})
 def bb(a):return a.get_window_extent(rr)
 waves=[bb(a) for a in axes]
 test('nine original progressive panels and four full waveform panels retained',len(left)==9 and len(axes)==4)
 test('one condensed header and no bottom captions',len(fig.texts)==1 and '\n' not in header.get_text() and header.get_position()[1]>.95)
 test('header contains exactly the requested three fields',C['case_label']=='IECON 2026' and header.get_text()==C['case_label']+"   |   "+r'$n$'+f" = {W['speed_used_rpm']:.1f} r/min   |   "+r'$T^{\ast}$'+f" = {W['torque_used_Nm']:.3f} Nm")
 test('header speed n uses italic mathematical notation',C['header_speed_symbol_mathtext']==r'$n$' and r'$n$' in header.get_text() and C['mathtext_fontset']=='stix')
 test('header is horizontally centered',header.get_horizontalalignment()=='center' and header.get_position()[0]==.5 and abs((bb(header).x0+bb(header).x1)/2-WIDTH/2)<1e-8)
 test('paper line waveform notation uses prime and component r',heads[3].get_text()==r'Line voltage $v^{\prime}_{r}$ (V)')
 test('electrical rotor angle matches paper notation',axes[3].get_xlabel()==r'Electrical angle $\theta_{\mathrm{r}}$ ($^\circ$)')
 alltexts=[a for a in fig.findobj(match=matplotlib.text.Text) if a.get_visible() and a.get_text()]
 test('cycle mean words removed',all('cycle mean' not in a.get_text().lower() for a in alltexts))
 outside=[{'text':a.get_text(),'bounds':list(bb(a).bounds)} for a in alltexts if bb(a).x0<-.5 or bb(a).y0<-.5 or bb(a).x1>WIDTH+.5 or bb(a).y1>HEIGHT+.5]
 test('every visible label fits inside the frame',not outside,outside=outside)
 test('minimum label font is 24 points',min(a.get_fontsize() for a in alltexts)>=24)
 test('open phase current exactly zero and explicit dashed curve',np.all(phases['current'][0].get_ydata()==0) and phases['current'][0].get_linestyle()=='--' and phases['current'][0].get_zorder()==7)
 test('only three compact right-hand measurements',sum(len(a.texts) for a in rails)==3 and len(rails[1].texts)==0)
 test('no footer text occupies the bottom margin',all(a.get_position()[1]>.95 for a in fig.texts))
 test('all seven physical limit lines retained',len(limit_lines)==7 and all(a.get_color()==RED for a in limit_lines))
 test('left limits use the three exact paper symbols',
  [a.get_text() for a in limit_texts]==[r'$\tau^{\mathrm{mx}}$',r'$v_{\mathrm{pk}}^{\mathrm{mx}}$',r'$i_{\mathrm{pk}}^{\mathrm{mx}}$'])
 for label,ax in zip(limit_texts,[left[2],left[3],left[4]]):
  b=bb(label);ab=bb(ax)
  test('symbolic limit label fits within its own plot '+label.get_text(),
   b.x0>=ab.x0 and b.x1<=ab.x1 and b.y0>=ab.y0 and b.y1<=ab.y1,
   bounds_px=list(b.bounds),axes_bounds_px=list(ab.bounds))
 test('exact torque waveform retained',np.array_equal(torque_line.get_ydata(),torque))
 for row,leg in zip([1,2,3],legends):
  test('waveform legend outside data '+str(row),all(not bb(leg).overlaps(b) for b in waves) and bb(leg).y0>waves[row].y1,legend_bounds=list(bb(leg).bounds),wave_boxes=[list(b.bounds) for b in waves])
  test('heading and legend do not overlap '+str(row),not bb(leg).overlaps(bb(heads[row])))
 test('header does not overlap panel headings',all(not bb(header).overlaps(bb(h)) for h in heads))
 for i,a in enumerate(left):
  for j,b in enumerate(left[i+1:],i+1):test('left axis labels distinct '+str(i)+' '+str(j),not bb(a.yaxis.label).overlaps(bb(b.yaxis.label)))
 for k in range(6):
  test('original current and EMF and consistent phase colour '+PHASES[k],np.array_equal(phases['current'][k].get_ydata(),current[:,k]) and np.array_equal(phases['back_emf'][k].get_ydata(),emf[:,k]) and phases['current'][k].get_color()==phases['back_emf'][k].get_color()==PC[k] and PC[k]!=RED)
 for k in range(10):test('original line voltage '+PAIRS[k],np.array_equal(line_curves[k].get_ydata(),voltage[:,k]) and line_curves[k].get_color()==LC[k] and LC[k]!=RED)
 for row,key in [(1,'back_emf_V'),(2,'phase_current_A'),(3,'healthy_line_voltage_V')]:
  data=emf if row==1 else current if row==2 else voltage
  test('fixed scale and no clipping '+key,np.array_equal(axes[row].get_ylim(),C['waveform_y_limits'][key]) and axes[row].get_ylim()[0]<float(data.min()) and axes[row].get_ylim()[1]>float(data.max()))
 right_maximum_waveform_width=max([torque_line.get_linewidth()]+[a.get_linewidth() for g in phases.values() for a in g]+[a.get_linewidth() for a in line_curves])
 test('right waveform reference width measured from actual plotted artists',right_maximum_waveform_width==C['right_maximum_waveform_stroke_width_pt'])
 markers=[]
 for key,group in groups.items():
  values=np.asarray(P[key]);mv=np.asarray(metrics[key]);values=values[:,1:] if key=='phase_rms_current_A' else values;mv=mv[1:] if key=='phase_rms_current_A' else mv
  for j,(context,trace,marker) in enumerate(group):
   val=float(mv[j] if values.ndim==2 else mv);pv=values[:,j] if values.ndim==2 else values
   test('exact progressive context '+key+str(j),np.array_equal(context.get_ydata(),pv) and np.array_equal(context.get_xdata(),x))
   test('left progressive and future curves use the reviewed bold strokes '+key+str(j),
    trace.get_linewidth()==C['left_progressive_trace_width_pt']==6.0 and context.get_linewidth()==C['left_future_context_width_pt']==4.0)
   test('future curve remains visible and moving marker exceeds trace width '+key+str(j),
    context.get_alpha()==C['left_future_context_alpha']==.65 and marker.get_markersize()==C['left_marker_size_pt']==8.0)
   test('left future and progressive strokes at least match right maximum nominal ink width '+key+str(j),
    context.get_linewidth()*context.get_alpha()>=right_maximum_waveform_width and trace.get_linewidth()>=right_maximum_waveform_width)
   test('same-cycle progressive marker '+key+str(j),np.array_equal(marker.get_xdata(),[progress]) and float(marker.get_ydata()[0])==val)
   test('original prefix ending at actual frame '+key+str(j),np.array_equal(trace.get_xdata(),prefix_x) and np.array_equal(trace.get_ydata(),np.r_[pv[:stop],val]))
   if key=='phase_rms_current_A':test('RMS colour agrees with current and EMF '+str(j),all(a.get_color()==PC[j+1] for a in (context,trace,marker)))
   markers.append({'metric':key,'phase':PHASES[j+1] if values.ndim==2 else None,'value':val,'progress':progress})
 rendered_labels={}
 for key,a in measurement_labels.items():
  decimals=2 if key=='peak_line_voltage_V' else 4;displayed=float(a.get_text().split('\n')[1].split()[0])
  test('rounded bracket label matches waveform '+key,abs(displayed-live[key])<=.5*10**(-decimals)+1e-12 and abs(brackets[key]['length']-live[key])<1e-12)
  test('measurement outside all waveform data '+key,all(not bb(a).overlaps(b) for b in waves))
  bar=bracket_artists[key][0];test('drawn bracket endpoints '+key,np.array_equal(bar.get_ydata(),[brackets[key]['minimum'],brackets[key]['maximum']]))
  rendered_labels[key]={'text':a.get_text(),'displayed_numeric_value':displayed,'full_precision_waveform_measurement':live[key],'decimal_places':decimals,'bounds_px':list(bb(a).bounds)}
 geometry={'left_axes_positions_normalized':[list(a.get_position().bounds) for a in left],
  'waveform_axes_positions_normalized':[list(a.get_position().bounds) for a in axes],
  'data_plot_area_fraction':sum(a.get_position().width*a.get_position().height for a in left+axes),
  'intercolumn_gap_fraction':rx-left_x-left_w,'minimum_label_font_pt':min(a.get_fontsize() for a in alltexts),
  'minimum_nominal_font_pixels_at_1280x720':24*DPI/72*1280/WIDTH,
  'left_progressive_trace_width_pt':C['left_progressive_trace_width_pt'],
  'left_future_context_width_pt':C['left_future_context_width_pt'],
  'left_future_context_alpha':C['left_future_context_alpha'],
  'left_marker_size_pt':C['left_marker_size_pt'],
  'right_maximum_waveform_width_pt':right_maximum_waveform_width,
  'left_trace_nominal_pixels_at_1280x720':C['left_progressive_trace_width_pt']*DPI/72*.5,
  'left_trace_nominal_pixels_at_960x540':C['left_progressive_trace_width_pt']*DPI/72*.375,
  'left_limit_labels':[{'text':a.get_text(),'bounds_px':list(bb(a).bounds)} for a in limit_texts],
  'header_bounds_px':list(bb(header).bounds),'right_text_items':3,
  'legends':[{'labels':[t.get_text() for t in l.get_texts()],'bounds_px':list(bb(l).bounds)} for l in legends]}
 return fig,{'id':f['id'],'filename':f"frame_{ordinal:04d}.png",'source_index_1based':source,'speed_rpm':float(W['speed_used_rpm']),
  'torque_requested_Nm':float(W['torque_used_Nm']),'trajectory_progress_percent':progress,'angle_samples':len(theta),'live':live,
  'brackets':brackets,'rendered_bracket_labels':rendered_labels,'current_peak_phase':PHASES[ip],'voltage_peak_pair':PAIRS[vp],
  'header_text':header.get_text(),'layout_id':C['layout_id'],'geometry':geometry,'moving_markers_from_actual_frame_W_Q':True,
  'actual_drawn_marker_measurements':markers,'layout_checks_passed':len(checks),'layout_checks':checks,
  'scientific_limit_compliance':'FAIL_CURRENT_AND_VOLTAGE','recording_ready_with_all_limits_claim':False}
