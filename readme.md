## Hand Gesture Detection

A lightweight, real-time hand gesture detection app using OpenCV and CVZone (MediaPipe under the hood). It opens your webcam, tracks a single hand, and classifies simple gestures like fist, point, peace, and open hand.

### Features
- **Real-time tracking**: Uses `cvzone.HandTrackingModule.HandDetector` for fast hand landmark detection.
- **Simple gestures**: Detects thumb/index logic and counts raised fingers to map to commands.
- **On-screen feedback**: Displays the recognized gesture text on the video feed.

## Project Structure
```
.
├─ gesture_detection.py      # Main application
├─ readme.md                 # This file
└─ .venv312/                 # (Optional) Python 3.12 virtual environment
```

## Requirements
- **OS**: Windows 10/11 (tested)
- **Python**: 3.10 – 3.12 (project uses a `.venv312` virtual environment)
- **Webcam**

### Python packages
- `opencv-python`
- `cvzone`
- `mediapipe` (dependency of `cvzone` but install explicitly for reliability)
- `numpy`

## Quick Start (Windows PowerShell)

### 1) Clone or open the project directory
Open Windows PowerShell and `cd` into the project folder:
```powershell
cd "D:\Python Shit\Hand-gesture-detection"
```

### 2) Create and activate a virtual environment (recommended)
If you already have `.venv312`, activate it. Otherwise, create one with Python 3.12 (or your installed version):
```powershell
# Create venv (only if you don't already have one)
python -m venv .venv312

# Activate
.\.venv312\Scripts\Activate.ps1
```

If PowerShell blocks scripts, run as Administrator once:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then re-run the activation command.

### 3) Install dependencies
```powershell
pip install --upgrade pip
pip install opencv-python cvzone mediapipe numpy
```

### 4) Run the app
```powershell
python .\gesture_detection.py
```

Press `q` to quit the window.

## How It Works
- The script initializes a webcam stream at 1280×720.
- `HandDetector(detectionCon=0.8, maxHands=1)` finds a single hand and returns 21 landmarks.
- Logic determines which fingers are up by comparing fingertip landmarks against lower joints. Thumb logic accounts for left vs right hands.
- A gesture label is derived from the count and combination of raised fingers and rendered onto the frame.

## Gestures and Labels
- **0 fingers**: Fist / Stop
- **Index only (1)**: Point / Go
- **Index + Middle (2)**: Peace
- **All five (5)**: Open Hand / Play

Note: Gesture mapping is easily customizable in `gesture_detection.py`.

## Configuration
- **Webcam index**: If the wrong camera opens or you have multiple cameras, edit the index in `gesture_detection.py`:
```python
cap = cv2.VideoCapture(0)  # try 1 or 2 if needed
```
- **Resolution**: Adjust via:
```python
cap.set(3, 1280)  # width
cap.set(4, 720)   # height
```
- **Detector confidence**: Increase/decrease detection threshold:
```python
detector = HandDetector(detectionCon=0.8, maxHands=1)
```

## Troubleshooting
- **Black window / no frames**:
  - Another app may be using the webcam. Close it and retry.
  - Try `VideoCapture(1)` or `VideoCapture(2)`.
- **ImportError: cv2/cvzone/mediapipe not found**:
  - Ensure the venv is activated and run `pip install opencv-python cvzone mediapipe numpy`.
- **PowerShell cannot run Activate.ps1**:
  - Run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` and re-activate.
- **Laggy video**:
  - Lower resolution or ensure your environment uses a Release build of OpenCV (`opencv-python`).

## Development Notes
- This project prioritizes readability over compactness. Finger state logic lives in `gesture_detection.py` for easy modification.
- `cvzone` wraps MediaPipe’s hand tracking making it simpler to work with landmarks and hand type.

## Extending
- Map gestures to custom actions (e.g., media controls, robot commands).
- Add more robust gesture classifiers using time-based smoothing or ML.
- Support multi-hand interactions by setting `maxHands=2` and iterating over detected hands.

