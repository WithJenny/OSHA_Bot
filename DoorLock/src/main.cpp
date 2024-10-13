#include <Arduino.h>
#include <WiFi.h>



const char* ssid = "Duktop";
const char* password = "leleponz";

const uint ServerPort = 8080;
WiFiServer Server(ServerPort);
WiFiClient RemoteClient;

void CheckForConnections();
void setup()
{
  // initialize LED digital pin as an output.
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
    delay(1000);
    WiFi.mode(WIFI_AP);
    WiFi.begin(ssid, password);
    Serial.println("\nConnecting");

    while(WiFi.status() != WL_CONNECTED){
        Serial.print(".");
        delay(100);
    }

    Serial.println("\nConnected to the WiFi network");
    Serial.print("Local ESP32 IP: ");
    Serial.println(WiFi.localIP());
    Server.begin();
}

void loop()
{
 
  delay(10);

  CheckForConnections();

}

void CheckForConnections()
{
  Serial.print("checking on ");
  Serial.println(WiFi.localIP());
  if (Server.hasClient())
  {
    // If we are already connected to another computer, 
    // then reject the new connection. Otherwise accept
    // the connection. 
    if (RemoteClient.connected())
    {
      Serial.println("Connection rejected");
      Server.available().stop();

      while (RemoteClient.available()>0) {
        char c = RemoteClient.read();
        RemoteClient.write(c);
      }
    }
    else
    {
      Serial.println("Connection accepted");
      RemoteClient = Server.available();
    }
  }
}