"""Tests for the Flask application routes and functionality."""

import io
import os
import sys

import pytest
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import allowed_file, app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    app.config["UPLOAD_FOLDER"] = "test_uploads"
    os.makedirs("test_uploads", exist_ok=True)
    with app.test_client() as client:
        yield client
    # Cleanup
    if os.path.exists("test_uploads"):
        for file in os.listdir("test_uploads"):
            os.remove(os.path.join("test_uploads", file))
        os.rmdir("test_uploads")


class TestRoutes:
    """Test suite for application routes."""

    def test_index_route(self, client):
        """Test that the index route returns HTML."""
        response = client.get("/")
        assert response.status_code == 200
        assert b"NeuroCanvas" in response.data
        assert b"Generative Art Studio" in response.data

    def test_gallery_route(self, client):
        """Test that the gallery route returns HTML."""
        response = client.get("/gallery")
        assert response.status_code == 200
        assert b"Gallery" in response.data

    def test_image_lab_route(self, client):
        """Test that the image lab route returns HTML."""
        response = client.get("/image-lab")
        assert response.status_code == 200
        assert b"Image Lab" in response.data

    def test_audio_lab_route(self, client):
        """Test that the audio lab route returns HTML."""
        response = client.get("/audio-lab")
        assert response.status_code == 200
        assert b"Audio Lab" in response.data

    def test_interactive_art_route(self, client):
        """Test that the interactive art route returns HTML."""
        response = client.get("/interactive-art")
        assert response.status_code == 200
        assert b"Interactive Art" in response.data

    def test_generate_cyberpunk_route(self, client):
        """Test that the cyberpunk generation route returns an image."""
        response = client.get("/generate/cyberpunk")
        assert response.status_code == 200
        assert response.content_type == "image/png"
        assert len(response.data) > 0

    def test_data_viz_route(self, client):
        """Test that the data visualization route returns an image."""
        response = client.get("/data-viz")
        assert response.status_code == 200
        assert response.content_type == "image/png"
        assert len(response.data) > 0

    def test_generate_caption_route(self, client):
        """Test that the caption generation route returns JSON."""
        response = client.get("/generate/caption")
        assert response.status_code == 200
        assert response.content_type == "application/json"
        data = response.get_json()
        assert "caption" in data
        assert isinstance(data["caption"], str)


class TestFileValidation:
    """Test suite for file validation functions."""

    def test_allowed_file_with_valid_extension(self):
        """Test that allowed_file returns True for valid extensions."""
        assert allowed_file("test.png") is True
        assert allowed_file("test.jpg") is True
        assert allowed_file("test.jpeg") is True
        assert allowed_file("test.mp3") is True
        assert allowed_file("test.wav") is True

    def test_allowed_file_with_invalid_extension(self):
        """Test that allowed_file returns False for invalid extensions."""
        assert allowed_file("test.exe") is False
        assert allowed_file("test.pdf") is False
        assert allowed_file("test") is False

    def test_allowed_file_case_insensitive(self):
        """Test that allowed_file is case-insensitive."""
        assert allowed_file("test.PNG") is True
        assert allowed_file("test.JPG") is True


class TestImageProcessing:
    """Test suite for image processing functionality."""

    def test_process_image_with_valid_file(self, client):
        """Test image processing with a valid image file."""
        # Create a test image
        img = Image.new("RGB", (100, 100), color="red")
        img_io = io.BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        response = client.post(
            "/process/image",
            data={"image": (img_io, "test.png")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "processedUrl" in data

    def test_process_image_without_file(self, client):
        """Test image processing without a file."""
        response = client.post(
            "/process/image", data={}, content_type="multipart/form-data"
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_process_image_with_invalid_extension(self, client):
        """Test image processing with invalid file type."""
        img_io = io.BytesIO(b"fake content")
        response = client.post(
            "/process/image",
            data={"image": (img_io, "test.exe")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data


class TestErrorHandling:
    """Test suite for error handling."""

    def test_404_error(self, client):
        """Test that 404 errors are handled."""
        response = client.get("/nonexistent-route")
        assert response.status_code == 404
