// Animate stat numbers when in view
function animateStats() {
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach(stat => {
        if (stat.getAttribute('data-animated')) return;
        const rect = stat.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            stat.setAttribute('data-animated', 'true');
            const target = +stat.getAttribute('data-count');
            let current = 0;
            const duration = 1800; // Smoother and slower
            const frameRate = 60;
            const totalFrames = Math.round(duration / (1000 / frameRate));
            const increment = target / totalFrames;
            const isMoney = stat.parentElement.textContent.includes('Funding');
            function update(frame = 0) {
                current += increment;
                if (current >= target || frame >= totalFrames) {
                    current = target;
                }
                stat.textContent = isMoney
                    ? '$' + Math.floor(current).toLocaleString()
                    : Math.floor(current).toLocaleString() + (target >= 1000 && !isMoney ? '+' : '');
                if (current < target && frame < totalFrames) {
                    requestAnimationFrame(() => update(frame + 1));
                }
            }
            update();
        }
    });
}
window.addEventListener('scroll', animateStats);
window.addEventListener('DOMContentLoaded', animateStats);