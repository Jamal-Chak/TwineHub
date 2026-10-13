# Media reconciliation and implementation results

## Completed website

All five pages now share the dark indigo/cyan design, sticky navigation, active page indicators, mobile menu, service links, contact details and supplied social links. Home includes six services, four process steps, portfolio previews and enquiry preparation. About includes the mission and four values. Services includes thumbnails and category links. Gallery includes all five category filters and a native modal image/video viewer with previous/next, Escape, outside click, focus return and native video controls. Closing or changing media pauses and unloads the video. Contact includes hours, enquiry preparation, map and directions.

No contact service is configured. WhatsApp and email actions prepare messages and explicitly say they have not yet been sent. All displayed contact details use 069 240 3008, 11 Bunyan and tone4dmedia@gmail.com.

## Inventory

`assets/metadata.json` is authoritative: **30 entries (27 images and 3 videos)**. The homepage, gallery and local admin/image-map utilities all use it. `gallery/metadata.json` is a preserved historical inventory whose original descriptions were often inaccurate. No consumer uses it. Supplied filenames were also sometimes misleading; public descriptions reflect the visually inspected content rather than those filenames.

The reported “12 optimized images” did not describe the checkout: before this implementation `assets/images/` contained 20 files, comprising 14 supplied optimized copies and six byte-identical brand/decorative/icon copies. The six copies were not optimized portfolio photos. The public portfolio now includes 19 project photographs and eight design/concept/promotional images, clearly titled as such, rather than presenting logos/backgrounds as client work.

All 14 newly supplied images are included: 11 photographs and three Tone4DMedia promotional graphics. Both IMG_20260910 photographs are retained: their hashes and visually different compositions do not substantiate the guide's duplicate claim.

13 of the 14 historical gallery images are retained as optimized public copies. `gallery/image7.jpg` is excluded from the public output because it is watermarked VectorStock safety-sign artwork, not evidence of a completed client project. Its original is preserved. The original stationery/logo/identity artwork is retained with neutral concept/design descriptions rather than unsupported client claims.

Decorative `images/hero.jpg` (abstract light trails), original social PNG/SVG icons and their copied assets are not portfolio entries or deployed assets. Text social links preserve the exact supplied Facebook and Instagram destinations. The WhatsApp PNG was identical to the Instagram PNG, so it is not used. `assets/images/logo.png` and `assets/images/background.jpg` are preserved in the deployment as intended public brand assets; the hero uses the supplied branded tow-truck photograph.

## Optimization and videos

All 27 portfolio image outputs were regenerated using orientation correction, a maximum 1600×1600 bounding box, progressive JPEG quality 72 and EXIF stripping. Every output is smaller than its source. Total source bytes: 49,682,848; total output bytes: 4,383,627 (91.2% reduction). `media-audit.json` lists every source/output mapping, dimensions, bytes and EXIF-field count.

The three prepared H.264/AAC videos already existed at implementation start. Full decoding verified each output; MP4 box parsing verified that `moov` precedes `mdat` for progressive startup. Combined size: 120,060,116 source bytes → 22,314,928 output bytes (81.4% reduction).

| Original video | Public video | Corresponding poster |
| --- | --- | --- |
| images/2026-05-09-163723937.mp4 | assets/videos/studio-tour.mp4 | assets/posters/poster-studio-tour.jpg |
| images/VID_20250901_162957.mp4 | assets/videos/project-install.mp4 | assets/posters/poster-project-install.jpg |
| images/VID_20260424_122709.mp4 | assets/videos/branding-showcase.mp4 | assets/posters/poster-branding-showcase.jpg |

All three posters were present, contrary to the reported one-poster inventory. Each was verified by regenerating the source's one-second frame with the original extraction settings and comparing decoded pixels: mean difference 0.0 for all three. No missing poster references remain. Videos are loaded only in the viewer with native controls, playsinline, preload=metadata and no autoplay.

## Public output and checks

No previous hosting configuration was present. `build_site.py` creates an allowlisted `dist/`: five HTML pages, CSS, JavaScript, metadata, and 35 intended public media files (27 images, three videos, three posters, logo and background). `netlify.toml` selects that directory. Originals remain untouched in `images/` and `gallery/`. Neither an ignore file nor the word “private” secures a repository-root HTTP server; only serve/deploy the generated output.

