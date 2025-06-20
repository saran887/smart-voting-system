# import cv2
import os
import sqlite3

# Directory where the images are saved
SAVE_DIR = "saved_images"

# SQLite Database setup
conn = sqlite3.connect("voter_faces.db")
cursor = conn.cursor()

# Function to create the vote_counts table if it doesn't exist
def create_vote_counts_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vote_counts (
        candidate_id TEXT PRIMARY KEY,
        vote_count INTEGER
    )
    ''')
    conn.commit()

# Function to view all saved images
def view_saved_images():
    # Check if the directory exists
    if not os.path.exists(SAVE_DIR):
        print("No saved images directory found.")
        return

    # Get the list of all image files in the directory
    image_files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.jpg') or f.endswith('.png')]

    # Check if there are no image files
    if not image_files:
        print("No images found in the saved directory.")
        return

    # Display each image
    for image_file in image_files:
        image_path = os.path.join(SAVE_DIR, image_file)
        image = cv2.imread(image_path)  # Read the image
        cv2.imshow(f"Saved Image: {image_file}", image)  # Display the image
        cv2.waitKey(0)  # Wait until any key is pressed

    # Close all windows after displaying all images
    cv2.destroyAllWindows()

# Function to delete a specific photo
def delete_specific_photo():
    # Get the list of all image files in the directory
    image_files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.jpg') or f.endswith('.png')]

    if not image_files:
        print("No images found in the saved directory.")
        return

    print("Saved Images:")
    for idx, image_file in enumerate(image_files):
        print(f"{idx + 1}. {image_file}")

    try:
        # Ask the user to select an image to delete
        choice = int(input("Enter the number of the image you want to delete: ")) - 1

        if choice < 0 or choice >= len(image_files):
            print("Invalid choice.")
            return

        # Delete the selected image from the directory
        selected_image = image_files[choice]
        image_path = os.path.join(SAVE_DIR, selected_image)
        os.remove(image_path)
        print(f"Deleted {selected_image} from the directory.")

        # Delete the corresponding entry in the database
        name = os.path.splitext(selected_image)[0]  # Strip file extension to get name
        cursor.execute("DELETE FROM voters WHERE name = ?", (name,))
        conn.commit()
        print(f"Deleted {name} from the database.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to delete all photos
def delete_all_photos():
    # Confirm the user's intent
    confirm = input("Are you sure you want to delete all images? (yes/no): ").strip().lower()

    if confirm == "yes":
        # Delete all images in the directory
        for file in os.listdir(SAVE_DIR):
            if file.endswith('.jpg') or file.endswith('.png'):
                os.remove(os.path.join(SAVE_DIR, file))

        print("Deleted all images from the directory.")

        # Delete all records from the database
        cursor.execute("DELETE FROM voters")
        conn.commit()
        print("Deleted all records from the database.")

    else:
        print("Deletion cancelled.")

# Main function to provide options
def main():
    # Ensure the vote_counts table exists
    create_vote_counts_table()

    while True:
        print("\nOptions:")
        print("1. View Saved Images")
        print("2. Delete a Specific Image")
        print("3. Delete All Images")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_saved_images()
        elif choice == "2":
            delete_specific_photo()
        elif choice == "3":
            delete_all_photos()
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
