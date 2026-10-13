'use strict';
document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('year').textContent = new Date().getFullYear();
  const toggle = document.getElementById('mobileToggle'), nav = document.getElementById('siteNav');
  function closeNav() { nav.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); toggle.setAttribute('aria-label','Open navigation'); }
  toggle.addEventListener('click', () => {
    const open = !nav.classList.contains('open'); nav.classList.toggle('open',open);
    toggle.setAttribute('aria-expanded',String(open)); toggle.setAttribute('aria-label',open ? 'Close navigation' : 'Open navigation');
  });
  nav.addEventListener('click', e => { if (e.target.closest('a')) closeNav(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { closeNav(); toggle.focus(); } });
  window.matchMedia('(min-width: 769px)').addEventListener('change',closeNav);
  const form = document.getElementById('contactForm');
  if (form) form.addEventListener('submit', e => {
    e.preventDefault();
    const data = new FormData(form);
    const body = `Hello Tone4DMedia,\n\nName: ${data.get('name')}\nEmail: ${data.get('email')}\nService: ${data.get('service')}\n\n${data.get('message')}`;
    const email = e.submitter?.value === 'email';
    const url = email ? `mailto:tone4dmedia@gmail.com?subject=${encodeURIComponent('Website enquiry: '+data.get('service'))}&body=${encodeURIComponent(body)}` : `https://wa.me/27692403008?text=${encodeURIComponent(body)}`;
    document.getElementById('formStatus').textContent = `Opening ${email ? 'your email app' : 'WhatsApp'}. Your enquiry is not sent yet; send it in that app.`;
    if (email) window.location.href = url; else window.open(url,'_blank','noopener,noreferrer');
  });
  const gallery = document.getElementById('gallery'), preview = document.getElementById('galleryPreview');
  if (!gallery && !preview) return;
  const dialog = document.getElementById('viewer'), media = document.getElementById('viewerMedia');
  let visible = [], current = 0, opener;
  function stopMedia() { const video = media.querySelector('video'); if (video) { video.pause(); video.removeAttribute('src'); video.load(); } media.replaceChildren(); }
  function show(index) {
    stopMedia(); current = (index + visible.length) % visible.length;
    const item = visible[current], element = document.createElement(item.type === 'video' ? 'video' : 'img');
    if (item.type === 'video') { element.controls = true; element.playsInline = true; element.preload = 'metadata'; element.poster = item.poster; element.setAttribute('aria-label',item.title); }
    else element.alt = item.alt;
    element.src = item.src; media.append(element);
    document.getElementById('viewerTitle').textContent = item.title;
    document.getElementById('viewerDescription').textContent = item.description;
    document.getElementById('viewerPosition').textContent = `${current + 1} / ${visible.length}`;
  }
  function open(index,button) { opener = button; show(index); dialog.showModal(); document.body.classList.add('viewer-open'); document.getElementById('closeViewer').focus(); }
  document.getElementById('closeViewer').addEventListener('click',() => dialog.close());
  dialog.addEventListener('close',() => { stopMedia(); document.body.classList.remove('viewer-open'); opener?.focus(); });
  dialog.addEventListener('click',e => { if (e.target !== dialog) return; const r = dialog.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close(); });
  document.getElementById('previous').addEventListener('click',() => show(current - 1));
  document.getElementById('next').addEventListener('click',() => show(current + 1));
  dialog.addEventListener('keydown',e => { if (e.target.tagName === 'VIDEO') return; if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1); } if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1); } });
  function render(items) {
    visible = items; const target = gallery || preview; target.replaceChildren();
    items.forEach((item,index) => {
      const card = document.createElement('button'); card.type = 'button'; card.className = 'project-card'; card.setAttribute('aria-label',`View ${item.type === 'video' ? 'video: ' : ''}${item.title}`);
      const img = document.createElement('img'); img.src = item.type === 'video' ? item.poster : item.src; img.alt = item.alt; img.loading = 'lazy'; img.width = 480; img.height = 360;
      const body = document.createElement('span'); body.className = 'card-body';
      const category = document.createElement('span'); category.className = 'project-category'; category.textContent = `${item.category}${item.type === 'video' ? ' · Play video ▶' : ' · View image ↗'}`;
      const title = document.createElement('strong'); title.textContent = item.title;
      const description = document.createElement('span'); description.className = 'project-description'; description.textContent = item.description;
      body.append(category,title,description); card.append(img,body); card.addEventListener('click',() => open(index,card)); target.append(card);
    });
    const status = document.getElementById('galleryStatus'); if (status) status.textContent = `${items.length} projects shown`;
  }
  fetch('assets/metadata.json').then(res => { if (!res.ok) throw new Error('Portfolio unavailable'); return res.json(); }).then(items => {
    if (preview) { render([14,16,17,1,25,27].map(i => items[i]).filter(Boolean)); return; }
    const filters = [...document.querySelectorAll('[data-filter]')];
    function filter(category) { if (!filters.some(btn => btn.dataset.filter === category)) category = 'all'; filters.forEach(btn => btn.setAttribute('aria-pressed',String(btn.dataset.filter === category))); render(category === 'all' ? items : items.filter(item => item.category === category)); }
    filters.forEach(btn => btn.addEventListener('click',() => filter(btn.dataset.filter)));
    filter(new URLSearchParams(window.location.search).get('category') || 'all');
  }).catch(() => { const target = document.getElementById('galleryStatus') || preview; target.textContent = 'The portfolio could not be loaded. Please refresh or contact us to see our work.'; });
});
