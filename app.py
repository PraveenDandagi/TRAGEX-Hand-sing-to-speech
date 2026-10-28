import time
from dataclasses import dataclass
from typing import Optional

import cv2
import mediapipe as mp
import pyttsx3


APP_TITLE = "Tragex - Sign to Speech"
STABLE_SECONDS = 1.0
SPEAK_COOLDOWN = 1.5


@dataclass
class GestureState:
    label: Optional[str] = None
    since: float = 0.0
    last_spoken: Optional[str] = None
    last_spoken_at: float = 0.0


class Speaker:
    def __init__(self) -> None:
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.engine.setProperty("volume", 1.0)

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()


def finger_states(hand_landmarks, handedness_label: str) -> dict[str, bool]:
    landmarks = hand_landmarks.landmark

    # Thumb direction depends on handedness and the mirrored preview.
    if handedness_label == "Right":
        thumb_open = landmarks[4].x < landmarks[3].x
    else:
        thumb_open = landmarks[4].x > landmarks[3].x

    return {
        "thumb": thumb_open,
        "index": landmarks[8].y < landmarks[6].y,
        "middle": landmarks[12].y < landmarks[10].y,
        "ring": landmarks[16].y < landmarks[14].y,
        "pinky": landmarks[20].y < landmarks[18].y,
    }


def classify_gesture(fingers: dict[str, bool]) -> Optional[str]:
    thumb = fingers["thumb"]
    index = fingers["index"]
    middle = fingers["middle"]
    ring = fingers["ring"]
    pinky = fingers["pinky"]

    count = sum([thumb, index, middle, ring, pinky])

    if count == 0:
        return "Stop"
    if thumb and not index and not middle and not ring and not pinky:
        return "Water"
    if index and not middle and not ring and not pinky and not thumb:
        return "Help"
    if index and middle and not ring and not pinky and not thumb:
        return "Yes"
    if index and middle and ring and pinky and not thumb:
        return "Hello"
    if count >= 4:
        return "Thank you"
    return None


def draw_overlay(frame, label: Optional[str], status: str) -> None:
    height, width = frame.shape[:2]

    cv2.rectangle(frame, (0, 0), (width, 72), (20, 24, 31), -1)
    cv2.putText(frame, APP_TITLE, (18, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, status, (18, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 200, 220), 2)

    if label:
        cv2.rectangle(frame, (0, height - 92), (width, height), (20, 24, 31), -1)
        cv2.putText(frame, f"Detected: {label}", (18, height - 52), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 153), 2)
        cv2.putText(
            frame,
            "Press Q to quit",
            (18, height - 18),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (180, 200, 220),
            2,
        )


def main() -> int:
    speaker = Speaker()
    state = GestureState()

    hands = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )
    draw_utils = mp.solutions.drawing_utils
    connections = mp.solutions.hands.HAND_CONNECTIONS

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open the camera.")
        return 1

    print("Camera started. Press Q in the window to quit.")

    try:
        while True:
            ok, frame = camera.read()
            if not ok:
                print("Failed to read a frame from the camera.")
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            detected_label: Optional[str] = None
            status = "Show one hand to the camera."

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                handedness = "Right"
                if results.multi_handedness:
                    handedness = results.multi_handedness[0].classification[0].label

                draw_utils.draw_landmarks(frame, hand_landmarks, connections)
                fingers = finger_states(hand_landmarks, handedness)
                detected_label = classify_gesture(fingers)

                if detected_label:
                    status = "Hold the gesture steady to speak it."
                else:
                    status = "Hand detected, but gesture is not clear yet."

            now = time.monotonic()
            if detected_label != state.label:
                state.label = detected_label
                state.since = now
                if detected_label is None:
                    state.last_spoken = None

            if state.label and (now - state.since) >= STABLE_SECONDS:
                if state.last_spoken != state.label and (now - state.last_spoken_at) >= SPEAK_COOLDOWN:
                    speaker.speak(state.label)
                    state.last_spoken = state.label
                    state.last_spoken_at = now
                    status = f"Speaking: {state.label}"

            draw_overlay(frame, state.label, status)
            cv2.imshow(APP_TITLE, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("s") and state.label:
                speaker.speak(state.label)
                state.last_spoken = state.label
                state.last_spoken_at = time.monotonic()
            if key in (ord("q"), 27):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        hands.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
