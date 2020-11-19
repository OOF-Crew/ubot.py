import datetime,config,urllib.parse,urllib.request,asyncio,os

import logging
from telethon.sync import TelegramClient,events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from pytrends.request import TrendReq

#Life Games ~ Coins wholesome
@client.on(events.NewMessage(outgoing=True, pattern=r'\.lgc', from_users='me'))
async def lifeGamesCoins(update):
    global lgc
    chatid=await update.message.get_chat()
    lgc=True
    await client.send_message(chatid,"Sstatus")

#Life Games ~ Ferma bet durante il bonus
@client.on(events.NewMessage(incoming=True))
async def lifeGamesBonusStop(update):
    global lgb
    global lgbFerma
    messaggio=update.message.message
    if ("🚫 "+config.nomeUtente+" you can't bet coins that you don't own!" in messaggio) and update.message.from_id==819560568 and lgb:
        lgbFerma=True

#Life Games ~ Funzione che fa bettare automaticamente il doppio del numero  inserito
@client.on(events.NewMessage(outgoing=True, pattern=r'\.double', from_users='me'))
async def double(update):
    messaggio=update.message.message
    chatid=await update.message.get_chat()
    await client.delete_messages(chatid,update.message)
    await asyncio.sleep(.5)
    await client.send_message(chatid,"Bbet "+str(int(togliPunti(messaggio[7:]))*2))

#LifeGames ora bonus ~ Inizio
@client.on(events.NewMessage(outgoing=True, pattern=r'\.lgb', from_users='me'))
async def lifeGamesBonus(update):
    global lgb
    lgb=True
    await lifeGamesBonusBet()

#LifeGames ora bonus ~ Ferma manualmente
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ilgb', from_users='me'))
async def stopLifeGamesBonus(update):
    global lgb
    lgb=False

#LifeGames ~ Comando Status
@client.on(events.NewMessage(incoming=True))
async def lifeGamesStatus(update):
    global lgb
    global lgbFerma
    global lgc
    global fatto
    global esecuzione
    chatid=await update.message.get_chat()
    if (("Informations of "+config.nomeUtente) in update.message.message) and update.message.from_id==819560568 and lgb and esecuzione==False:
        fatto=True
        parole=funzioneZero(int(togliPunti(update.message.message.split()[46]))//3)
        for count in range(0,19):
            if datetime.datetime.now().hour==21:
                esecuzione=True
                if lgbFerma==True:
                    lgbFerma=False
                    fatto=False
                    esecuzione=False
                    await lifeGamesBonusBet()
                    break
                await client.send_message(-1001365440323,"Bbet "+str(parole))
                await asyncio.sleep(7)
        esecuzione=False
        fatto=False
        await lifeGamesBonusBet()
    elif (("Informations of "+config.nomeUtente) in update.message.message) and (update.message.from_id==819560568 or update.message.from_id==1094814227) and lgc:
        await asyncio.sleep(7)
        await client.send_message(chatid,"Bbet "+str(complementare(togliPunti(update.message.message.split()[46][2:]))))
        lgc=False

#Funzione che controlla se effettivamente LifeGames ha ricevuto la richiesta di stampare lo status
async def controlloStatus():
    global fatto
    global esecuzione
    await asyncio.sleep(7)
    while fatto==False and esecuzione==False:
        await asyncio.sleep(7)
        await client.send_message(-1001365440323,'Sstatus')

#LifeGames ora bonus ~ Bet
async def lifeGamesBonusBet():
    global lgb
    global esecuzione
    if datetime.datetime.now().hour==21 and lgb and esecuzione==False:
        await asyncio.sleep(7)
        await client.send_message(-1001365440323,'Sstatus')
        await controlloStatus()

#Funzione che genera il numero di coins da bettare
def complementare(numero):
    cifre="1"
    for count in range(0,len(numero)):
        cifre=cifre+"0"
    return (int(cifre)-int(numero))

#Funzione per sostituire le cifre di un numero con 0 tranne le prime 2
def funzioneZero(numero):
    numero=str(numero)
    stringaNumero=numero[0:2]
    for count in range(0,len(numero)-2):
        stringaNumero+="0"
    return int(stringaNumero)

#Funzione che toglie i punti
def togliPunti(numero):
    return numero.replace(".","")


client.start()
print("\nBot online!\nPer un elenco dei comandi invia un messaggio con scritto `.help`")
client.run_until_disconnected()
