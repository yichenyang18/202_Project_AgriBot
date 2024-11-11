#include <IRremote.h>

// Define motor control pins
int motor1Pin1 = 3; // Motor 1 forward
int motor1Pin2 = 4; // Motor 1 reverse
int motor2Pin1 = 5; // Motor 2 forward
int motor2Pin2 = 6; // Motor 2 reverse

// Set up IR receiver pin
int recv_pin = 2;  // IR receiver connected to pin 2
IRrecv irrecv(recv_pin);
decode_results results;

void setup()
{
  // Start serial communication
  Serial.begin(9600);
  
  // Initialize motor pins
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  
  // Enable IR receiver
  irrecv.enableIRIn();
}

void loop() {
  if (irrecv.decode(&results)) {
    long int decCode = results.value;  // Get the decoded value
    Serial.println(decCode);           // Print the decoded value for debugging
    
    // Check the IR code and move accordingly
    if (decCode == 0xFF629D) { // Forward
      moveForward();
    }
    else if (decCode == 0xFF22DD) { // Backward
      moveBackward();
    }
    else if (decCode == 0xFFC23D) { // Left
      turnLeft();
    }
    else if (decCode == 0xFF02FD) { // Right
      turnRight();
    }
    else if (decCode == 0xFFFFFFFF) { // Stop
      stopCar();
    }
    
    irrecv.resume(); // Receive the next value
  }
}

// Function to move the car forward
void moveForward() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

// Function to move the car backward
void moveBackward() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, HIGH);
}

// Function to turn the car left
void turnLeft() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, HIGH);
  digitalWrite(motor2Pin2, LOW);
}

// Function to turn the car right
void turnRight() {
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
}

// Function to stop the car
void stopCar() {
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  digitalWrite(motor2Pin1, LOW);
  digitalWrite(motor2Pin2, LOW);
}
