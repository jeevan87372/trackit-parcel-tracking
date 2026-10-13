/**
 * ============================================================================
 * TrackIt — Parcel Tracking System (DevOps Laboratory Project)
 * Module 2: Client-Side Interactive Logic & Live Query Support
 * ============================================================================
 * 
 * Provides clean, interactive UI behavior:
 * 1. Mobile navigation menu toggle
 * 2. Quick sample fill & auto-submit to trigger live SQLite queries
 * 3. Error suggestion pills to quickly test valid tracking numbers
 * 4. Clipboard copy for tracking codes
 * 5. Smooth scrolling to search results
 * 6. Active section highlighting in navigation bar
 */

document.addEventListener('DOMContentLoaded', () => {
    // ------------------------------------------------------------------------
    // 1. Mobile Navigation Menu Toggle
    // ------------------------------------------------------------------------
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('mobile-open');
        });

        // Close menu when a navigation link is clicked
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('mobile-open');
            });
        });
    }

    // ------------------------------------------------------------------------
    // 2. Tracking Form & Quick-Fill Actions
    // ------------------------------------------------------------------------
    const trackingForm = document.getElementById('trackingForm');
    const trackingInput = document.getElementById('trackingIdInput');

    // Quick-Fill Sample Buttons (Under Search Bar)
    const quickButtons = document.querySelectorAll('.quick-btn');
    quickButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const sampleId = btn.getAttribute('data-id');
            if (sampleId && trackingInput && trackingForm) {
                trackingInput.value = sampleId;
                trackingForm.submit();
            }
        });
    });

    // Suggestion Pills inside the "Not Found" Error Box
    const sugPills = document.querySelectorAll('.sug-pill');
    sugPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const sampleId = pill.getAttribute('data-id');
            if (sampleId && trackingInput && trackingForm) {
                trackingInput.value = sampleId;
                trackingForm.submit();
            }
        });
    });

    // Smoothly scroll to search results if present on page load
    const searchResultCard = document.querySelector('.search-result-card, .search-error-card');
    if (searchResultCard) {
        setTimeout(() => {
            searchResultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 200);
    }

    // ------------------------------------------------------------------------
    // 3. Copy Tracking Number to Clipboard
    // ------------------------------------------------------------------------
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const textToCopy = btn.getAttribute('data-copy');
            if (textToCopy) {
                try {
                    await navigator.clipboard.writeText(textToCopy);
                    const originalTitle = btn.getAttribute('title');
                    btn.setAttribute('title', 'Copied!');
                    btn.style.color = '#10b981';

                    setTimeout(() => {
                        btn.setAttribute('title', originalTitle || 'Copy tracking number');
                        btn.style.color = '';
                    }, 2000);
                } catch (err) {
                    console.warn('Clipboard copy failed:', err);
                }
            }
        });
    });

    // ------------------------------------------------------------------------
    // 4. Active Navigation Link Highlighting on Scroll
    // ------------------------------------------------------------------------
    const sections = document.querySelectorAll('section[id]');
    window.addEventListener('scroll', () => {
        const scrollY = window.pageYOffset;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 120;
            const sectionId = current.getAttribute('id');
            const correspondingLink = document.querySelector(`.nav-menu a[href*="${sectionId}"]`);

            if (correspondingLink) {
                if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                    document.querySelectorAll('.nav-menu .nav-link').forEach(link => link.classList.remove('active'));
                    correspondingLink.classList.add('active');
                }
            }
        });
    });

    // ------------------------------------------------------------------------
    // 5. Module 3: Admin Tracking ID Generator Helper
    // ------------------------------------------------------------------------
    const btnGenId = document.getElementById('btnGenId');
    const trackingIdField = document.getElementById('trackingIdField');

    if (btnGenId && trackingIdField) {
        btnGenId.addEventListener('click', () => {
            // Generate TRK- followed by 6 random digits
            const randomCode = Math.floor(100000 + Math.random() * 900000);
            trackingIdField.value = `TRK-${randomCode}`;
            trackingIdField.focus();
        });
    }
});
