


//cmac config
//#define DEBUG

#define BAUDRATE     115200

#define CEPIN     7
#define CSPIN     8

#define DEFAULT_CHANNEL   1
#define DATARATE     RF24_250KBPS  //RF24_1MBPS = 0, RF24_2MBPS, RF24_250KBPS        
#define PALEVEL       RF24_PA_HIGH //RF24_PA_MIN,RF24_PA_LOW, RF24_PA_HIGH, RF24_PA_MAX,
#define AUTOACK     false
#define AUTOCHANNEL   false
#define NUM_CHANNELS     126
#define PACKET_SIZE     32//PAYLOAD
#define CONFIRMACAO true

#define PIPE_TX       0xf0f0F0F0E1LL
#define PIPE_RX       0xf0f0F0F0D2LL

//enderecos
//#define COORDINATOR_ADDR   0X00
#define COORDINATOR_ADDR   0X00
#define BROADCAST_ADDR   0XFF
#define MY_ADDR   0XFF //FF read address from eeprom
#define EEPROM_ADDR 10

//coordinator mac
#define TIMETORECONNECT 60000000 // TEMPO MAXIMO DE ESPERA DO TOKEN

#define MAXTIMEWAITINGPACKET 2500//us
#define TIMENEWCONNECTIONS 7000//us
#define SLOTTIME 52 //http://www.sciencedirect.com/science/article/pii/S2405959516300650



#define PIFS 100// microseconds


//csmaca mac
#define SIFS 160// microseconds
#define DIFS 264
#define BACKOFF 320
#define CCA 168
#define SUPERFRAMETIME 3000


// intervalos
#define NETWORK 0X00
#define SLEEPTIMEMIN 999//MILISEGUNDOS
#define SLEEPTIMEMAX 1000//MILISEGUNDOS
//100 CSMA IMPOSSÍVEL


//mensagens
#define ACKMSG   0X01
#define NEWCONNECTIONSMSG   0X02

#define TOKENMSG   0X03
#define RTSMSG   0X04
#define CTSMSG   0X05
#define DATAMSG 0X06
#define OUTMSG 0X07


byte waitingConnections[3]={BROADCAST_ADDR,MY_ADDR,NEWCONNECTIONSMSG};
byte rts[3]={COORDINATOR_ADDR,MY_ADDR,RTSMSG};





