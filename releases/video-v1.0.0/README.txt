IECON 2026 PHASE-a-OPEN H21 VIDEO - COMPACT LAYOUT V5
======================================================

PURPOSE AND SCIENTIFIC STATUS
-----------------------------
This package rebuilds the delivered 20 s current-reference video for the
paper's symmetrical six-phase nonsalient PMSM, phase a open, star connection,
one isolated neutral, five pole pairs and zero cogging torque.

It includes the full original H21/nt250 LUT. The entry reconstructs references
from that LUT; it does not rerun the offline LP/QP optimizer, a controller,
Simulink, Maxwell or an experiment. All original requested operating points
and coefficients are preserved. The waveform current and voltage limits
are exceeded slightly between the original 250 optimization angles.
Scientific limit compliance remains FAIL_CURRENT_AND_VOLTAGE.

PACKAGE CONTENTS
----------------
rebuild_iecon2026_opf_video.m
  One self-contained MATLAB entry file, with private waveform/metric functions
  and embedded Python layout, encoding support and a complete-frame inspector.
  It extracts support code ONLY into the explicit working output folder.
  There are no external project-script or original source-folder dependencies.

LUTs_data_OPF_H21_nt250.mat
  Exact full source-file copy, not a reduced or substituted LUT.
  303 torque rows x 532 retained frequency columns x 6 phases x 11 harmonics.
  IRe/IIm remain float32 in storage and are converted to double for synthesis.

IECON2026_OPFa_H21_inputs.mat
  The two original 1,443,053-sample double vectors speed_m2 [r/min] and
  torque_m2 [Nm]; both original EMF vectors angleEMF [electrical rad] and
  backEMF [V per mechanical rad/s]; the complete unchanged selected trajectory
  struct; and the original plot_data context for numerical comparison.
  All 9,973 plot-context rows are recalculated from LUT waveforms in the entry.
  Stored plot metrics are comparison references, not substitutes for rebuilding.

STEP8_Video_frame_samples.csv
  600 original frame sample indices, playback times and 24 columns including
  actual speed, requested/mean torque, ripple, peak current, all-healthy-pair
  peak voltage, five separate phase RMS currents, copper loss, d1/q1 means,
  neutral residual and signed current/voltage excesses.

IECON2026_OPFa_H21_speed_ramp_video.mp4
  The revised, verified 20 s video with compact layout v5.

IECON2026_OPFa_H21_package.json
  Readable machine, sampling, source provenance, runtime and reference hashes.
  Earlier configuration status fields are preserved as historical records;
  current completion and limitations are in REPRODUCTION_VERIFICATION.json.
  Historical absolute paths document where inputs came from; the entry never
  uses those paths to locate scientific files. Runtime inputs are adjacent
  package files. The entry contains its own frozen runtime definition.

REPRODUCTION_VERIFICATION.json
  Current presentation, complete decode, source preservation and representative
  relocated rebuild checks; verification scopes are stated explicitly.

MANIFEST_SHA256.txt
  SHA-256 for every other package member; this file excludes its own hash.

STEP5_Numerical_verification_and_recording_readiness.txt
STEP8_verification.json
  Unchanged earlier evidence: full-path continuous-angle limitations and the
  first-layout recording checks. STEP8_verification.json describes the older
  3840 x 2324 presentation and its older MP4 hash, not this compact video.
  Current layout and video checks are in REPRODUCTION_VERIFICATION.json.
  Historical absolute paths are provenance and are not needed by the rebuild.

README.txt
  This document.

HOW TO REBUILD
--------------
The loose Step-7/Step-8 scripts and layout configuration retained in the
parent Video folder describe the preceding presentation. To rebuild this
compact revision, use the MATLAB entry extracted from this current ZIP.

1. Extract the ZIP into an ordinary nonsynchronized working location.
   Keep all package files together in the enclosed IECON2026_OPFa_H21_package
   folder. Do not edit, rename or substitute its four runtime input files.

2. Use a separate output folder outside OneDrive. In MATLAB, for example:

   package_dir = 'C:\Users\agyep\AppData\Local\CodexScratch\IECON2026_H21\IECON2026_OPFa_H21_package';
   output_root = 'C:\Users\agyep\AppData\Local\CodexScratch\IECON2026_H21_runs';
   addpath(package_dir)

3. To recalculate all 9,973 context rows and all 600 native cycles without
   rendering, run:

   rebuild_iecon2026_opf_video('check',fullfile(output_root,'check'));

