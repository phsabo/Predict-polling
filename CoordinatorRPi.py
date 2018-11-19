#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys


#from __future__ import print_function
import time
from RF24 import *
import RPi.GPIO as GPIO
import re
import numpy as np
import statistics
#import matplotlib.pyplot as plt
import datetime
import csv
file = open("cmacConfig.h","r")
texto = file.read()

#now = datetime.datetime.now()
#datastr= ('{:02d}'.format(now.year)+'{:02d}'.format(now.month)+'{:02d}'.format(now.day)+"-"+'{:02d}'.format(now.hour)+'{:02d}'.format(now.minute)+'{:02d}'.format(now.second))
#resultFile = open((datastr+".txt"),'w')
    
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
list_nodes_acabou_de_enviar=[]
list_nodes_acabou_de_enviar_aux=[]
Packet = []
qtde_nodes = 0
DeltaDelay=int(2*MAXTIMEWAITINGPACKET/1000)#milisegundos

qtdeAmostras=5 #largura da tabela
listKnowing=np.zeros(1)


#análise

qtdeAnalise=200
auxPoll=0
lastPpP=np.zeros(qtdeAnalise)
lastDelays=np.zeros(qtdeAnalise)

TotalPolls=0
TotalPacketsReceived=0
TotalPacketsLost=0
TotalDelay=0
MeanDelay=0
flagFifo=False

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
    delayMicroseconds(PIFS)
    radio.stopListening()
    while ( radio.available()) :
        radio.startListening()
        delayMicroseconds(PIFS)
        radio.stopListening()
    radio.write(bytes(msg))
    radio.startListening()  # Now, continue listening
    started_waiting_at = micros()       # Wait here until we get a response, or timeout (250ms)
    timeout = False
    while (not timeout):
        while (not radio.available()) and (not timeout):
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
                delayMicroseconds(PIFS)
                while ( radio.available()) :
                    radio.startListening()
                    delayMicroseconds(PIFS)
                    radio.stopListening()
                radio.stopListening()
                radio.write( bytes(msg), 3 )
                radio.startListening()

def sendToken(dest):
    global Packet
    global TotalPolls
    global auxPoll
    global lastPpP
    msg = [(dest), (MY_ADDR), (TOKENMSG)]
#    while ( radio.available()) :
#        radio.startListening()
#        delayMicroseconds(PIFS)
#        radio.stopListening()
    radio.stopListening()
    radio.write( bytes(msg), 3 )
    radio.startListening()                          # Now, continue listening
    TotalPolls+=1
    auxPoll+=1
    started_waiting_at = micros()                   # Wait here until we get a response, or timeout (250ms)
    timeout = False
    while (not timeout):
        while ( not radio.available()  ):
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

            
            msg = [(dest), (MY_ADDR), (ACKMSG)]
            delayMicroseconds(PIFS)
#            while ( radio.available()) :
#                radio.startListening()
#                delayMicroseconds(PIFS)
#                radio.stopListening()
            radio.stopListening()
            radio.write( bytes(msg), 3 )
            radio.startListening()

def printPacket():
    global TotalPolls
    global TotalPacketsReceived
    global TotalPacketsLost
    global TotalDelay
    global MeanDelay
    global qtde_nodes

    global lastDelays
    global lastPpP
    #global resultFile
    #text=""
    frase=""
    for i in range(8,len(Packet)):
        frase+=chr(Packet[i])
        
    if (len(Packet)>2):
        if flagFifo:
            print("F ", end='')
            #text+="F "
        print("q",qtde_nodes, end='')
        #text+="q "+str(qtde_nodes)
        TotalPacketsReceived+=1
        print(" node",(Packet[1]), end='')
        #text+=" node "+str(Packet[1])
        index = [Packet[2], Packet[3]]
        print(" n", (u8toInt(index)), end='')
        #text+=" n "+str(u8toInt(index))
        if (len(Packet)>8):
            
            tempo = [Packet[4], Packet[5], Packet[6], Packet[7]]
            TotalDelay+=u8toInt(tempo)
            lastDelays=np.roll(lastDelays,-1)
            lastDelays[-1]=u8toInt(tempo)
 
            print("\tatraso:",(u8toInt(tempo)), end='')
            #text+="\tatraso:"+str(u8toInt(tempo))
            TotalPacketsLost+=int(Packet[9])
            print("\tperdidos:",int(Packet[9]), end='' ) #//perdidos
            #text+="\tperdidos:"+str(int(Packet[9]))
            #print("\tmsg:",frase, end='')
            print("\tpks:",TotalPacketsReceived, end='')
            #text+="\tpks:"+str(TotalPacketsReceived)
            print("\tdly:",int(TotalDelay/TotalPacketsReceived), end='')
            #text+="\tdly:"+str(int(TotalDelay/TotalPacketsReceived))
            print("\tlst:",TotalPacketsLost, end='')
            #text+="\tlst:"+str(TotalPacketsLost)
            print("\tTps:",TotalPolls, end='')
            #text+="\tTps:"+str(TotalPolls)
            print("\tPpP:",int(TotalPolls/TotalPacketsReceived), end='')
            #text+="\tPpP:"+str(int(TotalPolls/TotalPacketsReceived))
            print("\tMedLstDly:",int(np.mean(lastDelays)), end='')
            #text+="\tMedLstDly:"+str(int(np.mean(lastDelays)))
            print("\tMedLstPpP:",int(np.mean(lastPpP)))
            #text+="\tMedLstPpP:"+str(int(np.mean(lastPpP)))
            #resultFile.write(text)
                              

