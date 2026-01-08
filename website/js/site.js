document.addEventListener('DOMContentLoaded', function () {
    // Open modal when clicking product images
    function openModal(title, imgSrc) {
        const backdrop = document.querySelector('.modal-backdrop');
        if (!backdrop) return;
        const modalTitle = backdrop.querySelector('.modal-title');
        const modalImg = backdrop.querySelector('.modal-body img');
        const orderBtn = backdrop.querySelector('.modal-order');
        modalTitle.textContent = title;
        modalImg.src = imgSrc;
        orderBtn.href = 'https://wa.me/918329875106?text=I%20want%20to%20order%20' + encodeURIComponent(title);
        backdrop.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        const backdrop = document.querySelector('.modal-backdrop');
        if (!backdrop) return;
        backdrop.style.display = 'none';
        document.body.style.overflow = '';
    }

    document.body.addEventListener('click', function (e) {
        const img = e.target.closest('.card img');
        if (img) {
            const card = img.closest('.card');
            const titleEl = card.querySelector('h4');
            const title = titleEl ? titleEl.textContent.trim() : 'Product';
            const src = img.dataset.large || img.src;
            openModal(title, src);
        }
    });

    // Close buttons and backdrop click
    document.querySelectorAll('.modal-close').forEach(b => b.addEventListener('click', closeModal));
    document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
        backdrop.addEventListener('click', function (e) {
            if (e.target === backdrop) closeModal();
        });
    });

    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', function (e) {
            e.preventDefault();
            const id = this.getAttribute('href').slice(1);
            const el = document.getElementById(id);
            if (el) el.scrollIntoView({ behavior: 'smooth' });
        });
    });
});