4. For the full video, supply a real absolute Python executable containing the
   libraries listed below. On the verified workstation it is:

   python_exe = 'C:\Users\agyep\AppData\Local\Programs\Python\Python313\python.exe';
   rebuild_iecon2026_opf_video('full',fullfile(output_root,'full'), ...
       'PythonExecutable',python_exe);

   The result is written as IECON2026_OPFa_H21_speed_ramp_video.mp4 in that
   output folder. The entry also writes per-frame reviews, numerical checks,
   dependency records, complete encoded-video checks and reproduction_review.json.

   Ten representative static frames can be rebuilt using mode 'preview'.
   Preview frames retain the original operating points and order; they are not
   a timed clip.

5. FFmpeg and FFprobe must be on PATH. Alternatively supply their absolute
   files as 'FFmpegExecutable' and 'FFprobeExecutable' name/value arguments.

The package is read-only during execution. It verifies input hashes before
and after rebuilding. Missing or changed data is rejected, with no fallback
to an original project/snapshot. Generated files must remain outside OneDrive.
Use a fresh output folder when starting another complete run. An existing
folder with a different or unknown run binding is rejected.

The MATLAB process launches Python with UseShellExecute=false,
CreateNoWindow=true and Hidden window style. The renderer uses Matplotlib Agg;
no visible figure/window is opened. Logs are saved as python_<action>_stdout.log
and python_<action>_stderr.log in the output folder.

DEPENDENCIES AND REFERENCE IDENTITY
----------------------------------
Verified environment:
  Windows; base MATLAB with JVM and its Windows .NET process support
  MATLAB 26.1.0.3346908 (R2026a) Update 5
  Python 3.13.3
  NumPy 2.4.6
  SciPy 1.18.1
  Matplotlib 3.11.2
  Pillow 12.3.0
  threadpoolctl 3.7.0
  FFmpeg/FFprobe 8.1.2 full build
  Times New Roman; the exact regular-font SHA is in the package metadata

The default StrictReference=true checks these rendering dependencies, all
original native array fingerprints, every recalculated plot-context value,
every PNG hash and every decoded RGB frame against the delivered compact-v5
reference. Native waveform fingerprints still match the original calculation.
A font or runtime mismatch is reported rather than silently accepted.

'StrictReference',false permits different binary rounding or rendering
versions while retaining fixed numerical comparison tolerances and recording
all reference-identity results. That option was not used for the verified
full rebuild. Identical MP4 bytes on arbitrary systems/codec builds are not
promised; the package records the actual binary and decoded-pixel comparisons.

TRAJECTORY SELECTION
--------------------
The original paired source has 1,443,053 samples and no physical time vector.
The selected contiguous prefix is original MATLAB indices 1 through 1,314,036,
ending immediately before the first original speed strictly above 1500 r/min.
Last retained speed: 1499.9999630365924 r/min.
First excluded sample: index 1,314,037, 1500.0004660400325 r/min.
The entry checks that this first excluded point is rejected for invalid
coefficient interpolation support.

The starting source fluctuations are retained, including 27,016 samples below
the nominal 850-r/min selection description. Minimum speed is approximately
849.8702620131035 r/min; no sample was clipped, sorted, smoothed or synthesized.
Requested and used speed/torque arrays remain equal, with separate fields.

The video displays exactly 600 original points:
  indices = floor(linspace(1,1314036,600) + 0.5)
This selects original samples and preserves their order. It does not interpolate
speed or torque or replace the stored million-sample trajectory.

ANGLES, COEFFICIENT INTERPOLATION AND MODEL
-----------------------------------------
The original optimization grid has nt=250:
  theta_e(j) = 2*pi*j/250, j=1,...,250.
Rebuilt waveform and context cycles have 16,000 angles:
  theta_e(j) = 2*pi*j/16000, j=1,...,16000.
Each grid contains 2*pi and excludes 0, with no duplicated endpoint.

All odd harmonics h=1,3,...,21 are used independently for phases b through f:
  i_k = sum_h [IRe_kh*cos(h*(theta_e-phi_k))
             + IIm_kh*sin(h*(theta_e-phi_k))]
  phi_k=(k-1)*pi/3; i_a=0.

Coefficients use convex bilinear interpolation in torque and retained
electrical frequency, after verifying the stored feasible envelope and all
nonzero-weight corner supports. No infeasible zero-filled corner is used.

Electrical frequency is f1=n*5/60. Below the first retained frequency,
79.69999694824219 Hz (956.3999633789062 r/min), coefficients use the first
frequency column. The first 259,714 selected samples have this treatment.
Actual speed is retained for omega_m=2*pi*n/60 and omega_e=5*omega_m, back-EMF
and voltage. f1Low denotes voltage-limit activation, not minimum feasible speed.

Normalized EMF is interpolated periodically and linearly with phase shifts.
On the even grid, its first half becomes 0.5*(raw_first_half-raw_second_half)
and its second half is the negative of that first half. EMF then scales by
actual mechanical angular speed. Phase a's EMF remains in the machine model.

