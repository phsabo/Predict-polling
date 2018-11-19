#include "nRF24L01.h"
#include "RF24.h"
#include <SPI.h>
#include "printf.h"
#include "cmacConfig.h"
#include <avr/sleep.h>
#include <avr/power.h>
#include <EEPROM.h>

char Packet[PACKET_SIZE];

bool conectado = false;
uint16_t index = 0;
uint8_t perdidos = 0;
byte my_address = 0;

RF24 radio(CEPIN, CSPIN);

void setup(void) {
  Serial.begin(BAUDRATE);
  printf_begin();

  Serial.println("teste receptor");

  radio.begin();
  radio.setPALevel(PALEVEL);
  radio.enableDynamicPayloads();
  //radio.setPayloadSize(PACKET_SIZE);
  radio.setDataRate(DATARATE);
  radio.setAutoAck(AUTOACK);
  radio.setCRCLength(RF24_CRC_8);
  radio.setChannel(DEFAULT_CHANNEL);
  radio.openWritingPipe(PIPE_TX);
  radio.openReadingPipe(1, PIPE_RX);
  radio.startListening();
  radio.stopListening();
  radio.printDetails();

  radio.startListening();
  randomSeed(millis());
  if (MY_ADDR!=0XFF){
    my_address = MY_ADDR;
  }else{
    //read from eeprom
    my_address = EEPROM.read(EEPROM_ADDR);
  }
}


