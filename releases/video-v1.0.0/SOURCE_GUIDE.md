# Guide to the video-generation source

The sole resource author/creator is **Alejandro G. Yepes**. This guide belongs
to standalone video package **1.0.0**, documentation revision **7**.
See [AUTHORSHIP_AND_CITATION.md](AUTHORSHIP_AND_CITATION.md) for resource and
research-paper attribution. Publication metadata revisions do not change the
commented source or its scientific and reproduction checks.

Alejandro G. Yepes created this supplementary video and its generation resources using ChatGPT 6.1 Sol (OpenAI).
This assistance acknowledgment is separate from resource authorship and from the research paper's authorship.
See [ACKNOWLEDGMENTS.txt](ACKNOWLEDGMENTS.txt).

This guide accompanies the commented `rebuild_iecon2026_opf_video.m`.
Start with [README.md](README.md) for installation and run commands, then read
the MATLAB file's help header and the comments beside each calculation.
In MATLAB, `help rebuild_iecon2026_opf_video` displays the public entry's
instructions. The long encoded blocks at the end are frozen support source;
the readable Python copies described below are easier to inspect.

## Files and responsibilities

| File | Purpose |
| --- | --- |
| `rebuild_iecon2026_opf_video.m` | Single public MATLAB entry. Contains loading, coefficient interpolation, waveform reconstruction, metrics, input guards and orchestration |
| `LUTs_data_OPF_H21_nt250.mat` | Full original LUT of phase-current Fourier coefficients and stored feasibility information |
| `IECON2026_OPFa_H21_inputs.mat` | Original paired speed/torque samples, selected trajectory, normalized EMF and reference plot context |
| `STEP8_Video_frame_samples.csv` | Original sample identities and reference metrics for the 600 displayed frames |
| `IECON2026_OPFa_H21_speed_ramp_video.mp4` | Delivered reference movie; required for the package's reproduction checks |
| `IECON2026_OPFa_H21_package.json` | Readable configuration/provenance; its `runtime_definition` matches the definition embedded in MATLAB |
| `REFERENCE_INPUTS.json` | Current MATLAB entry hash, four mandatory input identities and reference environment |
| `rendering_support/exact_layout.py` | Fixed figure geometry, traces, labels, colours, measurement brackets and artist checks |
| `rendering_support/package_driver.py` | Dependency preflight, native-cycle loading, rendering, encoding and reproduction orchestration |
| `rendering_support/exact_inspector.py` | Encoded format/timing, complete decode, image fidelity and frame-order checks |

The three readable Python files are exact copies of the embedded payloads.
The MATLAB entry extracts and executes its embedded copies in the chosen
output folder. Editing a readable Python copy by itself does not change a
MATLAB-generated video. The embedded definition also fixes its reference
hashes, data selection and rendering parameters.

## MATLAB function map

The entry is a **function file**, not a script to execute section by section.
Call its first function with `check`, `preview` or `full`. Its other functions
are private implementation details in the same file.

| Function | What to read in its comments |
| --- | --- |
| `rebuild_iecon2026_opf_video` | Modes, inputs, output ownership, trajectory preservation, comparison scope and reports |
| `pkg_rebuild_plot_context` | Why all 9,973 progressive rows are recalculated using the common waveform engine |
| `load_model` | LUT dimensions, units, machine parameters, feasible-vertex mask and normalized EMF identity |
| `interpolate_coefficients` | Actual versus lookup frequency, bilinear weights, infeasible-corner rejection and neutral-current bound |
| `reconstruct` | The paper's harmonic/phase-angle convention, analytical derivative, voltage and torque equations |
| `normalized_emf` | Periodic linear interpolation and paired or pointwise half-wave symmetrization |
| `iecon2026_opf_cycle_metrics` | Same-cycle torque, ripple, peaks, individual phase RMS, copper loss and complete-vector d1/q1 |
| `pkg_metric_comparison` | Frame identity, 17 scalar checks, units, extrema and independent Parseval comparison |
| `pkg_python` | Hidden process launch, literal Windows arguments, concurrent log capture and error propagation |
| `pkg_payload` | The four frozen encoded payloads and why readable copies are inspection aids |

## Scientific conventions that must stay together

- **Phase and harmonic order:** phases a-f correspond to indices 1-6;
  `phi_k=(k-1)*pi/3`; `h=1,3,...,21`. LUT coefficients have dimensions
  `[torque point, electrical-frequency point, phase, harmonic]` and units A.
  Interpolated coefficients are `[operating point, phase, harmonic]`.
- **Current reconstruction:**
  `i_k=sum_h(IRe_kh*cos(h*(theta-phi_k))+IIm_kh*sin(h*(theta-phi_k)))`.
  Each healthy phase has independent coefficients. Phase a remains exactly
  zero. The small float32 neutral residual is measured, not projected away.
- **Speed:** input `n` is mechanical r/min. `omega_m=2*pi*n/60` and
  `omega_e=5*omega_m`. LUT frequency is electrical Hz. Below the first
  retained column, only coefficient lookup frequency is held at that column;
  EMF and inductive voltage use actual speed.
- **EMF and torque:** stored `e_prime=e/omega_m` has units V/(mechanical rad/s).
  Use periodic linear interpolation followed by half-wave symmetrization.
  Here `T=sum_k(e_prime_k*i_k)` because `T_cog=0`; no further speed or
  pole-pair factor belongs in that torque expression.
