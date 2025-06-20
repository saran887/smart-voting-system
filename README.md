# Smart Voting System 🗳️📷

This is a Face Recognition-based Smart Voting System built with Python, OpenCV, face_recognition, and SQLite. It allows secure registration of voters using facial recognition, ensures one vote per person, and lets users vote for predefined candidates.

---

## 🧰 Features

- Register voters using webcam and face recognition
- Prevent duplicate voting using face encodings
- Vote using GUI buttons (Tkinter)
- View saved images
- View and delete vote counts
- SQLite database for persistent storage

---

## 📁 Project Structure

```
smart_voting/
├── face.py                  # Main app: face detection, registration, voting
├── database.py              # View/delete saved images and database entries
├── vote_count.py            # View and delete all vote counts
├── voter_faces.db           # SQLite database storing face data and votes
├── saved_images/            # Folder where face images are saved
├── name_counter.txt         # Tracks the last used voter number
```

---

## 📦 Dependencies

Install the following packages before running the application:

```bash
pip install opencv-python
pip install face_recognition
pip install numpy
pip install pyttsx3
pip install pillow
```

> ⚠️ Note: `face_recognition` requires `dlib` and CMake. Use the below command to install it (Windows):

```bash
pip install cmake
pip install dlib
pip install face_recognition
```

Or follow the official [face_recognition installation guide](https://github.com/ageitgey/face_recognition#installation).

---

## 🚀 How to Run

### 1. Run the main application:
```bash
python face.py
```
- Press **S** to register a voter and vote.
- Press **Q** to quit and optionally reset the voter counter.

### 2. Manage saved images and face records:
```bash
python database.py
```
- View saved images
- Delete individual or all images and related DB entries

### 3. View or clear vote counts:
```bash
python vote_count.py
```
- View all votes per candidate
- Option to delete/reset all votes

---

## 📸 Webcam Access

Ensure your webcam is properly connected. The app uses the default camera (`cv2.VideoCapture(0)`).

---

## 👥 Candidate List

There are 28 predefined candidates (projects), and each one is vote-eligible via a button in the GUI.

---

## 🔒 Duplicate Detection

Each face is encoded and checked against the DB to prevent double voting. If a match is found, the voter is denied access.

---

## 💾 Data Storage

- **Face Data**: Stored in `voter_faces.db` as numpy-encoded BLOBs
- **Images**: Saved in the `saved_images/` folder
- **Vote Count**: Stored in the `candidate_votes` table

---

## 📄 License

This project is for educational/demo purposes and is free to use.

---

## 🙋‍♂️ Author

Developed by [saran887](https://github.com/saran887)
