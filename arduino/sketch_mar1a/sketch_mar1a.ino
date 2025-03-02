#include <Wire.h>
#include <BH1750.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Create an instance of the BH1750 sensor
BH1750 lightMeter;

// Define the analog input pin for the soil moisture sensor
const int soilSensorPin = 36; // GPIO36 (Ve pin)

// Define the OLED display width and height
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

// Create an instance of the SSD1306 display
Adafruit_SSD1306 oledDisplay(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Initialize I2C communication with custom pins
  Wire.begin(4, 5); // SDA on GPIO4, SCL on GPIO5
  
  // Initialize the BH1750 sensor with the correct I2C address
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("BH1750 sensor initialized");
  } else {
    Serial.println("Error initializing BH1750 sensor");
  }

  // Initialize the OLED display
  if (!oledDisplay.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Replace 0x3C with the correct address if different
    Serial.println("SSD1306 allocation failed");
    for (;;);
  }
  oledDisplay.display();
  delay(2000); // Pause for 2 seconds
  oledDisplay.clearDisplay();
}

void loop() {
  // Read light intensity from the BH1750 sensor
  float lux = lightMeter.readLightLevel();

  // Read the analog value from the soil moisture sensor
  int soilMoistureValue = analogRead(soilSensorPin);

  // Print the light intensity to the Serial Monitor
  Serial.print("Light Intensity: ");
  Serial.print(lux);
  Serial.println(" lx");

  // Print the soil moisture value to the Serial Monitor
  Serial.print("Soil Moisture Value: ");
  Serial.println(soilMoistureValue);

  // Display the values on the OLED
  oledDisplay.clearDisplay();
  oledDisplay.setTextSize(1);
  oledDisplay.setTextColor(SSD1306_WHITE);
  oledDisplay.setCursor(0, 0);
  oledDisplay.print("Light Intensity: ");
  oledDisplay.print(lux);
  oledDisplay.println(" lx");
  oledDisplay.print("Soil Moisture: ");
  oledDisplay.println(soilMoistureValue);
  oledDisplay.display();

  // Wait for a second before reading again
  delay(1000);
}