/* ═══════════════════════════════════════════════════
   ANIRACH MINGKHWAN — Portfolio Scripts
   ═══════════════════════════════════════════════════ */

(function () {
  'use strict';

  // Respect the OS-level motion preference: the reduced-motion CSS media
  // block can shrink transition/animation durations, but it cannot stop a
  // scrollY-driven inline transform (the hero parallax below), so that one
  // needs a JS-side guard too.
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ── Nav scroll effect ──
  const nav = document.getElementById('nav');
  let lastScroll = 0;

  function onScroll() {
    const y = window.scrollY;
    nav.classList.toggle('scrolled', y > 60);
    lastScroll = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ── Mobile menu ──
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');

  if (hamburger) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      hamburger.classList.toggle('active');
    });
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        hamburger.classList.remove('active');
      });
    });
  }

  // ── Scroll reveal ──
  // Opt IN to the hidden state. Everything below only runs with JS available,
  // so the page is never left blank by a script that failed to load.
  document.documentElement.classList.add('js-reveal');
  const reveals = document.querySelectorAll('[data-reveal]');

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          // Stagger siblings
          const siblings = Array.from(entry.target.parentElement.querySelectorAll('[data-reveal]'));
          const idx = siblings.indexOf(entry.target);
          setTimeout(() => {
            entry.target.classList.add('revealed');
          }, reduceMotion ? 0 : idx * 120);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });

    reveals.forEach(el => observer.observe(el));
  } else {
    // Fallback: show all
    reveals.forEach(el => el.classList.add('revealed'));
  }

  // ── Smooth anchor scroll ──
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href.length < 2) return;               // bare "#" — let the browser be
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // ── Parallax-lite for hero bg text ──
  const bgText = document.querySelector('.hero__bg-text');
  if (bgText && !reduceMotion) {
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      if (y < window.innerHeight) {
        bgText.style.transform = `translate(-50%, calc(-55% + ${y * 0.15}px))`;
      }
    }, { passive: true });
  }

})();
