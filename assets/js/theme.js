const toggle = document.querySelector('.theme-toggle');
const themes = ['system', 'light', 'dark'];
function updateThemeButton() {
  const current = document.documentElement.dataset.theme || 'system';
  const next = themes[(themes.indexOf(current) + 1) % themes.length];
  toggle.textContent = `Theme: ${current[0].toUpperCase()}${current.slice(1)}`;
  toggle.setAttribute('aria-label', `Color theme: ${current}. Change to ${next}.`);
}
if (toggle) {
  toggle.hidden = false;
  updateThemeButton();
  toggle.addEventListener('click', () => {
    const current = document.documentElement.dataset.theme || 'system';
    const next = themes[(themes.indexOf(current) + 1) % themes.length];
    if (next === 'system') delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = next;
    try {
      if (next === 'system') localStorage.removeItem('theme');
      else localStorage.setItem('theme', next);
    } catch (_) { /* The selection still applies to this page. */ }
    updateThemeButton();
  });
}
