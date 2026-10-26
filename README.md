# ⚡ Thanos Snap — Google Meet

### 🟣 Snap your fingers. Watch the dust fly.

A Thanos-inspired, gesture-controlled video effect for Google Meet. Use hand gestures to trigger a cinematic purple particle disintegration effect in your webcam feed.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV"/>
  <img src="https://img.shields.io/badge/MediaPipe-0097A7?style=for-the-badge&logo=google&logoColor=white" alt="MediaPipe"/>
  <img src="https://img.shields.io/badge/Chrome_Extension-4285F4?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Chrome Extension"/>
</p>

<p align="center">
  <b>Gesture Recognition · Real-Time Video Processing · Purple Particle Effects</b>
</p>

---

## 🌌 What is this?

Ever wanted to make your webcam disappear like half the universe in *Avengers: Infinity War*?

**Thanos Snap — Google Meet** is an experimental project that combines computer vision, hand gesture recognition, and real-time video processing to bring a little Marvel-style chaos to your video calls.

The project uses a Python companion application to process webcam frames and output the effect through a virtual camera. A Chrome extension provides a convenient way to control the companion.

## ✨ Features

- 🖐️ **Hand gesture detection** — Uses MediaPipe to detect hands in the webcam feed.
- 🟣 **Purple dust effect** — Creates a Thanos-inspired particle disintegration animation.
- 🎥 **Real-time video processing** — Processes webcam frames using OpenCV.
- 🧩 **Chrome extension controls** — Start and stop the companion through the extension popup.
- 📹 **Virtual camera output** — Routes processed video to a virtual camera for use in Google Meet.
- 🐍 **Python-powered backend** — Uses Flask for local communication between the extension and companion application.

> **Current prototype:** The effect processes the video frame as a whole. It does not yet perform precise person segmentation or isolate individual body parts. Gesture behavior and virtual camera compatibility may depend on your setup.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Companion application |
| OpenCV | Webcam capture and image processing |
| MediaPipe | Hand landmark detection |
| Flask | Local communication API |
| pyvirtualcam | Virtual camera video output |
| HTML, CSS, JavaScript | Chrome extension interface |
| Chrome Extensions API | Extension functionality |
| Google Meet | Video-call destination |

## 🏗️ How It Works

```text
Webcam
   ↓
Python Companion
   ↓
MediaPipe Hand Detection
   ↓
Gesture Recognition
   ↓
Purple Particle Effect
   ↓
Virtual Camera Output
   ↓
Google Meet
```

The Chrome extension communicates with the Python companion through a local Flask server to control the effect.

## 📁 Project Structure

```text
thanos-snap-google-meet/
│
├── companion.py
├── requirements.txt
├── .gitignore
├── README.md
│
└── extension/
    ├── manifest.json
    ├── popup.html
    ├── popup.css
    └── popup.js
```

## 🚀 Getting Started

### Prerequisites

Install the following before running the project:

- Python 3.11 recommended
- Google Chrome
- Git
- A working webcam
- A compatible virtual camera setup

### 1. Clone the repository

```bash
git clone https://github.com/Ankit-singh19/thanos-snap-google-meet.git
```

Navigate into the project directory:

```bash
cd thanos-snap-google-meet
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked by your PowerShell execution policy, you can run the companion using the virtual environment's Python executable directly.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

If multiple Python versions are installed, use the Python executable inside `.venv` to avoid installing packages into the wrong environment.

### 4. Start the Python companion

```powershell
python companion.py
```

Keep the terminal open while using the extension.

The companion exposes a local control endpoint at:

```text
http://127.0.0.1:8765
```

You can check its status at:

```text
http://127.0.0.1:8765/status
```

### 5. Load the Chrome extension

1. Open Google Chrome.
2. Visit `chrome://extensions`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the project's `extension` folder.
6. Pin the extension if you want quick access.

### 6. Connect Google Meet

1. Start the Python companion.
2. Open the extension popup and use its controls.
3. Configure a compatible virtual camera output.
4. Open Google Meet.
5. Go to **Settings → Video → Camera**.
6. Select the virtual camera that is receiving the processed frames.

**Troubleshooting tip:** If Google Meet says the camera is unavailable, close applications that may be holding the virtual camera, check the companion status endpoint, and verify that the virtual camera driver is installed and working.

## 🎬 Demo

Have a screen recording or GIF of the effect? Add it here to make the repository more engaging.

For example, save your demo as `assets/demo.gif` and add:

```markdown
![Thanos Snap Demo](assets/demo.gif)
```

Only add this image reference after placing the actual GIF at that path.

## 🔮 Future Improvements

- 🎯 Person segmentation instead of whole-frame disintegration
- ✋ More reliable gesture recognition and configurable triggers
- ✨ More realistic particle physics and dust trails
- 🎨 Customizable particle colors and effect intensity
- ⚙️ Better error handling and virtual camera setup guidance
- 🎥 Demo recordings and performance improvements

## 🤝 Contributing

Contributions, bug reports, and feature suggestions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your changes locally.
5. Open a pull request with a clear description.

For larger changes, consider opening an issue first to discuss the idea.

## ⚠️ Disclaimer

This is an independent experimental project inspired by a fictional visual effect from Marvel's *Avengers: Infinity War*.

It is not affiliated with or endorsed by Marvel, Disney, Google, or the Google Meet team. Product names and trademarks belong to their respective owners.

## 👨‍💻 Author

**Ankit Singh**

- GitHub: [@Ankit-singh19](https://github.com/Ankit-singh19)
- Project Repository: [thanos-snap-google-meet](https://github.com/Ankit-singh19/thanos-snap-google-meet)

---

<p align="center">
  <b>🟣 Ready to make your next video call a little more cinematic?</b>
  <br/>
  Star ⭐ the repository if you find the project interesting!
</p>
