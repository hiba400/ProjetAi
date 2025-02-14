const canvas = document.getElementById('liveCanvas');
const ctx = canvas.getContext('2d');

canvas.addEventListener('click', (e) => {
  const rect = canvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  drawCircle(x, y);
});

function drawCircle(x, y) {
  const radius = Math.random() * 50 + 10;
  const r = Math.floor(Math.random() * 256);
  const g = Math.floor(Math.random() * 256);
  const b = Math.floor(Math.random() * 256);
  ctx.fillStyle = `rgba(${r},${g},${b},0.8)`;
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function saveCanvas() {
  const link = document.createElement('a');
  link.download = `art_${Date.now()}.png`;
  link.href = canvas.toDataURL();
  link.click();
}