Resistance is 1.4 ohm in every VSD axis. VSD inductances [alpha,beta,x,y,0+,0-]
are [0.012,0.012,0.0113,0.0113,0.0094,0.0094] H. The paper reports 0- only;
0+=9.4 mH is retained from its matching MATLAB implementation.
Voltage follows the complete VSD model and analytic current derivative.
All ten healthy line pairs are used: bc,bd,be,bf,cd,ce,cf,de,df,ef.
Torque is sum_k normalized_EMF_k*i_k with Tcog=0.

All live metrics and all moving markers derive from the displayed cycle.
Each healthy phase has its own RMS current. Copper loss is
1.4*sum_k mean(i_k^2). d1/q1 means use the complete current vector and the
documented historical display convention (negative conventional Park d/q).

PLAYBACK AND LIMITATIONS
-----------------------
The full video has exactly 600 frames at 30 fps and duration 20.000000 s,
2560 x 1440 fixed pixels (16:9), H.264 High, yuv420p, limited-range BT.709, no audio.
Frame k begins at (k-1)/30 s. The last frame begins at 19.9666667 s and completes
at 20 s. Encoding uses CRF 4, slow preset, four threads and exact colour tags.

20 s is playback duration. The source supplies no physical sample period.
The left axis is original trajectory progress and the right is electrical
angle 0-360 degrees. Coefficient time derivatives along the ramp, controller
tracking, flux saturation, FEA and experimental measurements are not modeled.

Physical prescribed limits are 4.34 A peak phase current, 290 V peak healthy
line voltage and 2 Nm peak-to-peak torque ripple. The original LUT was optimized
at 250 angles. The earlier full-path audit found continuous-angle maxima:
  Current: [4.346018184232,4.346018192883] A
  Voltage: [290.942789996125,290.942790522166] V
  Torque ripple: [1.916966661023,1.916966662228] Nm pp
Thus current and voltage fail; ripple passes. These are full original-point
bounds from the included Step-5 report, not maxima over only 600 video frames.
The earlier audit also encloses straight diagnostic connections between original
trajectory points. Including these connections gives current bounds
[4.346018190299,4.346018192883] A, voltage bounds
[290.942812409000,290.942812504687] V and the same ripple upper bound.
These diagnostic connections do not add or replace any displayed source sample.

The stored float32 coefficients leave a neutral-current residual bounded by
approximately 5.60473794248179e-7 A over the original ramp. Exact phase-a zero
is verified; exact zero for the complete neutral sum is not claimed, and no
projection is applied. Dense-angle mean torque can differ from the prescribed
250-angle mean by up to about 2.75926422981243e-5 Nm.

The 16,000-angle display peaks are sampled values. Their apparent convergence
is not a continuous-angle feasibility certificate. The separate Step-5 audit
supplies continuous bounds; its original certification procedure is documented
but is not rerun by this video-rebuild entry.

The first displayed dense-grid voltage excess is full frame 302 (10.033333 s),
and current excess is frame 515 (17.133333 s). These are events in the 600-frame
subset, not exact solver active-set transitions or first full-path events.

RETAINED COMPACT PRESENTATION AND PAPER NOTATION
----------------------------------------------
The compact layout introduced in revision 2 is retained in revision 5.
This revision changes the presentation only. It retains all nine progressive
panels, all four waveform panels, all five separate healthy-phase RMS curves,
all ten healthy line voltages and all original operating points and waveforms.

The centered header contains only IECON 2026, speed and torque reference.
The speed symbol n is italic mathematical text. There
are no footer captions and no "cycle mean" words in the axis labels. The three
right-side readings are torque ripple, peak phase current and peak line voltage.
Repeated frequencies, individual RMS numbers, mean/request repeats, margins,
source indices and explanatory prose have been removed from the right side.

The plot areas occupy 59.1602% of the frame, compared with 47.1518% in layout v1
(25.47% more plot area). The column gap is 5.8% of the frame width, previously
9.0% in layout v1 (35.56% smaller). The waveform panels are 39.5% of the frame width,
27.8% in layout v1 (42.09% wider). Font sizes are at least 24 pt at 100 dpi,
equivalent to a nominal 16.67 pixels when shown at 1280 x 720. The smallest
layout-v1 legend font was equivalent to 6.94 pixels at that display width.
The header is 32 pt and the three outside readings are 28 pt. Curves are
thicker and the phase colours have stronger contrast on white backgrounds.

Readability has been inspected at 1280 x 720 and 960 x 540. A display smaller
than these review sizes may still benefit from enlarging the video.

