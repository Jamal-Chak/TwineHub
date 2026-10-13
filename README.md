# Tone4DMedia

Five static pages for the Benoni design, printing and branding business.

Build: python build_site.py

Preview: python -m http.server 8080 --bind 127.0.0.1 --directory dist

Open http://127.0.0.1:8080/. HTTP is required for portfolio metadata loading.

Deploy **only dist/**. vercel.json configures Vercel as a static site (framework Other), runs python3 build_site.py, and serves dist/. netlify.toml selects the same output for Netlify. An existing host serving the repository root must be reconfigured to serve dist/. Git ignore rules do not restrict HTTP access.

For Vercel, set the project's Root Directory to the repository root containing vercel.json and build_site.py. Remove any obsolete Python application preset, main.py entrypoint, or Python-specific install-command override from the project settings. The repository configuration overrides the framework, build command and output directory. No package installation is needed: build_site.py uses only Python's standard library and copies the prepared assets. It does not run build_media.py. Deploy a revision containing this configuration; remote deployment success must be checked in Vercel after redeployment.

The public build allowlists the five pages, CSS, JavaScript, authoritative metadata and referenced public assets. Original images/, historical gallery/, admin utilities, Python scripts and repository documents are excluded. Public logo and background copies are preserved.

assets/metadata.json is the authoritative portfolio inventory, used by the website and both local inventory utilities. gallery/metadata.json is the historical inventory retained for provenance. See MEDIA_REPORT.md, media-update-mapping.json and media-audit.json for source-to-public mappings, categorisation and measured sizes. qa/media-before.json and qa/original-media-before.json preserve the inventory and hashes recorded before the latest import.

The business address is 11 Bunyan Street Benoni. Directions use an exact-address Google Maps search, with no unverified map coordinates.

There is no contact delivery backend configured. Enquiry actions prepare WhatsApp or email messages; visitors send the message in their chosen app.

build_media.py requires Pillow and imageio-ffmpeg to regenerate supplied copies. The deployment build uses only the Python standard library and prepared assets. Run python verify_site.py while the local server is running for HTTP, privacy and media checks. Browser checks are separate.
