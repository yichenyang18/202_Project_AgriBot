import serial
import time
import cv2
import torch  # For YOLOv5 model inference
import numpy as np
import RPi.GPIO as GPIO  # For stepper motor control (Jetson Nano GPIO)
from stepper import StepperMotor  # Assuming you're using a custom class for controlling stepper motors

# Connect to Arduino via serial (Assuming Arduino is connected to /dev/ttyACM0)
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Define stepper motor pins
motor_pins = [17, 18, 27, 22]  # Example GPIO pins for controlling stepper motor
laser_motor = StepperMotor(motor_pins)

# Initialize the camera (assuming using a USB webcam or the Jetson Nano camera)
cap = cv2.VideoCapture(0)

# Initialize GPIO for controlling movement (this can be extended to more motors)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define car movement commands
MOVE_FORWARD = b'F'
MOVE_BACKWARD = b'B'
TURN_LEFT = b'L'
TURN_RIGHT = b'R'
STOP = b'S'

# Load the pretrained YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='path_to_your_model.pt')  # Load your custom trained model

# Function to perform pest detection using YOLOv5
def detect_pest(frame):
    # Perform inference using YOLOv5
    results = model(frame)  # Pass the frame to the model
    detections = results.xywh[0].cpu().numpy()  # Get bounding boxes of detected pests
    pests = []
    
    for *xywh, conf, cls in detections:
        if conf > 0.5:  # Only consider detections with confidence > 50%
            pests.append(xywh)  # Store the pest's bounding box coordinates
    
    return pests

def move_car(command):
    """Send the movement command to the Arduino via serial."""
    arduino.write(command)
    time.sleep(1)

def stop_car():
    """Stop the car."""
    move_car(STOP)

def control_laser(pests):
    """Control the laser pointer using stepper motors to point at pests."""
    for pest in pests:
        x, y, w, h = pest  # Bounding box coordinates (xywh format)
        # Example: Move the laser motor based on the position of the pest (adjust as needed)
        laser_motor.move_to_position(x, y)  # Move laser to (x, y) position

# Main loop
try:
    while True:
        # Read image from camera
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            continue
        
        # Pest detection using YOLOv5
        pests = detect_pest(frame)
        
        if pests:
            # If pests are found, stop the car and control the laser
            stop_car()
            print("Pest detected, controlling laser.")
            control_laser(pests)
        else:
            # If no pests are found, continue driving the car
            print("No pest detected, moving forward.")
            move_car(MOVE_FORWARD)
        
        # Show the frame with detected pests (if any)
        cv2.imshow("Pest Detection", frame)
        
        # Exit on key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted.")

finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()
    arduino.close()
