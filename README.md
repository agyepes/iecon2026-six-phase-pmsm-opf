# IEEE IECON 2026 supplementary collections

[**Run the interactive viewer online — no download required**](https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/viewer/)

[Paper and supplementary collection](https://agyepes.github.io/iecon2026-six-phase-pmsm-opf/) · [GitHub repository](https://github.com/agyepes/iecon2026-six-phase-pmsm-opf) · [Download the offline package](downloads/IECON2026_OPF_Supplementary_v1.0.1.zip)

**Version 1.0.1 · 7 October 2026.** The resource accompanies the IEEE IECON 2026 open-phase-fault paper **[25]**. The online viewer and offline download use this release. [Earlier release v1.0.0](https://github.com/agyepes/iecon2026-six-phase-pmsm-opf/releases/tag/v1.0.0) remains available. A separate archive DOI has not yet been assigned.

## Run the viewer online

Readers can open the direct viewer link above or select **Run interactive viewer** on the OPF homepage. The viewer runs directly in the browser; downloading or extracting a ZIP is optional. Its short online entry is **viewer/**, which automatically opens the selected versioned HTML. It opens the version 1.0.1 HTML online or from this local folder. The paper [25] remains identified in the viewer and collection.

The direct viewer link is featured at the top of this README and in the repository About website field. Readers need no GitHub account or MATLAB installation to use the online viewer.

For the current hosting settings and maintenance instructions, see [GITHUB_PAGES_SETUP.txt](GITHUB_PAGES_SETUP.txt). The empty **.nojekyll** marker prepares the existing files for static GitHub Pages hosting.

## Open a local copy

To review the collection locally, extract the complete website ZIP and open **index.html** in a browser. Select **Run interactive viewer** to open the viewer. **Download package** provides the optional offline release and documentation.

The homepages have no external scripts, stylesheets, fonts or images. They can be read offline. The interactive viewer requires JavaScript; its calculations also work offline. Paper and licence links need an internet connection. Local download links may open a file or prompt for a save location, depending on the browser.

Open **lut-reduction/index.html** for the separate collection associated with the LUT-reduction paper **[26]**. It currently contains the paper citation and preprint link, with categories reserved for future supplementary files. No separate software or data release is listed there.

## Paper association

The main collection is associated with:

Alejandro G. Yepes, Wessam E. Abdel-Azim, Oscar López, Petros Karamanakos, Ayman S. Abdel-Khalik, and Jesús Doval-Gandoy, “Current References for Minimum Copper Loss and Torque Ripple in the Full Torque-Speed Range for Symmetrical Six-Phase PMSMs With Nonsinusoidal Back-EMF Under an Open-Phase Fault,” IEEE IECON 2026, Doha, Qatar, 18–21 October 2026. Author preprint DOI: [10.48550/arXiv.2607.24633](https://doi.org/10.48550/arXiv.2607.24633).

The other collection is associated with:

Alejandro G. Yepes, Shirin Rahmanpour, Oscar López, Wessam E. Abdel-Azim, Petros Karamanakos, Ayman S. Abdel-Khalik, and Jesús Doval-Gandoy, “Optimization of Current Lookup Tables for Minimum Stator Copper Loss and Torque Ripple in the Full Torque-Speed Range for a Six-Phase PMSM With Nonsinusoidal Back-EMF,” IEEE IECON 2026. Author preprint DOI: [10.48550/arXiv.2607.24395](https://doi.org/10.48550/arXiv.2607.24395).

These DOIs identify the author preprints, not the website, release package or IEEE proceedings records. Reference numbers follow the OPF viewer. The compact-LUT implementation in the OPF viewer uses the supporting reduction approach of [26]; the viewer remains supplementary material for [25].

## Contents

- **index.html** — OPF collection homepage, with online use as its primary action.
- **viewer/index.html** — short entry that automatically opens the selected versioned viewer.
- **.nojekyll** and **GITHUB_PAGES_SETUP.txt** — static-hosting marker and one-time publisher instructions.
- **collection.json** — OPF paper metadata and resource list, with available files distinguished from reserved categories.
- **releases/v1.0.1/** — the exact nine files from the completed OPF supplementary release, including the viewer, README, citations, licence, change log, validation record and checksums.
- **downloads/** — the revised OPF version 1.0.1 package ZIP and its SHA-256 checksum.
- **lut-reduction/** — the separate homepage, citation and resource list for [26].
- **LICENSE.txt**, **VALIDATION.md**, **manifest.json** and **SHA256SUMS.txt** — licence, verification and integrity information for this website distribution.

All website links use relative paths for included files, so the same folder structure can be used locally or on a static web host. No account, build process or server application is required. The GitHub repository and Pages site are public. Archiving and social-media announcements are separate publication steps.

## Interpreting the viewer

The version 1.0.1 viewer keeps the calculation scripts and embedded data of published version 1.0.0. This revision adds an acknowledgment and updates the README. Its comparison criteria and opening instructions are in [the viewer guide](releases/v1.0.1/README.md); the model and detailed constraint checks are available in the HTML.

## Add resources later

1. Place new files in a new versioned release folder, with documentation, citation, licence and checksums appropriate to that release. Keep earlier releases unchanged. Update **viewer/index.html** only when a newer version should become the default online viewer.
2. Add a descriptive resource entry to the appropriate collection.json and a matching link on that collection’s homepage. The JSON resource lists document the collections; the static pages do not automatically rebuild from them.
3. Update the current release indicator only when that release is actually available. Reserved MATLAB, dataset and video categories are not downloads.
4. Keep resources primarily associated with [26] in its separate collection. Cross-link the two collections when a resource supports both papers, and state its primary association.
5. Check local links, file hashes, paper metadata, offline use and the layouts again. Rebuild the website checksum list and archive after any change.
6. Once public hosting and archiving are completed, add the verified public URLs and archive identifiers to the relevant homepage, documentation and collection metadata. Do not replace a paper DOI with a package DOI.

## Acknowledgment

This interactive HTML viewer was created with the help of ChatGPT (OpenAI).

## Licence

The original collection pages and their accompanying documentation are offered under CC BY 4.0; see [LICENSE.txt](LICENSE.txt). The included release retains its own [licence notice](releases/v1.0.1/LICENSE.txt). Linked research publications retain their own reuse terms.
