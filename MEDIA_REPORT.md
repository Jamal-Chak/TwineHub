# Final media and address update

The website now uses **11 Bunyan Street Benoni** in all five pages, contact details, footers, page descriptions and enquiry messages. Phone, call, WhatsApp, email and supplied social links are preserved. Directions use an exact-address Google Maps search; no coordinates are assigned. Municipal records identify the street address, but the business-specific map pin could not be independently verified.

## Inventory and categorisation

| Portfolio | Before | After |
| --- | ---: | ---: |
| Images | 27 | 52 |
| Videos | 3 | 3 |
| Total entries | 30 | 55 |

All 30 previous IDs, media references and public image/video/poster bytes are preserved. All 25 newly supplied files were added; no exact duplicate was found against existing or previously excluded sources. Different angles remain separate entries. All 66 original files in images/ and gallery/ are unchanged.

| New owner folder | Images added | Public category |
| --- | ---: | --- |
| Banners | 7 | Banners |
| Shop branding and Signage | 6 | Shop branding & signage |
| TShirts | 2 | T-shirt printing |
| Vehicle branding | 10 | Vehicle branding |

The separate **Shop Branding** folder is empty and preserved. It is not merged with the populated shop branding/signage folder or used to infer projects. Older Branding & design and Signage categories remain available. The All filter contains all 55 entries.

| Current category | Images | Videos |
| --- | ---: | ---: |
| Branding & design | 5 | 0 |
| Signage | 9 | 3 |
| Shop branding & signage | 6 | 0 |
| T-shirt printing | 8 | 0 |
| Vehicle branding | 14 | 0 |
| Banners | 10 | 0 |

Visual inspection corrected titles, descriptions, alt text and misplaced entries. The former shopfront-display entry ID9 is two roll-up banners (now Banners); ID22 is an exterior Eye Doctor sign (now Signage). Artwork, illustrations and mockups are labelled explicitly. Legacy filenames are kept to preserve published references. Client/business names are used only where visible in supplied artwork.

## Images and presentation

Only new public copies were generated: orientation corrected, original ratios preserved, at most 1600px per edge, progressive JPEG quality72, RGB, EXIF stripped. The 25 sources total 45,140,567 bytes; public copies total 4,703,854 bytes (89.58% smaller). Filenames include source-folder prefixes to avoid collisions. Existing media was not reoptimized.

Home previews use stable IDs45,55,35,39,25,29: T-shirt, vehicle, banner, shopfront, promotional design and existing video. Home/services thumbnails and links use metadata IDs25,39,45,55,35,24. The About photo uses ID39. Captions identify the pictured work. Gallery, service and About images use contain-style presentation so the full printed design remains visible. Image dimensions are explicit and below-fold media is lazy-loaded.

The existing viewer retains complete images, native video controls, playsinline, metadata preload, original posters, no autoplay, and pause/unload on close or navigation. Descriptive category labels include the new combined shop category.

## Mapping and preservation

[media-update-mapping.json](media-update-mapping.json) records every new source ? public asset ? category ? title ? description, source/public hashes and bytes, existing corrections, before/after counts and uncertainties. [media-audit.json](media-audit.json) retains all prior mappings and adds the new optimization measurements. [qa/media-before.json](qa/media-before.json) captures previous metadata/public hashes; [qa/original-media-before.json](qa/original-media-before.json) captures all original source hashes.

Historically excluded gallery/image7.jpg remains preserved and excluded because it is watermarked stock safety-sign artwork. Decorative original hero/social assets remain outside the portfolio; supplied social links are unchanged. Intended public logo/background copies remain present. No new source file was excluded or left unprocessed.

## Build and verification

The unchanged build_site.py produced exactly68 allowlisted files: five HTML pages, CSS, JavaScript, authoritative metadata, 52 portfolio images, three videos, three posters, logo and background. Original source folders, QA snapshots, mapping/report files and development utilities are outside dist. vercel.json is unchanged: framework null, python3 build_site.py, output dist; no Python app entrypoint was introduced.