void teste() {
  if ( radio.available() ) {                                  // if there is data ready
    unsigned long got_time;
    while (radio.available()) {                             // Dump the payloads until we've gotten everything
      radio.read( &got_time, sizeof(unsigned long) );       // Get the payload, and see if this was the last one.
      // Spew it.  Include our time, because the ping_out millis counter is unreliable
      printf("Got payload %lu @ %lu...\n", got_time, millis()); // due to it sleeping
    }

    radio.stopListening();                                  // First, stop listening so we can talk
    radio.write( &got_time, sizeof(unsigned long) );        // Send the final one back.
    Serial.println(F("Sent response."));
    radio.startListening();                                 // Now, resume listening so we catch the next packets.
  } else {
    //Serial.println(F("Sleeping"));
    //delay(20);                                             // Delay so the serial data can print out
    //do_sleep();

  }
}
bool tryConnect() {
  // Now, resume listening so we catch the next packets.

  if ( radio.available() ) {                                  // if there is data ready
    byte msg[3];
    bool waitingResponse = false;
    while (radio.available()) {                             // Dump the payloads until we've gotten everything
//      Serial.println("recebeu algo");
      radio.read( &msg, 3 );       // Get the payload, and see if this was the last one.
      // Spew it.  Include our time, because the ping_out millis counter is unreliable
//      printf("%0x %0x %0x\n\r", msg[0], msg[1], msg[2]);
      if (msg[0] == BROADCAST_ADDR & msg[1] == COORDINATOR_ADDR & msg[2] == NEWCONNECTIONSMSG) {
//        Serial.println("try connect");
        msg[0] = COORDINATOR_ADDR;
        msg[1] = my_address;
        delayMicroseconds(random(0, PIFS));
        radio.stopListening();
        radio.write(&msg, 3);
        waitingResponse = true;
        radio.startListening();
        //printf("Got payload %lu @ %lu...\n",got_time,millis()); // due to it sleeping
      } else {
        radio.flush_rx();
      }

    }

    unsigned long started_waiting_at = micros();    // Wait here until we get a response, or timeout (250ms)
    bool timeout = false;

    while ((!timeout) & waitingResponse)
    {
      while ( ! radio.available()  ) {
        if (micros() - started_waiting_at > 50000 ) { // Break out of the while loop if nothing available
          timeout = true;
          break;
        }
      }
      if ( timeout ) {                                // Describe the results
        Serial.println("failed connect");
        return false;
      } else {
        byte msg[3];                     // Grab the response, compare, and send to debugging spew
        radio.read( &msg, 3 );
        if (msg[0] == my_address & msg[1] == COORDINATOR_ADDR & msg[2] == ACKMSG) {

          Serial.println("connected");
          return true;
        }
      }
    }
  }
  return false;
}
void conectar() {
  radio.powerUp();
  radio.startListening();
  while (! conectado) {
    //Serial.println("Tentando conectar");
    //teste();
    bool conectando = tryConnect();
    if (conectando) {
      conectado = true;
      Serial.println("CONECTADO");
    }
  }
  radio.powerDown();
}
bool packMsg(String msg, uint8_t addr, uint32_t tempo, uint16_t index)
{
  if (msg.length() > PACKET_SIZE - 8) {
    Serial.println("ERRO msg muito grande");
    return false;
  }
  for (int i = 0; i < PACKET_SIZE; i++)
  {
    Packet[i] = ' ';
  }
  for (int i = 0; i < (msg.length()); i++)
  {
    Packet[i + 8] = msg.charAt(i);
  }
  Packet[0] = char(addr);
  Packet[1] = char(my_address);
  Packet[2] = index >> 8;
  Packet[3] = index ;
  Packet[9] = perdidos;
  if (tempo == 0) {
    Packet[4] = 0;
    Packet[5] = 0;
    Packet[6] = 0;
    Packet[7] = 0;
  } else {
    Packet[4] = tempo >> 24;
    Packet[5] = tempo >> 16;
    Packet[6] = tempo >> 8;
    Packet[7] = tempo ;
  }
  return true;
}
bool sendMsg(String mensagem) {
  while (!conectado) {
    //Serial.println("Não conectado, conectando");
    conectar();
  }
  if (conectado) {
    radio.powerUp();
    radio.startListening();                         // Now, continue listening
    unsigned long started_waiting_at = micros();    // Wait here until we get a response, or timeout (250ms)
    bool timeout = false;
    while (! timeout)
    {
      while ( ! radio.available()  ) {
        if (micros() - started_waiting_at > TIMETORECONNECT ) { // Break out of the while loop if nothing available
          timeout = true;
          break;
        }
      }
      if ( timeout ) {
        Serial.println("conexão perdida");
        conectado = false;
        return false;
      } else {

        byte msg[3];
        radio.read( &msg, 3 );
        if (msg[0] == my_address & msg[1] == COORDINATOR_ADDR & msg[2] == TOKENMSG) {
//          printf("token recebido \n\r");
          //printf("%0x %0x %0x\n\r", msg[0], msg[1], msg[2]);
          if (!packMsg(mensagem, COORDINATOR_ADDR, (micros() - started_waiting_at), index)) {
            //Serial.println("ERRO PACOTE INVÁLIDO");
            return false;
          } else {
            radio.stopListening();

//            printf("enviando packet %u \n\r", index);
            radio.write( &Packet, PACKET_SIZE );
            radio.startListening();
            if (CONFIRMACAO){
              timeout = false;
              delayMicroseconds(PIFS);
              unsigned long started_send_at = micros();
              while (!timeout)
              {
                while ( ! radio.available()  ) {
                  if (micros() - started_send_at > 10000 ) { // Break out of the while loop if nothing available
                    timeout = true;
                    break;
                  }
                }
                if ( timeout ) {                                // Describe the results
  //                Serial.println("confirmação não recebida aguardando próximo token para retransmissão");
                  timeout = false; //Confirmação não recebida
  
                  radio.flush_rx();
                  break;
                  //return false;
  
                } else {
                  byte msg[3];                     // Grab the response, compare, and send to debugging spew
                  radio.read( &msg, 3 );
                  if (msg[0] == my_address & msg[1] == COORDINATOR_ADDR & msg[2] == ACKMSG) {
  
                    Serial.println("ack recebido");
                    index++;
                    radio.powerDown();
                    return true;
                  } else {
                    timeout = false; //pacote recebido não foi ack
                    radio.flush_rx();
                  }
                }
              }
            }else{
              index++;
              radio.powerDown();
              return true;
            }
            
          }
        } else {
          timeout = false; //pacote recebido não foi token
          radio.flush_rx();
        }
      }
    }
  }
}

void loop(void) {
  while (!conectado) {
    Serial.println("Não conectado, conectando");
    conectar();
  }
  unsigned int intervalo;
  unsigned long initTime = millis();
  while (true) {
    intervalo = random(SLEEPTIMEMIN, SLEEPTIMEMAX);
    while ((millis() - initTime) < intervalo) {
      //faz nada
    }
    initTime = millis();
    //delay(random(SLEEPTIMEMIN, SLEEPTIMEMAX));
    //delay(SLEEPTIME);
    //Serial.print("t");
    while (! sendMsg("  MENSAGEM DO NO1234567")) {
//      Serial.println("falhou em enviar");
    }
    perdidos = 0;
    while (millis() - initTime >= intervalo) {
      perdidos++;
      initTime += intervalo;
    }
  }
}
