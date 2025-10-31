import os
from datetime import datetime

def create_daily_folders(base_path):
    # Get today's date in format "23-September"
    today = datetime.now().strftime("%d-%B")
    today_path = os.path.join(base_path, today)

    # Create main date folder
    if not os.path.exists(today_path):
        os.makedirs(today_path)
        print(f"Created folder: {today_path}")
    else:
        print(f"Folder already exists: {today_path}")

    # Subfolders
    subfolders = ["Daily_Activity", "Tasks"]

    for folder in subfolders:
        folder_path = os.path.join(today_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created subfolder: {folder_path}")
        else:
            print(f"Subfolder already exists: {folder_path}")

if __name__ == "__main__":
    # Change this to where you want the folders created
    base_path = r"C:\Users\Aniket\OneDrive\Desktop\fsai\js totorails"
    create_daily_folders(base_path)
