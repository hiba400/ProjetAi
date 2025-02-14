document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.regenerate-btn').forEach(btn => {
      btn.addEventListener('click', async function() {
        const imgContainer = this.closest('.art-card').querySelector('img');
        imgContainer.style.opacity = '0.5';
        const newArt = await fetch(this.dataset.endpoint)
          .then(response => response.blob())
          .then(blob => URL.createObjectURL(blob));
        imgContainer.src = newArt;
        imgContainer.style.opacity = '1';
      });
    });
  });
  