def checkLostNodes():
    global listKnowing
    global qtde_nodes
    #global resultFile
    if qtde_nodes>0:
        #print(listKnowing)
        l=listKnowing[:, -1:] #ultima coluna
        print("\t\t",int(millis()))
        for i in range(len(l)):
            print(list_nodes[i],"\t", int(millis()-l[i]),"\t", int(l[i]))
        #print (l)
        for i in range(len(l)-1,-1,-1):
            if (millis()-l[i]>TIMETORECONNECT and millis()-l[i]<TIMETORECONNECT*TIMETORECONNECT):
                listKnowing=np.delete(listKnowing, i, axis=0)
                qtde_nodes-=1
                print ("removeu", list_nodes[i])
                #resultFile.write("removeu "+str(list_nodes[i]))
                list_nodes.pop(i)
        #return -1
   
       
def Polling(modo):
    global AuxNode
    global aux
    global listKnowing
    global flagFifo
    #global resultFile
    now=millis()
    
    if(modo=="hibrid" and listKnowing.min()!=0):
        #média das diferenças
        dif=listKnowing[:, 1:]-listKnowing[:, :-1]
        l=np.mean(dif, axis=1).astype(int)
        print(l)
        if (aux==qtde_nodes*qtdeAmostras*2):
            listKnowing[:][-1]=0
            aux=0
            return -1
        nextTrans=l+listKnowing[:,-1]
        l2=nextTrans-now+DeltaDelay#+np.random.randint(0,DeltaDelay*5,size=len(l))
        value=np.min(l2)
        #if(value<DeltaDelay and value>-(qtde_nodes*DeltaDelay)):
        if(value<qtde_nodes*DeltaDelay/10):
            aux=aux+1
            return np.argmin(l2)
        else:
            return -1
    if(modo=="knowingstd" and listKnowing.min()!=0):
        # l média das diferenças
        dif=listKnowing[:, 1:]-listKnowing[:, :-1]
        dp=np.std(dif, ddof=0, axis=1).astype(int)
        value=np.max(dp)
        l=np.mean(dif, axis=1).astype(int)
        if (value>(np.min(l))/3):
            
            listKnowing[np.argmax(dp)][-1]=0
            print(list_nodes[np.argmax(dp)], "desvio")
            #resultFile.write("desvio "+str(list_nodes[np.argmax(dp)]))
                
            return -1
        nextTrans=l+listKnowing[:,-1]
        #l2 tempo até a próxima transmissão
        l2=nextTrans-now
        value=np.min(l2)
        flagFifo=False
        if(value<4*DeltaDelay):
            if nodePollPast == np.argmin(l2) and qtde_nodes>1:
                l3=l2
                l3[np.argmin(l2)]=10000
                if micros()%2==0:
                    #print(np.argmin(l3))
                    return np.argmin(l3)
                else:
                    l4=l3
                    l4[np.argmin(l3)]=10000
                    #print(np.argmin(l4))
                    return np.argmin(l4)
            else:
                return np.argmin(l2)
        else:
            return -1
    elif(modo=="knowing" and listKnowing.min()!=0):
        #média das diferenças
        l=np.mean(listKnowing[:, 1:]-listKnowing[:, :-1],axis=1).astype(int)
        nextTrans=l+listKnowing[:,-1]
        l2=nextTrans-now#+np.random.randint(0,DeltaDelay*5,size=len(l))
        value=np.min(l2)
        #if(value<DeltaDelay and value>-(qtde_nodes*DeltaDelay)):
        if(value<(2*DeltaDelay)):
            #print(l, np.argmin(l2))
            return np.argmin(l2)
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
        #print("F ", end='')
        return AuxNode
        

DisciplinaServico="knowingstd" #FIFO, knowing, knowingstd, hibrid, random
started_waiting_at = micros()
started_waiting_at2 = micros()#checar nós caidos
started_waiting_at3 = micros()#atualizacão forcada
AuxNode=0
aux=0
nodePoll=0
nodePollPast=0
PacketsSend=0
AttTableTime=3 #minutos
# forever loop

while 1:
    if (micros() - started_waiting_at > min([500000*qtde_nodes,2000000])): #novas conexoes a cada 10segundos
        newConnections()
        started_waiting_at = micros()
    if (micros() - started_waiting_at2 > TIMETORECONNECT*1000/2):#verifica nós caídos
        checkLostNodes()
        started_waiting_at2 = micros()
    if (micros() - started_waiting_at3 > AttTableTime*60000000):#atualiza a tabela com fifo
        print("Timout Atualizando Tabela")
        listKnowing[-1][-1]=0
        started_waiting_at3 = micros()
        #resultFile.close()
        #resultFile = open((datastr+".txt"),'w')
        

    if(qtde_nodes>0):
        nodePoll=Polling(DisciplinaServico)
        if (nodePoll != -1):
            sendToken(list_nodes[nodePoll])
            nodePollPast=nodePoll
            




