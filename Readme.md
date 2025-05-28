# Gesture Volume Control

This project controls the system volume using hand gestures detected through the webcam. It uses OpenCV for video processing, MediaPipe for hand detection, and Pycaw for interacting with the system's audio controls.

## Requirements

- Python 3.10 or above
- OpenCV
- MediaPipe
- NumPy
- Pycaw
- comtypes

## Installation

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```
## Usage

Run the script using the following command:
```bash
python HandVolumeControl.py
```

Make sure your webcam is connected. The program detects the distance between your thumb and index finger and adjusts the system volume accordingly.

## How it Works

- The webcam captures video frames.
- MediaPipe detects hand landmarks.
- The distance between the thumb tip and index finger tip is calculated.
- This distance is mapped to the system volume range.
- The volume is updated in real-time as the distance changes.

## Exit

Press the d key to stop the program.
