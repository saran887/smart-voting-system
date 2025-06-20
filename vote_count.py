import sqlite3

# Candidate list for voting
candidates = {
    '1': "Packet PC",
    '2': "Online Chatbot Based Ticketing System",
    '3': "Food Waste Management and Donation",
    '4': "Organ Donor App",
    '5': "IoT Based Waste Management",
    '6': "Chatbot",
    '7': "AI Tool/ISL App",
    '8': "Chatbot for E-Tourist",1
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

# Function to check and display the vote counts for all candidates
def check_votes():
    conn = sqlite3.connect("voter_faces.db")
    cursor = conn.cursor()
    cursor.execute("SELECT candidate_id, vote_count FROM candidate_votes")
    rows = cursor.fetchall()

    if not rows:
        print("No votes recorded yet.")
    else:
        print("Vote Counts:")
        for row in rows:
            candidate_id = row[0]
            vote_count = row[1]
            candidate_name = candidates.get(candidate_id, "Unknown Candidate")
            print(f"{candidate_id}. {candidate_name}: {vote_count} votes")
    
    conn.close()

# Function to delete all votes for all candidates with confirmation
def delete_all_votes():
    # Ask for confirmation
    confirm = input("Are you sure you want to delete all votes for all candidates? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Deletion canceled.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect("voter_faces.db")
    cursor = conn.cursor()

    try:
        # Reset the vote counts for all candidates to 0
        cursor.execute("UPDATE candidate_votes SET vote_count = 0")
        conn.commit()
        print("All votes have been deleted for all candidates.")

        # Debug: Show updated table
        cursor.execute("SELECT * FROM candidate_votes")
        print("\nUpdated Vote Counts:")
        rows = cursor.fetchall()
        for row in rows:
            candidate_id = row[0]
            vote_count = row[1]
            candidate_name = candidates.get(candidate_id, "Unknown Candidate")
            print(f"{candidate_id}. {candidate_name}: {vote_count} votes")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

# Main function to run the code
def main():
    while True:
        print("\nMenu:")
        print("1. View Vote Counts")
        print("2. Delete All Votes")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            check_votes()
        elif choice == '2':
            delete_all_votes()
        elif choice == '3':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
