import io
import logging
import os
import random

import matplotlib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file, url_for

matplotlib.use("Agg")  # Must be set before importing pyplot

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFilter
from pydub import AudioSegment
from pydub.effects import speedup
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration from environment variables with safe defaults
app.config.update(
    {
        "UPLOAD_FOLDER": os.path.join("static", "uploads"),
        "MAX_CONTENT_LENGTH": int(
            os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024)
        ),  # 16 MB
        "ALLOWED_EXTENSIONS": {"png", "jpg", "jpeg", "mp3", "wav"},
        "SECRET_KEY": os.getenv("SECRET_KEY", "dev-secret-key-change-in-production"),
        "DEBUG": os.getenv("FLASK_DEBUG", "False").lower() == "true",
    }
)

# MIME type mapping for validation
ALLOWED_MIME_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
}


# ----------------------
# Helper Functions
# ----------------------
def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed.

    Args:
        filename: Name of the file to check

    Returns:
        True if file extension is in allowed extensions, False otherwise
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


def validate_file_type(file, allowed_extensions: set) -> tuple[bool, str | None]:
    """Validate file by extension and MIME type.

    Args:
        file: FileStorage object from Flask request
        allowed_extensions: Set of allowed file extensions

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file or not file.filename:
        return False, "No file provided"

    # Check extension
    if not allowed_file(file.filename):
        return False, "File type not allowed"

    # Check MIME type
    ext = file.filename.rsplit(".", 1)[1].lower()
    expected_mime = ALLOWED_MIME_TYPES.get(ext)
    if expected_mime and file.mimetype != expected_mime:
        logger.warning(f"MIME type mismatch: {file.mimetype} != {expected_mime}")
        return False, "Invalid file type"

    return True, None


def apply_glitch_effect(image: Image.Image) -> Image.Image:
    """Apply glitch effect by randomly shifting horizontal bands.

    Args:
        image: PIL Image object to process

    Returns:
        Processed PIL Image with glitch effect
    """
    np_img = np.array(image)
    height, width, channels = np_img.shape
    num_glitches = random.randint(10, 20)
    for _ in range(num_glitches):
        band_height = random.randint(1, max(1, height // 20))
        row_start = random.randint(0, height - band_height)
        shift = random.randint(-50, 50)
        np_img[row_start : row_start + band_height] = np.roll(
            np_img[row_start : row_start + band_height], shift, axis=1
        )
    return Image.fromarray(np_img)


def process_audio_effect(audio_path: str, effect: str = "reverse") -> str:
    """Apply audio effect (reverse or speedup) and return processed filename.

    Args:
        audio_path: Path to the audio file
        effect: Type of effect to apply ('reverse' or 'speedup')

    Returns:
        Filename of the processed audio file

    Raises:
        Exception: If audio processing fails
    """
    try:
        sound = AudioSegment.from_file(audio_path)
        if effect == "reverse":
            processed = sound.reverse()
        elif effect == "speedup":
            processed = speedup(sound, playback_speed=1.5)
        else:
            processed = sound

        processed_filename = f"processed_{os.path.basename(audio_path)}"
        processed_path = os.path.join(app.config["UPLOAD_FOLDER"], processed_filename)
        processed.export(processed_path, format=audio_path.rsplit(".", 1)[1].lower())
        return processed_filename
    except Exception as e:
        logger.error(f"Audio processing error: {e}")
        raise


# ----------------------
# Generative Art Engine
# ----------------------
class NeuroCanvas:
    """Generative art engine for creating cyberpunk-style artworks."""

    def __init__(self, width: int = 1200, height: int = 800) -> None:
        """Initialize the NeuroCanvas generator.

        Args:
            width: Canvas width in pixels
            height: Canvas height in pixels
        """
        self.width = width
        self.height = height
        # Create a dark background canvas
        self.canvas = Image.new("RGB", (width, height), "#0f172a")
        self.draw = ImageDraw.Draw(self.canvas)

    def _neon_color(self) -> tuple[int, int, int]:
        """Return a random neon color (RGB tuple).

        Returns:
            Tuple of (R, G, B) values
        """
        colors = [
            (57, 255, 20),  # Neon Green
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
            (255, 255, 0),  # Neon Yellow
            (255, 105, 180),  # Hot Pink
        ]
        return random.choice(colors)

    def generate_cyberpunk(self) -> Image.Image:
        """Generate a cyberpunk style artwork.

        Returns:
            PIL Image object with generated artwork
        """
        for _ in range(random.randint(50, 100)):
            color = self._neon_color()
            self._draw_neon_polygon(color)

        self.canvas = self.canvas.filter(ImageFilter.SMOOTH_MORE)
        return self.canvas

    def _draw_neon_polygon(self, color: tuple[int, int, int]) -> None:
        """Draw a neon polygon with glow effect.

        Args:
            color: RGB color tuple for the polygon
        """
        sides = random.randint(3, 8)
        size = random.randint(30, 150)
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        angle = 360 / sides
        points = [
            (
                x + size * np.cos(np.deg2rad(angle * i)),
                y + size * np.sin(np.deg2rad(angle * i)),
            )
            for i in range(sides)
        ]
        # Draw polygon several times with increasing stroke width for a glow effect
        for i in range(3):
            self.draw.polygon(points, outline=color, width=2 + i)


# ----------------------
# Routes
# ----------------------


@app.route("/")
def index() -> str:
    """Render the homepage.

    Returns:
        Rendered HTML template for homepage
    """
    return render_template("index.html")


@app.route("/gallery")
def gallery() -> str:
    """Render the gallery page.

    Returns:
        Rendered HTML template for gallery
    """
    return render_template("gallery.html")


@app.route("/generate/cyberpunk")
def generate_cyberpunk():
    """Generate a cyberpunk artwork and return as image.

    Returns:
        Flask response with PNG image
    """
    generator = NeuroCanvas()
    img = generator.generate_cyberpunk()
    img_buffer = io.BytesIO()
    img.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    return send_file(img_buffer, mimetype="image/png")


@app.route("/data-viz")
def data_viz():
    """Generate a creative data visualization using weather data.

    Returns:
        Flask response with PNG chart image or error message
    """
    try:
        df = pd.read_csv(os.path.join("data", "weather_data.csv"))
    except FileNotFoundError:
        logger.error("Weather data file not found")
        return "Weather data file not found.", 404
    except Exception as e:
        logger.error(f"Error reading weather data: {e}")
        return "Error processing data.", 500

    try:
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df["date"], df["temperature"], color="#00ff9d", linewidth=2, marker="o")
        ax.fill_between(df["date"], df["temperature"], color="#00ff9d22")
        ax.set_title("Neural Weather Patterns", color="white", fontsize=18)
        ax.set_facecolor("#0f172a")
        fig.set_facecolor("#0f172a")

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png")
        plt.close()
        img_buffer.seek(0)
        return send_file(img_buffer, mimetype="image/png")
    except Exception as e:
        logger.error(f"Error generating visualization: {e}")
        return "Error generating visualization.", 500


@app.route("/image-lab", methods=["GET"])
def image_lab() -> str:
    """Render the image lab page.

    Returns:
        Rendered HTML template for image lab
    """
    return render_template("image-lab.html")


@app.route("/process/image", methods=["POST"])
def process_image():
    """Process uploaded image with glitch effect.

    Returns:
        JSON response with processed image URL or error message
    """
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Validate file type
    is_valid, error_msg = validate_file_type(file, {"png", "jpg", "jpeg"})
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        image = Image.open(filepath).convert("RGB")
        glitched = apply_glitch_effect(image)
        processed_filename = "glitched_" + filename
        processed_path = os.path.join(app.config["UPLOAD_FOLDER"], processed_filename)
        glitched.save(processed_path)

        logger.info(f"Image processed successfully: {filename}")
        return jsonify(
            {
                "processedUrl": url_for(
                    "static", filename="uploads/" + processed_filename
                )
            }
        )
    except Exception as e:
        logger.error(f"Image processing error: {e}")
        return jsonify({"error": "Failed to process image"}), 500


@app.route("/audio-lab", methods=["GET"])
def audio_lab() -> str:
    """Render the audio lab page.

    Returns:
        Rendered HTML template for audio lab
    """
    return render_template("image-lab.html", audio_lab=True)


@app.route("/process/audio", methods=["POST"])
def process_audio():
    """Process uploaded audio with effects.

    Returns:
        JSON response with processed audio URL or error message
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Validate file type
    is_valid, error_msg = validate_file_type(file, {"mp3", "wav"})
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        effect = request.form.get("effect", "reverse")
        processed_filename = process_audio_effect(filepath, effect=effect)

        logger.info(f"Audio processed successfully: {filename}")
        return jsonify(
            {
                "processedUrl": url_for(
                    "static", filename="uploads/" + processed_filename
                )
            }
        )
    except Exception as e:
        logger.error(f"Audio processing error: {e}")
        return (
            jsonify({"error": "Failed to process audio. FFmpeg may be required."}),
            500,
        )


@app.route("/interactive-art")
def interactive_art() -> str:
    """Render the interactive art canvas page.

    Returns:
        Rendered HTML template for interactive art
    """
    return render_template("interactive-art.html")


@app.route("/generate/caption", methods=["GET"])
def generate_caption():
    """Generate a random artistic caption.

    Returns:
        JSON response with random caption
    """
    captions = [
        "Where algorithms dream and pixels dance.",
        "A neural spark ignites a canvas of code.",
        "Abstract pulses of digital emotion.",
        "When data meets art, magic happens.",
        "An interplay of randomness and design.",
    ]
    return jsonify({"caption": random.choice(captions)})


# ----------------------
# Run the App
# ----------------------
if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    debug_mode = app.config.get("DEBUG", False)
    logger.info(
        f"Starting NeuroCanvas in {'debug' if debug_mode else 'production'} mode"
    )
    app.run(debug=debug_mode)
