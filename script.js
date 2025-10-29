/* ====== Basic utilities ====== */
document.addEventListener('DOMContentLoaded', () => {
  // fill years
  const yearElems = ['year', 'yearAbout', 'yearServices', 'yearGallery', 'yearContact'];
  yearElems.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.textContent = new Date().getFullYear();
  });

  // mobile nav toggle
  const toggle = document.getElementById('mobileToggle');
  const nav = document.querySelectorAll('.nav');
  if (toggle) {
    toggle.addEventListener('click', () => {
      nav.forEach(n => {
        n.style.display = (n.style.display === 'flex') ? 'none' : 'flex';
      });
    });
  }

  // Build gallery using metadata when available (keeps descriptions accurate)
  const galleryContainer = document.getElementById('gallery');
  const galleryPreview = document.getElementById('galleryPreview');

  function createImgElement(src, alt) {
    const img = document.createElement('img');
    img.src = src;
    img.alt = alt || '';
    img.loading = 'lazy';
    img.style.cursor = 'pointer';
    img.addEventListener('error', () => {
      img.style.display = 'none';
    });
    img.addEventListener('click', () => window.open(src, '_blank'));
    return img;
  }

  // Try to load gallery metadata (single source of truth for titles/alt/category)
  fetch('gallery/metadata.json')
    .then(res => {
      if (!res.ok) throw new Error('metadata not found');
      return res.json();
    })
    .then(items => {
      if (galleryContainer) {
        items.forEach(item => {
          const img = createImgElement(item.src, item.alt || item.title || `Project ${item.id}`);
          galleryContainer.appendChild(img);
        });
      }

      if (galleryPreview) {
        items.slice(0, 6).forEach(item => {
          const img = createImgElement(item.src, item.alt || item.title || `Project ${item.id}`);
          galleryPreview.appendChild(img);
        });
      }
    })
    .catch(() => {
      // Fallback: use gallery/imageN.jpg and a small known set (14)
      const TOTAL_IMAGES = 14;
      if (galleryContainer) {
        for (let i = 1; i <= TOTAL_IMAGES; i++) {
          const src = `gallery/image${i}.jpg`;
          const img = createImgElement(src, `Project ${i}`);
          galleryContainer.appendChild(img);
        }
      }

      if (galleryPreview) {
        for (let i = 1; i <= Math.min(6, TOTAL_IMAGES); i++) {
          const src = `gallery/image${i}.jpg`;
          const img = createImgElement(src, `Project ${i}`);
          galleryPreview.appendChild(img);
        }
      }
    });

  // contact form: POST to backend (update URL if needed)
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const statusEl = document.getElementById('formStatus');
      statusEl.textContent = 'Sending...';
      const data = Object.fromEntries(new FormData(contactForm).entries());
      const ENDPOINT = 'http://localhost:5050/api/contact';

      try {
        const res = await fetch(ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });

        if (res.ok) {
          statusEl.style.color = 'lightgreen';
          statusEl.textContent = 'Message sent — we will contact you shortly.';
          contactForm.reset();
        } else {
          throw new Error('Failed to send');
        }
      } catch (err) {
        statusEl.style.color = 'orange';
        statusEl.textContent = 'Could not send via API — opening email client as fallback...';
        const mail = `mailto:tone4dmedia@gmail.com?subject=Website%20Contact%20from%20${encodeURIComponent(data.name || 'Visitor')}&body=${encodeURIComponent(JSON.stringify(data, null, 2))}`;
        setTimeout(() => window.location.href = mail, 800);
      }
    });
  }
});
