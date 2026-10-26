# Thanos Snap for Google Meet (prototype)

This project uses a **local Python companion app + Chrome extension + OBS Virtual Camera**.
A pure Chrome extension cannot reliably replace the camera stream that Google Meet sends to other people, so this prototype processes your webcam locally and publishes the processed frames through OBS Virtual Camera.

## Requirements
- Windows 10/11 (other OSes may need different virtual-camera setup)
- Python 3.10 or 3.11 recommended
- Google Chrome
- OBS Studio installed, with **OBS Virtual Camera** available
- A webcam

## Install
1. Install OBS Studio from https://obsproject.com/ and open it once.
2. In a terminal, open this project folder.
3. Create a virtual environment (recommended):
   ```powershell
   py -3.11 -m venv .venv
   .\\.venv\\Scripts\\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Run the companion app:
   ```powershell
   python companion.py
   ```
   Leave the terminal running. The app listens only on `127.0.0.1:8765`.
6. Load the Chrome extension:
   - Open `chrome://extensions`
   - Enable **Developer mode**
   - Click **Load unpacked**
   - Select the `extension` folder inside this project.
7. Click the Thanos Snap extension icon and press **Connect**.
8. In Google Meet: **More options → Settings → Video → Camera → OBS Virtual Camera**.
9. Keep the companion app running and use your **real webcam** as the camera source inside the app; Meet uses OBS Virtual Camera.

## Gestures
- **Open palm, then make a fist**: trigger the dust effect.
- **Open palm, then bring thumb and index finger together**: also triggers the effect.
- The trigger has a cooldown to prevent repeated activations.

Hand gestures are heuristic and may need tuning for your lighting, camera angle, and hand visibility.

## Important limitations
- This is a prototype, not a polished production extension.
- The effect currently disintegrates the *whole outgoing frame* into purple dust; it does not segment your body from the background.
- OBS Virtual Camera must be available. If `pyvirtualcam` cannot find it, open OBS and start **Start Virtual Camera** first, then rerun the companion app.
- The Chrome extension controls the local companion app; it does not bypass Google Meet or change other participants' devices.
- Keep the app visible/running and grant webcam permission when prompted.
- The local HTTP service has no authentication and binds to localhost only. Do not change it to listen on a public interface.
