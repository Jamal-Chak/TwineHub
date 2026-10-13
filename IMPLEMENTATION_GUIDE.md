# Tone4DMedia Website - Implementation Guide for AI Chat

This guide provides complete specifications for implementing a modern facelift of the Tone4DMedia website.

## 1. Project Overview

**Company:** Tone4DMedia  
**Business:** Design, Printing & Branding Agency  
**Location:** Benoni, South Africa (11 Bunyan)  
**Contact:** 069 240 3008 | WhatsApp: 069 240 3008 | Email: tone4dmedia@gmail.com

**Architecture:** Static HTML/CSS/JavaScript (no build process, no server required)

## 2. Asset Structure

### Current Asset Structure

```
TwineHub/
├── assets/
│   ├── images/          # Optimized website images
│   │   ├── hero.jpg
│   │   ├── background.jpg
│   │   ├── logo.png
│   │   ├── facebook.png
│   │   ├── instagram.png
│   │   └── whatsapp.png

### New Media to Add

Create these folders if they don't exist:
- `assets/images/` - Optimized website images
- `assets/videos/` - Video files
- `assets/posters/` - Video poster images

## 3. Contact Details (Use Consistently)

| Item | Value |
|------|-------|
| Phone | 069 240 3008 |
| Call link | tel:+27692403008 |
| WhatsApp | https://wa.me/27692403008 |
| Email | tone4dmedia@gmail.com |
| Displayed address | 11 Bunyan |

## 4. Design System

### Color Palette

```css
--color-bg: #0a0a0f;
--color-bg-light: #12121a;
--color-bg-card: #1a1a24;
--color-text: #e8e8ed;
--color-text-muted: #9494a8;
--color-primary: #6366f1;
--color-primary-dark: #4f46e5;
--color-secondary: #06b6d4;
--color-accent: #f59e0b;
--color-border: #2a2a3a;
```

### Typography

- **Primary font:** Inter (Google Fonts)
- **Font weights:** 400 (regular), 500 (medium), 600 (semi-bold), 700 (bold), 800 (extra-bold)
- **Headings:** 700 weight, line-height 1.2
- **Body:** 1.6 line-height

### Components

#### Buttons

```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 28px;

## 5. Page Requirements

### Homepage (index.html)

**Sections (in order):**
1. **Hero** - Full-screen with background image (hero.jpg), overlay gradient, badge ("Design. Print. Brand."), title ("We craft brands that leave a mark"), subtitle, and two buttons ("Request a Quote" and "View Our Work")
2. **Services** - Grid of 6 service cards with icons
3. **Process** - 4 steps (Consultation → Design & Planning → Production → Delivery)
4. **Gallery Preview** - Featured projects with photos
5. **Contact** - Contact details card + contact form
6. **Footer** - About, contact details, social links, copyright

**Contact info to include:**
- Phone: 069 240 3008
- WhatsApp: https://wa.me/27692403008
- Email: tone4dmedia@gmail.com
- Address: 11 Bunyan

### About Page (about.html)

**Sections:**
1. **Hero** - Brief intro with background image
2. **About Us** - Two-column layout (text + image)
3. **Values** - 4 value cards
4. **Contact CTA** - Simple CTA section
5. **Footer**

### Services Page (services.html)

**Sections:**
1. **Hero** - Services introduction
2. **Services Grid** - 6 service cards with icons and gallery thumbnails
3. **Process** - 4 steps
4. **Quote Section** - CTA section with "Request a Quote" button

## 6. Portfolio (Gallery) Requirements

### metadata.json Structure

```json
[
  {
    "id": 1,
    "src": "assets/images/hero.jpg",
    "type": "image",
    "title": "Brand Identity Project",
    "category": "branding",
    "description": "Complete brand identity design with logo and visual system",
    "alt": "Brand identity design with logo"
  },
  {
    "id": 2,
    "src": "assets/images/background.jpg",
    "type": "image",
    "title": "Print Production Setup",
    "category": "production",
    "description": "Print production environment with equipment and materials",
    "alt": "Print production equipment"
  },
  {
    "id": 3,
    "src": "assets/videos/2026-05-09-163723937.mp4",
    "type": "video",
    "title": "Video Project",
    "category": "branding",
    "description": "Video project showcase",
    "poster": "assets/posters/hero_poster.jpg"
  }
]
```

