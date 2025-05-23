document.addEventListener('DOMContentLoaded', function() {
    // Animation for dashboard elements
    const animateElements = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach((element, index) => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                // Add staggered animation delay
                setTimeout(() => {
                    element.classList.add('animate', 'fade-in', 'is-visible');
                }, index * 100);
            }
        });
    };
    
    // Run animation check on load and scroll
    animateElements();
    window.addEventListener('scroll', animateElements);
    
    // Chart initialization for founder dashboard
    const initFounderCharts = function() {
        // Visitor engagement chart
        const engagementCtx = document.getElementById('founderEngagementChart');
        if (engagementCtx) {
            new Chart(engagementCtx, {
                type: 'line',
                data: {
                    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    datasets: [{
                        label: 'Profile Views',
                        data: [12, 19, 15, 17, 22, 26, 30],
                        borderColor: '#3B0D8B',
                        backgroundColor: 'rgba(59, 13, 139, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }, {
                        label: 'Matches',
                        data: [3, 2, 4, 5, 7, 6, 9],
                        borderColor: '#F72585',
                        backgroundColor: 'rgba(247, 37, 133, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Weekly Engagement'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Investor interest by industry
        const interestCtx = document.getElementById('founderInterestChart');
        if (interestCtx) {
            new Chart(interestCtx, {
                type: 'polarArea',
                data: {
                    labels: ['Tech', 'Healthcare', 'Finance', 'Education', 'E-commerce'],
                    datasets: [{
                        data: [30, 18, 12, 9, 15],
                        backgroundColor: [
                            'rgba(59, 13, 139, 0.7)',
                            'rgba(127, 0, 255, 0.7)',
                            'rgba(247, 37, 133, 0.7)',
                            'rgba(255, 107, 0, 0.7)',
                            'rgba(58, 12, 163, 0.7)'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Investor Interest by Industry'
                        }
                    }
                }
            });
        }
    };

    // Chart initialization for investor dashboard
    const initInvestorCharts = function() {
        // Startup discovery chart
        const discoveryCtx = document.getElementById('investorDiscoveryChart');
        if (discoveryCtx) {
            new Chart(discoveryCtx, {
                type: 'bar',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    datasets: [{
                        label: 'Startups Discovered',
                        data: [42, 53, 67, 78],
                        backgroundColor: 'rgba(127, 0, 255, 0.7)',
                        borderColor: 'rgba(127, 0, 255, 1)',
                        borderWidth: 1
                    }, {
                        label: 'Matches Made',
                        data: [12, 17, 22, 25],
                        backgroundColor: 'rgba(255, 107, 0, 0.7)',
                        borderColor: 'rgba(255, 107, 0, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: true,
                            text: 'Monthly Discovery'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // Startup stage distribution
        const stageCtx = document.getElementById('investorStageChart');
        if (stageCtx) {
            new Chart(stageCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Seed', 'Series A', 'Series B', 'Growth', 'Pre-IPO'],
                    datasets: [{
                        data: [45, 25, 15, 10, 5],
                        backgroundColor: [
                            'rgba(59, 13, 139, 0.7)',
                            'rgba(127, 0, 255, 0.7)',
                            'rgba(247, 37, 133, 0.7)',
                            'rgba(255, 107, 0, 0.7)',
                            'rgba(58, 12, 163, 0.7)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        title: {
                            display: true,
                            text: 'Startup Stage Distribution'
                        }
                    }
                }
            });
        }
    };

    // Initialize appropriate charts based on dashboard type
    if (document.querySelector('.dashboard-founder')) {
        initFounderCharts();
    }

    if (document.querySelector('.dashboard-investor')) {
        initInvestorCharts();
    }

    // Animate numbers in dashboard counters
    const animateCounters = function() {
        const counters = document.querySelectorAll('.counter-value');
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 1500; // ms
            const step = target / (duration / 16); // assuming 60fps
            
            let current = 0;
            const counterInterval = setInterval(() => {
                current += step;
                if (current >= target) {
                    counter.textContent = target;
                    clearInterval(counterInterval);
                } else {
                    counter.textContent = Math.floor(current);
                }
            }, 16);
        });
    };

    // Run counter animations when elements are in view
    const observeCounters = function() {
        const counters = document.querySelectorAll('.counter-value');
        if (!counters.length) return;
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.disconnect();
                }
            });
        });
        
        observer.observe(document.querySelector('.counter-value'));
    };

    observeCounters();

    // Swipe functionality for matching cards
    const initSwipeCards = function() {
        const cards = document.querySelectorAll('.swipe-card');
        if (!cards.length) return;
        
        cards.forEach(card => {
            let startX, startY, moveX, moveY;
            let threshold = 100; // minimum distance to be considered a swipe
            
            card.addEventListener('touchstart', (e) => {
                startX = e.touches[0].clientX;
                startY = e.touches[0].clientY;
            });
            
            card.addEventListener('touchmove', (e) => {
                moveX = e.touches[0].clientX;
                moveY = e.touches[0].clientY;
                
                const diffX = moveX - startX;
                const diffY = moveY - startY;
                
                // Only apply transform if primarily horizontal movement
                if (Math.abs(diffX) > Math.abs(diffY)) {
                    e.preventDefault();
                    card.style.transform = `translateX(${diffX}px) rotate(${diffX * 0.05}deg)`;
                    
                    // Change opacity of like/dislike indicators
                    if (diffX > 0) {
                        document.querySelector('.swipe-like-indicator').style.opacity = Math.min(diffX / threshold, 1);
                        document.querySelector('.swipe-dislike-indicator').style.opacity = 0;
                    } else if (diffX < 0) {
                        document.querySelector('.swipe-dislike-indicator').style.opacity = Math.min(Math.abs(diffX) / threshold, 1);
                        document.querySelector('.swipe-like-indicator').style.opacity = 0;
                    }
                }
            });
            
            card.addEventListener('touchend', () => {
                const diffX = moveX - startX;
                
                if (Math.abs(diffX) >= threshold) {
                    // Complete the swipe animation
                    const swipeDirection = diffX > 0 ? 'right' : 'left';
                    card.classList.add(`swipe-${swipeDirection}`);
                    
                    // Record the swipe action
                    const profileId = card.getAttribute('data-profile-id');
                    const action = swipeDirection === 'right' ? 'like' : 'dislike';
                    
                    // Make API call to record action
                    fetch(`/accounts/swipe/${profileId}/${action}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCsrfToken(),
                            'Content-Type': 'application/json'
                        }
                    }).then(response => response.json())
                    .then(data => {
                        console.log(`Swipe ${action} recorded`);
                        
                        // If it's a match, show match alert
                        if (data.match) {
                            showMatchAlert(data.matched_profile);
                        }
                    })
                    .catch(error => {
                        console.error('Error recording swipe:', error);
                    });
                    
                    // Remove card after animation
                    setTimeout(() => {
                        card.remove();
                        
                        // Show next card if available
                        const nextCard = document.querySelector('.swipe-card.d-none');
                        if (nextCard) {
                            nextCard.classList.remove('d-none');
                        } else {
                            // No more cards
                            document.querySelector('.swipe-empty-state').classList.remove('d-none');
                        }
                    }, 300);
                } else {
                    // Reset card position
                    card.style.transform = '';
                    document.querySelector('.swipe-like-indicator').style.opacity = 0;
                    document.querySelector('.swipe-dislike-indicator').style.opacity = 0;
                }
            });
        });
    };

    initSwipeCards();

    // Get CSRF token from cookies
    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length, cookie.length);
            }
        }
        return null;
    }

    // Create and animate decorative elements
    const createDecorativeElements = function() {
        const decorContainer = document.querySelector('.decorative-container');
        if (!decorContainer) return;
        
        // Create random decorative circles
        for (let i = 0; i < 5; i++) {
            const circle = document.createElement('div');
            circle.classList.add('decorative-circle');
            
            // Random position
            circle.style.top = `${Math.random() * 100}%`;
            circle.style.left = `${Math.random() * 100}%`;
            
            // Random size
            const size = 50 + Math.random() * 150;
            circle.style.width = `${size}px`;
            circle.style.height = `${size}px`;
            
            // Random opacity
            circle.style.opacity = 0.05 + Math.random() * 0.1;
            
            decorContainer.appendChild(circle);
        }
        
        // Create random decorative dots
        for (let i = 0; i < 15; i++) {
            const dot = document.createElement('div');
            dot.classList.add('decorative-dots');
            
            // Random position
            dot.style.top = `${Math.random() * 100}%`;
            dot.style.left = `${Math.random() * 100}%`;
            
            // Random size
            const size = 2 + Math.random() * 8;
            dot.style.width = `${size}px`;
            dot.style.height = `${size}px`;
            
            // Random animation delay
            dot.style.animationDelay = `${Math.random() * 5}s`;
            
            decorContainer.appendChild(dot);
        }
        
        // Create blob shapes
        for (let i = 0; i < 3; i++) {
            const blob = document.createElement('div');
            blob.classList.add('decorative-blob');
            
            // Random position
            blob.style.top = `${Math.random() * 100}%`;
            blob.style.left = `${Math.random() * 100}%`;
            
            // Random size
            const size = 100 + Math.random() * 200;
            blob.style.width = `${size}px`;
            blob.style.height = `${size}px`;
            
            // Random animation delay
            blob.style.animationDelay = `${Math.random() * 5}s`;
            
            decorContainer.appendChild(blob);
        }
    };

    createDecorativeElements();
});