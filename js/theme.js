
// APPLY SAVED THEME BEFORE THE PAGE IS PAINTED (LOADED IN <head> WITHOUT defer)
if (localStorage.getItem('theme') === 'dark') {
    document.documentElement.classList.add('theme-dark');
}


// THEME SWITCH
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');

    if (!themeToggle) return;

    themeToggle.checked = document.documentElement.classList.contains('theme-dark');

    themeToggle.addEventListener('change', () => {
        if (themeToggle.checked) {
            document.documentElement.classList.add('theme-dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('theme-dark');
            localStorage.setItem('theme', 'light');
        }
    });
});
