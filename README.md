Facial Recognition Attendance System with Live Dashboard
This project is a real-time facial recognition attendance system built with Python. It includes:
Camera-based face recognition using OpenCV and LBPHFaceRecognizer
Automatic attendance logging to a CSV file (once per person per day)
Modern, live dashboard built with Dash (Plotly) to visualize attendance
The system is ideal for classrooms, offices, or any environment where automated attendance tracking is needed.
Features
Detects faces in real-time using your webcam
Marks attendance automatically, once per person per day
Stores attendance data in a CSV file (attendance.csv)
Live, visually appealing dashboard shows:
All attendance records
Today’s attendance
Summary bar chart of total days present
Dashboard refreshes automatically every few seconds
Modern, card-style layout with color highlights

Project Structure

project/

│
├─ dataset/ Folder containing training images (one folder per person)
├─ trainer.yml Trained LBPH model 
├─ labels.csv Mapping of label IDs to names 
├─ attendance.csv Attendance log (
├─ attendance_opencv.py Real-time camera face recognition & attendance script
├─ dashboard_dash.py Modern attendance dashboard (Dash/Plotly)
├─ README.md This file

Requirements

Python 3.8 or higher

Packages:

pip install opencv-python opencv-contrib-python pandas dash

Optional (if using virtual environment):

python -m venv .venv
source .venv/bin/activate (Linux/macOS)
.venv\Scripts\activate (Windows)
pip install -r requirements.txt

How to Use

Train the recognizer
Put each person's images in the dataset folder, with one folder per person
Run attendance_opencv.py once — it will automatically train the model and save trainer.yml
Run the attendance system
python attendance_opencv.py
The camera will start
Detected faces will be marked in attendance.csv automatically
Press q to quit the camera window (optional)
Run the live dashboard
python dashboard_dash.py
The dashboard opens in your browser at http://127.0.0.1:8050/
Updates automatically every 5 seconds to show live attendance


Notes
Attendance is marked once per person per day
Dashboard reads directly from attendance.csv, so it works even if the camera system is running separately
Ensure good lighting for more accurate face recognition
License
This project is licensed under the MIT License.
Feel free to modify and use it for personal or educational purposes
Acknowledgements
OpenCV for face recognition
Dash/Plotly for dashboard visualization

Python community for examples and tutorials