Paper-consistent line-voltage notation is v'_r, r=1,...,10, as defined on
manuscript page 4 in (14)-(15). The healthy line vector is bold v', and v_pk
is its maximum absolute component over one electrical cycle. The exact order
is bc, bd, be, bf, cd, ce, cf, de, df, ef; for example, v'_1=v_b-v_c and
v'_10=v_e-v_f. The left peak plot and the bracket label remain v_pk. The
electrical-angle label uses theta_r, the paper's rotor electrical position;
the internal theta_e_rad variable contains those same electrical angles.

Displayed precision is 0.1 r/min and 0.001 Nm in the header; 0.0001 Nm for
the ripple bracket, 0.0001 A for peak current and 0.01 V for peak line voltage.
Brackets and curves use unrounded data, with no clipping or rescaling. Full
precision remains in the included frame table and numerical verification.
The shorter display is not a new feasibility claim: the earlier continuous
current/voltage exceedances remain, as documented above and in Step 5.

RETAINED LEFT TRACE VISIBILITY
------------------------------
These trace settings were introduced in revision 4 and are retained.
The nine left panels now use 6.0-point progressive curves, increased from
3.6 points in revision 3. All five individual phase RMS curves use this width.
At 100 dpi this is nominally 8.333 pixels at 2560 x 1440, 4.167 pixels at
1280 x 720 and 3.125 pixels at 960 x 540, before display antialiasing.

The full-path context is now 4.0 points at 0.65 opacity, increased from
1.8 points at 0.15 opacity. This makes the left paths visible from the first
frame and strengthens the path ahead of the moving operating point. Moving
markers are 8.0 points. The dashed requested-torque reference is 3.0 points
and is drawn behind the main torque curve. The right waveform styles are
preserved: their largest waveform stroke is 2.0 points. The left progressive
curves are wider, and even the context has greater nominal width times
opacity (2.6 points) than that right maximum (2.0 points). These nominal
measurements supplement the actual encoded small-screen visual review.

The red tau^mx, v_pk^mx and i_pk^mx limit symbols remain unchanged from the
verified revision-3 paper and healthy-video comparison, with upright (roman)
pk and mx. All three use 26-point mathematical text. Their complete bounding
boxes fit within their own panels below the dashed limit lines. The original
limits remain 2 Nm, 290 V and 4.34 A.

The distinct delivered filename IECON2026_OPFa_H21_speed_ramp_video_v5.mp4
identifies this revision. It has exactly the same bytes as the canonical
IECON2026_OPFa_H21_speed_ramp_video.mp4. The eleven-member ZIP includes the
canonical MP4 only; the extra revision filename is outside the ZIP.

HEADER REVISION
---------------
The single top line is centered and contains exactly IECON 2026, the speed
n = ... r/min and the torque reference T* = ... Nm. Only n is newly italicized;
the speed number and unit keep their existing upright type. The phase-a-open,
H21 and zero-cogging descriptors have been removed from this top line.
Header numbers, precision and scientific meanings are preserved.

Every new lossless source frame has been compared with the preceding delivered
frame: all RGBA pixels below the top 66 rows are bit-exact. The changed text
fits entirely inside those 66 rows. All 600 headers are centered and contain
only the three requested fields. Video encoding can introduce small compression
differences; full-frame and plot-region compression fidelity is checked below.

PACKAGE VERIFICATION
--------------------
This revision changes only the top header. The MATLAB calculation and entry
function bodies preceding the embedded presentation payloads are byte-identical
to the preceding verified package. The embedded renderer and its definitions
are updated. The LUT, merged inputs and frame table remain byte-identical.
The complete new video uses the original 600 native waveform cycles, with
all 4,200 array fingerprints verified again. All 19 context-field fingerprints
match the previously independently recalculated 9,973-row context.

A fresh execution of this revised MATLAB entry, with its search path reset
to the defaults, rebuilt all 9,973 context rows and ten representative cycles.
Every context value and all 70 native array fingerprints matched exactly.
All ten preview PNGs matched the corresponding new full-video PNGs exactly.
The earlier full 600-cycle MATLAB recalculation remains applicable through
the unchanged scientific source/data bindings; it was not rerun in this revision.
The new default-reference PNG and decoded-RGB hashes cover all 600 video frames.

The 90-frame pilot was fully decoded and checked before the complete video.
Every pilot PNG matches its corresponding full-video PNG. The full video was
decoded completely, verifying dimensions, duration, all 600 presentation
timestamps, frame order, colour tags, compression fidelity and drawing checks.
Encoded start, constraint-transition and endpoint frames were inspected at
1280 x 720 and 960 x 540 for the centered, simplified header and italic n.

All embedded support payloads and the readable runtime definition agree.
The ZIP has a verified exact eleven-member allowlist, CRC checks and a SHA-256
manifest for every other member. The saved deliverables are reopened and
checked against these verified artifacts; readback and preservation of other
files are recorded in the adjacent STEP9_verification.json.
Older Step-5 and Step-8 reports retain their original dates and scope.
