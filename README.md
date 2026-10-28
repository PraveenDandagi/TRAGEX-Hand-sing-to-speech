# TRAGEX-Hand-sing-to-speech
**Tragex – Sign to Speech** is a small Windows desktop demo that uses your webcam to recognize a handful of hand gestures and speak the matching phrase aloud.

It uses **OpenCV** to capture and display camera frames, **MediaPipe** to detect hand landmarks, and a simple finger-position heuristic to classify gestures. A recognized gesture must be held steady for about a second before it is spoken.

Run it with `python app.py` or double-click `run.bat`. Install its dependencies from `requirements.txt`. Press **Q** or **Esc** to quit, or **S** to speak the current gesture again.

It’s a lightweight gesture demo, not a trained sign-language translator: it recognizes only these specific poses and does not interpret full signing or context. The implementation is in `app.py`, and the project notes are in `README.md`.
