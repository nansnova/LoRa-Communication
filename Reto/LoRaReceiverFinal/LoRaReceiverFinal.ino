#include <Wire.h>                                                   //Import the required libraries
#include <LoRa.h>
#include "boards.h"
#include <WiFiMulti_Generic.h>
WiFiMulti_Generic wifiMulti;

#include <InfluxDbClient.h>
#include <InfluxDbCloud.h>

#define WIFI_SSID "TP-Link_89CA"                                                                                  //Network Name
#define WIFI_PASSWORD "47626096"                                                                                  //Network Password
#define INFLUXDB_URL "http://192.168.1.70:8086"                                                                  //InfluxDB v2 server url, e.g. https://eu-central-1-1.aws.cloud2.influxdata.com (Use: InfluxDB UI -> Load Data -> Client Libraries)
#define INFLUXDB_TOKEN "lB4hzN2Fh7lyajxjtvO9IXpwkvKNiljnLrvDCMGahHR0spHhr3Y128pzimD9o9dw2Bg7mkTsN2LW73bQWTx-BA==" //InfluxDB v2 server or cloud API token (Use: InfluxDB UI -> Data -> API Tokens -> <select token>)
#define INFLUXDB_ORG "EQ5"                                                                                        //InfluxDB v2 organization id (Use: InfluxDB UI -> User -> About -> Common Ids )
#define INFLUXDB_BUCKET "LoRa"                                                                                    //InfluxDB v2 bucket name (Use: InfluxDB UI ->  Data -> Buckets)
#define TZ_INFO "AEDT+11"                                                                                         //InfluxDB v2 timezone

InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN, InfluxDbCloud2CACert);                 //InfluxDB client instance with preconfigured InfluxCloud certificate

Point sensor("weather");                                            //Data point

void setup()
{
    initBoard();
    // When the power is turned on, a delay is required.
    delay(1500);

    Serial.println("LoRa Receiver");

    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DI0_PIN);
    if (!LoRa.begin(LoRa_frequency)) {
        Serial.println("Starting LoRa failed!");
        while (1);
    }

    WiFi.mode(WIFI_STA);                                              //Setup wifi connection
    wifiMulti.addAP(WIFI_SSID, WIFI_PASSWORD);
  
    Serial.print("Connecting to wifi");                               //Connect to WiFi
    while (wifiMulti.run() != WL_CONNECTED) 
    {
      Serial.print(".");
      delay(100);
    }
    Serial.println();
  
    //sensor.addTag("device", DEVICE);                                   //Add tag(s) - repeat as required
    sensor.addTag("SSID", WIFI_SSID);
  
    timeSync(TZ_INFO, "pool.ntp.org", "time.nis.gov");                 //Accurate time is necessary for certificate validation and writing in batches
  
    if (client.validateConnection())                                   //Check server connection
    {
      Serial.print("Connected to InfluxDB: ");
      Serial.println(client.getServerUrl());
    } 
    else 
    {
      Serial.print("InfluxDB connection failed: ");
      Serial.println(client.getLastErrorMessage());
    }
 }

void loop()
{
    // try to parse packet
    int packetSize = LoRa.parsePacket();
    if (packetSize) {
        // received a packet
        Serial.print("Received packet '");
        String recv = "";
        // read packet
        while (LoRa.available()) {
            recv += (char)LoRa.read();
        }
        Serial.println(recv);

    sensor.clearFields();                                              //Clear fields for reusing the point. Tags will remain untouched
    sensor.addField("temperature", recv.c_str());                              // Store measured value into point
    if (wifiMulti.run() != WL_CONNECTED)                               //Check WiFi connection and reconnect if needed
    Serial.println("Wifi connection lost");

    if (!client.writePoint(sensor))                                    //Write data point
    {
      Serial.print("InfluxDB write failed: ");
      Serial.println(client.getLastErrorMessage());
    }
}
}
