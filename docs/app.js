/* ==========================================================================
   ÁNGEL SARRIÓN — PERSONAL SPACE
   Client Script: Live Madrid Clock, Theme & Language Management, Print
   ========================================================================== */

(function () {
  'use strict';

  // --- Theme Management ---
  const THEME_KEY = 'as_synth_theme';
  const themeToggleBtn = document.getElementById('theme-toggle');

  function initTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY) || 'synthwave';
    setTheme(savedTheme);
  }

  function setTheme(theme) {
    if (theme === 'paper') {
      document.documentElement.setAttribute('data-theme', 'paper');
      if (themeToggleBtn) {
        themeToggleBtn.innerHTML = '⚡ Synthwave';
        themeToggleBtn.setAttribute('aria-label', 'Switch to Synthwave Dark theme');
      }
    } else {
      document.documentElement.removeAttribute('data-theme');
      if (themeToggleBtn) {
        themeToggleBtn.innerHTML = '📄 LaTeX Paper';
        themeToggleBtn.setAttribute('aria-label', 'Switch to LaTeX Paper theme');
      }
    }
    localStorage.setItem(THEME_KEY, theme);
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme') === 'paper' ? 'paper' : 'synthwave';
      setTheme(current === 'paper' ? 'synthwave' : 'paper');
    });
  }

  // --- Language Switcher Navigation (Works on file://, localhost, and GitHub Pages) ---
  function initLanguageSwitcher() {
    document.querySelectorAll('.lang-btn, .lang-toggle-btn').forEach(btn => {
      btn.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (!href || href === '#' || this.classList.contains('active')) {
          e.preventDefault();
          return;
        }
        e.preventDefault();
        const isTargetEs = href.includes('es');
        localStorage.setItem('as_lang_pref', isTargetEs ? 'es' : 'en');
        window.location.href = href;
      });
    });
  }

  // --- Mobile Menu Toggle ---
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });

    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
      });
    });
  }

  // --- Active Nav Link on Scroll ---
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link[href^="#"]');

  function updateActiveNav() {
    const scrollY = window.pageYOffset + 120;
    sections.forEach(section => {
      const sectionHeight = section.offsetHeight;
      const sectionTop = section.offsetTop;
      const sectionId = section.getAttribute('id');

      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${sectionId}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveNav, { passive: true });

  // --- Print Trigger ---
  document.querySelectorAll('.action-print-cv').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      window.print();
    });
  });

  // --- Live Dynamic Clock in Spain (Europe/Madrid) ---
  function updateLiveClock() {
    const timeEl = document.getElementById('live-spain-time');
    if (!timeEl) return;
    try {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('en-GB', {
        timeZone: 'Europe/Madrid',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      });
      timeEl.textContent = timeStr;
    } catch (e) {
      const now = new Date();
      timeEl.textContent = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
    }
  }

  // --- Initialize ---
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    initLanguageSwitcher();
    updateActiveNav();
    updateLiveClock();
    setInterval(updateLiveClock, 10000);
  });
})();
