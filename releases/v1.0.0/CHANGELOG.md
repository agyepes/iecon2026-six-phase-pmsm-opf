# Change log

## 1.0.0 — 6 October 2026

Initial supplementary package associated with the IEEE IECON 2026 open-phase-fault paper [25].

- Includes the current compact-LUT HTML with nominal 290 V boundaries, the adjusted NSBE-FRML mean-torque comparison, independent plot controls, current and voltage plots, loss views, and back-EMF waveform/harmonic exports.
- Retains the latest one-bar-per-harmonic spectrum and optional percentage-of-fundamental scale.
- Removes the redundant “Feasibility labels” block. Retains the results-table footnote and places the link to the detailed constraint checks in that footnote; the link opens the containing model section and its constraint-check subsection.
- Adds opening instructions, scope and limitations, primary and supporting paper citations, a CC BY 4.0 licence notice, validation notes, and an integrity manifest.

The glossary edit changes presentation only. The calculation scripts, embedded numerical data, model settings, and method implementations are unchanged from the source HTML used for this release.

Package version **1.0.0** identifies this supplementary release. The retained internal HTML model identifier is **1.4-nsbe-mean-matched-290v-boundaries**; it is not the package version.

This release records known compact-interpolation and NSBE-FRML voltage-sampling limitations. It does not refine the LUT, introduce a closed-loop drive model, or replace a current generator.

Future additions will be recorded in subsequent package versions. Earlier viewer variants are not included as separate releases in this ZIP.

### Pre-publication wording update — 7 October 2026

- Added IEEE to the IEEE IECON 2026 references for papers [25] and [26], with consistent wording in the viewer and accompanying citations.
- Refreshed release manifests, checksums and archives. Calculation scripts and embedded data are unchanged.
