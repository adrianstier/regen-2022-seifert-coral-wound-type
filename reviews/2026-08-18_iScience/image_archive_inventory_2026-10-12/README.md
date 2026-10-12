# Coral wound-type image archive discovery

Inventory date: October 12, 2026. Read-only search of the mounted Stier_Lab NAS and accessible project folders in Google Drive, using the astier@ucsb.edu account. No source assets were changed, moved, or uploaded. This is a candidate inventory, not a verified complete archive.

## Main collections

| Collection | Location | Files | Size (decimal GB) | Contents |
| --- | --- | ---: | ---: | --- |
| Experiment 1, NAS original candidate | `/Volumes/Stier_Lab/3. Wound_Type_Airbrush_Dremel_2022 (Ashley copy)/3. Wound_Type_Airbrush_Dremel_2022/Wound comparison study` | 639 | 4.87 | 221 VSI, 320 PNG, 96 JPG, 1 AI, 1 PSD |
| Experiment 2, NAS original candidate | `/Volumes/Stier_Lab/Moorea 2025/Moorea 2025/Wound-Type 2025/Porites Wound Type` | 2,105 | 12.96 | 1,046 VSI, 1,052 TIFF, 7 AVI; includes uninjured samples |
| Experiment 2, additional early exports | `/Volumes/Stier_Lab/coral_regeneration_photos_videos/Porites TIFS` | 100 | 0.63 | TIFF exports; possible duplication of the main collection |
| Selected images and figure assembly | `/Volumes/Stier_Lab/Moorea 2025/Moorea 2025/Wound-Type 2025/Wound-Type manuscript Figures` | 212 | 2.77 | Mostly TIFF; edited images and figure assembly sources |
| Manuscript figures, including histology | `/Volumes/Stier_Lab/coral-regeneration/Manuscripts/B_wound_type/figures` | 72 | 2.68 | Illustrator, Photoshop, JPG, PDF, PNG, SVG; includes older versions |
| Experiment 3 fragment photographs | `/Volumes/Stier_Lab/coral-regeneration/Projects/21. Wound_type_histology_2025/data/Porites histology photos` | 23 | 0.032 | 15 JPG and 8 HEIC, before histological processing |

Counts are files, not unique photographs or biological replicates. Native microscope files, image exports, alternative magnifications/channels, and edited figures can represent the same specimen or image. Collection sizes must not be added to estimate a deduplicated deposit.

## Google Drive locations

