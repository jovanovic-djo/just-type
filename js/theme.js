
// THEME SWITCH
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');

    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('theme-dark');
        if (themeToggle) themeToggle.checked = true;
    }

    if (themeToggle) {
        themeToggle.addEventListener('change', () => {
            if (themeToggle.checked) {
                document.documentElement.classList.add('theme-dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.classList.remove('theme-dark');
                localStorage.setItem('theme', 'light');
            }
        });
    }
});
