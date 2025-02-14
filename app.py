from flask import Flask, render_template, request, send_file, redirect, url_for, jsonify
import random
import io
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Must be set before importing pyplot
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFilter
from werkzeug.utils import secure_filename
from datetime import datetime
from pydub import AudioSegment
from pydub.effects import speedup

app = Flask(__name__)
app.config.update({
    'UPLOAD_FOLDER': os.path.join('static', 'uploads'),
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16 MB
    'ALLOWED_EXTENSIONS': {'png', 'jpg', 'jpeg', 'mp3', 'wav'},
    'SECRET_KEY': 'your-secret-key-here'
})

# ----------------------
# Helper Functions
# ----------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def apply_glitch_effect(image):
    """Applique un effet glitch en décalant aléatoirement des bandes horizontales."""
    np_img = np.array(image)
    height, width, channels = np_img.shape
    num_glitches = random.randint(10, 20)  # Augmente le nombre de glitches
    for _ in range(num_glitches):
        # Choix d'une bande horizontale aléatoire
        band_height = random.randint(1, max(1, height // 20))
        row_start = random.randint(0, height - band_height)
        shift = random.randint(-50, 50)  # Décalage plus important pour un effet plus visible
        # Décale la bande de lignes horizontalement (axis=1 correspond aux colonnes)
        np_img[row_start:row_start + band_height] = np.roll(np_img[row_start:row_start + band_height], shift, axis=1)
    return Image.fromarray(np_img)


def process_audio_effect(audio_path, effect='reverse'):
    """Apply a simple audio effect (reverse or speedup) and return path to processed file."""
    sound = AudioSegment.from_file(audio_path)
    if effect == 'reverse':
        processed = sound.reverse()
    elif effect == 'speedup':
        processed = speedup(sound, playback_speed=1.5)
    else:
        processed = sound  # No change if effect not recognized

    processed_filename = f"processed_{os.path.basename(audio_path)}"
    processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
    processed.export(processed_path, format=audio_path.rsplit('.', 1)[1].lower())
    return processed_filename

# ----------------------
# Generative Art Engine
# ----------------------
class NeuroCanvas:
    def __init__(self, width=1200, height=800):
        self.width = width
        self.height = height
        # Create a dark background canvas
        self.canvas = Image.new('RGB', (width, height), '#0f172a')
        self.draw = ImageDraw.Draw(self.canvas)
    
    def _neon_color(self):
        """Return a random neon color (RGB tuple)."""
        colors = [
            (57, 255, 20),   # Neon Green
            (0, 255, 255),   # Cyan
            (255, 0, 255),   # Magenta
            (255, 255, 0),   # Neon Yellow
            (255, 105, 180)  # Hot Pink
        ]
        return random.choice(colors)
    
    def generate_cyberpunk(self):
        """Generate a cyberpunk style artwork."""
        for _ in range(random.randint(50, 100)):
            shape_type = random.choice(['neon_poly', 'hologram'])
            color = self._neon_color()
            if shape_type == 'neon_poly':
                self._draw_neon_polygon(color)
            # (Optional: add additional shape types here)
                
        self.canvas = self.canvas.filter(ImageFilter.SMOOTH_MORE)
        return self.canvas

    def _draw_neon_polygon(self, color):
        sides = random.randint(3, 8)
        size = random.randint(30, 150)
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        angle = 360 / sides
        points = [
            (x + size * np.cos(np.deg2rad(angle * i)),
             y + size * np.sin(np.deg2rad(angle * i)))
            for i in range(sides)
        ]
        # Draw polygon several times with increasing stroke width for a glow effect
        for i in range(3):
            self.draw.polygon(points, outline=color, width=2+i)

# ----------------------
# Routes
# ----------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/artwork')
def artwork_detail():
    # For demonstration, simply show one generated artwork.
    # In a complete implementation, you might retrieve artwork details from a database.
    art_url = url_for('generate_cyberpunk')
    return render_template('artwork_detail.html', image=art_url)

@app.route('/generate/cyberpunk')
def generate_cyberpunk():
    generator = NeuroCanvas()
    img = generator.generate_cyberpunk()
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

@app.route('/generate/art', methods=['POST'])
def generate_art_endpoint():
    """
    Generate art based on a given style.
    For now, only 'cyberpunk' style is implemented.
    """
    data = request.get_json()
    style = data.get('style', 'cyberpunk')
    # Future: Add other styles or parameters from 'params'
    generator = NeuroCanvas()
    img = generator.generate_cyberpunk()
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

@app.route('/data-viz')
def data_viz():
    """Generate a creative data visualization using weather data."""
    try:
        df = pd.read_csv(os.path.join('data', 'weather_data.csv'))
    except FileNotFoundError:
        return "Weather data file not found.", 404

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['date'], df['temperature'], color='#00ff9d', linewidth=2, marker='o')
    ax.fill_between(df['date'], df['temperature'], color='#00ff9d22')
    ax.set_title('Neural Weather Patterns', color='white', fontsize=18)
    ax.set_facecolor('#0f172a')
    fig.set_facecolor('#0f172a')
    
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    plt.close()
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype='image/png')

@app.route('/visualize/data')
def visualize_data():
    """Return JSON data for Plotly visualization (used by viz.js)."""
    dataset = request.args.get('dataset', 'weather')
    try:
        df = pd.read_csv(os.path.join('data', 'weather_data.csv'))
    except FileNotFoundError:
        return jsonify({"error": "Data file not found."}), 404

    traces = [{
        'x': df['date'].tolist(),
        'y': df['temperature'].tolist(),
        'type': 'scatter',
        'mode': 'lines+markers',
        'line': {'color': '#00ff9d'},
        'fill': 'tozeroy'
    }]
    layout = {
        'title': 'Neural Weather Patterns',
        'paper_bgcolor': '#0f172a',
        'plot_bgcolor': '#0f172a',
        'font': {'color': 'white'}
    }
    return jsonify({"traces": traces, "layout": layout})

@app.route('/image-lab', methods=['GET'])
def image_lab():
    return render_template('image-lab.html')

@app.route('/process/image', methods=['POST'])
def process_image():
    # Vérifier que le fichier est envoyé sous la clé "image"
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        # Ouvre l'image et applique l'effet glitch amélioré
        image = Image.open(filepath).convert('RGB')
        glitched = apply_glitch_effect(image)
        processed_filename = 'glitched_' + filename
        processed_path = os.path.join(app.config['UPLOAD_FOLDER'], processed_filename)
        glitched.save(processed_path)
        return jsonify({"processedUrl": url_for('static', filename='uploads/' + processed_filename)})
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/audio-lab', methods=['GET'])
def audio_lab():
    return render_template('image-lab.html', audio_lab=True)

@app.route('/process/audio', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        effect = request.form.get('effect', 'reverse')  # 'reverse' or 'speedup'
        processed_filename = process_audio_effect(filepath, effect=effect)
        return jsonify({"processedUrl": url_for('static', filename='uploads/' + processed_filename)})
    return jsonify({"error": "File type not allowed"}), 400

@app.route('/interactive-art')
def interactive_art():
    return render_template('interactive-art.html')

@app.route('/generate/caption', methods=['GET'])
def generate_caption():
    """Bonus: Generate a random caption (a simple ML/Markov-chain style demo)."""
    captions = [
        "Where algorithms dream and pixels dance.",
        "A neural spark ignites a canvas of code.",
        "Abstract pulses of digital emotion.",
        "When data meets art, magic happens.",
        "An interplay of randomness and design."
    ]
    return jsonify({"caption": random.choice(captions)})

# ----------------------
# Run the App
# ----------------------
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
