# IECON 2026 supplementary video and generation files — v1.0.0

**Version 1.0.0 · presentation revision 5 · documentation revision 8**

**Sole resource author/creator: Alejandro G. Yepes.**
This is supplementary software and visualization material accompanying the paper,
provided as one video-and-generation package, separate from the existing
interactive HTML supplement.

**Video-package version DOI:** [10.5281/zenodo.23304581](https://doi.org/10.5281/zenodo.23304581).
Use this version DOI to identify the exact software release. Copies distributed on other platforms identify the same supplementary resource.

Package title: Supplementary video and generation files for the IECON 2026 paper “Current References for Minimum Copper Loss and Torque Ripple in the Full Torque-Speed Range for Symmetrical Six-Phase PMSMs With Nonsinusoidal Back-EMF Under an Open-Phase Fault”

A 20-second, quasi-steady visualization of the paper's stored current references
for a symmetrical six-phase PMSM with **phase a open**, nonsinusoidal back-EMF,
one isolated neutral, five pole pairs, odd harmonics through **H = 21**, and
**zero cogging torque**. Speed increases approximately from 850 to 1500 r/min
along the original load curve. The video uses the full original LUT.

The MATLAB entry reconstructs references from an existing LUT. The offline
LP/QP optimization that produced the LUT is described in the paper; this
package supplies its stored results and the video calculation. It does not
run the optimizer or a current-control simulation.

## Watch or rebuild

- Watch **`IECON2026_OPFa_H21_speed_ramp_video.mp4`** at its original 16:9 aspect ratio.
- For reproduction, extract **`IECON2026_OPFa_H21_video_and_generation_v1.0.0.zip`** into a nonsynchronized local
  folder. Keep the enclosed `IECON2026_OPFa_H21_package` files together.
- A complete extracted package includes both MAT files, the frame CSV and
  the delivered MP4. **The MP4 is also a required reference input**, used to
  check reproduction. A GitHub source checkout alone lacks these large inputs.

The original frozen technical guide is [README.txt](README.txt); the current
verification summary is [VERIFICATION_SUMMARY.md](VERIFICATION_SUMMARY.md).

## Reference movie and upload copy

The original movie inside the ZIP is the generator's required reference
input and retains its original bytes, technical metadata and hash.
Use that enclosed reference for reproduction.

The separate loose MP4 is the publishing copy. Its embedded title now uses
the agreed package title, and its creator tag names Alejandro G. Yepes.
No compressed video was re-encoded: all 600 encoded packets, their timing
and all 600 decoded RGB frames are identical to the archived reference.
Only the container metadata and resulting whole-file checksum differ.
Do not overwrite the ZIP's reference MP4 with the loose upload copy.
See [UPLOAD_VIDEO_VERIFICATION.json](UPLOAD_VIDEO_VERIFICATION.json).

## Commented source and code guide

The earlier comment revision (documentation revision 1) expanded the MATLAB
help header, added navigable sections and explained units, dimensions, equations, interpolation boundaries,
actual versus lookup speed, measurements and verification beside the code.
Read [SOURCE_GUIDE.md](SOURCE_GUIDE.md) for the function/file map, report
interpretation and adaptation rules. In MATLAB, use
`help rebuild_iecon2026_opf_video` to read the public entry instructions.

That revision changed comments and accompanying documentation. Every executable
MATLAB statement, embedded Python/definition payload, scientific input and
movie byte is preserved. [ANNOTATION_VERIFICATION.json](ANNOTATION_VERIFICATION.json)
records reversible source edits and the earlier strict check of all 9,973 context
rows and 600 cycles. The complete render/decode proof was obtained before
this comment revision; its source identity is recorded separately. The
original README.txt and historical proofs retain their earlier hashes and
scope. Use this README and the current verification records for this package.

## Requirements

The supplied entry is verified on **Windows**, using base MATLAB with JVM and
its Windows .NET process launcher. It requires no Optimization Toolbox or
Simulink for this video rebuild. Rendering additionally requires Python,
NumPy, SciPy, Matplotlib, Pillow, threadpoolctl, FFmpeg and FFprobe, and an
installed Times New Roman font. These dependencies are installed separately.

The exact reference uses MATLAB R2026a Update 5, Python 3.13.3,
FFmpeg/FFprobe 8.1.2, and the versions in
[requirements-reference.txt](requirements-reference.txt). See
[REFERENCE_INPUTS.json](REFERENCE_INPUTS.json) for dependency versions,
font identity and the four required input hashes.

`StrictReference=true` is the default. It requires reference Python packages,
FFmpeg version and font hashes, and exact native arrays, plot context, rendered
PNGs and decoded pixels. `StrictReference=false` relaxes exact reference
identity while retaining numerical tolerance checks and recording differences.
That option does not remove the Windows or installed-font requirements, and
does not turn a different rendering into a verified identical reproduction.

## Run in MATLAB

Set the MATLAB current folder to the extracted `IECON2026_OPFa_H21_package`.
The following examples use the current user's local application-data folder;
no path from the original author's workstation is required. Use a **new output
folder** for each run. Outputs must be outside OneDrive and outside the package.

```matlab
output_root = fullfile(getenv('LOCALAPPDATA'),'IECON2026_H21_rebuild');

% Recalculate all 9,973 context rows and all 600 cycles without rendering.
rebuild_iecon2026_opf_video('check',fullfile(output_root,'check'));

% Set this to the absolute python.exe of your chosen Python environment.
python_exe = fullfile(getenv('LOCALAPPDATA'), ...
    'Programs','Python','Python313','python.exe');

% Rebuild ten representative static frames.
rebuild_iecon2026_opf_video('preview',fullfile(output_root,'preview'), ...
    'PythonExecutable',python_exe);

% Rebuild, encode, decode and inspect the full 600-frame video.
rebuild_iecon2026_opf_video('full',fullfile(output_root,'full'), ...
    'PythonExecutable',python_exe);
```

The Python executable must be a real installed file, not a Windows Store
alias. Install the pinned packages into that environment using
`python -m pip install -r requirements-reference.txt`. FFmpeg and FFprobe must
be on PATH or supplied as absolute executable paths using the name/value
arguments `FFmpegExecutable` and `FFprobeExecutable`. The output folder
contains logs, numerical checks, frame checks and `reproduction_review.json`.

The script keeps its input package read-only and verifies input hashes before
and after execution. It uses hidden child processes and the Matplotlib Agg
backend. Historical paths in the original metadata are provenance only.
The readable [rendering_support/](rendering_support/) files exactly match the
embedded Python support; the MATLAB entry remains the single execution entry.

## What the video shows

The left column follows speed, mean torque, torque ripple, peak healthy line
voltage, peak phase current, individual healthy-phase RMS currents, complete-
vector d1/q1 means, and stator copper loss. The right column shows one complete
electrical cycle of torque, back-EMF, phase current and all **ten** line voltages
between healthy phases b-f. The line-voltage symbol follows the paper,
`v'_r`; all waveform measurements come from those same cycles.

Phase a's current is exactly zero; its back-EMF remains in the machine model.
RMS values differ across healthy phases because the reference currents are
unbalanced. The mean d1/q1 display retains the documented historical sign
convention and is derived from the complete phase-current vector.

## Sampling and interpretation

The original paired trajectory has 1,443,053 samples and no physical time
vector. The selected prefix contains original indices 1-1,314,036, ending at
1499.999963 r/min immediately before the first unsupported point above 1500.
Its original fluctuations and approximately 849.87-r/min minimum are retained.
There is no speed/torque clipping, smoothing, sorting or synthetic endpoint.

The 600 displayed original indices are
`floor(linspace(1,1314036,600) + 0.5)`.
The 20 seconds at 30 fps are **playback time**, not a physical acceleration
time or a demonstration of controller tracking. Each fixed operating point
is reconstructed on 16,000 electrical angles. The original optimization used
250 angles, including 2*pi and excluding 0; the reconstruction follows the
same endpoint convention with a finer grid.

Coefficient interpolation is bilinear in torque and retained electrical
frequency, with feasible-envelope and nonzero-weight corner checks. Below
the first retained column (956.399963 r/min), coefficients use that column,
while back-EMF and voltage retain the actual physical speed. EMF is
periodically linearly interpolated and half-wave symmetrized. Current uses
the paper's phase-angle convention for every odd harmonic 1,3,...,21.

## Numerical qualification

Prescribed peak-current, peak-line-voltage and peak-to-peak ripple limits are
4.34 A, 290 V and 2 Nm. The separate continuous-angle audit of the full
original trajectory bounds the maxima as follows:

| Quantity | Continuous-angle maximum bounds | Result |
| --- | --- | --- |
| Peak phase current | 4.346018184232-4.346018192883 A | 0.006018193 A above the cap, approximately 0.1387% |
| Peak healthy line voltage | 290.942789996125-290.942790522166 V | 0.942790522 V above the cap, approximately 0.3251% |
| Torque ripple, peak to peak | 1.916966661023-1.916966662228 Nm | Below 2 Nm |

The maximum overshoots are approximately **0.139% in current** and
**0.325% in line voltage**; the table gives their more precise values.

**Continuous-angle current and voltage compliance fails.** These small
overshoots of the original LUT occur between optimization angles and are
preserved, not rescaled or hidden. The 16,000-angle display is sampled; it is
not itself a continuous-angle feasibility certificate. The included Step-5
report describes the earlier full-path audit, also covering straight diagnostic
connections (whose voltage upper bound is 290.942812504687 V).

Those enclosures use conservative double-precision calculations with explicit
roundoff allowances; they are not a formal directed-rounding interval proof.
The report's Section 10 lists files from the original audit workspace. Those
separate continuous-audit scripts and numerical MAT files are not bundled in
this video-generation archive. The supplied entry regenerates the video
waveforms and display metrics; it does not rerun that separate audit.

Float32 LUT storage leaves a neutral-current residual below about
5.605e-7 A over the original ramp. No neutral projection is applied.
Dense-angle mean torque may differ from the 250-angle prescribed mean by
about 2.76e-5 Nm. This release does not simulate current tracking, switching,
coefficient derivatives during acceleration, FEA or experimental measurements.
It does not demonstrate the paper's separate cogging-compensation result or
comparisons with other methods.

## Resource citation, research paper and licence

Cite the paper when using the method. If you use or adapt the generation files, also cite the specific software release used.

**Specific software-release citation (when the files are used or adapted):**

Alejandro G. Yepes (2026), Supplementary video and generation files for the IECON 2026 paper “Current References for Minimum Copper Loss and Torque Ripple in the Full Torque-Speed Range for Symmetrical Six-Phase PMSMs With Nonsinusoidal Back-EMF Under an Open-Phase Fault”, version 1.0.0. Zenodo. https://doi.org/10.5281/zenodo.23304581.

This citation identifies the video-and-generation release, version 1.0.0.
The existing HTML DOIs identify the separate HTML resource.

**Cite the associated research paper with all six authors, in order:**

Alejandro G. Yepes, Wessam E. Abdel-Azim, Oscar López, Petros Karamanakos, Ayman S. Abdel-Khalik, and Jesús Doval-Gandoy, “Current References for Minimum Copper Loss and Torque Ripple in the Full Torque-Speed Range for Symmetrical Six-Phase PMSMs With Nonsinusoidal Back-EMF Under an Open-Phase Fault,” in IECON 2026 - 52nd Annual Conference of the IEEE Industrial Electronics Society, Doha, Qatar, 18-21 October 2026. Author preprint: arXiv:2607.24633v3, doi: 10.48550/arXiv.2607.24633.

The DOI above identifies the author preprint. An IEEE proceedings DOI and
page range have not been verified. The paper's research authorship remains
separate from the sole authorship of these supplementary resources.

See [AUTHORSHIP_AND_CITATION.md](AUTHORSHIP_AND_CITATION.md),
[CITATION.txt](CITATION.txt), [CITATION.cff](CITATION.cff) and
[CITATION.bib](CITATION.bib). The CFF's main citation is the resource;
the research paper is a reference, not a replacement preferred citation.
If integrating this folder into the existing repository, use the citation
in this versioned video folder; a repository-root citation for the HTML
supplement does not identify the video package.

The original package materials use [CC BY 4.0](LICENSE.txt).
Dependencies, fonts and linked research publications retain their own terms.
Assistance acknowledgments are separate in
[ACKNOWLEDGMENTS.txt](ACKNOWLEDGMENTS.txt).

## Creation acknowledgment

Alejandro G. Yepes created this supplementary video and its generation resources using ChatGPT 6.1 Sol (OpenAI).
This assistance acknowledgment is separate from resource authorship and from the research paper's authorship.

## Associated research funding

The paper acknowledges the Spanish State Research Agency (AEI) and project
**PID2022-136908OB-I00**, MCIN/AEI/10.13039/501100011033/FEDER-UE.
The project number is normalized to the hyphenated form in the
[official AEI grant listing](https://www.aei.gob.es/ayudas-concedidas/buscador-ayudas-concedidas?code=PID2022-136908OB-I00). This records the associated research
funding; it does not claim an additional award for the visualization package.

## Related interactive HTML supplement

The existing interactive HTML supplement remains a separate resource,
version 1.0.1. This video uses the full H21 LUT; the viewer uses a compact
LUT and its own documented comparison rules and tolerances. Those rules
must not replace the video's full-LUT numerical qualification.

- [Existing HTML release 1.0.1](https://doi.org/10.5281/zenodo.23222573)
- [Existing HTML all-versions DOI](https://doi.org/10.5281/zenodo.23222572)
- [Interactive HTML viewer](https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/viewer/)
- [Existing repository](https://github.com/agyepes/iecon2026-six-phase-pmsm-opf)
- [Associated paper preprint](https://arxiv.org/abs/2607.24633v3)

The two HTML DOIs above identify the HTML supplement. The video ZIP and
loose MP4 are distributed together through the video-package version DOI
[10.5281/zenodo.23304581](https://doi.org/10.5281/zenodo.23304581).
The existing HTML ZIP is not included in this video-generation package.

## Current verification: documentation revision 8

The complete archive and all internal checksums are checked independently.
The latest strict MATLAB calculation was completed during Step 6 from the
extracted documentation-revision-6 archive: all 9,973 progressive rows and
19 fields match exactly, and all 600 cycles pass 4,200 array fingerprints and
10,200 scalar comparisons. The entry and all four required inputs in this
revision are byte-identical to those used in that execution. The source
archive hash, execution time and this byte-identity bridge are recorded in
[CURRENT_RELEASE_VERIFICATION.json](CURRENT_RELEASE_VERIFICATION.json).

This revision audits those records and corrects documentation; it does not
perform another MATLAB run, render, encode or continuous-angle audit. A fresh
media check confirms that all 600 encoded packets and decoded RGB frames
still match the archived reference and embedded gold fingerprints. Earlier
rendering and physical-limit audits keep their original scope and dates.
Actual platform upload/download receipts stay outside the reproduction
archive to avoid circular checksums. Publication status must be checked in
those receipts; a reserved DOI alone does not establish publication.

### Earlier documentation revision 6

Documentation revision 6 specifies ChatGPT 6.1 Sol (OpenAI) in the
creation acknowledgments and prepared platform descriptions. Sole human
resource authorship and the full research-paper citations remain as above.
The ZIP is repacked and its checksums are refreshed. This revision changes
documentation and private-draft metadata only; the MATLAB entry, embedded
and readable helpers, scientific inputs and both movies retain their bytes.
The prior revision-5 audit and numerical/rendering proofs remain historical
evidence with their original times and source identities. The final
private-draft upload/download receipt is outside the ZIP.

### Earlier documentation revision 5

Documentation revision 5 rechecks publication steps 1-5 against the local
manuscript, public citation sources, package files and the same private
Zenodo draft. It corrects the licence credit to include the already-reserved
video DOI and makes the required Zenodo account-integration check explicit
before a later GitHub release. The revised documents are independently
checked and the archive is repacked. The final replacement-upload receipt
is kept separately in Publication_texts/Zenodo_draft_upload_verification.json.
A fresh media check compares all 600 encoded packets and decoded RGB
frames with the archived reference and embedded reference fingerprints.
The MATLAB entry, all four embedded payloads, readable Python support,
scientific inputs and original reference movie retain their exact bytes.
No scientific calculation, video rendering or encoding was repeated.
The documented current/voltage overshoots and historical execution
identities remained unchanged. The record was unpublished at that review.
