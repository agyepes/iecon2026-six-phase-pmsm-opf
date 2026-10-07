# Validation record — version 1.0.0

Checked on **6 October 2026**. This record describes verification of the packaged viewer and documentation; it is not a new audit of every torque–speed point or a validation of a physical drive.

## Viewer identity and preservation

- Packaged HTML: `IECON2026_OPF_Comparison_NSBE_MeanTorque_290V_Boundaries.html`.
- SHA-256: `ae91320aa33f502f7baf23d317fd1a4704400e045c18b5e5f292caf49f27b6b9`.
- The packaged HTML matches the updated project file byte for byte.
- The separate “Feasibility labels” block was removed, with the existing detailed-check link moved into the preserved table footnote.
- All calculation scripts and the embedded data/metadata match the source before that presentation edit. The other HTML variants in the source folder were unchanged.
- The internal model identifier remains `1.4-nsbe-mean-matched-290v-boundaries`; the supplementary package version is `1.0.0`.

## Browser and interaction checks

The viewer was opened directly from a local file in **headless Chrome 154.0.8037.98**, with network access disabled for the page. Its embedded data, calculations, results table, and plots initialized without captured page errors or unhandled promise rejections.

Checks included:

- The default point, 5 N·m and 1500 r/min, producing five method rows.
- The retained constraint-check link opening both its enclosing model section and its own subsection.
- The table, footnote, and link at 1280-pixel and 390-pixel viewport widths, in light and dark themes; no page-wide horizontal overflow or overlap with the following block was detected. The wide results table retains its own horizontal scrolling on the narrow viewport.
- Results exported as JSON with all five methods.
- Waveforms exported as CSV with 250 angular samples and a header.
- The back-EMF spectrum using one series and exporting percentage-of-fundamental values.
- An entered target of 20 N·m at 200 r/min reporting the NSBE-FRML mean-torque result as unavailable.
- Independently extracting the ZIP and confirming that its HTML is byte for byte identical to the offline-tested copy.

These checks establish operation in the tested Chrome environment. Firefox, Safari, and a separate Edge run were not tested as part of this package preparation.

## Documentation and package checks

- Paper titles and author order were checked against the current HTML and the arXiv version-3 records for [25] and [26]. The local OPF manuscript PDF was reopened, with its first page and Fig. 7 page inspected visually, to check citation and scope.
- Conference location and dates were checked against the [official IEEE IECON 2026 site](https://www.iecon2026.org/).
- The DOI entries explicitly identify author preprints. No IEEE proceedings DOI, supplementary-package DOI, public repository URL, or page range was invented.
- `CITATION.cff` was parsed and validated against the official Citation File Format 1.2.0 schema.
- Local documentation links and HTML fragment links were checked for existing targets, with unique HTML IDs.
- The CC BY 4.0 licence notice follows the licence used for the author's existing related supplementary resources; it applies to this package, not to linked publisher papers.
- The ZIP was extracted independently, its archive integrity checked, and every extracted file compared byte for byte with the release folder. Manifest sizes and SHA-256 values were recomputed.

## Scope of this verification

The current generators, compact grid, and selected numerical criteria were retained. These package checks do **not** resolve compact-interpolation errors, NSBE-FRML voltage sensitivity to angular sampling, or the absence of a controller/switching model. They do not reproduce the paper's FEA cogging-compensation or example load-curve results. See [README.md](README.md) for the comparison criteria and limitations.

The archive contains only the viewer and release documentation/metadata. Source MAT files, cited paper PDFs, credentials, browser profiles, and temporary verification files are not included.

## Bibliographic wording update — 7 October 2026

References [25] and [26] and their accompanying paper mentions now use **IEEE IECON 2026**. The updated project and packaged HTML match byte for byte. All script blocks, including the embedded data and metadata, are byte-identical to the previously checked viewer. Citation metadata, local links, manifest values and ZIP contents were checked again; the earlier browser and numerical checks above were not repeated for this wording-only update.
