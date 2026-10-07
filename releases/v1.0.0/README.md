# Interactive supplementary material for the IEEE IECON 2026 open-phase-fault paper

**Version 1.0.0 · 6 October 2026**

This package accompanies **[25] Current References for Minimum Copper Loss and Torque Ripple in the Full Torque-Speed Range for Symmetrical Six-Phase PMSMs With Nonsinusoidal Back-EMF Under an Open-Phase Fault**, by Alejandro G. Yepes, Wessam E. Abdel-Azim, Oscar López, Petros Karamanakos, Ayman S. Abdel-Khalik, and Jesús Doval-Gandoy.

[Read the author preprint of the OPF paper [25]](https://arxiv.org/abs/2607.24633v3) · [Author preprint DOI](https://doi.org/10.48550/arXiv.2607.24633)

The viewer lets readers explore the paper's proposed current references and comparison methods at torque–speed operating points. It evaluates a steady-state mathematical model for a symmetrical six-phase nonsalient PMSM, with phase a open and a star connection with one isolated neutral point.

The proposed method in [25] computes the healthy phases' Fourier coefficients offline. Its optimization first minimizes sampled torque ripple, then minimizes stator copper loss while retaining approximately that minimum ripple and satisfying the specified constraints. This HTML uses an existing, reduced coefficient grid; it does not run the offline optimization.

## Open the viewer

1. Extract the ZIP completely.
2. Open [IECON2026_OPF_Comparison_NSBE_MeanTorque_290V_Boundaries.html](IECON2026_OPF_Comparison_NSBE_MeanTorque_290V_Boundaries.html) in a modern web browser with JavaScript enabled.
3. Enter a torque and mechanical speed, or select a point on the boundary map. Wait for the table and plots to finish updating.
4. Use each plot's own method controls to select the curves you want to compare. Use **Export results**, **Export waveforms**, or the back-EMF export control to save numerical data.

The HTML is self-contained and works offline. It needs no MATLAB installation, server, additional data files, or network connection for its calculations. Paper and licence links require internet access. The browser must support Web Workers and decompression of the embedded data. This release was checked in Chrome; verification details are in [VALIDATION.md](VALIDATION.md).

The input controls accept 0–20 N·m and 0–1800 r/min. These are exploration ranges, not an assertion that every point is feasible. The viewer evaluates the entered point rather than projecting it onto a boundary.

## What readers can explore

- The proposed and comparison torque–speed boundaries, with the healthy case as a boundary-only reference.
- A five-method results table: the proposed compact-LUT calculation, NSBE-FRML, and the star-adapted Atallah variants with γ = 1, 2.3, and 3.
- Phase currents, required line voltages, pole-voltage references, and torque over an electrical cycle.
- Total stator copper losses at the selected point and across speed at the entered torque.
- Back-EMF waveforms and the low-order odd harmonics 1, 3, …, 13. The spectrum uses one representative phase and one bar per harmonic, with amplitude or percentage-of-fundamental scaling.
- The model assumptions, constraint checks, source fingerprints, and bibliography.

Pole-voltage references use the DC-link midpoint and min–max common-mode injection over phases b–f. Their nominal guides are ±145 V; the calculated references are not clipped to those guides. The torque plot's ±1 N·m guides are centred on the midpoint of the proposed method's minimum and maximum torque.

The waveform and spectrum controls, including their exports, describe calculated references or model quantities. They are not measured inverter or machine signals.

## How [26] supports this package

The viewer remains supplementary material for the **OPF paper [25]**. The related IECON paper **[26] Optimization of Current Lookup Tables for Minimum Stator Copper Loss and Torque Ripple in the Full Torque-Speed Range for a Six-Phase PMSM With Nonsinusoidal Back-EMF** supplies the BS3B LUT-reduction approach.

That approach was demonstrated for healthy operation in [26] and adapted here to the OPF grid of [25]. The original OPF grid has 303 × 532 torque–speed points; the compact grid used in this HTML has 33 × 55. Both use odd current harmonics through order 21 and 250 electrical-angle samples. The complete full-LUT viewer and original MAT files are not included in this package.

**The method proposed in [26] is evaluated here only through the compact-LUT implementation.** This package is not a separate reproduction of all results in [26].

[Read the LUT-reduction author preprint [26]](https://arxiv.org/abs/2607.24395v3) · [Author preprint DOI](https://doi.org/10.48550/arXiv.2607.24395)

Reference numbers in this documentation follow those in the HTML.

## Interpret the comparisons

The nominal limits are **4.34 A peak phase current, 290 V peak line voltage between healthy phases, and 2 N·m peak-to-peak torque ripple**.

| View or calculation | Criterion used in this version |
| --- | --- |
| Top boundary map | All displayed boundaries use the nominal 290 V voltage limit, with the numerical tolerance of their respective calculation. The proposed and healthy limits are stored LUT boundaries. The Atallah limits are saved comparison results. NSBE-FRML is recalculated using the mean-torque adjustment and retains its existing 1% current and ripple allowances. |
| Selected-point table and loss curves | The selected criterion includes a 1% allowance: 4.3834 A, 292.9 V, and 2.02 N·m, plus the stated numerical tolerances. The table distinguishes nominal compliance, compliance within the allowance, exceeded limits, and unavailable results. |
| Torque matching | The proposed compact LUT is checked against the requested mean torque with its existing allowance. NSBE-FRML adjusts its internal reference to match the entered mean torque within numerical tolerance. Atallah retains an instantaneous-torque target at every evaluated angle. |

A common 290 V boundary limit does not make all methods' torque criteria, current/ripple allowances, or boundary sampling identical. The detailed checks and numerical tolerances remain available through **Constraint checks for each method**, linked beneath the results table.

For each torque, a saved Atallah boundary shows the upper end of the first consecutive feasible speed interval. Any later feasible interval after an intervening failure is omitted from that boundary. Entered operating points are checked independently.

In the loss-versus-speed plot, solid segments pass the viewer's selected criterion and dashed segments fail one or more checks. A method may have available curves at other speeds even when its selected-point calculation is unavailable. Read the selected-point legend status and the table together.

## Limitations that matter

**Compact interpolation.** Results are recomputed from interpolated coefficients and can differ from the full LUT, particularly near its boundary. A point inside the stored proposed boundary can still exceed a limit in the compact implementation; the table reports that failure. The original offline optimization does not guarantee that every interpolated compact result has strictly lower loss than every feasible comparison result.

**NSBE-FRML in this version.** An outer adjustment targets the entered mean torque. This differs from the instantaneous-torque criterion used for its original comparison in Fig. 7 of [25]. Its complete published ripple-control and gradual RMS-current-limitation stages are not implemented. A target for which no matching current solution is found is reported as unavailable, rather than displayed with a different achieved mean torque.

**NSBE-FRML voltage sampling.** The retained current generator can produce abrupt reference changes. A voltage estimate based on 250 electrical-angle samples may depend strongly on angular resolution and underestimate the requirement associated with those changes. Therefore its sampled boundary is not proof of physical realizability at that speed. This HTML does not simulate a digital current controller, switching, bandwidth, or tracking error. A real controller's smoothing would change the resulting currents and must be evaluated together with torque, ripple, and losses; it is not represented here.

**Atallah rejection policy.** “Current references infeasible” describes failure of the implemented current-reference calculation to return acceptable currents. It is not proof that every possible constrained current solution is impossible. The star adaptation and original rejection policy are retained.

**Sampled steady-state model.** Checks are made at 250 electrical angles and do not establish continuous-angle or hardware compliance. The healthy case supplies a boundary only. Cogging torque is set to zero; no FEA waveforms, closed-loop transient simulation, or example load-curve plot is included. Consequently the viewer does not reproduce the paper's cogging-compensation result or all of its load-curve results.

These limitations are documented in this package; its preparation did not replace the current generators, refine the compact grid, or resolve the voltage-sampling sensitivity.

## Files, citation, and licence

| File | Purpose |
| --- | --- |
| `IECON2026_OPF_Comparison_NSBE_MeanTorque_290V_Boundaries.html` | Self-contained interactive viewer, including its data and source fingerprints. |
| [CITATION.md](CITATION.md) | Human-readable citations for the OPF paper [25] and supporting LUT-reduction paper [26]. |
| [CITATION.cff](CITATION.cff) | Machine-readable package metadata, with [25] as the preferred citation. |
| [LICENSE.txt](LICENSE.txt) | CC BY 4.0 licence notice and attribution information. |
| [CHANGELOG.md](CHANGELOG.md) | Release history and scope of version 1.0.0. |
| [VALIDATION.md](VALIDATION.md) | Checks performed on this packaged copy and their scope. |
| [manifest.json](manifest.json) | Release metadata and checksums of the payload files. |
| [SHA256SUMS.txt](SHA256SUMS.txt) | Checksums, including the manifest, for integrity verification. |

When using this resource, cite **the OPF paper [25]** and identify **supplementary package version 1.0.0**. Also cite [26] when discussing the LUT-reduction approach. The linked arXiv DOIs identify the author preprints; they are not IEEE proceedings DOIs or a DOI for this supplementary package.

The HTML, embedded numerical data, and accompanying original documentation are supplied under **Creative Commons Attribution 4.0 International (CC BY 4.0)**, as described in [LICENSE.txt](LICENSE.txt). The linked papers retain their own publication and reuse terms.

This first package contains the viewer and its documentation. Future MATLAB files, datasets, or videos can be added in subsequent releases, with their provenance and changes recorded separately.
