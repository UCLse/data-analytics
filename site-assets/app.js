const progressKey = 'heat-cascade-workshop-progress-v1';
let completed = new Set();
try { const stored = JSON.parse(localStorage.getItem(progressKey) || '[]'); if (Array.isArray(stored)) completed = new Set(stored.filter(value => typeof value === 'string')); } catch {}
const validStems = [...document.querySelectorAll('[data-completed]')].map(element => element.dataset.completed);
completed = new Set([...completed].filter(stem => validStems.includes(stem)));
function updateProgress() {
  document.querySelectorAll('[data-completed]').forEach(element => element.classList.toggle('done', completed.has(element.dataset.completed)));
  document.querySelectorAll('[data-card-state]').forEach(element => element.textContent = completed.has(element.dataset.cardState) ? 'Completed' : 'Open workshop');
  document.querySelectorAll('[data-mark]').forEach(button => { const done = completed.has(button.dataset.mark); button.textContent = done ? 'Completed ✓' : 'Mark complete'; button.setAttribute('aria-pressed', String(done)); });
  const text = document.getElementById('progress-text'); if (text) text.textContent = `${completed.size} / 14`;
  const bar = document.getElementById('course-progress'); if (bar) bar.value = completed.size;
  try { localStorage.setItem(progressKey, JSON.stringify([...completed])); } catch {}
}
updateProgress();
document.querySelectorAll('[data-mark]').forEach(button => button.addEventListener('click', () => { const stem = button.dataset.mark; completed.has(stem) ? completed.delete(stem) : completed.add(stem); updateProgress(); }));
document.getElementById('reset-progress')?.addEventListener('click', () => { completed.clear(); updateProgress(); });
const search = document.getElementById('lesson-search');
search?.addEventListener('input', () => {
  const query = search.value.trim().toLowerCase(); let count = 0;
  document.querySelectorAll('.lesson-card').forEach(card => { const matches = card.dataset.search.toLowerCase().includes(query); card.hidden = !matches; if (matches) count++; });
  document.querySelectorAll('.course-section').forEach(section => section.hidden = ![...section.querySelectorAll('.lesson-card')].some(card => !card.hidden));
  document.getElementById('search-empty').hidden = count > 0;
});
const menu = document.querySelector('.menu-button');
menu?.addEventListener('click', () => { const expanded = menu.getAttribute('aria-expanded') === 'true'; menu.setAttribute('aria-expanded', String(!expanded)); document.body.classList.toggle('menu-open', !expanded); });
document.addEventListener('keydown', event => { if (event.key === 'Escape') { document.body.classList.remove('menu-open'); menu?.setAttribute('aria-expanded','false'); } });
document.querySelectorAll('.prose pre').forEach(pre => {
  const button = document.createElement('button'); button.type = 'button'; button.className = 'copy-button'; button.textContent = 'Copy code'; button.setAttribute('aria-label','Copy this code block');
  button.addEventListener('click', async () => { try { await navigator.clipboard.writeText(pre.querySelector('code').textContent); button.textContent = 'Copied'; } catch { button.textContent = 'Select and copy'; } setTimeout(() => button.textContent = 'Copy code', 1800); });
  pre.append(button);
});
