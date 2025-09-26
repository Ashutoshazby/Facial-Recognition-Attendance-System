import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime

# ---------------------------
# Paths
# ---------------------------
DATASET_DIR = "dataset"
TRAINER_FILE = "trainer.yml"
LABELS_FILE = "labels.csv"
CSV_FILE = "attendance.csv"

# ---------------------------
# Train recognizer
# ---------------------------
def train_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    ids = []
    faces = []
    label_map = {}
    label_id = 0

    for person in os.listdir(DATASET_DIR):
        person_dir = os.path.join(DATASET_DIR, person)
        if not os.path.isdir(person_dir):
            continue
        print(f"[INFO] Training {person}...")
        label_map[label_id] = person
        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                continue
            detected = face_cascade.detectMultiScale(img, scaleFactor=1.2, minNeighbors=5)
            for (x, y, w, h) in detected:
                faces.append(img[y:y+h, x:x+w])
                ids.append(label_id)
        label_id += 1

    if len(faces) == 0:
        print("[ERROR] No faces found in dataset.")
        return None, None

    recognizer.train(faces, np.array(ids))
    recognizer.save(TRAINER_FILE)

    pd.DataFrame(list(label_map.items()), columns=["id", "name"]).to_csv(LABELS_FILE, index=False)
    print(f"[INFO] Training complete. Model saved to {TRAINER_FILE}")
    return recognizer, label_map

# ---------------------------
# Load recognizer
# ---------------------------
def load_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(TRAINER_FILE)
    labels_df = pd.read_csv(LABELS_FILE)
    label_map = dict(zip(labels_df["id"], labels_df["name"]))
    return recognizer, label_map

# ---------------------------
# Mark attendance once per day
# ---------------------------
def mark_attendance(name):
    today = datetime.now().date()
    ts = datetime.now()

    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        if not set(["name", "date", "timestamp"]).issubset(df.columns):
            df = pd.DataFrame(columns=["name", "date", "timestamp"])
    else:
        df = pd.DataFrame(columns=["name", "date", "timestamp"])

    # check if already marked today
    if not ((df["name"] == name) & (df["date"] == str(today))).any():
        record = {"name": name, "date": str(today), "timestamp": ts.isoformat()}
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        print(f"[ATTENDANCE] {name} marked at {ts.strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    return False

# ---------------------------
# Continuous Attendance
# ---------------------------
def run_attendance_system():
    if not os.path.exists(TRAINER_FILE):
        recognizer, label_map = train_recognizer()
        if recognizer is None:
            return
    else:
        recognizer, label_map = load_recognizer()

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)

    print("[INFO] Running Attendance System (Press 'q' to quit)")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Could not read from camera.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            label_id, confidence = recognizer.predict(roi)

            if confidence < 70:
                name = label_map[label_id]
                color = (0, 255, 0)
                if mark_attendance(name):  # only prints if newly marked
                    print(f"[INFO] {name} is present today.")
            else:
                name = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        cv2.imshow("Attendance System", frame)

        # exit loop if 'q' pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    run_attendance_system()