"""Tests for the NeuroCanvas generative art engine."""

import os
import sys

import numpy as np
from PIL import Image

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import NeuroCanvas


class TestNeuroCanvas:
    """Test suite for NeuroCanvas class."""

    def test_neurocanvas_initialization(self):
        """Test that NeuroCanvas initializes with correct dimensions."""
        canvas = NeuroCanvas(width=800, height=600)
        assert canvas.width == 800
        assert canvas.height == 600
        assert canvas.canvas is not None
        assert canvas.draw is not None

    def test_neurocanvas_default_dimensions(self):
        """Test that NeuroCanvas uses default dimensions when not specified."""
        canvas = NeuroCanvas()
        assert canvas.width == 1200
        assert canvas.height == 800

    def test_neon_color_returns_valid_rgb(self):
        """Test that _neon_color returns a valid RGB tuple."""
        canvas = NeuroCanvas()
        color = canvas._neon_color()
        assert isinstance(color, tuple)
        assert len(color) == 3
        assert all(0 <= c <= 255 for c in color)

    def test_generate_cyberpunk_returns_image(self):
        """Test that generate_cyberpunk returns a PIL Image."""
        canvas = NeuroCanvas()
        image = canvas.generate_cyberpunk()
        assert isinstance(image, Image.Image)
        assert image.mode == "RGB"
        assert image.size == (canvas.width, canvas.height)

    def test_generate_cyberpunk_different_results(self):
        """Test that generate_cyberpunk produces different results on each call."""
        canvas1 = NeuroCanvas()
        canvas2 = NeuroCanvas()

        img1 = canvas1.generate_cyberpunk()
        img2 = canvas2.generate_cyberpunk()

        # Convert to arrays for comparison
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Images should be different (not identical)
        assert not np.array_equal(arr1, arr2)
