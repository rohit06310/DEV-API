/* ═══════════════════════════════════════════════════════
   API Sense AI — Workflow Page Script
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ─── Scroll Reveal: Step Sections ───
  const stepSections = document.querySelectorAll('.step-section, .final-section');

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: '0px 0px -60px 0px' }
  );

  stepSections.forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.05}s`;
    revealObserver.observe(el);
  });

  // Also reveal the final section
  const finalSection = document.querySelector('.final-section');
  if (finalSection) {
    finalSection.style.opacity = '0';
    finalSection.style.transform = 'translateY(28px)';
    finalSection.style.transition = 'opacity 0.8s cubic-bezier(0.16,1,0.3,1), transform 0.8s cubic-bezier(0.16,1,0.3,1)';

    const finalObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            finalObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    finalObserver.observe(finalSection);
  }


  // ─── Code Editor: Tab Switching ───
  const editorTabs = document.querySelectorAll('.editor-tab');
  const codePanels = document.querySelectorAll('.code-panel');
  const editorFile = document.querySelector('.editor-file');

  const fileNames = {
    python: 'github_client.py',
    javascript: 'github_client.js',
    java: 'GitHubClient.java',
  };

  editorTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const lang = tab.dataset.lang;

      // Toggle active tab
      editorTabs.forEach((t) => t.classList.remove('active'));
      tab.classList.add('active');

      // Toggle code panel
      codePanels.forEach((p) => p.classList.remove('active'));
      const targetPanel = document.getElementById(`code-${lang}`);
      if (targetPanel) targetPanel.classList.add('active');

      // Update filename
      if (editorFile) editorFile.textContent = fileNames[lang] || 'client';
    });
  });


  // ─── Copy Code Button ───
  const copyBtn = document.getElementById('btn-copy');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      const activePanel = document.querySelector('.code-panel.active');
      if (!activePanel) return;

      const codeText = activePanel.textContent;
      navigator.clipboard.writeText(codeText).then(() => {
        const originalHTML = copyBtn.innerHTML;
        copyBtn.innerHTML = `
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
          Copied!
        `;
        copyBtn.style.borderColor = 'rgba(52,211,153,0.4)';
        copyBtn.style.color = '#34d399';

        setTimeout(() => {
          copyBtn.innerHTML = originalHTML;
          copyBtn.style.borderColor = '';
          copyBtn.style.color = '';
        }, 2000);
      });
    });
  }


  // ─── Regenerate Button Animation ───
  const regenBtn = document.getElementById('btn-regenerate');
  if (regenBtn) {
    regenBtn.addEventListener('click', () => {
      const icon = regenBtn.querySelector('svg');
      if (icon) {
        icon.style.transition = 'transform 0.5s cubic-bezier(0.16,1,0.3,1)';
        icon.style.transform = 'rotate(360deg)';
        setTimeout(() => { icon.style.transform = ''; }, 600);
      }
    });
  }


  // ─── Chat Suggestion Click ───
  const chatInput = document.querySelector('.chat-input');
  const chatSuggestions = document.querySelectorAll('.chat-suggestion');

  chatSuggestions.forEach((btn) => {
    btn.addEventListener('click', () => {
      if (chatInput) {
        chatInput.value = btn.textContent;
        chatInput.focus();

        // Brief highlight
        btn.style.borderColor = 'rgba(167,139,250,0.4)';
        btn.style.color = '#a78bfa';
        btn.style.background = 'rgba(167,139,250,0.08)';
        setTimeout(() => {
          btn.style.borderColor = '';
          btn.style.color = '';
          btn.style.background = '';
        }, 800);
      }
    });
  });


  // ─── Scraper Bars: Animate on Scroll ───
  const scraperSection = document.getElementById('step-2');
  if (scraperSection) {
    const barObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const bars = entry.target.querySelectorAll('.scraper-bar');
            bars.forEach((bar, i) => {
              setTimeout(() => {
                bar.style.width = bar.style.getPropertyValue('--w');
              }, i * 200);
            });
            barObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    barObserver.observe(scraperSection);

    // Initially hide bars
    const initBars = scraperSection.querySelectorAll('.scraper-bar');
    initBars.forEach((b) => { b.style.width = '0'; });
  }


  // ─── Confidence Fill: Animate on Scroll ───
  const usecaseSection = document.getElementById('step-4');
  if (usecaseSection) {
    const confObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const fill = entry.target.querySelector('.confidence-fill');
            if (fill) {
              setTimeout(() => {
                fill.style.width = fill.style.getPropertyValue('--w');
              }, 300);
            }
            confObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.3 }
    );
    confObserver.observe(usecaseSection);
  }


  // ─── Nav Scroll Effect ───
  const nav = document.getElementById('nav');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 30) {
      nav.style.borderBottomColor = 'rgba(255,255,255,0.08)';
    } else {
      nav.style.borderBottomColor = 'rgba(255,255,255,0.04)';
    }
  }, { passive: true });


  // ─── Download Button ───
  const dlBtn = document.getElementById('btn-download');
  if (dlBtn) {
    dlBtn.addEventListener('click', () => {
      const activePanel = document.querySelector('.code-panel.active');
      if (!activePanel) return;

      const codeText = activePanel.textContent;
      const activeLang = document.querySelector('.editor-tab.active')?.dataset.lang || 'python';
      const ext = { python: 'py', javascript: 'js', java: 'java' }[activeLang] || 'txt';
      const fileName = `github_client.${ext}`;

      const blob = new Blob([codeText], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    });
  }

});
