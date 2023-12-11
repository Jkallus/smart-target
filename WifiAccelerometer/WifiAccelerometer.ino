/*
 *  This sketch sends random data over UDP on a ESP32 device
 *
 */
#include <WiFi.h>
#include <WiFiUdp.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// WiFi network name and password:
const char * networkName = "Josh's Wi-Fi Network";
const char * networkPswd = "FFFFFFFFFF";

Adafruit_MPU6050 mpu_bl;
Adafruit_MPU6050 mpu_tr;

//IP address to send UDP data to:
// either use the ip address of the server or 
// a network broadcast address
const char * udpAddress = "192.168.8.19";
const int udpPort = 65238;

//Are we currently connected?
boolean connected = false;

//The udp library class
WiFiUDP udp;

void setup(){
  // Initilize hardware serial:
  Serial.begin(115200);

  if (!mpu_bl.begin(0x68)) {
    Serial.println("Failed to find Bottom Left MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("Bottom Left MPU6050 Found!");

  if (!mpu_tr.begin(0x69)) {
    Serial.println("Failed to find Top Right MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("Top Right MPU6050 Found!");


  mpu_bl.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu_bl.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu_bl.setFilterBandwidth(MPU6050_BAND_260_HZ);

  mpu_tr.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu_tr.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu_tr.setFilterBandwidth(MPU6050_BAND_260_HZ);

  //Connect to the WiFi network
  connectToWiFi(networkName, networkPswd);
}

void loop(){
  //only send data when connected
  if(connected){
    //Send a packet
    udp.beginPacket(udpAddress,udpPort);
    sensors_event_t a_bl, g_bl, temp_bl;
    sensors_event_t a_tr, g_tr, temp_tr;
    mpu_bl.getEvent(&a_bl, &g_bl, &temp_bl);
    mpu_tr.getEvent(&a_tr, &g_tr, &temp_tr);

    printf("BottomLeftAZ:%f,TopRightAZ:%f\n\r", a_bl.acceleration.z, a_tr.acceleration.z);
    
    udp.printf("blax:%f,blay:%f,blaz:%f,trax:%f,tray:%f,traz:%f,ms:%d", a_bl.acceleration.x, a_bl.acceleration.y, a_bl.acceleration.z, a_tr.acceleration.x, a_tr.acceleration.y, a_tr.acceleration.z, millis());
    //udp.printf("ms since boot: %d", millis());
    udp.endPacket();
  }
  //Wait for 1 second
  //delay(10);
}

void connectToWiFi(const char * ssid, const char * pwd){
  Serial.println("Connecting to WiFi network: " + String(ssid));

  // delete old config
  WiFi.disconnect(true);
  //register event handler
  WiFi.onEvent(WiFiEvent);
  
  //Initiate connection
  WiFi.begin(ssid, pwd);

  Serial.println("Waiting for WIFI connection...");
}

//wifi event handler
void WiFiEvent(WiFiEvent_t event){
    switch(event) {
      case ARDUINO_EVENT_WIFI_STA_GOT_IP:
          //When connected set 
          Serial.print("WiFi connected! IP address: ");
          Serial.println(WiFi.localIP());  
          //initializes the UDP state
          //This initializes the transfer buffer
          udp.begin(WiFi.localIP(),udpPort);
          connected = true;
          break;
      case ARDUINO_EVENT_WIFI_STA_DISCONNECTED:
          Serial.println("WiFi lost connection");
          connected = false;
          break;
      default: break;
    }
}