### Lightbox Requirements

- Image viewer with larger preview

## 10. Files to Modify

| File | Changes Needed |
|------|----------------|
| style.css | Already redesigned (complete) |
| index.html | Complete redesign |
| about.html | Complete redesign |
| services.html | Complete redesign |
| gallery.html | Complete redesign |
| contact.html | Complete redesign |
| script.js | Add mobile menu, gallery lightbox, form handling |

## 11. Console Commands

**Start local server:**
```bash
cd C:\Users\Tessl\Documents\GitHub\TwineHub
python -m http.server 8080
```

**Open in browser:**
```
http://localhost:8080/
```

**Check for errors:**
```bash
# Check all images load
Select-String 'https://' index.html

# Check for broken links
Select-String 'href="[^"]*\.html[^"]*"' *.html
```

## 12. Success Criteria

- [ ] All pages have consistent modern design
- [ ] Hero sections use real project photos
- [ ] Gallery supports both images and videos

- [ ] All pages have consistent modern design
- [ ] Hero sections use real project photos
- [ ] Gallery supports both images and videos
- [ ] Mobile menu works correctly
- [ ] Contact form submits properly
- [ ] All pages have working navigation
- [ ] All contact details are correct
- [ ] No broken images or links
- [ ] Pages are responsive
- [ ] Performance is good (no excessive downloads)

## 12. Deployment Note

For public deployment, only use the `assets/` folder (optimized copies). The `images/` folder contains source media that should remain private.

### Public Deployment Structure

```
twinehub.com/
├── index.html
├── about.html
├── services.html
├── gallery.html
├── contact.html
├── assets/
│   ├── images/
│   │   ├── hero.jpg
│   │   ├── background.jpg
│   │   ├── logo.png
│   │   └── (social icons)
│   ├── videos/
│   ├── posters/
│   └── metadata.json
└── style.css
└── script.js
```

## 13. Next Steps

1. Provide this guide to chat/AI for implementation
2. The AI will need to:
   - Create the complete redesigned pages
   - Implement the gallery with video support
   - Add mobile menu navigation
   - Complete the lightbox viewer
   - Implement form handling
3. Test locally before deploying

## 14. Quick Reference

**Local Development:**
```bash
cd C:\Users\Tessl\Documents\GitHub\TwineHub
python -m http.server 8080
```

**Website URL:**
```
http://localhost:8080/
```

**Key Contact:**
- Phone: 069 240 3008
- WhatsApp: https://wa.me/27692403008
- Email: tone4dmedia@gmail.com
- Address: 11 Bunyan
- [ ] Mobile menu works correctly
- [ ] Contact form submits properly
- [ ] All pages have working navigation
- [ ] All contact details are correct
- [ ] No broken images or links
- [ ] Pages are responsive
- [ ] Performance is good (no excessive downloads)

## 13. Media Summary

### Videos Available

| Filename | Size |
|----------|------|
| 2026-05-09-163723937.mp4 | 10 MB |
| VID_20250901_162957.mp4 | 44 MB |
| VID_20260424_122709.mp4 | 65 MB |

### Photos Available

| Filename | Type |
|----------|------|
| hero.jpg | Hero background |
| background.jpg | Background image |
| Branding_040120.png | Branding graphics |
| Tshirt printing_040152.png | T-shirt printing graphics |
| Vehicle_040039.png | Vehicle branding graphics |
| IMG_20250801_120648.jpg | Client photo |
| IMG_20251017_154858_edit.jpg | Client photo |
| IMG_20251017_154912_edit.jpg | Client photo |
| IMG_20260318_162144.jpg | Client photo |
| IMG_20260408_124114.jpg | Client photo |
| IMG_20260720_151231.jpg | Client photo |
| IMG_20260723_103538.jpg | Client photo |
| IMG_20260804_124057.jpg | Client photo |
| IMG_20260810_101435.jpg | Client photo |
| IMG_20260910_100500.jpg | Client photo (duplicate) |
- Video player with native controls
- Play/pause functionality
- Escape key to close
- Click outside to close
- Focus management
- Keyboard support (arrow keys for navigation)

