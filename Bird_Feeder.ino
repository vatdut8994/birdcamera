#include "esp_camera.h"
#include <WiFi.h>
//
// WARNING!!! PSRAM IC required for UXGA resolution and high JPEG quality
//            Ensure ESP32 Wrover Module or other board with PSRAM is selected
//            Partial images will be transmitted if image exceeds buffer size
//

// Select camera model

//Lunenburg: c0p3nHag3n

#include <ESP_Mail_Client.h>

#define WIFI_SSID "SpectrumSetup-8265"

#define WIFI_PASSWORD "routinewinter686"

#define SMTP_server "smtp.gmail.com"

#define SMTP_Port 465

#define sender_email "vatdut8994@gmail.com"

#define sender_password "jxkb dgsu guib gthl"

#define Recipient_email "vatdut8994@gmail.com"

#define Recipient_name "Mercer"

#define CAMERA_MODEL_WROVER_KIT // Has PSRAM

#include "camera_pins.h"

const char* ssid     = "SpectrumSetup-8265";   //input your wifi name
const char* password = "routinewinter686";   //input your wifi passwords


int distanceThreshold = 0;
int cm = 0;
int inches = 0;

void startCameraServer();

SMTPSession smtp;

long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT);  // Clear the trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Sets the trigger pin to HIGH state for 10 microseconds
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  // Reads the echo pin, and returns the sound wave travel time in microseconds
  return pulseIn(echoPin, HIGH);
}


long distance() {
  distanceThreshold = 350;
  // measure the ping time in cm
  cm = 0.01723 * readUltrasonicDistance(2, 0);
  return cm;
}

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  
  // if PSRAM IC present, init with UXGA resolution and higher JPEG quality
  //                      for larger pre-allocated frame buffer.
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  sensor_t * s = esp_camera_sensor_get();
  // drop down frame size for higher initial frame rate
  s->set_framesize(s, FRAMESIZE_VGA);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");

  smtp.debug(1);

  ESP_Mail_Session session;

  session.server.host_name = SMTP_server ;

  session.server.port = SMTP_Port;

  session.login.email = sender_email;

  session.login.password = sender_password;

  session.login.user_domain = "";

  /* Declare the message class */

  SMTP_Message message;

  message.sender.name = "ESP 32";

  message.sender.email = sender_email;

  message.subject = "ESP32 Bird Camera";

  message.addRecipient(Recipient_name,Recipient_email);

  String textMsg = WiFi.localIP().toString();

  message.text.content = textMsg.c_str();
  message.text.content = textMsg.c_str();

  message.text.charSet = "us-ascii";

  message.text.transfer_encoding = Content_Transfer_Encoding::enc_7bit;

  if (!smtp.connect(&session))

    return;

  if (!MailClient.sendMail(&smtp, &message))

    Serial.println("Error sending Email, " + smtp.errorReason());
}

void loop() {
  int bird_dist = distance();
  Serial.println(bird_dist);

  if (bird_dist < 15){
    delay(1000);
    if (distance() < 15){
        Serial.println("WE GOT A BIRD");

        ESP_Mail_Session session;
      
        session.server.host_name = SMTP_server ;
      
        session.server.port = SMTP_Port;
      
        session.login.email = sender_email;
      
        session.login.password = sender_password;
      
        session.login.user_domain = "";
      
        /* Declare the message class */
      
        SMTP_Message message;
      
        message.sender.name = "ESP 32";
      
        message.sender.email = sender_email;
      
        message.subject = "ESP32 Bird Camera";
        
      
        message.addRecipient(Recipient_name,Recipient_email);
      
        String textMsg = "Bird Detected! Check out the footage at: http://" + WiFi.localIP().toString();
      
        message.text.content = textMsg.c_str();
        message.text.content = textMsg.c_str();
      
        message.text.charSet = "us-ascii";
      
        message.text.transfer_encoding = Content_Transfer_Encoding::enc_7bit;
      
        smtp.connect(&session);
      
        if (!MailClient.sendMail(&smtp, &message))
      
          Serial.println("Error sending Email, " + smtp.errorReason());
          
//        delay(300000);
          delay(60000);
    }
  }
}