- **Voltage:** derive the phase voltage from the complete VSD machine model
  and analytical `di/dtheta`. The paper's `v'_r` denotes component r of
  `v'=G_prime*v`. Check all ten healthy-terminal pairs:
  bc, bd, be, bf, cd, ce, cf, de, df and ef. Keep the open phase's EMF in the
  machine model. Its current being zero does not make its induced EMF zero.
- **Metrics:** waveform arrays are `[point, angle, phase/line]`; reductions
  across angle use dimension 2. Ripple is `max(T)-min(T)`, and phase/line
  peaks use absolute values. Compute RMS separately for each phase. Physical
  stator copper loss is `1.4*sum_k(RMS_k^2)` W. The normalized A-squared
  quantity is a different field. Parseval checks consistency independently.
- **d1/q1:** use the complete six-phase current vector and the documented
  negative-Park display convention. Left-panel d1/q1 values are cycle means;
  a balanced single-coefficient shortcut is unsuitable for this fault case.

The scalar voltage peak is `v_pk`; the voltage waveform is `v'_r`. The
paper's limit names are `i_pk^mx`, `v_pk^mx` and `tau^mx`, corresponding to
4.34 A, 290 V and 2 Nm. The machine's reported nameplate values are separate
from those optimization limits.

## Selection, sampling and limits

Original speed and torque arrays contain 1,443,053 paired samples. This
release retains the contiguous prefix 1-1,314,036, without clipping, sorting,
smoothing or creating a synthetic endpoint. The first excluded point fails
the nonzero-weight interpolation-support check. Passing the envelope alone
does not guarantee usable coefficients at all bounding vertices.

The displayed source indices are `floor(linspace(1,1314036,600)+0.5)`.
Each displayed cycle uses 16,000 uniform electrical angles, excluding 0 and
including 2*pi once. The offline optimization used 250 angles. Frame k starts
at `(k-1)/30` seconds of playback; the last frame starts at 19.9666667 s and
the complete 600-frame movie lasts 20 s. This is not physical acceleration
time or a controller-tracking simulation.

`check` verifies all 600 sampled cycles; `preview` verifies/renders ten
selected cycles. Both recalculate the complete progressive context. Only
`full` encodes and checks the entire movie. `StrictReference=true` checks
exact reference identities in the applicable mode. Setting it to false
does not disable mandatory input hashes or change any physical limits.

Reproduction verification and continuous-angle feasibility answer different
questions. The separate full-path audit found current/voltage excesses of
approximately 0.139%/0.325%, while ripple remained below 2 Nm. These excesses
remain in the data and movie. The included Step-5 report describes that
earlier audit; the video entry does not rerun its separate continuous-audit
scripts. A sampled-cycle reproduction PASS must not be described as proof
of continuous-angle current/voltage compliance.

## Reading run outputs

| Output in the chosen working folder | Meaning |
| --- | --- |
| `run_binding.json` | Exact entry hash, mode, input identities and executable paths; prevents incompatible output reuse |
| `runtime_definition.json` | Decoded definition actually used in this run |
| `progressive_context_verification.json` | Recalculated context comparisons, with tolerance and bit-exact results |
| `rebuilt_plot_context.mat` | Newly calculated progressive data consumed by the renderer |
| `native_verification.json` | Checked cycle IDs, array fingerprints, scalar errors and physical-status qualifications |
| `dependency_preflight.json` | Rendering environment and font/tool identities; preview/full only |
| `rendered_frames/` and `frame_verification/` | Verified PNGs and per-frame scientific/artist checks; preview/full only |
| `python_*_stdout.log`, `python_*_stderr.log` | Captured diagnostics from hidden support processes |
| `reproduction_review.json` and rebuilt MP4 | Complete encode/decode verification and output movie; full only |

Use a fresh output folder after changing the source, mode or runtime options.
If a guard fails, read its error and logs. Turning off strict reproduction
checks is not a remedy for unsupported LUT points or inconsistent science.

## Comment revision and historical evidence

The earlier comment revision (documentation revision 1) adds MATLAB help, section headings and explanatory
comments, and corrects four existing comment lines. No executable MATLAB
statement, embedded payload, reference input or video byte is changed.
[ANNOTATION_VERIFICATION.json](ANNOTATION_VERIFICATION.json) records the
original/current source hashes, reversible comment-edit map and fresh
numerical check of the annotated entry. Reversing only the recorded comment
edits recovers the original entry byte for byte.

The full 600-frame render/decode proof was obtained before this comment
revision. [CURRENT_RELEASE_VERIFICATION.json](CURRENT_RELEASE_VERIFICATION.json)
identifies that earlier source and the subsequent comment-equivalence and
fresh numerical checks separately. The original `README.txt`,
`REPRODUCTION_VERIFICATION.json` and `STEP8_verification.json` are preserved
historical evidence with their own source hashes and scopes.

For a derivative with new coefficients, trajectory, physics, sampling or
layout, update the relevant embedded configuration and identities, verify
the derivative, and label it as changed. Do not remove guards to force a
different dataset through the fixed reference package. Licence, attribution
and paper citation are in the accompanying release documents.

## Citation instructions

Cite the paper when using the method. If you use or adapt the generation files, also cite the specific software release used.

This package is supplementary software and visualization material accompanying
the paper. The current README and AUTHORSHIP_AND_CITATION.md distinguish the
sole-author software release from the six-author research paper.
