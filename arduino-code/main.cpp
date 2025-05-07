#include "LoRaWan_APP.h"
#include "Arduino.h"
#include <Wire.h>
#include <BH1750.h>

// LoRaWAN OTAA parameters
uint8_t devEui[] = { 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x06, 0x53, 0xC8 };
uint8_t appEui[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
uint8_t appKey[] = { 0x74, 0xD6, 0x6E, 0x63, 0x45, 0x82, 0x48, 0x27, 0xFE, 0xC5, 0xB7, 0x70, 0xBA, 0x2B, 0x50, 0x45 };

// LoRaWAN ABP parameters
uint8_t nwkSKey[] = { 0x15, 0xB1, 0xD0, 0xEF, 0xA4, 0x63, 0xDF, 0xBE, 0x3D, 0x11, 0x18, 0x1E, 0x1E, 0xC7, 0xDA, 0x85 };
uint8_t appSKey[] = { 0xD7, 0x2C, 0x78, 0x75, 0x8C, 0xDC, 0xCA, 0xBF, 0x55, 0xEE, 0x4A, 0x77, 0x8D, 0x16, 0xEF, 0x67 };
uint32_t devAddr = (uint32_t)0x007E6AE1;

// LoRaWAN settings
uint16_t userChannelsMask[6] = { 0x00FF, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000 };
LoRaMacRegion_t loraWanRegion = ACTIVE_REGION;
DeviceClass_t loraWanClass = CLASS_A;
uint32_t appTxDutyCycle = 15000;
bool overTheAirActivation = true;
bool loraWanAdr = true;
bool isTxConfirmed = true;
uint8_t appPort = 2;
uint8_t confirmedNbTrials = 4;

// BH1750 light sensor
BH1750 lightMeter1(0x23); // Default address
BH1750 lightMeter2(0x5C); // Alternate address
const int soilSensorPin = 16; // Soil moisture sensor pin (RX2)

// Prepare the payload
static void prepareTxFrame(uint8_t port) {
    int soilMoistureValue = analogRead(soilSensorPin);
    float lightIntensity = lightMeter1.readLightLevel();
    if (lightIntensity < 0) {
        lightIntensity = lightMeter2.readLightLevel();
    }

    uint16_t lightValue = (uint16_t)lightIntensity;

    appDataSize = 4;
    appData[0] = (soilMoistureValue >> 8) & 0xFF; // High byte of soil moisture
    appData[1] = soilMoistureValue & 0xFF;       // Low byte of soil moisture
    appData[2] = (lightValue >> 8) & 0xFF;       // High byte of light intensity
    appData[3] = lightValue & 0xFF;             // Low byte of light intensity
}

void setup() {
    Serial.begin(115200);

    Wire.begin(4, 15); // SDA, SCL
    Wire.setClock(100000);

    if (!lightMeter1.begin(BH1750::CONTINUOUS_HIGH_RES_MODE) && 
        !lightMeter2.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
        Serial.println("[BH1750] Device is not configured!");
    }
}

void loop() {
    switch (deviceState) {
        case DEVICE_STATE_INIT: {
#if (LORAWAN_DEVEUI_AUTO)
            LoRaWAN.generateDeveuiByChipID();
#endif
            LoRaWAN.init(loraWanClass, loraWanRegion);
            // LoRaWAN.setDefaultDR(3);
            break;
        }
        case DEVICE_STATE_JOIN: {
            LoRaWAN.join();
            break;
        }
        case DEVICE_STATE_SEND: {
            prepareTxFrame(appPort);
            LoRaWAN.send();
            deviceState = DEVICE_STATE_CYCLE;
            break;
        }
        case DEVICE_STATE_CYCLE: {
            txDutyCycleTime = appTxDutyCycle + randr(-APP_TX_DUTYCYCLE_RND, APP_TX_DUTYCYCLE_RND);
            LoRaWAN.cycle(txDutyCycleTime);
            deviceState = DEVICE_STATE_SLEEP;
            break;
        }
        case DEVICE_STATE_SLEEP: {
            LoRaWAN.sleep();
            break;
        }
        default: {
            deviceState = DEVICE_STATE_INIT;
            break;
        }
    }
}