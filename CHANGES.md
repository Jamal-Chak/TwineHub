Changes made on 2025-10-27

- Added `gallery/metadata.json` which contains titles, alt text and categories for gallery images.
- Updated `script.js` to load `gallery/metadata.json` (with a fallback) and corrected gallery paths to `gallery/...`.
- Updated `index.html` to load metadata for the homepage gallery preview so preview images have descriptive alt text and lazy-loading.
- Updated `gallery.html` to load metadata and initialize the gallery from the single metadata source. A fallback is present if the metadata file is missing.
- Added lazy-loading (loading="lazy") for gallery and preview images to improve performance.

How to edit image descriptions

1. Open `gallery/metadata.json`.
2. Edit the `title` and `alt` fields for the image entries.
3. Reload `index.html` or `gallery.html` in the browser to see updates.

Notes

- If you add more images to the `gallery/` folder, update `gallery/metadata.json` with new entries (increment `id` and provide `src` like `gallery/image15.jpg`).
- The site uses the metadata file as the single source of truth for gallery information.

Tools
-----

Two PowerShell tools were added under `tools/`:

- `tools/check-gallery-metadata.ps1` — compares files in the `gallery/` folder with `gallery/metadata.json` and reports:
	- image files with no metadata entry (orphan files)
	- metadata entries that point to missing files

- `tools/rename-images.ps1` — generates SEO-friendly filenames from image titles in `gallery/metadata.json`, does a dry-run if run with `-WhatIf`, and when run without `-WhatIf` renames files and updates `gallery/metadata.json` accordingly.

Usage examples (PowerShell, run from project root):

```powershell
# Check metadata consistency
.\tools\check-gallery-metadata.ps1

# Dry-run rename suggestions
.\tools\rename-images.ps1 -WhatIf

# Perform rename and update metadata.json
.\tools\rename-images.ps1
```

Admin UI
--------

An admin page has been added: `admin.html`. It can load `gallery/metadata.json` (when served via HTTP), let you edit entries inline, add/remove/reorder items, preview the generated JSON, copy it to clipboard, or download an updated `metadata.json` to replace the file in the repository.

Usage notes:

- Open `admin.html` in a browser (recommended via a local static server to avoid file:// fetch restrictions). Example:

	```powershell
	cd path\to\tone4dmedia-website-main
	python -m http.server
	# then open http://localhost:8000/admin.html in your browser
	```

- Edit entries and click "Download JSON" to save your changes to `metadata.json` locally, then copy it into `gallery/metadata.json` in this project.

