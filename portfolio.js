'use strict';

const filters = document.querySelector('.filters');
const cards = [...document.querySelectorAll('.work-card')];
const status = document.querySelector('#gallery-status');
if (filters) {
  filters.hidden = false;
  filters.addEventListener('click', (event) => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    const category = button.dataset.filter;
    filters.querySelectorAll('button').forEach((item) => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    cards.forEach((card) => {
      card.hidden = category !== 'all' && card.dataset.category !== category;
    });
    status.textContent = `${cards.filter((card) => !card.hidden).length} projects shown: ${button.textContent}.`;
  });
}

const dialog = document.querySelector('#work-dialog');
const media = document.querySelector('#dialog-media');
const title = document.querySelector('#dialog-title');
const label = document.querySelector('#dialog-label');
const source = document.querySelector('#dialog-source');
const note = document.querySelector('#dialog-note');
let opener;

function closeProject() {
  dialog.close();
}

if (dialog && typeof dialog.showModal === 'function') {
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[data-video], a[data-graphic]');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0) return;
    event.preventDefault();
    opener = link;
    title.textContent = link.dataset.title;
    label.textContent = link.dataset.label;
    media.replaceChildren();
    const isVideo = Boolean(link.dataset.video);
    if (isVideo) {
      const frame = document.createElement('iframe');
      frame.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(link.dataset.video)}?autoplay=1&rel=0`;
      frame.title = link.dataset.title;
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      media.append(frame);
      source.href = link.href;
      source.textContent = 'Watch on YouTube ↗';
      note.textContent = 'Selected film · Original upload and credits on YouTube.';
    } else {
      const image = document.createElement('img');
      image.src = link.dataset.graphic;
      image.alt = link.querySelector('img')?.alt || `${link.dataset.title} graphic`;
      media.append(image);
      source.href = link.dataset.sourceLabel ? link.href : 'https://sites.google.com/view/erniedemaluanjr/projects/graphic-designs';
      source.textContent = link.dataset.sourceLabel || 'View creative archive ↗';
      note.textContent = link.dataset.note || 'Selected graphic from my public creative archive.';
    }
    dialog.classList.toggle('graphic-dialog', !isVideo);
    document.body.classList.add('dialog-open');
    dialog.showModal();
    dialog.querySelector('.dialog-close').focus({ preventScroll: true });
  });
  dialog.querySelector('.dialog-close').addEventListener('click', closeProject);
  dialog.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const first = dialog.querySelector('.dialog-close');
    const last = source;
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) closeProject();
  });
  dialog.addEventListener('close', () => {
    media.replaceChildren();
    document.body.classList.remove('dialog-open');
    opener?.focus({ preventScroll: true });
  });
}