- [Experiment 1 project](https://drive.google.com/drive/folders/17ynlZHpUySEW4NzFUJJZjhEVF-OqKFD3): 1,138 source-image candidates (6.19 GB), excluding the unrelated Island experiment and figure/timeline candidates. These include duplicated branches: available Drive MD5 checksums identify 589 distinct binary files among these candidates. This does not establish 589 unique photographs or reconcile the NAS collection.
- [Experiment 2 project](https://drive.google.com/drive/folders/1vm3IcmAfuZXF6cFQ3NTBTI0IA3cN5qIe): notes, scoring sheets, and pointers to NAS images. The main Porites image collection is on the NAS, not in this Drive folder. Acropora pulchra files belong to a separate experiment.
- [Histology project](https://drive.google.com/drive/folders/1j89PWbxYHYL7vmiFnzOBTm2gEwEBBaTq) and [fragment photographs](https://drive.google.com/drive/folders/1uqwzJJr62uokUxMWv4GI4EWKEhagmC6w): 23 pre-processing photographs, with histology metadata and characterization sheets. These are not stained tissue-section micrographs.
- [Histology specimen metadata](https://docs.google.com/spreadsheets/d/1rQUtYIC_tjwQ_hH0BkXV3892KkmOuSrIHz-XkWeHQD4/edit) and [histology characterization](https://docs.google.com/spreadsheets/d/1jwhFNV1rcPGVLm6AqL76ry2yETJ85d6brooLo2Air-U/edit).
- [Final figure assemblies](https://drive.google.com/drive/folders/15DJbDGTCVDoEwz4kcCkBZZg_o844nfyL): 14 Illustrator/JPG files. Filenames may use outdated supplementary figure numbering.
- [Figure 6 histology assembly](https://drive.google.com/drive/folders/1XWCqn1_4pMogtJ2_1hut8peJ_ZIedfzx): the NAS copy of `Fig. 6_V2.ai` is 1.67 GB and contains seven embedded high-resolution raster images. Their dimensions range from 14,811 x 6,507 to 22,081 x 8,382 pixels. These were inventoried using the file's PDF-compatible representation, not extracted. Their processing/cropping/stitching history is unknown.

## Issues to resolve before a public deposit

1. **Identify the original stained-section images.** They were not located as standalone source files in the searched folders. Ask Ashley where the originals underlying Figure 6 are stored. Embedded Illustrator images are a fallback, not proof of original unprocessed microscopy files.
2. **Reconcile Experiment 1 identifiers.** Some old folder genus labels disagree with the scored-data/sample-key identifiers, including sample 1a and 10a. Do not rename or assign species from the old folder labels without checking the original identifier history with Ashley/Molly.
3. **Check Experiment 2 filenames.** ID 10 appears in the Air Brush folder as well as the Dremmel folder, whereas the scored data place it in Scrape. There are also D12 filenames and filenames that do not fit the usual ID/day pattern. Determine whether these are typos, misplaced files, or valid additional images before constructing metadata.
4. **Check missing final fluorescence images.** No files matching the searched D63/RFP naming pattern for colonies 5 and 18 were found. This agrees with missing final scores but does not rule out differently named images.
5. **Check coverage and file readability.** Representative JPG/TIFF headers were readable, and Figure 6's PDF representation was readable. Every image and native VSI file has not been opened or validated; determine whether any native files require companion data. Fragment photographs found cover D7, D14, and D21, not every histology sampling time.
6. **Separate source and processed images.** Exclude unrelated Island and Acropora pulchra experiments, redundant exports, old figure versions, OS junk, and unrelated method trials from the paper's deposit. Keep processed figure sources separately labeled if included.
7. **Agree on public scope and licensing.** Obtain coauthor agreement on which images to release and the license, then prepare a specimen/image key linking the released files to the analysis and figures.

## Suggested archive structure

- `experiment_1/native/` and `experiment_1/exports/`
- `experiment_2/native/` and `experiment_2/exports/`
- `experiment_3/fragment_photos/` and `experiment_3/section_images/`
- `processed_figure_sources/`, if useful and explicitly labeled
- `image_metadata.csv`, `README`, and checksum manifests

Metadata should record original path/name, released filename, specimen and parent-colony identifiers, species, treatment, observation day, imaging channel, magnification/scale where known, native-to-export relationships, processing steps, and manuscript figure/panel where applicable. Leave genuinely unknown values explicit; do not infer specimen identity solely from conflicting folder names.

Zenodo's [current file guidance](https://help.zenodo.org/docs/deposit/manage-files/) allows 50 GB and 100 files by default and recommends ZIP packaging for large sets of files. The two principal NAS collections total about 17.84 GB before deduplication, but final deposit size remains to be determined. Preserve native files alongside open image exports; group the thousands of files into documented archives rather than individual uploads. No Zenodo draft or public record has been created.

## Inventory files and limitations

- `nas_originals.csv`: 3,130 file records across the six separately inventoried NAS collections, including one auxiliary export folder. Histology fragment photos are listed in `nas_files.csv`, not in this count.
- `nas_originals_summary.json`: NAS collection totals and extension breakdowns.
- `drive_files.csv` and `drive_folders.json`: recursively enumerated Drive files/folders under the four project roots above; unrelated files are retained with exclusion categories for auditability.
- `nas_files.csv`: sparse NAS copies of the three Drive project folders, not the full original imaging collections. The `.gdoc` and `.gsheet` files are pointers, not exported document contents.
- `drive_duplicate_checksums.json`: exact duplicate candidates based on available Drive MD5 metadata. No full NAS checksum pass was performed.
- `nas_drive_size_comparison.csv`: only 49 literal path matches; matching sizes do not verify matching content. Its single size mismatch is in the excluded Acropora pulchra experiment. Slash-to-space normalization and incomplete NAS project mirrors limit this comparison.
- `candidate_checks.json`: treatment-folder filename summaries, representative image headers, and Figure 6's embedded-image inventory.
- `location_notes.json`: text read from project notes and image-location documents.
- `summary.json`: refined classifications, totals, traversal errors (none), and size-comparison limitations.

The search is restricted to accessible Drive project roots and identified mounted NAS locations. It is not proof that no additional images exist elsewhere, and it does not establish complete specimen/day/channel coverage.
