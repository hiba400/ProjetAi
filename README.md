# Interactive Generative Art Gallery

Welcome to the **Interactive Generative Art Gallery** – a creative web application that showcases generative art, data visualizations, and interactive tools for manipulating images and art. This project demonstrates how to combine Python, Flask, and various libraries to build an engaging digital art gallery.

## Project Overview

The Interactive Generative Art Gallery features:

- **Generative Art Pieces:** Randomly generated artworks created using Python's object-oriented programming, loops, and conditionals.
- **Data-Driven Visualizations:** Creative visual representations of data (e.g., weather data) using Matplotlib and Pandas.
- **Image Manipulation:** A tool (Image Lab) that allows users to upload images and apply a glitch effect.
- **Interactive Art Canvas:** An HTML5 canvas where users can click to generate colorful, random shapes.
- **(Optional) Audio Manipulation & Machine Learning:** Additional features can include audio processing (with PyDub) and bonus ML features (e.g., art caption generation or style transfer).

## Features

- **Generative Art Engine:** Uses a custom `NeuroCanvas` class to create cyberpunk-style artwork.
- **Data Visualization:** Displays creative data visualizations with Matplotlib.
- **Image Lab:** Allows users to upload an image and apply a glitch effect using Pillow.
- **Interactive Canvas:** Lets users draw by clicking on a canvas, which generates random colored circles.
- **Responsive Web Design:** All pages include inline CSS for a consistent look and feel.
- **Flask Web App:** Hosts all these interactive features and serves as the project's backend.

## Installation

### Prerequisites

- **Python 3.7+**  
- **Git** (optional, for cloning the repository)

### Setup Instructions

1. **Clone the Repository or Download the ZIP:**
   ```bash
   git clone https://github.com/yourusername/interactive-generative-art-gallery.git
   cd interactive-generative-art-gallery
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   - On **Windows:**
     ```bash
     venv\Scripts\activate.bat
     ```
   - On **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies:**
   ```bash
   pip install flask pillow matplotlib pandas numpy
   ```
   For audio processing (optional):
   ```bash
   pip install pydub
   ```
   > **Note:** For audio processing, ensure you have [FFmpeg](https://ffmpeg.org/) installed on your system.

## Running the Application

1. **Ensure your virtual environment is activated.**
2. **Run the Flask application:**
   ```bash
   python app.py
   ```
3. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
interactive-generative-art-gallery/
├── app.py
├── static/
│   └── js/
│       ├── app.js
│       ├── image-lab.js
│       └── interactive-art.js
│   └── uploads/         # For uploaded images and audio files
└── templates/
    ├── index.html
    ├── gallery.html
    ├── image-lab.html
    ├── interactive-art.html
    └── artwork_detail.html
```

## Troubleshooting

- **Template Not Found Error:** Ensure all HTML template files are in the `templates/` folder and named correctly.
- **Cyberpunk Art Generation Error:** Verify that `self._draw_data_stream(color)` call is removed from `generate_cyberpunk()` method.
- **404 Errors for Static Files:** Check directory structure and route configurations.
- **Virtual Environment Issues:** Confirm proper virtual environment activation before installing dependencies.

## Future Enhancements

- **Audio Processing:** Add advanced audio manipulation using PyDub and additional filters.
- **Machine Learning:** Integrate style transfer or art caption generation using TensorFlow or PyTorch.
- **User Interaction:** Implement user authentication, saved galleries, and interactive art customization tools.

## License

This project is for educational purposes. Feel free to modify and improve it for your own use.

---

Enjoy exploring the intersection of art and technology with the Interactive Generative Art Gallery!