## 7. Implementation Order

1. **Create asset folders** (already done):
   - `assets/images/`
   - `assets/videos/`
   - `assets/posters/`

2. **Add images to `assets/images/`:**
   - hero.jpg (hero background)
   - background.jpg (background image)

3. **Add videos to `assets/videos/`:**
   - 2026-05-09-163723937.mp4
   - VID_20250901_162957.mp4
   - VID_20260424_122709.mp4

4. **Add posters to `assets/posters/`:**
   - hero_poster.jpg (video preview)

5. **Update `style.css`** (already done with new design)

6. **Update `index.html`** with new layout

7. **Update `about.html`** with new layout

8. **Update `services.html`** with new layout

9. **Update `gallery.html`** with new gallery system

10. **Update `contact.html`** with new layout

11. **Update `script.js`** for:
    - Mobile menu
    - Gallery lightbox
    - Form handling
    - Scroll animations

## 8. Technical Requirements

### Responsive Design

- Mobile menu toggle
- Nav stays at top on scroll
- Cards stack on mobile
- Contact form inputs full width on mobile

### Accessibility

- Proper contrast ratios
- Alt text for all images
- Keyboard navigation support
- Focus indicators
- Reduced motion support

### Performance

- Lazy load images
- Video uses native controls
- No autoplay with sound
- Poster images for videos
- Optimized file sizes

## 9. Notes

- **Do not invent** testimonials, statistics, or team members
- **Use existing** brand identity and colors
- **Preserve** original functionality
- **Check media** for duplicates (IMG_20260910_100500.jpg is duplicate)
- **Do not overwrite** original files in images/ folder
- **Keep originals** in images/ folder (not public)
- **Use optimized copies** in assets/ folder
5. **Footer**

### Gallery Page (gallery.html)

**Features:**
- Filter buttons for categories
- Grid of gallery items (images and videos)
- Lightbox viewer
- Each item: title, category, description, media preview

**Category filters:** All, Branding, Signage, Printing, Vehicle, Banners

### Contact Page (contact.html)

**Sections:**
1. **Hero** - Contact introduction
2. **Contact Grid** - Left: contact info (phone, WhatsApp, email, address) | Right: contact form
3. **Map** - Simple map embed
4. **Footer**
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-primary { background: #6366f1; color: white; }
.btn-secondary { background: transparent; color: #e8e8ed; border: 2px solid #2a2a3a; }
```

#### Cards

```css
.service-card {
  background: #1a1a24;
  border: 1px solid #2a2a3a;
  border-radius: 12px;
  padding: 32px;
  transition: all 0.3s ease;
}
.service-card:hover {
  border-color: #6366f1;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}
```
│   ├── videos/          # Video files
│   │   ├── 2026-05-09-163723937.mp4
│   │   ├── VID_20250901_162957.mp4
│   │   └── VID_20260424_122709.mp4
│   ├── posters/         # Video poster images
│   │   └── hero_poster.jpg
│   ├── metadata.json    # Gallery metadata
│   └── script.js        # Shared JavaScript
├── gallery/
│   ├── metadata.json    # Original gallery metadata (needs updating)
│   └── image1-14.jpg    # Original gallery images
├── style.css            # Stylesheet (already redesigned)
├── script.js            # Shared JavaScript
├── index.html           # Homepage (needs redesign)
├── about.html           # About page (needs redesign)
├── services.html        # Services page (needs redesign)
├── gallery.html         # Gallery page (needs redesign)
├── contact.html         # Contact page (needs redesign)
└── images/              # Source media folder
```

### New Media to Add

Create these folders if they don't exist:
- `assets/images/` - Optimized website images
- `assets/videos/` - Video files
- `assets/posters/` - Video poster images