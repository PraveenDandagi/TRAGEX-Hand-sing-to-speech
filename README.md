<<<<<<< HEAD
# Tragex - Sign to Speech

This is a simple camera-based sign-to-speech demo for Windows.

## What it does

- Opens your webcam
- Detects one hand using MediaPipe
- Recognizes a few simple gestures
- Speaks the detected sign out loud

## Gestures

- Open palm: `Hello`
- Fist: `Stop`
- Thumb only: `Water`
- Index finger only: `Help`
- Index + middle fingers: `Yes`
- Open hand with four or five fingers: `Thank you`

## Run

1. Install the Python packages:

```bash
pip install -r requirements.txt
```

2. Start the app:

```bash
python app.py
```

Or double-click `run.bat`.

## Controls

- `Q` or `Esc` closes the camera window
- `S` speaks the currently detected sign

## Notes

- This is a lightweight demo, not a full trained sign-language model.
- It is meant to be easy to run and easy to understand.
=======
# TRAGEX-Hand-sing-to-speech
**Tragex – Sign to Speech** is a small Windows desktop demo that uses your webcam to recognize a handful of hand gestures and speak the matching phrase aloud.

It uses **OpenCV** to capture and display camera frames, **MediaPipe** to detect hand landmarks, and a simple finger-position heuristic to classify gestures. A recognized gesture must be held steady for about a second before it is spoken.

Run it with `python app.py` or double-click `run.bat`. Install its dependencies from `requirements.txt`. Press **Q** or **Esc** to quit, or **S** to speak the current gesture again.

It’s a lightweight gesture demo, not a trained sign-language translator: it recognizes only these specific poses and does not interpret full signing or context. The implementation is in `app.py`, and the project notes are in `README.md`.
>>>>>>> 52fbd01f0530b5387813fd1d6e9f899b1e2ccca6
