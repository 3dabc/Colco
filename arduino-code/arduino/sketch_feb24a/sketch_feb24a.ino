// Define the analog input pin
const int soilSensorPin = Ve; // Ve pin

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
}

void loop() {
  // Read the analog value from the soil sensor
  int sensorValue = analogRead(soilSensorPin);

  // Print the sensor value to the Serial Monitor
  Serial.print("Soil Moisture Value: ");
  Serial.println(sensorValue);

  // Wait for a second before reading again
  delay(1000);
}