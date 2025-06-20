import tkinter as tk
import pyttsx3
import cv2
import numpy as np
import face_recognition
import sqlite3
import os

# Initialize SQLite 
conn = sqlite3.connect("voter_faces.db")
cursor = conn.cursor()

# Create a table to store face encodings
cursor.execute('''
CREATE TABLE IF NOT EXISTS voters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    face_encoding BLOB
)
''')

# Create a table to store vote counts for candidates
cursor.execute('''
CREATE TABLE IF NOT EXISTS candidate_votes (
    candidate_id TEXT PRIMARY KEY,
    vote_count INTEGER
)
''')
conn.commit()

# Folder to save captured images
SAVE_DIR = "saved_images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# File to store the last name counter
COUNTER_FILE = "name_counter.txt"

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()

# Function to load the last used name_counter from the file
def load_name_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as file:
            return int(file.read())
    return 1  # Default starting value if file doesn't exist

# Function to save the current name_counter to the file
def save_name_counter(counter):
    with open(COUNTER_FILE, 'w') as file:
        file.write(str(counter))

# Function to capture an image from the webcam
def capture_image(name_counter, cam):
    ret, frame = cam.read()
    if not ret:
        print("Error: Failed to capture image.")
        return None, name_counter

    img_path = os.path.join(SAVE_DIR, f"captured_image_{name_counter}.jpg")
    cv2.imwrite(img_path, frame)  # Save the captured image
    return img_path, name_counter + 1

# Function to detect and encode the face from the captured image
def encode_face(image_path):
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    
    if len(face_locations) == 0:
        speak("No face detected. Please try again!")
        print("No face detected in the image.")
        # Optionally delete the image since no face found
        if os.path.exists(image_path):
            os.remove(image_path)
        return None
    
    # Assume the first detected face is the primary one
    face_encoding = face_recognition.face_encodings(image, face_locations)[0]
    return face_encoding

# Function to check if the captured face is already in the database
def check_duplicate(face_encoding):
    cursor.execute("SELECT face_encoding FROM voters")
    rows = cursor.fetchall()
    
    for row in rows:
        db_encoding = np.frombuffer(row[0], dtype=np.float64)  # Decode stored face
        matches = face_recognition.compare_faces([db_encoding], face_encoding)
        if True in matches:
            speak("You have already voted. Access denied!")
            print("Duplicate face detected.")
            return True
    return False

# Function to store a new face in the database
def store_new_face(name, face_encoding):
    face_blob = face_encoding.tobytes()  # Convert numpy array to binary
    cursor.execute("INSERT INTO voters (name, face_encoding) VALUES (?, ?)", (name, face_blob))
    conn.commit()
    speak(f"Welcome, {name}! You can now vote.")
    print(f"Stored new face for {name}.")

# Function to handle the image capture and proceed with face recognition
def capture_and_process(cam, name_counter):
    img_path, updated_counter = capture_image(name_counter, cam)
    if img_path:
        face_encoding = encode_face(img_path)
        if face_encoding is not None:  # Check if face encoding is valid (not None)
            if check_duplicate(face_encoding):
                # No increment in counter if duplicate found
                return name_counter
            name = f"Person_{updated_counter - 1}"  # Name based on the counter
            store_new_face(name, face_encoding)
            print(f"{name} registered successfully.")
            voting_section()
            # Save updated counter after successful registration
            save_name_counter(updated_counter)
            return updated_counter
        else:
            # Face encoding failed, do not increment counter
            return name_counter
    return name_counter  # If no image captured, keep counter unchanged

# Candidate list for voting
candidates = {
    '1': "Packet PC",
    '2': "Online Chatbot Based Ticketing System",
    '3': "Food Waste Management and Donation",
    '4': "Organ Donor App",
    '5': "IoT Based Waste Management",
    '6': "Chatbot",
    '7': "AI Tool/ISL App",
    '8': "Chatbot for E-Tourist",
    '9': "Augmented Reality in Ornithology",
    '10': "AI for Student Wellbeing",
    '11': "Optimizing Productivity and Safety",
    '12': "Smart Dust Cart",
    '13': "AR Companion for Interactive Systems",
    '14': "Smart Cradle System",
    '15': "Gas Weight Monitoring",
    '16': "Smart Parking System",
    '17': "Automatic Rain Shutter",
    '18': "IoT Based Smart Rover",
    '19': "Smart Irrigation System for Turmeric Plants",
    '20': "RFID Based Smart Trolley",
    '21': "Crisis Compass",
    '22': "TrashCash",
    '23': "Learning About Extinct Species",
    '24': "E-Waste Management System",
    '25': "YogiSense",
    '26': "NutriHub",
    '27': "Vehicle Underbody Inspection System",
    '28': "CT Image Denoising",
}

# Function to show the voting section
def voting_section():
    # Create Tkinter window for voting
    root = tk.Tk()
    root.title("Vote for Candidate")
    root.geometry("800x600")  # Set the initial window size
    root.state("zoomed")  # Make the window full screen

    # Add a title
    title_label = tk.Label(root, text="Select a Candidate to Vote For", font=("Arial", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=20)

    # Display candidates in 3 columns
    for idx, (key, name) in enumerate(candidates.items()):
        row = (idx // 3) + 1  # Calculate row number
        col = idx % 3  # Calculate column number
        candidate_button = tk.Button(
            root,
            text=f"{key}. {name}",
            font=("Arial", 14),
            command=lambda key=key: [vote(key), root.destroy()]  # Close window after vote
        )
        candidate_button.grid(row=row, column=col, padx=20, pady=10, sticky="ew")

    root.mainloop()

# Function to register a vote for a candidate
def vote(candidate_key):
    candidate_name = candidates[candidate_key]

    # Check if the candidate already has votes in the database
    cursor.execute("SELECT vote_count FROM candidate_votes WHERE candidate_id = ?", (candidate_key,))
    row = cursor.fetchone()

    if row:
        # Candidate already exists, update the vote count
        new_vote_count = row[0] + 1
        cursor.execute("UPDATE candidate_votes SET vote_count = ? WHERE candidate_id = ?", (new_vote_count, candidate_key))
    else:
        # Candidate does not exist, insert a new record with vote count 1
        cursor.execute("INSERT INTO candidate_votes (candidate_id, vote_count) VALUES (?, ?)", (candidate_key, 1))

    conn.commit()
    print(f"You voted for {candidate_name}.")
    speak(f"You voted for {candidate_name}.")

# Function to ask the user if they want to reset the person counter
def ask_reset_counter():
    response = input("Do you want to reset the person count? (yes/no): ").strip().lower()
    if response == "yes":
        save_name_counter(1)  # Reset counter to 1
        print("Person count has been reset.")
        speak("Person count has been reset.")
    else:
        print("Person count reset canceled.")
        speak("Person count reset canceled.")

# Main function to run the application
def main():
    name_counter = load_name_counter()
    
    # Start the webcam feed
    cam = cv2.VideoCapture(0)
    
    print("Press 'S' to capture an image and register a new voter.")
    print("Press 'Q' to quit.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Error: Failed to grab frame.")
            break
        
        # Display the frame to the user
        cv2.imshow("Webcam Feed", frame)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):  # If 'S' is pressed, capture an image
            name_counter = capture_and_process(cam, name_counter)  # Update the counter properly

        if key == ord('q'):  # If 'Q' is pressed, ask for reset or quit
            ask_reset_counter()
            break
    
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
