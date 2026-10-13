# Tone4DMedia

Five static pages for the Benoni design, printing and branding business.

Build: python build_site.py

Preview: python -m http.server 8080 --bind 127.0.0.1 --directory dist

Open http://127.0.0.1:8080/. HTTP is required for portfolio metadata loading.

Deploy **only dist/**. netlify.toml configures that output for Netlify. No previous hosting configuration or live deployment was found in this checkout. An existing host serving the repository root must be reconfigured to serve dist/. Git ignore rules do not restrict HTTP access.

The public build allowlists the five pages, CSS, JavaScript, authoritative metadata and referenced public assets. Original images/, historical gallery/, admin utilities, Python scripts and repository documents are excluded. Public logo and background copies are preserved.

assets/metadata.json is the authoritative portfolio inventory, used by the website and both local inventory utilities. gallery/metadata.json is the historical inventory retained for provenance. See MEDIA_REPORT.md and media-audit.json for reconciliation and measured sizes.

There is no contact delivery backend configured. Enquiry actions prepare WhatsApp or email messages; visitors send the message in their chosen app.

build_media.py requires Pillow and imageio-ffmpeg to regenerate supplied copies. The deployment build uses only the Python standard library and prepared assets. Run python verify_site.py while the local server is running for HTTP, privacy and media checks. Browser checks are separate.
