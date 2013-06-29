#include <x10.h>
#include <x10constants.h>

// temperature sensor
#include <Wire.h>
#include <DS1631.h>

// X10 pin assignments
#define ZC_PIN       2
#define TRANS_PIN    6
#define RECV_PIN     4

// Command state-machine
#define COMMAND_STATE    0
#define HOUSE_CODE_STATE 1
#define UNIT_CODE_STATE  2
#define REPEAT_STATE     3
#define ACTION_STATE     4
#define INITIAL_STATE    COMMAND_STATE

// Commands
#define CMD_LIGHT_QUERY     's'
#define CMD_TEMP_QUERY      't'
#define CMD_X10             'x'
#define CMD_HELP            '?'

// X10 actions
#define X10_ON      '|'
#define X10_OFF     'O'
#define X10_BRIGHT  '+'
#define X10_DIM     '-'

// Pins
const int ledPin = 13;
const int analogInPin = A0;

// LED heartbeat
int ledState = LOW;
long previousMillis = 0;
long interval = 500;

// Serial commands & state-machine
int incomingByte = 0;
int commandState = INITIAL_STATE;

// X10
x10 myHouse = x10(ZC_PIN, TRANS_PIN, RECV_PIN);
int currentHouseCode = 0;
int currentUnitCode = 0;
int currentAction = 0;
int currentRepeatTimes = 0;

// Photoresistor analog input
int sensorValue = 0;

// initialize temperature sensor with bus address of 0 (A0-2 tied to ground)
DS1631 temperature(0);

void sendX10Command() {
  int houseCode, unitCode, command, repeatTimes;
  switch (currentHouseCode) {
    case 'A': houseCode = HOUSE_A; break;
    case 'B': houseCode = HOUSE_B; break;
    case 'C': houseCode = HOUSE_C; break;
    case 'D': houseCode = HOUSE_D; break;
    case 'E': houseCode = HOUSE_E; break;
    case 'F': houseCode = HOUSE_F; break;
  }
  switch (currentUnitCode) {
    case '1': unitCode = UNIT_1; break;
    case '2': unitCode = UNIT_2; break;
    case '3': unitCode = UNIT_3; break;
    case '4': unitCode = UNIT_4; break;
    case '5': unitCode = UNIT_5; break;
    case '6': unitCode = UNIT_6; break;
    case '7': unitCode = UNIT_7; break;
    case '8': unitCode = UNIT_8; break;
    case '9': unitCode = UNIT_9; break;
    case 'a': unitCode = UNIT_10; break;
    case 'b': unitCode = UNIT_11; break;
    case 'c': unitCode = UNIT_12; break;
    case 'd': unitCode = UNIT_13; break;
    case 'e': unitCode = UNIT_14; break;
    case 'f': unitCode = UNIT_15; break;
    case 'g': unitCode = UNIT_16; break;
  }
  switch (currentAction) {
    case X10_ON:     command = ON; break;
    case X10_OFF:    command = OFF; break;
    case X10_BRIGHT: command = BRIGHT; break;
    case X10_DIM:    command = DIM; break;
  }
  // convert from ascii to byte
  repeatTimes = currentRepeatTimes - 48;

  myHouse.write(houseCode, unitCode, 1);
  myHouse.write(houseCode, command, repeatTimes);
}

void printCurrentState() {
    Serial.print(commandState);
    Serial.print(" House:");
    Serial.write(currentHouseCode);
    Serial.print(" Unit:");
    Serial.write(currentUnitCode);
    Serial.print(" Action:");
    Serial.write(currentAction);
    Serial.print(" Repeat:");
    Serial.write(currentRepeatTimes);
    Serial.print("\r\n");
}

void handleCommand(int command) {
  switch (commandState) {
    case COMMAND_STATE:
      if (command == CMD_LIGHT_QUERY) {
        sensorValue = analogRead(analogInPin);
        Serial.println(map(sensorValue, 0, 1023, 0, 255));
      }
      else if (command == CMD_TEMP_QUERY) {
        // get temperature sensor value
        float temp = temperature.readTempOneShot();
        Serial.println(temp, 4);
      }
      else if (command == CMD_X10) {
        commandState = HOUSE_CODE_STATE;
      }
      else if (command == CMD_HELP) {
        Serial.println("Lightbot 5000 reporting for duty!");
        Serial.println("Current state: ");
        printCurrentState();
        Serial.print(CMD_LIGHT_QUERY);
        Serial.println(": returns current light sensor value");
        Serial.print(CMD_X10);
        Serial.println(": send an X10 command, format:");
        Serial.println("   [house][unit][repeat][action]");
        Serial.print(CMD_HELP);
        Serial.println(": this help");
        break;
      }
      break;

    case HOUSE_CODE_STATE:
      if (command < 'A' || command > 'F') {
        Serial.println("Unrecognized house code.");
        printCurrentState();
        commandState = INITIAL_STATE;
        break;
      }
      currentHouseCode = command;
      commandState = UNIT_CODE_STATE;
      break;

    case UNIT_CODE_STATE:
      if (! ((command >= '1' && command <= '9')
          || (command >= 'a' && command <= 'g'))) {
        Serial.println("Unrecognized unit code.");
        printCurrentState();
        commandState = INITIAL_STATE;
        break;
      }
      currentUnitCode = command;
      commandState = REPEAT_STATE;
      break;

    case REPEAT_STATE:
      if (command < '1' || command > '9') {
        Serial.println("Unrecognized repeat times.");
        printCurrentState();
        commandState = INITIAL_STATE;
        break;
      }
      currentRepeatTimes = command;
      commandState = ACTION_STATE;
      break;

    case ACTION_STATE:
      if (! (command == X10_ON ||
             command == X10_OFF ||
             command == X10_BRIGHT ||
             command == X10_DIM)) {
        Serial.println("Unrecognized action code.");
        printCurrentState();
        commandState = INITIAL_STATE;
        break;
      }
      currentAction = command;
      sendX10Command();
      Serial.print("Sent X10 command: ");
      printCurrentState();
      commandState = INITIAL_STATE;
      break;

    default:
      Serial.println("Unknown state.");
      printCurrentState();
      commandState = INITIAL_STATE;
      break;
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);

  // join I2C bus for temperature sensor
  Wire.begin();
  //int config = temperature.readConfig();
  //Serial.print("Temperature settings before: ");
  //Serial.println(config, BIN);

  // set temperature sensor to 12-bit, 1 shot mode
  temperature.writeConfig(13);

  //config = temperature.readConfig();
  //Serial.print("Temperature settings after: ");
  //Serial.println(config, BIN);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    handleCommand(incomingByte);
  }

  if (myHouse.received()) {
    //myHouse.debug();
    myHouse.reset();
  }

  if (millis() - previousMillis > interval) {
    previousMillis = millis();

    if (ledState == LOW) {
      ledState = HIGH;
    }
    else {
      ledState = LOW;
    }

    digitalWrite(ledPin, ledState);
  }
}
