document.querySelectorAll('.product-card, .hero-card').forEach(card => {
  card.addEventListener('mousemove', e => {
    if (window.matchMedia('(max-width: 760px)').matches) return;
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width - .5;
    const y = (e.clientY - r.top) / r.height - .5;
    card.style.transform = `rotateY(${x * 18}deg) rotateX(${-y * 14}deg) translateY(-5px)`;
  });
  card.addEventListener('mouseleave', () => card.style.removeProperty('transform'));
});
