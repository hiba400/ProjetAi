document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
      document.getElementById('originalImage').src = event.target.result;
      document.getElementById('originalImage').style.display = 'block';
    }
    reader.readAsDataURL(file);
  });
  
  document.getElementById('imageForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData();
    const fileInput = document.getElementById('imageInput');
    // Utiliser la clé "image" pour correspondre à ce qui est attendu par le backend
    formData.append('image', fileInput.files[0]);
    const response = await fetch('/process/image', { method: 'POST', body: formData });
    const result = await response.json();
    if (result.processedUrl) {
      document.getElementById('processedImage').src = result.processedUrl;
    }
  });
  