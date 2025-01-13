// Sidebar functionality
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    function toggleSidebar() {
        sidebar.classList.toggle('closed');
    }

    function toggleDropdown(e) {
        e.preventDefault();
        const dropdownMenu = this.nextElementSibling;
        dropdownMenu.classList.toggle('show');
    }

    toggleBtn.addEventListener('click', toggleSidebar);
    closeBtn.addEventListener('click', toggleSidebar);
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', toggleDropdown);
    });

    // Close sidebar on mobile when clicking outside
    document.addEventListener('click', (e) => {
        const isClickInside = sidebar.contains(e.target) || toggleBtn.contains(e.target);
        if (!isClickInside && window.innerWidth <= 768 && !sidebar.classList.contains('closed')) {
            sidebar.classList.add('closed');
        }
    });
});