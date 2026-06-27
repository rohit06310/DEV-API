/* ========================================
   API Sense AI — Interactive Script
   ======================================== */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Intersection Observer: Reveal on Scroll ───
  const revealSections = () => {
    const targets = document.querySelectorAll(
      '.quick-section, .features-section, .stats-section'
    );

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');

            // Animate stat bars and counters when stats section appears
            if (entry.target.classList.contains('stats-section')) {
              animateStats();
            }

            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );

    targets.forEach((el) => {
      el.classList.add('reveal');
      observer.observe(el);
    });

    // Stagger children grids
    const grids = document.querySelectorAll(
      '.quick-grid, .features-grid, .stats-grid'
    );
    const gridObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            gridObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -30px 0px' }
    );

    grids.forEach((el) => {
      el.classList.add('reveal-stagger');
      gridObserver.observe(el);
    });
  };

  revealSections();

  // ─── Animate Stats: Counter + Bars ───
  const animateStats = () => {
    // Animate bars
    const bars = document.querySelectorAll('.stat-bar-fill');
    bars.forEach((bar) => {
      requestAnimationFrame(() => {
        bar.classList.add('animated');
      });
    });

    // Animate counter values
    const counters = document.querySelectorAll('.stat-value[data-target]');
    counters.forEach((counter) => {
      const target = parseInt(counter.dataset.target, 10);
      const duration = 1800;
      const startTime = performance.now();

      const easeOutQuart = (t) => 1 - Math.pow(1 - t, 4);

      const updateCounter = (currentTime) => {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easedProgress = easeOutQuart(progress);
        const current = Math.round(easedProgress * target);
        counter.textContent = current.toLocaleString();

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        }
      };

      requestAnimationFrame(updateCounter);
    });
  };

  // ─── Analyze Button: Click Feedback ───
  const analyzeBtn = document.getElementById('analyze-btn');

  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', () => {
      // Add loading state
      analyzeBtn.classList.add('loading');
      const originalHTML = analyzeBtn.innerHTML;

      analyzeBtn.innerHTML = `
        <svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
        </svg>
        Analyzing...
        <span class="btn-shimmer"></span>
      `;

      // Add spinner CSS dynamically
      if (!document.getElementById('spin-style')) {
        const style = document.createElement('style');
        style.id = 'spin-style';
        style.textContent = `
          @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
          .spin { animation: spin 0.8s linear infinite; }
        `;
        document.head.appendChild(style);
      }

      // Simulate processing
      setTimeout(() => {
        analyzeBtn.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          Analysis Complete
        `;
        analyzeBtn.style.background = 'linear-gradient(135deg, #34d399 0%, #22d3ee 100%)';

        setTimeout(() => {
          analyzeBtn.innerHTML = originalHTML;
          analyzeBtn.style.background = '';
          analyzeBtn.classList.remove('loading');
        }, 2000);
      }, 2500);
    });
  }

  // ─── Quick Cards: Populate Input ───
  const apiData = {
    github: {
      url: 'https://docs.github.com/en/rest',
      useCase: 'Automate repository management, pull requests, and CI/CD workflows.'
    },
    stripe: {
      url: 'https://docs.stripe.com/api',
      useCase: 'Process payments, manage subscriptions, and handle invoicing.'
    },
    openai: {
      url: 'https://platform.openai.com/docs/api-reference',
      useCase: 'Integrate AI-powered text generation and embeddings.'
    },
    twilio: {
      url: 'https://www.twilio.com/docs/usage/api',
      useCase: 'Send SMS, make voice calls, and build real-time communications.'
    },
    discord: {
      url: 'https://discord.com/developers/docs/reference',
      useCase: 'Build bots, manage servers, and create interactive Discord integrations.'
    }
  };

  const quickCards = document.querySelectorAll('.quick-card');
  const urlInput = document.getElementById('api-url');
  const useCaseInput = document.getElementById('use-case');

  quickCards.forEach((card) => {
    card.addEventListener('click', () => {
      const api = card.dataset.api;
      const data = apiData[api];

      if (data && urlInput && useCaseInput) {
        // Smooth scroll to input
        document.getElementById('input-section').scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        });

        // Populate with a slight delay for visual effect
        setTimeout(() => {
          urlInput.value = data.url;
          useCaseInput.value = data.useCase;

          // Add brief highlight animation
          urlInput.style.borderColor = 'rgba(167, 139, 250, 0.6)';
          useCaseInput.style.borderColor = 'rgba(167, 139, 250, 0.6)';
          urlInput.style.boxShadow = '0 0 0 3px rgba(167, 139, 250, 0.12)';
          useCaseInput.style.boxShadow = '0 0 0 3px rgba(167, 139, 250, 0.12)';

          setTimeout(() => {
            urlInput.style.borderColor = '';
            useCaseInput.style.borderColor = '';
            urlInput.style.boxShadow = '';
            useCaseInput.style.boxShadow = '';
          }, 1200);
        }, 400);
      }
    });
  });

  // ─── Nav: Shrink on Scroll ───
  const nav = document.getElementById('main-nav');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > 20) {
      nav.style.borderBottomColor = 'rgba(255,255,255,0.08)';
    } else {
      nav.style.borderBottomColor = 'rgba(255,255,255,0.04)';
    }

    lastScroll = currentScroll;
  }, { passive: true });

  // ─── Smooth focus transitions for inputs ───
  const inputs = document.querySelectorAll('.field-input, .field-textarea, .field-select');
  inputs.forEach((input) => {
    input.addEventListener('focus', () => {
      input.closest('.field-group')?.classList.add('focused');
    });
    input.addEventListener('blur', () => {
      input.closest('.field-group')?.classList.remove('focused');
    });
  });

});
