document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const toggleBtn = document.getElementById('toggle-sidebar');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            if (window.innerWidth > 768) {
                if (sidebar.style.left === '-250px') {
                    sidebar.style.left = '0';
                    mainContent.style.marginLeft = '250px';
                } else {
                    sidebar.style.left = '-250px';
                    mainContent.style.marginLeft = '0';
                }
            } else {
                sidebar.classList.toggle('show-mobile');
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
