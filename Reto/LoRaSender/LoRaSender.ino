#include <LoRa.h>
#include "boards.h"
#include "DHT.h"

#define DHTPIN 33     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 22  (AM2302), AM2321

int counter = 0;
const int Trigger = 13;   //Pin digital 13 para el Trigger del sensor
const int Echo = 2;   //Pin digital 2 para el Echo del
int pinLED = 25;
int pinBoton = 14;


DHT dht(DHTPIN, DHTTYPE);
// Crear variable para estado del botón
bool boton = HIGH;

void setup()
{
    initBoard();
    // When the power is turned on, a delay is required.
    delay(1000);
    Serial.begin(9600);//iniciailzamos la comunicación
    dht.begin();
    pinMode(Trigger, OUTPUT); //pin como salida
    pinMode(Echo, INPUT);  //pin como entrada
    pinMode(pinLED,OUTPUT); // Salida digital para el LED
    pinMode(pinBoton,INPUT); // Entrada digital para el botón
    Serial.println("LoRa Sender");
    LoRa.setPins(RADIO_CS_PIN, RADIO_RST_PIN, RADIO_DI0_PIN);
    
    if (!LoRa.begin(LoRa_frequency)) {
        Serial.println("Starting LoRa failed!");
        while (1);
    }
}

void loop()
{
    int dis = distance();
    float temp = mediciones_dht();
    int edo = edo_boton();
    // send packet
    LoRa.beginPacket();
    LoRa.print("EQ5 ");
    LoRa.print(dis);
    LoRa.print(temp);
    LoRa.print(edo);
    //LoRa.print(counter);
    //string = String(dis);
    Serial.println(dis);
    Serial.println(temp);
    Serial.println(edo);
    LoRa.endPacket();

    #ifdef HAS_DISPLAY
    if (u8g2) {
        char buf[256];
        u8g2->clearBuffer();
        u8g2->drawStr(0, 12, "Transmitting: OK!");
        snprintf(buf, sizeof(buf), "Dis ultra: %d", dis);////////////////////////////
        //Serial.println(dis);
        u8g2->drawStr(0, 30, buf);
        snprintf(buf, sizeof(buf), "dht: %.*f", 3, temp);
        u8g2->drawStr(0, 46, buf);
        snprintf(buf, sizeof(buf), "edo: %d", edo);
        u8g2->drawStr(0, 64, buf);
        u8g2->sendBuffer();
    }
#endif
    counter++;
    delay(5000);
}

int distance()
{
  long t; //tiempo que demora en llegar el eco
  long d; //distancia en centimetros

  digitalWrite(Trigger, HIGH);
  delayMicroseconds(10);          //Enviamos un pulso de 10us
  digitalWrite(Trigger, LOW);

  t = pulseIn(Echo, HIGH); //obtenemos el ancho del pulso
  d = t *0.0343 / 2;

  if(d > 2 && d < 5)
  {
    return int(d);
  }
}

float mediciones_dht() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  /*if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  } */
  if (isnan(h)==false){
    return float(h);
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);
  /*
  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));*/
}

int edo_boton() {
  // Leer el estado del botón y encender o apagar el LED
  boton = digitalRead(pinBoton);
 
  if(boton == HIGH){            // Si el botón está pulsado
    digitalWrite(pinLED,HIGH);  // Enciende el LED
    return 1;
  }
  else{                         // Si no
    digitalWrite(pinLED,LOW);   // Apaga el LED
    return 0;
  }
}
