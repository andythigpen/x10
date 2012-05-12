#include <x10.h>
#include <x10constants.h>

#define ZC_PIN       2
#define TRANS_PIN    4
#define RECV_PIN     3
#define REPEAT_TIMES 1

#define HOUSE_CODE_STATE 1
#define UNIT_CODE_STATE  2
#define REPEAT_STATE     3
#define ACTION_STATE     4
#define INITIAL_STATE    HOUSE_CODE_STATE

const int ledPin = 13;
int ledState = LOW;
long previousMillis = 0;
long interval = 500;
int incomingByte = 0;
int commandState = HOUSE_CODE_STATE;

x10 myHouse = x10(ZC_PIN, TRANS_PIN, RECV_PIN);
int currentHouseCode = 0;
int currentUnitCode = 0;
int currentAction = 0;
int currentRepeatTimes = 0;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

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
    case '[': command = ON; break;
    case ']': command = OFF; break;
    case '+': command = BRIGHT; break;
    case '-': command = DIM; break;
    case '{': command = ALL_LIGHTS_ON; break;
    case '}': command = ALL_LIGHTS_OFF; break;
  }
  repeatTimes = currentRepeatTimes - 48;

  myHouse.write(houseCode, unitCode, REPEAT_TIMES);
  myHouse.write(houseCode, command, repeatTimes);
}

void handleCommand(int command) {
  switch (commandState) {
    case HOUSE_CODE_STATE:
      if (command == '?') {
        Serial.write("Still alive!\n");
        break;
      }
      if (command < 'A' || command > 'F') {
        Serial.write("Unrecognized house code.\n");
        commandState = INITIAL_STATE;
        break;
      }
      currentHouseCode = command;
      commandState = UNIT_CODE_STATE;
      break;
    case UNIT_CODE_STATE:
      if (! ((command >= '1' && command <= '9')
          || (command >= 'a' && command <= 'g'))) {
        Serial.write("Unrecognized unit code.\n");
        commandState = INITIAL_STATE;
        break;
      }
      currentUnitCode = command;
      commandState = REPEAT_STATE;
      break;
    case REPEAT_STATE:
      if (command < '1' || command > '9') {
        Serial.write("Unrecognized repeat times.\n");
        commandState = INITIAL_STATE;
        break;
      }
      currentRepeatTimes = command;
      commandState = ACTION_STATE;
      break;
    case ACTION_STATE:
      if (! (command == '+' || command == '-'
          || command == '[' || command == ']'
          || command == '{' || command == '}')) {
        Serial.write("Unrecognized action code.\n");
        commandState = INITIAL_STATE;
        break;
      }
      currentAction = command;
      sendX10Command();
      Serial.write("Received command.\n");
      commandState = INITIAL_STATE;
      break;
    default:
      Serial.write("Unknown state.\n");
      commandState = INITIAL_STATE;
      break;
  }
}

/*void handleCommand(int command) {
  switch (command) {
    case 'A':
    case 'B':
    case 'C':
    case 'D':
    case 'E':
    case 'F':
      currentHouseCode = command;
      Serial.write("Current House/Unit code is ");
      break;
    case '1':
    case '2':
    case '3':
    case '4':
    case '5':
    case '6':
    case '7':
    case '8':
    case '9':
    case 'a':
    case 'b':
    case 'c':
    case 'd':
    case 'e':
    case 'f':
    case '0':
      currentUnitCode = command;
      Serial.write("Current House/Unit code is ");
      break;
    case '?':
      Serial.write("Current House/Unit code is ");
      break;
    case '[':
      sendX10Command(ON);
      Serial.write("Turning on ");
      break;
    case ']':
      sendX10Command(OFF);
      Serial.write("Turning off ");
      break;
    case '+':
      sendX10Command(BRIGHT);
      Serial.write("Brightening ");
      break;
    case '-':
      sendX10Command(DIM);
      Serial.write("Dimming ");
      break;
    default:
      Serial.print("Unrecognized command\n");
      return;
  }

  Serial.write(currentHouseCode);
  Serial.write("-");
  Serial.write(currentUnitCode);
  Serial.write(".\n");
}*/

void loop() {

  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    //Serial.print("You wrote: ");
    //Serial.write(incomingByte);
    //Serial.print('\n');
    handleCommand(incomingByte);
  }

  if (myHouse.received()) {
    myHouse.debug();
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

    //Serial.write("Still Alive\n");
  }
}