Passed: isolated standard-library build; JavaScript syntax and diff whitespace checks; verify_site.py against localhost; exact output allowlist and source/output hashes; complete original and prior public-media preservation; all25 new mappings; optimized dimensions/orientation/aspect ratios/EXIF; all5 page contacts/social/address/directions; local references, metadata-consumer paths, matching gallery filter/category links, service thumbnail categories/captions/dimensions and stable homepage IDs; image/poster decoding; HTTP404 for private original/dev paths; all3 videos decoded fully, faststart verified, corresponding posters compared with mean pixel error0.0.

**Unavailable:** browser tool inventory returned no browsers/apps. Mobile/tablet/desktop rendering, real click filtering, full-image viewer interaction, keyboard/focus, native browser playback, console errors, external enquiry handoff and external map result were not tested or marked passed. Static structure, code review and HTTP/media checks passed; they do not substitute for these browser checks.

## Specific uncertainties

- Banners/IMG_20250709_115440.jpg shows a day-care display attached to a railing; flexible vs rigid construction is not established. It stays in the owner?s Banners category with neutral wording.
- Shop Branding has no supplied images; no entries are inferred.
- Exact Tone4DMedia map pin is unverified. The search query is 11 Bunyan Street Benoni. An [Ekurhuleni valuation record](https://ekurhuleni.gov.za/wp-content/uploads/2021/11/BENONI_FULL_TITLE_BOOK-5.pdf) supports the street address but does not establish this business?s pin.

## Files changed

Five HTML pages; script.js; style.css; assets/metadata.json; 25 new assets/images JPEGs; media-audit.json; media-update-mapping.json; verify_site.py; README.md; .gitignore; this report; two before-inventory JSON snapshots. Existing original media, video files/posters, historical exclusions, build_site.py and vercel.json are unchanged.

## New source mapping

| Source file | Public asset | Category | Title | Description |
| --- | --- | --- | --- | --- |
| images/Banners/IMG_20250510_095659.jpg | assets/images/banners-img-20250510-095659.jpg | banners | Apostolic Covenant roll-up banners | Two green and white Apostolic Covenant roll-up banners displayed indoors. |
| images/Banners/IMG_20250709_115440.jpg | assets/images/banners-img-20250709-115440.jpg | banners | Day-care promotional display | An All Stars Day Care promotional display with colourful illustrations attached to a metal railing. |
| images/Banners/IMG_20251223_194243.jpg | assets/images/banners-img-20251223-194243.jpg | banners | Go Ye roll-up banner | A purple and white Go Ye roll-up banner displayed against a brick wall. |
| images/Banners/IMG_20260114_103248.jpg | assets/images/banners-img-20260114-103248.jpg | banners | Community development roll-up banner | A white and green community development roll-up banner displayed outside. |
| images/Banners/IMG_20260320_130252.jpg | assets/images/banners-img-20260320-130252.jpg | banners | Dr Mashudu roll-up banner | A purple Dr Mashudu roll-up banner with medical-service information and a portrait. |
| images/Banners/IMG_20260521_205638.jpg | assets/images/banners-img-20260521-205638.jpg | banners | Go Ye portrait display | A freestanding Go Ye display with two portraits and a dark patterned background. |
| images/Banners/IMG_20260707_234004.jpg | assets/images/banners-img-20260707-234004.jpg | banners | Legal services roll-up banner | A white, navy and gold roll-up banner listing legal services. |
| images/Shop branding and Signage/IMG_20260703_121650.jpg | assets/images/shop-branding-and-signage-img-20260703-121650.jpg | shop-branding-signage | Surgery sign installation detail | A close-up of large blue surgery lettering being positioned above the street. |
| images/Shop branding and Signage/IMG_20260703_135206.jpg | assets/images/shop-branding-and-signage-img-20260703-135206.jpg | shop-branding-signage | Surgery storefront signage | Surgery and doctor lettering above a shopfront with printed window graphics. |
| images/Shop branding and Signage/IMG_20260910_100440.jpg | assets/images/shop-branding-and-signage-img-20260910-100440.jpg | shop-branding-signage | Medical exterior signs | Eye Doctor and physiotherapy signs mounted on the exterior of a brick building. |
| images/Shop branding and Signage/IMG_20260911_131413.jpg | assets/images/shop-branding-and-signage-img-20260911-131413.jpg | shop-branding-signage | Hair and beauty shopfront | Hair and beauty signage and portrait graphics across a shopfront and windows. |
| images/Shop branding and Signage/IMG_20260917_092131.jpg | assets/images/shop-branding-and-signage-img-20260917-092131.jpg | shop-branding-signage | Entrance address lettering | Black number and street-name lettering above a garage entrance. |
| images/Shop branding and Signage/IMG_20260918_122220.jpg | assets/images/shop-branding-and-signage-img-20260918-122220.jpg | shop-branding-signage | Auto-repair frontage signs | Auto-repair signage on a brick workshop frontage and metal gate. |
| images/TShirts/c8148203ef13a05cde28b35b7fb1ce8d_0.jpeg | assets/images/tshirts-c8148203ef13a05cde28b35b7fb1ce8d-0.jpg | printing | Printed slogan T-shirts | A selection of olive, black, tan and red T-shirts with printed text and emblems. |
| images/TShirts/IMG_20260912_173514.jpg | assets/images/tshirts-img-20260912-173514.jpg | printing | Primeview branded shirts | Two black shirts with large and small Primeview logo designs. |
| images/Vehicle branding/IMG_20250920_160015.jpg | assets/images/vehicle-branding-img-20250920-160015.jpg | vehicle | Apostolic Covenant car branding | Green and white Apostolic Covenant lettering and an emblem on a silver car. |
| images/Vehicle branding/IMG_20260227_193737.jpg | assets/images/vehicle-branding-img-20260227-193737.jpg | vehicle | Pro-Tech pickup rear graphics | The rear of a white Pro-Tech pickup with blue graphics and business lettering. |
| images/Vehicle branding/IMG_20260227_193750.jpg | assets/images/vehicle-branding-img-20260227-193750.jpg | vehicle | Pro-Tech pickup side graphics | A rear-side view of a white Pro-Tech pickup with blue graphics and business lettering. |
| images/Vehicle branding/IMG_20260227_193805.jpg | assets/images/vehicle-branding-img-20260227-193805.jpg | vehicle | Pro-Tech pickup front-side view | A front-side view of a white Pro-Tech pickup with business lettering on the doors. |
| images/Vehicle branding/IMG_20260606_121807.jpg | assets/images/vehicle-branding-img-20260606-121807.jpg | vehicle | Jozi Towing truck side branding | Red, black and white Jozi Towing graphics along the side of a tow truck. |
| images/Vehicle branding/IMG_20260607_152419.jpg | assets/images/vehicle-branding-img-20260607-152419.jpg | vehicle | SKT Towing truck front graphics | A front view of a purple truck with SKT Towing lettering above the windscreen. |
| images/Vehicle branding/IMG_20260607_152444.jpg | assets/images/vehicle-branding-img-20260607-152444.jpg | vehicle | SKT Towing cab side graphics | A side view of a purple truck cab with SKT Towing lettering and illustrated graphics. |
| images/Vehicle branding/IMG_20260708_193418.jpg | assets/images/vehicle-branding-img-20260708-193418.jpg | vehicle | Thandindlela coach side lettering | A side view of a white coach with blue Thandindlela Coaches lettering and star graphics. |
| images/Vehicle branding/IMG_20260709_153849.jpg | assets/images/vehicle-branding-img-20260709-153849.jpg | vehicle | Coach branding in progress | A front view of a coach with a worker above the windscreen and blue coach lettering. |
| images/Vehicle branding/IMG_20260710_151159.jpg | assets/images/vehicle-branding-img-20260710-151159.jpg | vehicle | SKT Towing pickup side graphics | A side view of a blue pickup with white SKT Towing and Recovery lettering. |
