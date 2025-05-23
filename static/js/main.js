document.addEventListener('DOMContentLoaded', function() {
    // Animate elements when they enter the viewport
    const animateElements = function() {
        const elements = document.querySelectorAll('.animated-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                element.classList.add('is-visible');
            }
        });
    };
    
    // Run the animation check on load and scroll
    animateElements();
    window.addEventListener('scroll', animateElements);
    
    // Enable Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Swipe functionality for the discover page
    const swipeContainer = document.getElementById('swipe-container');
    
    if (swipeContainer) {
        const profileCards = document.querySelectorAll('.profile-card');
        let currentCardIndex = 0;
        
        const showCurrentCard = () => {
            profileCards.forEach((card, index) => {
                if (index === currentCardIndex) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        };
        
        // Initialize to show the first card
        showCurrentCard();
        
        // Like action
        document.getElementById('like-button')?.addEventListener('click', function() {
            const currentCard = profileCards[currentCardIndex];
            const profileId = currentCard.dataset.profileId;
            
            // Animate the card
            currentCard.classList.add('swipe-right');
            
            // Make API call to record the like
            fetch(`/accounts/swipe/${profileId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Like recorded:', data);
                
                // Check if it's a match
                if (data.match) {
                    showMatchAlert(data.matched_profile);
                }
                
                // Move to next card after animation completes
                setTimeout(() => {
                    currentCard.classList.remove('swipe-right');
                    currentCardIndex = (currentCardIndex + 1) % profileCards.length;
                    showCurrentCard();
                }, 300);
            })
            .catch(error => {
                console.error('Error recording like:', error);
            });
        });
        
        // Dislike action
        document.getElementById('dislike-button')?.addEventListener('click', function() {
            const currentCard = profileCards[currentCardIndex];
            const profileId = currentCard.dataset.profileId;
            
            // Animate the card
            currentCard.classList.add('swipe-left');
            
            // Make API call to record the dislike
            fetch(`/accounts/swipe/${profileId}/dislike/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Dislike recorded:', data);
                
                // Move to next card after animation completes
                setTimeout(() => {
                    currentCard.classList.remove('swipe-left');
                    currentCardIndex = (currentCardIndex + 1) % profileCards.length;
                    showCurrentCard();
                }, 300);
            })
            .catch(error => {
                console.error('Error recording dislike:', error);
            });
        });
    }
    
    // Show match alert
    function showMatchAlert(matchedProfile) {
        const modalHtml = `
            <div class="modal fade" id="matchModal" tabindex="-1" aria-labelledby="matchModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title" id="matchModalLabel">It's a Match! 🎉</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center">
                            <p class="lead">You and ${matchedProfile.name} have matched!</p>
                            <p>Now you can start a conversation.</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Keep Swiping</button>
                            <a href="/accounts/matches/" class="btn btn-primary">Go to Matches</a>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        
        const matchModal = new bootstrap.Modal(document.getElementById('matchModal'));
        matchModal.show();
        
        document.getElementById('matchModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
    
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
    
    // User type toggle on registration page
    const founderBtn = document.getElementById('founderBtn');
    const investorBtn = document.getElementById('investorBtn');
    
    if (founderBtn && investorBtn) {
        const userTypeInput = document.getElementById('id_user_type');
        const founderQuote = document.getElementById('founderQuote');
        const investorQuote = document.getElementById('investorQuote');
        
        founderBtn.addEventListener('click', function() {
            founderBtn.classList.add('active');
            investorBtn.classList.remove('active');
            userTypeInput.value = 'founder';
            if (founderQuote && investorQuote) {
                founderQuote.style.display = 'block';
                investorQuote.style.display = 'none';
            }
        });
        
        investorBtn.addEventListener('click', function() {
            investorBtn.classList.add('active');
            founderBtn.classList.remove('active');
            userTypeInput.value = 'investor';
            if (founderQuote && investorQuote) {
                founderQuote.style.display = 'none';
                investorQuote.style.display = 'block';
            }
        });
    }
});