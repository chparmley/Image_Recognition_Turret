// Define pin connections & motor's steps per revolution
const int powerx = 6;
const int powery = 7;

const int dirPin = 2;
const int stepPin = 3;
const int dirPin2 = 4;
const int stepPin2 = 5;

const int motor_m0 = 8;
const int motor_m1 = 9;
const int motor_m2 = 10;

const int motor1_m0 = 11;
const int motor1_m1 = 12;
const int motor1_m2 = 13;

int step_distance = 1;
int step_speed = 1000; // 60 for microstep, 
int step_resolution = 4;

int xaxis_pos = 1280/7.5;
int yaxis_pos = 720/7.5;

float lastTimerTime = millis();
int power_saver = 0;
static int last_received_xpos = 0;


void setup()
{
  pinMode(powerx, OUTPUT);
  pinMode(powery, OUTPUT);
  // Declare pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  
  pinMode(motor_m0, OUTPUT);
  pinMode(motor_m1, OUTPUT);
  pinMode(motor_m2, OUTPUT);
  
  pinMode(motor1_m0, OUTPUT);
  pinMode(motor1_m1, OUTPUT);
  pinMode(motor1_m2, OUTPUT);

  // Microstepping for motor 1
  PORTB &= ~_BV(PB0);
  PORTB &= ~_BV(PB1);
  PORTB &= ~_BV(PB2);
  
  // Microstepping for motor 2
  PORTB &= ~_BV(PB3);
  PORTB &= ~_BV(PB4);
  PORTB &= ~_BV(PB5);
  
  Serial.begin(19200); // 19200 is the rate of communication

}

int change_resolution(){          
  switch(step_resolution){
    case 1:
      // set to full step
      // Microstepping for motor 1
      PORTB &= ~_BV(PB0);
      PORTB &= ~_BV(PB1);
      PORTB &= ~_BV(PB2);
      // Microstepping for motor 2
      PORTB &= ~_BV(PB3);
      PORTB &= ~_BV(PB4);
      PORTB &= ~_BV(PB5);
      break;

     case 2:
      // set to 1/2 step
      // Microstepping for motor 1
      PORTB |= _BV(PB0);
      PORTB &= ~_BV(PB1);
      PORTB &= ~_BV(PB2);
      // Microstepping for motor 2
      PORTB |= _BV(PB3);
      PORTB &= ~_BV(PB4);
      PORTB &= ~_BV(PB5);
      break;

     case 4:
      // set to 1/4 step
      // Microstepping for motor 1
      PORTB &= ~_BV(PB0);
      PORTB |= _BV(PB1);
      PORTB &= ~_BV(PB2);

      // Microstepping for motor 2
      PORTB &= ~_BV(PB3);
      PORTB |= _BV(PB4);
      PORTB &= ~_BV(PB5);
      break;
     case 8:
      // set to 1/8 step
      // Microstepping for motor 1
      PORTB |= _BV(PB0);
      PORTB |= _BV(PB1);
      PORTB &= ~_BV(PB2);
      // Microstepping for motor 2
      PORTB |= _BV(PB3);
      PORTB |= _BV(PB4);
      PORTB &= ~_BV(PB5);
      break;

     case 16:
      // set to 1/16 step
      // Microstepping for motor 1
      PORTB &= ~_BV(PB0);
      PORTB &= ~_BV(PB1);
      PORTB |= _BV(PB2);
      // Microstepping for motor 2
      PORTB &= ~_BV(PB3);
      PORTB &= ~_BV(PB4);
      PORTB |= _BV(PB5);
      break;

     case 32:
      // set to 1/32 step
      // Microstepping for motor 1
      PORTB |= _BV(PB0);
      PORTB &= ~_BV(PB1);
      PORTB |= _BV(PB2);
      // Microstepping for motor 2
      PORTB |= _BV(PB3);
      PORTB &= ~_BV(PB4);
      PORTB |= _BV(PB5);
      break;
  }
  return 0;
}

void loop()
{
  static int v = 0; // value to be sent to the stepper (0-200)
  if (Serial.available()) {
    PORTD &= ~_BV(PD6);
    PORTD &= ~_BV(PD7);
    char ch = Serial.read(); // read in a character from the serial port and assign to ch
    switch(ch) { // switch based on the value of ch
      case '0'...'9': // if it's numeric
          v = v * 10 + ch - '0';
          break;

      // getting the microstep resolution from serial port. Possible values: 1,2,4,8,16,32
      case 'r':
        if (step_resolution != int(v)){              
          step_resolution = int(v);
          change_resolution();
        }
        v = 0;
        break;

      case 's':
        if (step_speed != int(v)){              
          step_speed = int(v);
          change_resolution();
        }
        v = 0;
        break;
        
      case 'x': // if it's x
        if (int(v) > xaxis_pos){
          PORTD &= ~_BV(PD2);
          // Spin motor
          PORTD |= _BV(PD3);
          delayMicroseconds(step_speed);
          PORTD &= ~_BV(PD3);
          delayMicroseconds(step_speed);
          xaxis_pos+=1;
        }
        else if (int(v) < xaxis_pos){
          PORTD |= _BV(PD2);
          // Spin motor
          PORTD |= _BV(PD3);
          delayMicroseconds(step_speed);
          PORTD &= ~_BV(PD3);
          delayMicroseconds(step_speed);
          xaxis_pos-=1;
         }
        v = 0;
        break;
    
      case 'y': // if it's y
        if (int(v) < yaxis_pos){
          PORTD |= _BV(PD4);
          // Spin motor
          PORTD |= _BV(PD5);
          delayMicroseconds(step_speed);
          PORTD &= ~_BV(PD5);
          delayMicroseconds(step_speed);
          yaxis_pos-=1;
          }
        else if (int(v) > yaxis_pos){
          PORTD &= ~_BV(PD4);
          // Spin motor
          PORTD |= _BV(PD5);
          delayMicroseconds(step_speed);
          PORTD &= ~_BV(PD5);
          delayMicroseconds(step_speed);
          yaxis_pos+=1;
         }
        v = 0;
        break;
    }
  }
}