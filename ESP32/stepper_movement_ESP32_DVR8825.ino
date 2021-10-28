// X axis Motor pins
const int enable_x = 34;
const int dir_pin = 32;
const int step_pin = 33;
const int motor_m0 = 25;
const int motor_m1 = 26;
const int motor_m2 = 27;

// Y axis Motor pins
const int enable_y = 23;
const int dir_pin2 = 22;
const int step_pin2 = 21;
const int motor1_m0 = 19;
const int motor1_m1 = 18;
const int motor1_m2 = 5;


int step_speed = 60; // 60 for microstep, 
int step_resolution = 32;


void setup()
{  
  // Declare pins as Outputs
  pinMode(enable_x, OUTPUT);
  pinMode(enable_y, OUTPUT);
  
  pinMode(step_pin, OUTPUT);
  pinMode(dir_pin, OUTPUT);
  pinMode(step_pin2, OUTPUT);
  pinMode(dir_pin2, OUTPUT);
  
  pinMode(motor_m0, OUTPUT);
  pinMode(motor_m1, OUTPUT);
  pinMode(motor_m2, OUTPUT);
  
  pinMode(motor1_m0, OUTPUT);
  pinMode(motor1_m1, OUTPUT);
  pinMode(motor1_m2, OUTPUT);

  // Microstepping for motor 1
  digitalWrite(motor_m0, LOW);
  digitalWrite(motor_m1, LOW);
  digitalWrite(motor_m2, LOW);
  
  // Microstepping for motor 2
  digitalWrite(motor1_m0, LOW);
  digitalWrite(motor1_m1, LOW);
  digitalWrite(motor1_m2, LOW);

  // Turn on power to motors
  digitalWrite(enable_x, LOW);
  digitalWrite(enable_y, LOW);
    
  Serial.begin(19200); // 19200 is the rate of communication

}

int change_resolution(){          
  switch(step_resolution){
    case 1:
      // set to full step
      // Microstepping for motor 1
      digitalWrite(motor_m0, LOW);
      digitalWrite(motor_m1, LOW);
      digitalWrite(motor_m2, LOW);
      // Microstepping for motor 2
      digitalWrite(motor1_m0, LOW);
      digitalWrite(motor1_m1, LOW);
      digitalWrite(motor1_m2, LOW);
      break;

     case 2:
      // set to 1/2 step
      // Microstepping for motor 1
      digitalWrite(motor_m0, HIGH);
      digitalWrite(motor_m1, LOW);
      digitalWrite(motor_m2, LOW);
      // Microstepping for motor 2
      digitalWrite(motor1_m0, HIGH);
      digitalWrite(motor1_m1, LOW);
      digitalWrite(motor1_m2, LOW);
      break;

     case 4:
      // set to 1/4 step
      // Microstepping for motor 1
      digitalWrite(motor_m0, LOW);
      digitalWrite(motor_m1, HIGH);
      digitalWrite(motor_m2, LOW);
      // Microstepping for motor 2
      digitalWrite(motor1_m0, LOW);
      digitalWrite(motor1_m1, HIGH);
      digitalWrite(motor1_m2, LOW);
      break;
      
     case 8:
      // set to 1/8 step
      // Microstepping for motor 1
      digitalWrite(motor_m0, HIGH);
      digitalWrite(motor_m1, HIGH);
      digitalWrite(motor_m2, LOW);
      // Microstepping for motor 2
      digitalWrite(motor1_m0, HIGH);
      digitalWrite(motor1_m1, HIGH);
      digitalWrite(motor1_m2, LOW);
      break;

     case 16:
      // set to 1/16 step
      // Microstepping for motor 1
      digitalWrite(motor_m0, LOW);
      digitalWrite(motor_m1, LOW);
      digitalWrite(motor_m2, HIGH);
      // Microstepping for motor 2
      digitalWrite(motor1_m0, LOW);
      digitalWrite(motor1_m1, LOW);
      digitalWrite(motor1_m2, HIGH);
      break;

     case 32:
      // set to 1/32 step
      // Microstepping for motor 1
      digitalWrite(motor_m0, HIGH);
      digitalWrite(motor_m1, LOW);
      digitalWrite(motor_m2, HIGH);
      // Microstepping for motor 2
      digitalWrite(motor1_m0, HIGH);
      digitalWrite(motor1_m1, LOW);
      digitalWrite(motor1_m2, HIGH);
      break;
  }
  return 0;
}

void loop()
{
  static int v = 0; // value to be sent to the stepper (0-200)
  if (Serial.available()) {
    change_resolution();
    char ch = Serial.read(); // read in a character from the serial port and assign to ch
    switch(ch) { // switch based on the value of ch

      case 'r': // if it's r
          digitalWrite(dir_pin, LOW);
          // Spin motor
          digitalWrite(step_pin, HIGH);
          delayMicroseconds(step_speed);
          digitalWrite(step_pin, LOW);
          delayMicroseconds(step_speed);
          v = 0;
          break;
       
       case 'l':
          digitalWrite(dir_pin, HIGH);
          // Spin motor
          digitalWrite(step_pin, HIGH);
          delayMicroseconds(step_speed);
          digitalWrite(step_pin, LOW);
          delayMicroseconds(step_speed);
          v = 0;
          break;
    
      case 'u': // if it's u
          digitalWrite(dir_pin2, HIGH);
          // Spin motor
          digitalWrite(step_pin2, HIGH);
          delayMicroseconds(step_speed);
          digitalWrite(step_pin2, LOW);
          delayMicroseconds(step_speed);
          v = 0;
          break;
          
      case 'd':
          digitalWrite(dir_pin2, LOW);
          // Spin motor
          digitalWrite(step_pin2, HIGH);
          delayMicroseconds(step_speed);
          digitalWrite(step_pin2, LOW);
          delayMicroseconds(step_speed);
          v = 0;
          break;
    }
  }
}