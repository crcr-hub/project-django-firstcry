let currentIndex = 0;
  const carousel = document.getElementById('carousel123');
  const items = document.querySelectorAll('.carousel123-item');
  const totalItems = items.length;

  function updateCarousel() {
    const newTransformValue = -currentIndex * 100 + '%';
    carousel.style.transform = 'translateX(' + newTransformValue + ')';
  }

  function nextSlide() {
    if (currentIndex < totalItems - 1) {
      currentIndex++;
    } else {
      currentIndex = 0;
    }
    updateCarousel();
  }

  // Automatic slide change every 3 seconds
  setInterval(nextSlide, 3000);


  document.getElementById('nextBtn').addEventListener('click', () => {
    if (currentIndex < totalItems - 1) {
      currentIndex++;
    } else {
      currentIndex = 0;
    }
    updateCarousel();
  });

  document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
    } else {
      currentIndex = totalItems - 1;
    }
    updateCarousel();
  });