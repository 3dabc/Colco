#ifndef CONFIG_H
#define CONFIG_H

// LoRaWAN credentials
#define DEV_EUI "YOUR_DEVICE_EUI"  // DevEUI
#define APP_EUI "YOUR_APP_EUI"    // AppEUI
#define APP_KEY "YOUR_APP_KEY"    // AppKey

// LoRaWAN region
#define LORAWAN_REGION "US915"    // AU915-928 for Columbia

// LoRaWAN settings
#define LORAWAN_ADR_ON true       // Adaptive Data Rate
#define LORAWAN_CONFIRMED_MSG false
#define LORAWAN_PORT 1

#endif