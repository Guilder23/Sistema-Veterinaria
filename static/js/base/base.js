document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const toggleBtn = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebar-overlay');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sidebar.classList.toggle('active');
            if (sidebarOverlay) {
                sidebarOverlay.classList.toggle('active');
            }
        });
    }

    // Close sidebar when clicking outside on mobile
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            if (sidebar) sidebar.classList.remove('active');
            sidebarOverlay.classList.remove('active');
        });
    }

    // Also close sidebar when clicking a link on mobile
    const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                if (sidebar) sidebar.classList.remove('active');
                if (sidebarOverlay) sidebarOverlay.classList.remove('active');
            }
        });
    });

    // Theme Toggle (Dark Mode)
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const body = document.body;
    const themeIcon = themeToggleBtn ? themeToggleBtn.querySelector('i') : null;

    // Check for saved theme
    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        if (themeIcon) {
            themeIcon.classList.replace('fa-moon', 'fa-sun');
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            let theme = document.documentElement.getAttribute('data-theme');
            if (theme === 'dark') {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                if (themeIcon) themeIcon.classList.replace('fa-sun', 'fa-moon');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                if (themeIcon) themeIcon.classList.replace('fa-moon', 'fa-sun');
            }
        });
    }

    // Profile Dropdown Toggle
    const profileDropdown = document.getElementById('profile-dropdown');
    const dropdownMenu = document.getElementById('dropdown-menu');

    if (profileDropdown && dropdownMenu) {
        profileDropdown.addEventListener('click', function(e) {
            // Only toggle if clicking the header part (not inside the menu)
            if (!dropdownMenu.contains(e.target)) {
                e.stopPropagation();
                dropdownMenu.classList.toggle('show');
            }
        });

        document.addEventListener('click', function(e) {
            if (dropdownMenu.classList.contains('show') && !profileDropdown.contains(e.target)) {
                dropdownMenu.classList.remove('show');
            }
        });
    }

    // Auto-close alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
        
        const closeBtn = alert.querySelector('.close-alert');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => alert.remove());
        }
    });
});
