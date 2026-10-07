# Website validation record

Prepared and checked on 6 October 2026. This record concerns the two collection homepages and their distribution. The unchanged viewer has its own [version 1.0.0 validation record](releases/v1.0.0/VALIDATION.md).

## Content and association

- Both paper titles and complete author lists were checked against their arXiv version 3 records during preparation. OPF [25]: [arXiv:2607.24633v3](https://arxiv.org/abs/2607.24633v3). LUT reduction [26]: [arXiv:2607.24395v3](https://arxiv.org/abs/2607.24395v3).
- The conference location and dates were checked against the [IEEE IECON 2026 official website](https://www.iecon2026.org/): Doha, Qatar, 18–21 October 2026.
- The OPF viewer and release are associated with [25]. The supporting role of [26] is stated, and [26] has its own separate collection page.
- Future MATLAB, dataset and video categories have no download links or claims of existing files. The LUT-reduction collection has no separate file release listed.
- No public collection URL, repository, archive DOI or announcement has been invented. Both collection metadata files record a null public URL.

## Links and integrity

- All 32 local links on the two homepages resolved to existing files or valid page fragments.
- Both directions of the inter-collection navigation were exercised in a browser. The main **Open interactive viewer** link opened the included release HTML.
- The nine included release files matched the completed supplementary package byte for byte. The included OPF release ZIP matched the original archive, passed its CRC check and contained exactly the same nine files.
- OPF release ZIP SHA-256: `ce2e6c6ab5274b48e8a9826eac1d9589de6846a93aeb9e26831bd2bd6ffd0368`.
- Included viewer SHA-256: `ae91320aa33f502f7baf23d317fd1a4704400e045c18b5e5f292caf49f27b6b9`.
- The website distribution has its own manifest and SHA-256 file list. Its ZIP was extracted into a fresh folder and every extracted file was compared with the prepared distribution. The original release and project HTML files were rechecked during finalization.

## Browser and layout checks

The homepages were checked in headless **Chrome 154.0.8037.98** at widths **1280, 800, 390 and 360 CSS pixels**, in both light and dark mode. The OPF guide was also checked expanded at desktop and phone widths, giving **20 layout states** in total.

- No horizontal overflow, overlapping resource cards or clipped card/button text was detected in those states.
- All checked visible text had a calculated contrast ratio of at least **5.36:1** in its normal state, above the 4.5:1 threshold used by the check.
- Desktop pages, phone layouts, resource cards and expanded guide content were visually inspected from screenshots.
- The pages have descriptive links, a skip link, navigation and main landmarks, labelled sections, visible keyboard-focus styles and reduced-motion support. This is not a formal accessibility certification or a screen-reader audit.

## Offline and static-host use

- Both homepages were opened with browser networking disabled. They use embedded styles and icons and have no external runtime scripts, fonts or images.
- Following **Open interactive viewer** from the offline homepage completed the viewer’s default operating-point calculation and loss sweep. It reported 250 angular samples.
- The prepared folder was also served on a temporary local static HTTP server. Its then-existing 18 files returned exactly their on-disk bytes. The homepage’s viewer link again opened the correct HTML and completed its calculation.
- No public deployment was performed. Paper and licence links require internet access; local resources remain available offline.

## Scope of this verification

The website work does not change or independently revalidate the viewer’s scientific algorithms, model assumptions, original comparison boundaries or known sampling/interpolation limitations. Those remain as stated in the release documentation. Tests in this record establish the preparation, association, navigation, presentation and file integrity of the collection pages. They do not establish Firefox, Safari or other browser-engine compatibility.

## Bibliographic wording update — 7 October 2026

The paper references now consistently use **IEEE IECON 2026**. The two homepages, citation files and included OPF release were updated, and their local links, manifests, checksums and archive contents were checked again. The included viewer retains byte-identical calculation scripts and embedded data. The browser checks above record the earlier preparation; they were not repeated for this wording-only update.

## Direct online viewer entry — 7 October 2026

The collection now features **Run interactive viewer** as its primary action. The short **viewer/** entry automatically opens the unchanged version 1.0.0 viewer; an explicit fallback link is also provided. Downloads remain available for optional offline use. The empty **.nojekyll** file and **GITHUB_PAGES_SETUP.txt** prepare this distribution for static GitHub Pages hosting.

- The 24 distribution files were served through a temporary local HTTP server under a project subdirectory, matching a GitHub Pages project-site path structure. Every response matched the corresponding on-disk file; HTML was served as a webpage rather than an attachment.
- In headless **Chrome 155.0.8059.39**, the homepage button and both **viewer/** and **viewer/index.html** reached the correct versioned HTML. The default operating-point calculation produced all five method rows and the loss-versus-speed sweep without runtime errors. Changing speed to 200 r/min produced a new calculation result.
- With networking disabled, the extracted local homepage button and short entry still opened the viewer and completed its calculation and loss sweep. The viewer used no external runtime data or libraries in these checks.
- The updated homepage was checked at 1280, 390 and 360 CSS pixels in light and dark mode. The viewer and expanded publication-review page were also checked at desktop and phone widths, for 10 layout states in total. No page overflow or overlapping visible cards was detected. Homepage, viewer and review screenshots were visually inspected.
- All included release files and the OPF package archive remained byte-identical. Local links, paper association, manifests, checksums and the rebuilt website archive were verified again.

These checks establish the prepared local hosting arrangement. No GitHub repository or Pages configuration was changed, and no public deployment was performed. The final public homepage and direct viewer URL must be verified after publication. Scientific calculations and their documented limitations are unchanged.

## GitHub Pages publication — 7 October 2026

The collection is published at [https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/](https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/), with the direct viewer at [https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/viewer/](https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/viewer/). The repository is [agyepes/iecon2026-six-phase-pmsm-opf](https://github.com/agyepes/iecon2026-six-phase-pmsm-opf). Its publishing source is the **main** branch at the repository root, with HTTPS enabled.

The initial public deployment was checked against all 24 repository files. Served files matched their on-disk bytes; the .nojekyll hosting marker was checked through the repository API. The public OPF ZIP was downloaded and reopened independently, and its CRC, manifest and SHA-256 checksums matched the reviewed package.

In headless **Chrome/155.0.8059.39**, the homepage button and short viewer address opened the correct versioned HTML and completed the five-method operating-point calculation and loss sweep. An operating-point change produced a new result. Independent method visibility, the harmonic percentage view, JSON and CSV exports, and offline calculations from the downloaded ZIP were exercised successfully. The public homepage and viewer were checked at desktop and phone widths in light and dark mode, and their screenshots were visually inspected.

The nine-file OPF package and scientific viewer are unchanged. This publication verification adds hosting, navigation and distribution checks; it does not change the scientific scope documented in the release README.
