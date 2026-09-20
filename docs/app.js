/* ==========================================================================
   ÁNGEL SARRIÓN - PERSONAL SPACE
   Interactive Client Script: Theme, Localization, Actions & Print
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
        themeToggleBtn.innerHTML = '⚡ Synthwave Theme';
        themeToggleBtn.setAttribute('aria-label', 'Switch to Synthwave Dark theme');
      }
    } else {
      document.documentElement.removeAttribute('data-theme');
      if (themeToggleBtn) {
        themeToggleBtn.innerHTML = '📄 LaTeX Paper Theme';
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

  // --- Mobile Menu Toggle ---
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const navMenu = document.getElementById('nav-menu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('open');
      mobileToggle.setAttribute('aria-expanded', isOpen);
    });

    // Close mobile menu when clicking nav link
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

  // --- Print / Generate PDF Button ---
  const printBtns = document.querySelectorAll('.action-print-cv');
  printBtns.forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      window.print();
    });
  });

  // --- Initialize ---
  document.addEventListener('DOMContentLoaded', function () {
    initTheme();
    updateActiveNav();
  });
})();