Performed: local HTTP serving of `dist/`; successful responses for all five pages, navigation targets and metadata/media references; active-page/contact-link and duplicate-ID checks; image decoding; full video decoding; faststart and poster correspondence; JavaScript syntax check; and HTTP 404 checks for original media, historical metadata, admin utilities, build scripts, guide and Git config. All passed. See `verify_site.py` for repeatable HTTP/media checks.

Unavailable: browser inspection. The browser tool returned no available browsers after the local preview attempt. Mobile/tablet/desktop rendering, interactive filters and navigation, modal keyboard behavior, real browser playback, console errors, map rendering and external WhatsApp/email app handoffs have **not** been marked passed. Responsive rules and interactions are implemented, but those checks remain outstanding.

Remaining limitations: browser QA and verification of an existing live host's publish directory. Nothing was published or any remote host changed. No delivery backend is configured; labelled app-based enquiries work by design.

## Files changed

Five page HTML files; `style.css`; `script.js`; `admin.html`; `images-map.html`; `README.md`; `build_media.py` orientation handling; authoritative `assets/metadata.json`; 27 optimized portfolio JPEGs. Added `build_site.py`, `verify_site.py`, `netlify.toml`, `.gitignore`, this report and `media-audit.json`. Existing original media, videos and matched posters are preserved. `dist/` is generated and ignored.


## Image mapping

| Source | Public output | Source bytes | Output bytes |
| --- | --- | ---: | ---: |
| gallery\image1.jpg | assets\images\image1.jpg | 67734 | 60332 |
| gallery\image2.jpg | assets\images\image2.jpg | 154786 | 152450 |
| gallery\image3.jpg | assets\images\image3.jpg | 69999 | 61766 |
| gallery\image4.jpg | assets\images\image4.jpg | 167748 | 164421 |
| gallery\image5.jpg | assets\images\image5.jpg | 138318 | 135745 |
| gallery\image6.jpg | assets\images\image6.jpg | 120056 | 105993 |
| gallery\image8.jpg | assets\images\image8.jpg | 117612 | 115704 |
| gallery\image9.jpg | assets\images\image9.jpg | 15290 | 13222 |
| gallery\image10.jpg | assets\images\image10.jpg | 153903 | 151756 |
| gallery\image11.jpg | assets\images\image11.jpg | 84031 | 74781 |
| gallery\image12.jpg | assets\images\image12.jpg | 31760 | 30766 |
| gallery\image13.jpg | assets\images\image13.jpg | 101614 | 99311 |
| gallery\image14.jpg | assets\images\image14.jpg | 206734 | 204131 |
| images\IMG_20250801_120648.jpg.jpeg | assets\images\tshirt-orlando-pirates-front.jpg | 3508013 | 168378 |
| images\IMG_20251017_154858_edit_9745907859040.jpg.jpeg | assets\images\tee-proud-buccaneer-back.jpg | 1405428 | 157854 |
| images\IMG_20251017_154912_edit_9763115020179.jpg.jpeg | assets\images\brand-wall-showroom.jpg | 1871730 | 109698 |
| images\IMG_20260318_162144.jpg.jpeg | assets\images\wall-banner-quantum.jpg | 5036174 | 222177 |
| images\IMG_20260408_124114.jpg.jpeg | assets\images\branded-gazebo-event.jpg | 4499209 | 156720 |
| images\IMG_20260720_151231.jpg.jpeg | assets\images\pullup-hollywood-signage.jpg | 3265471 | 204195 |
| images\IMG_20260723_103538.jpg.jpeg | assets\images\branded-gazebo-fnb.jpg | 3289019 | 198273 |
| images\IMG_20260804_124057.jpg.jpeg | assets\images\brand-wall-studio.jpg | 6020489 | 332735 |
| images\IMG_20260810_101435.jpg.jpeg | assets\images\xframe-fighter-banner.jpg | 2975086 | 203171 |
| images\IMG_20260910_100500.jpg.jpeg | assets\images\signage-wall-interior.jpg | 5088055 | 326890 |
| images\IMG_20260910_100521.jpg.jpeg | assets\images\signage-installation.jpg | 5236692 | 300211 |
| images\Branding_040120.png | assets\images\branding-mockup-flyer.jpg | 2195130 | 216773 |
| images\Vehicle_040039.png | assets\images\vehicle-wrap-mockup.jpg | 2031034 | 246898 |
| images\Tshirt printing_040152.png | assets\images\apparel-tshirt-mockup.jpg | 1831733 | 169276 |
