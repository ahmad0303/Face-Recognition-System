# Face Recognition System

This repository contains code for a face recognition system implemented using Python and various libraries such as OpenCV, face_recognition, cvzone, firebase_admin, and dotenv.

## Installation

To run this project locally, follow these steps:

1. Clone the repository to your local machine using the following command:
   ```bash
   git clone https://github.com/ahmad0303/face-recognition-system.git
   ```

2. Navigate to the project directory:
   ```bash
   cd face-recognition-system
   ```

3. Install the required Python packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the Firebase credentials and environment variables:
   - Create a Firebase project and download the service account key (`serviceAccountKey.json`).
   - Set the `databaseURL` and `storageBucket` environment variables in a `.env` file.
     ```plaintext
     databaseURL=your_database_url
     storageBucket=your_storage_bucket
     ```

5. Run the main Python script:
   ```bash
   python main.py
   ```

## Usage

This face recognition system performs the following tasks:

1. **Face Detection:** It captures frames from the webcam and detects faces using the `face_recognition` library.

2. **Face Recognition:** It compares the detected faces with pre-encoded faces stored in `EncodeFile.p` to recognize known faces.

3. **Firebase Integration:** It integrates with Firebase to fetch student information and update check-in details.

4. **Mode Switching:** The system switches between different modes (e.g., normal mode, student information mode) based on face detection and recognition results.

## File Structure

- `face_recognition_system.py`: The main Python script that implements the face recognition system.
- `EncodeFile.p`: Pickle file containing pre-encoded face data.
- `serviceAccountKey.json`: Firebase service account key for authentication.
- `Resources/`: Directory containing background images and mode images used in the system.


## Acknowledgements

- [OpenCV](https://opencv.org/)
- [face_recognition](https://github.com/ageitgey/face_recognition)
- [cvzone](https://github.com/cvzone/cvzone)
- [Firebase](https://firebase.google.com/)
- [dotenv](https://pypi.org/project/python-dotenv/)

