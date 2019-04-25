#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys


import time
from RF24 import *
import RPi.GPIO as GPIO
import re
import numpy as np

file = open("cmacConfig.h","r")
texto = file.read()

DEFAULT_CHANNEL = int(re.search("DEFAULT_CHANNEL\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
DATARATE = str(re.search("DATARATE\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
PALEVEL = str(re.search("PALEVEL\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
AUTOACK = re.search("AUTOACK\ +(?P<var>.+?)(\ |\n|/)", texto).group("var").upper() == "TRUE"
AUTOCHANNEL = re.search("AUTOACK\ +(?P<var>.+?)(\ |\n|/)", texto).group("var").upper() == "TRUE"
NUM_CHANNELS = int(re.search("NUM_CHANNELS\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
PACKET_SIZE = int(re.search("PACKET_SIZE\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))

PIPE_TX = (int(re.search("PIPE_TX\ +(?P<var>.+?)(\ |\n|/)", texto).group("var")[:-2], 16))
print(hex(PIPE_TX))
PIPE_RX = (int(re.search("PIPE_RX\ +(?P<var>.+?)(\ |\n|/)", texto).group("var")[:-2], 16))
print(hex(PIPE_RX))

COORDINATOR_ADDR = (int(re.search("COORDINATOR_ADDR\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"), 16))
BROADCAST_ADDR = (int(re.search("BROADCAST_ADDR\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"), 16))
MY_ADDR = (int(re.search("MY_ADDR\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"), 16))

TIMETORECONNECT = int(re.search("TIMETORECONNECT\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
MAXTIMEWAITINGPACKET = int(re.search("MAXTIMEWAITINGPACKET\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
TIMENEWCONNECTIONS = int(re.search("TIMENEWCONNECTIONS\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
QTDELOOPS = int(re.search("QTDELOOPS\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
PIFS = int(re.search("PIFS\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))

SLOTTIME = int(re.search("SLOTTIME\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
SIFS = int(re.search("SIFS\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
DIFS = int(re.search("DIFS\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
BACKOFF = int(re.search("BACKOFF\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
CCA = int(re.search("CCA\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
SUPERFRAMETIME = int(re.search("SUPERFRAMETIME\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))

SLEEPTIMEMIN = int(re.search("SLEEPTIMEMIN\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))
SLEEPTIMEMAX = int(re.search("SLEEPTIMEMAX\ +(?P<var>.+?)(\ |\n|/)", texto).group("var"))

ACKMSG = (int(re.search("ACKMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))
NEWCONNECTIONSMSG = (int(re.search("NEWCONNECTIONSMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))
TOKENMSG = (int(re.search("TOKENMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))
RTSMSG = (int(re.search("RTSMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))
CTSMSG = (int(re.search("CTSMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))
DATAMSG = (int(re.search("DATAMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))
OUTMSG = (int(re.search("OUTMSG\ +(?P<var>.+?)(\ |\n|/|L)", texto).group("var"), 16))



########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md

# CE Pin, CSN Pin, SPI Speed

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B
# Setup for GPIO 15 CE and CE1 CSN with SPI Speed @ 8Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B+
# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
radio = RF24(RPI_BPLUS_GPIO_J8_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

# RPi Alternate, with SPIDEV - Note: Edit RF24/arch/BBB/spi.cpp and  set 'this->device = "/dev/spidev0.0";;' or as listed in /dev
#radio = RF24(22, 0);

##########################################


millis = lambda: int(round(time.time() * 1000))
micros = lambda: int(round(time.time() * 1000000))
def delayMicroseconds(tempo):
    time.sleep(tempo/1000000)
    
radio.begin()
print (PALEVEL)
#radio.setPALevel(PALEVEL)
#radio.setDataRate(DATARATE)
radio.setPALevel(RF24_PA_MAX)
radio.setDataRate(RF24_250KBPS)
radio.setAutoAck(AUTOACK)
radio.setChannel(DEFAULT_CHANNEL)
radio.setCRCLength(RF24_CRC_8) #RF24_CRC_DISABLED RF24_CRC_8 RF24_CRC_16
radio.enableDynamicPayloads()
#radio.setPayloadSize(PACKET_SIZE)
#radio.setRetries(5,15)
radio.openWritingPipe(PIPE_RX)
radio.openReadingPipe(1, PIPE_TX)

radio.printDetails()

radio.startListening()

list_nodes=[]
list_lastMsg=[]
listNodestoSend=np.zeros(1)
lastPoll=0
Packet = []
qtde_nodes = 0
DeltaDelay=int(3*MAXTIMEWAITINGPACKET/1000)#milisegundos

qtdeAmostras=5 #largura da tabela
listKnowing=np.zeros(1)


#análise

qtdeAnalise=200
auxPoll=0
lastPpP=np.zeros(qtdeAnalise)
lastDelays=np.zeros(qtdeAnalise)
lastErrors=np.zeros(qtdeAnalise)

TotalPolls=0
TotalPacketsReceived=0
TotalPacketsLost=0
TotalDelay=0
MeanDelay=0
flagFifo=False


dif = np.zeros(1)
dp = np.zeros(1)
l = np.zeros(1)
lFifo = np.zeros(1)
lstdvalues = 0
    

def u8toInt(b): 
    u=0
    for byte in b:
        u= u*256 + int(byte)
    return u

def printList():
    print("Nodes list")
    for i in range (qtde_nodes):
        print(list_nodes[i])


def addNodeToList(node): 
    global list_nodes
    global list_lastMsg
    global qtde_nodes
    global listKnowing
    global listNodestoSend
    naLista = False
    for i in range (qtde_nodes):
        if ( list_nodes[i] == node):
            listKnowing[i][-1]=0
            naLista = True
    if (not naLista):
        list_nodes.append(node)
        list_lastMsg.append(-1)
        qtde_nodes += 1
        listKnowing.resize(qtde_nodes,qtdeAmostras) ##atualiza tamanho da tabela
        listKnowing[-1][-1]=0
    listNodestoSend.resize(len(list_nodes),1)
    
def RefreshlistKnowing(pacote):
    global listKnowing
    global PacketsSend
    if (len(pacote)>=3):    
        node = int(pacote[1])
        index = u8toInt([pacote[2], pacote[3]])

        #if (list_nodes.index(node)>=0):
        try:
            i=list_nodes.index(node)
            if (list_lastMsg[i] != index):
                list_lastMsg[i] = index
                listKnowing[i]=np.roll(listKnowing[i],-1)
                listKnowing[i][qtdeAmostras-1]=millis() ##adiciona tempo na tabela
                PacketsSend+=1
        except ValueError:
            return
        
    
def newConnections():
    msg = [BROADCAST_ADDR, MY_ADDR, NEWCONNECTIONSMSG]
    #delayMicroseconds(PIFS)
    radio.stopListening()
    #while ( radio.available()) :
    #    radio.startListening()
    #    delayMicroseconds(PIFS)
    #    radio.stopListening()
    radio.write(bytes(msg))
    radio.startListening()  # Now, continue listening
    started_waiting_at = micros()       # Wait here until we get a response, or timeout (250ms)
    timeout = False
    while (not timeout):
        #delayMicroseconds(5)
        while (not radio.available()) and (not timeout):
            #delayMicroseconds(5)
            if (micros() - started_waiting_at > TIMENEWCONNECTIONS ): # Break out of the while loop if nothing available
                timeout = True
                break
        if ( timeout ):                             # Describe the results
            pass
        else:
            leng = radio.getDynamicPayloadSize()
            msg = list(radio.read( leng ))
            if ((msg[0] == (MY_ADDR)) and (msg[2] == (NEWCONNECTIONSMSG))) :
                print("novo nó: %d\n\r" % int(msg[1]))
                addNodeToList(int(msg[1]))
                msg[0] = (msg[1])
                msg[1] = (MY_ADDR)
                msg[2] = (ACKMSG)
                #delayMicroseconds(PIFS)
                #while ( radio.available()) :
                #    radio.startListening()
                #    delayMicroseconds(PIFS)
                #    radio.stopListening()
                radio.stopListening()
                radio.write( bytes(msg), 3 )
                radio.startListening()
                #delayMicroseconds(PIFS)

def sendToken(dest):
    global Packet
    global TotalPolls
    global auxPoll
    global lastPpP
    msg = [(dest), (MY_ADDR), (TOKENMSG)]
#    while ( radio.available()) : #verifica o meio antes de enviar
#        radio.startListening()
#        delayMicroseconds(PIFS)
#        radio.stopListening()
    radio.stopListening()
    radio.write( bytes(msg), 3 )
    radio.startListening()#
    #print(radio.whatHappened())##(tx_ok, tx_fail, tx_ready)
    TotalPolls+=1
    auxPoll+=1 #contagem de polls por pacote
    delayMicroseconds(PIFS)
    started_waiting_at = micros()                   # 
    timeout = False
    while (not timeout):
        #delayMicroseconds(5)
        while ( not radio.available()  ):
            #delayMicroseconds(5)
            if (micros() - started_waiting_at > MAXTIMEWAITINGPACKET ): # Break out of the while loop if nothing available
                  timeout = True
                  break
        if ( timeout ):                             # Describe the results
            pass
        else:
            leng = radio.getDynamicPayloadSize()
            Packet = list(radio.read( leng ))
            RefreshlistKnowing(Packet)  ##atualiza tabela

            lastPpP=np.roll(lastPpP,-1)
            lastPpP[-1]=auxPoll
            auxPoll=0
            printPacket()
            #if (listKnowing.min()!=0 and lastPpP[-1]>15):
            #    listKnowing[][-1]=0
            
            if (listKnowing.min()!=0):
                attLists()
                #print("attLists")

            
            msg = [(dest), (MY_ADDR), (ACKMSG)]
            
#            while ( radio.available()) :
#                radio.startListening()
#                delayMicroseconds(PIFS)
#                radio.stopListening()
            #delayMicroseconds(PIFS)
            radio.stopListening()
            radio.write( bytes(msg), 3 ) #ENVIA ACK
            radio.startListening()
            #print(radio.whatHappened())##(tx_ok, tx_fail, tx_ready)
            #delayMicroseconds(PIFS)
        return

def printPacket():
    global TotalPolls
    global TotalPacketsReceived
    global TotalPacketsLost
    global TotalDelay
    global MeanDelay
    global qtde_nodes

    global lastDelays
    global lastPpP
    global lastErrors
    frase=""
    for i in range(8,len(Packet)):
        frase+=chr(Packet[i])
        
    if (len(Packet)>2):
#        if flagFifo:
#            print("F ", end='')
#            pass

#        print("q",qtde_nodes, end='')
        TotalPacketsReceived+=1
#        print(" node",(Packet[1]), end='')
        index = [Packet[2], Packet[3]]
#        print(" n", (u8toInt(index)), end='')
        if (len(Packet)>8):
            
            tempo = [Packet[4], Packet[5], Packet[6], Packet[7]]
            TotalDelay+=u8toInt(tempo)
            lastDelays=np.roll(lastDelays,-1)
            lastDelays[-1]=u8toInt(tempo)
 
#            print("\tatraso:",(u8toInt(tempo)), end='')
            TotalPacketsLost+=int(Packet[9])
            lastErrors=np.roll(lastErrors,-1)
            lastErrors[-1]=int(Packet[9])

            if (lastErrors[-1]>0):
                if flagFifo:
                    print("F ", end='')
                    pass

                print("q",qtde_nodes, end='')
                print(" node",hex(int(Packet[1])), end='')
                print(" n", (u8toInt(index)), end='')

                print("\tatraso:",(u8toInt(tempo)), end='')

                print("\tperdidos:",int(Packet[9]), end='' ) #//perdidos
                #print("\tmsg:",frase, end='')
                #print("\tpks:",TotalPacketsReceived, end='')
                print("\tdly:",int(TotalDelay/TotalPacketsReceived), end='')

                print("\tlst:",TotalPacketsLost, end='')
                print("\tTps:",TotalPolls, end='')
                #print("\tPpP:",int(TotalPolls/TotalPacketsReceived), end='')
                print("\tPpP:",lastPpP[-1], end='')
                #print("\tMedLLost: %3.2f" % (((np.sum(lastErrors)+0.0001)/qtdeAnalise)*100), end='%')
                #print("\tMedLDly:",int(np.mean(lastDelays)), end='')
                #print("\tMedLPpP: %3.2f" % (np.mean(lastPpP)))

def printStatus():
    global TotalPolls
    global TotalPacketsReceived
    global TotalPacketsLost
    global TotalDelay
    global MeanDelay
    global qtde_nodes

    global lastDelays
    global lastPpP
    global lastErrors
    print(qtde_nodes, end='')
    print("\tpks:",TotalPacketsReceived, end='')
    print("\tdly:",int(TotalDelay/TotalPacketsReceived), end='')

    print("\tlst:",TotalPacketsLost, end='')
    print("\tTps:",TotalPolls, end='')
    print("\tMedLLost: %3.2f" % (((np.sum(lastErrors)+0.0001)/qtdeAnalise)*100), end='%')
    print("\tMedLDly:",int(np.mean(lastDelays)), end='')
    print("\tMedLPpP: %3.2f" % (np.mean(lastPpP)))

    

def checkLostNodes():
    global listKnowing
    global qtde_nodes
    global listNodestoSend

    if qtde_nodes>0:
        #print(listKnowing)
        l2=listKnowing[:, -1:] #ultima coluna
#        print("\t\t",int(millis()))
#        for i in range(len(l2)):
#            print(list_nodes[i],"\t last pkt ", int(millis()-l2[i]),"\t média ",end="")
#            if len(l)==len(l2):
#                print(int(l[i]))
#            else:
#                print()
        #print (l)
        for i in range(len(l2)-1,-1,-1):
            if (millis()-l2[i]>TIMETORECONNECT and millis()-l2[i]<TIMETORECONNECT*TIMETORECONNECT):
                listKnowing=np.delete(listKnowing, i, axis=0)
                qtde_nodes-=1
                print ("removeu", hex(list_nodes[i]))
                #resultFile.write("removeu "+str(list_nodes[i]))
                list_nodes.pop(i)
                listNodestoSend=np.delete(listNodestoSend, i)
                attLists()

def attLists():
    global dif
    global dp
    global l
    global lFifo
    global listKnowing
    global lstdvalues
    dif=listKnowing[:, 1:]-listKnowing[:, :-1]
    dp=np.std(dif, ddof=0, axis=1).astype(int)
    l=np.mean(dif, axis=1).astype(int)
    if(DisciplinaServico=="knowingstd"):
        lstdvalues = 250*np.log2(l/1000)+200
        for i in range(len(lstdvalues)):
            if (lstdvalues[i]<180):
                lstdvalues[i]=180
        if (np.min(lstdvalues-dp)<0):
            print ("desvio ",list_nodes[np.argmin(lstdvalues-dp)], " valor ",dp[np.argmin(lstdvalues-dp)])
            listKnowing[np.argmin(lstdvalues-dp)][-1]=0
        if(len(l)==len(lFifo)):
            if (np.min(lFifo)!=0 and np.max(l - lFifo )>200):
                print(l)
                print (lFifo)
                print(l-lFifo)
                listKnowing[np.argmin(lstdvalues-dp)][-1]=0
                print ("desvio 2",list_nodes[np.argmin(lstdvalues-dp)], " valor ",dp[np.argmin(lstdvalues-dp)])
           
def Polling(modo):
    global AuxNode
    global aux
    global listKnowing
    global flagFifo
    global listNodestoSend
    global lastPoll
    global list_nodes
    global dif
    global dp
    global l
    global lFifo
    now=millis()
    
    if(modo=="knowingstd" and listKnowing.min()!=0):
        nextTrans=l+listKnowing[:,-1]
        #l2 tempo até a próxima transmissão
        l2=nextTrans-now
        value=np.min(l2)
        if flagFifo:
            lFifo=l
        flagFifo=False
        coef=max(1, qtde_nodes/4)
        if(value<2*DeltaDelay*coef):
            for i in range(len(l2)):
                if (l2[i]<2*DeltaDelay*coef):
                    listNodestoSend[i]=1
                else:
                    listNodestoSend[i]=0
            for i in range(lastPoll+1, lastPoll+1+len(listNodestoSend)):
                if listNodestoSend[i%len(listNodestoSend)]==1:
                    return i%len(listNodestoSend)
        else:
            return -1
    elif(modo=="knowing" and listKnowing.min()!=0):
        nextTrans=l+listKnowing[:,-1]
        l2=nextTrans-now#+np.random.randint(0,DeltaDelay*5,size=len(l))
        flagFifo=False
        value=np.min(l2)
        if(value<2*DeltaDelay):
            for i in range(len(l2)):
                if (l2[i]<2*DeltaDelay):
                    listNodestoSend[i]=1
                else:
                    listNodestoSend[i]=0
            for i in range(lastPoll+1, lastPoll+1+len(listNodestoSend)):
                if listNodestoSend[i%len(listNodestoSend)]==1:
                    return i%len(listNodestoSend)
        else:
            return -1
    elif(modo=="random"):
        return np.random.randint(0, qtde_nodes)
    elif(modo=="FIFO"):
        AuxNode+=1
        AuxNode%=qtde_nodes
        return AuxNode
    else:
        AuxNode+=1
        AuxNode%=qtde_nodes
        flagFifo=True
        return AuxNode
        

DisciplinaServico="FIFO" #FIFO, knowing, knowingstd, hibrid, random
started_waiting_at = micros()
started_waiting_at2 = micros()#checar nós caidos
started_waiting_at3 = micros()#atualizacão forcada
started_waiting_at4 = micros()#atualizacão forcada
AuxNode=0
aux=0
nodePoll=0
nodePollPast=0
PacketsSend=0
AttTableTime=2 #minutos
# forever loop

while 1:
    if (micros() - started_waiting_at > min([500000*qtde_nodes,2000000])): #novas conexoes a cada 10segundos
        newConnections()
        started_waiting_at = micros()
    if (micros() - started_waiting_at2 > TIMETORECONNECT*1000):#verifica nós caídos
        checkLostNodes()
        started_waiting_at2 = micros()
    if (micros() - started_waiting_at3 > AttTableTime*60000000):#atualiza a tabela com fifo
        print("Timout Atualizando Tabela")
        listKnowing[:][-1]=0
        started_waiting_at3 = micros()
        #resultFile.close()
        #resultFile = open((datastr+".txt"),'w')
    if (micros() - started_waiting_at4 > 10000000):#printa info
        printStatus()
        started_waiting_at4 = micros()
        

    if(qtde_nodes>0):
        nodePoll=Polling(DisciplinaServico)
        if (nodePoll != -1):
            lastPoll=nodePoll
            sendToken(list_nodes[nodePoll])
            #delayMicroseconds(5)
        else:
            #fazer algo enquanto não tem polls para enviar
            #delayMicroseconds(500)
            pass
        
            




