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
