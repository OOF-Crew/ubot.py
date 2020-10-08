import datetime,config,urllib.parse,urllib.request,asyncio,os

import logging
import matplotlib.pyplot as plt
from telethon.sync import TelegramClient,events
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',level=logging.WARNING)

while True:
    scelta=input("\nVuoi utilizzare le attuali impostazioni? [S/N]\n")
    if (scelta=="S" or scelta=="s"):
        break
    elif (scelta=="N" or scelta=="n"):
        config.setNomeSessione(input("\nInserisci il nome della sessione. Valore attuale: "+config.nomeSessione+"\n"))
        config.setApiId(input("\nInserisci l'API ID. Valore attuale: "+str(config.apiId)+"\n"))
        config.setApiHash(input("\nInserisci l'API hash. Valore attuale: "+config.apiHash+"\n"))
        config.setNome(input("\nInserisci il tuo nome utente. Valore attuale: "+config.nomeUtente+"\n"))
        config.setIntervalloSpam(input("\nInserisci l'intervallo in secondi tra un messaggio di spam e l'altro. Valore attuale: "+str(config.intervalloSpam)+"\n"))
        break
    else:
        print("\nNon penso di aver capito\n")
client = TelegramClient(config.nomeSessione, config.apiId, config.apiHash)

lgb=False
spamRepeat=False
lgc=False
lgbFerma=False
fatto=False
esecuzione=False

#Funzione che invia un grafico delle ricerche eseguite su google dei parametri passati
@client.on(events.NewMessage(outgoing=True, pattern=r'\.help',from_users='me'))
async def help(update):
    chatid=await update.message.get_chat()
    await client.send_message(chatid,"""Elenco dei comandi:
    
    `.ping` -> Pong
    `.trends [parametro1,parametro2,...]` -> Grafico delle volte che sono stati cercati i parametri su Google
    `.file [percorso]` -> Invia il file indicato
    `.lmgtfy [keywords]` -> Automatizza la generazione di un link su lmgtfy
    `.calc [operazione]` -> Resituito il risultato dell'operazione
    `.id` -> Mette nei messaggi salvati l'id del mittente del messaggio a cui si sta rispondendo""")

#Funzione che invia un grafico delle ricerche eseguite su google dei parametri passati
@client.on(events.NewMessage(outgoing=True, pattern=r'\.trends',from_users='me'))
async def trends(update):
    messaggio=update.message.message[7:].split(',')
    chatid=await update.message.get_chat()
    pytrends.build_payload(messaggio, cat=0, timeframe='today 5-y', geo='', gprop='')
    data=pytrends.interest_over_time()
    for i in messaggio:
        plt.plot(data[i],label=i)
    plt.suptitle("Grafico delle ricerche")
    plt.xlabel("Anno")
    plt.legend()
    plt.savefig("trend.png")
    plt.close()
    await client.send_message(chatid,file="trend.png")
    os.remove("trend.png")
    
#Funzione che serve a inviare il file richiesto
@client.on(events.NewMessage(outgoing=True, pattern=r'\.file',from_users='me'))
async def inviaFile(update):
    messaggio=update.message.message
    chatid=await update.message.get_chat()
    await client.send_message(chatid,file=messaggio.split()[1])

#Funzione che automatizza la creazione di un link su lmgtfy
@client.on(events.NewMessage(outgoing=True, pattern=r'\.lmgtfy',from_users='me'))
async def lmgtfy(update):
    messaggio=update.message.message
    chatid=await update.message.get_chat()
    await client.send_message(chatid,"https://lmgtfy.app/?"+urllib.parse.urlencode({'q':messaggio[8:]}))

#Funzione che risolve un calcolo
@client.on(events.NewMessage(outgoing=True, pattern=r'\.calc', from_users='me'))
async def calc(update):
    chatid=await update.message.get_chat()
    await client.delete_messages(chatid,update.message)
    await client.send_message(chatid,str(eval(update.message.message[5:])))

#Ping pong
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ping', from_users='me'))
async def ping(update):
    chatid=await update.message.get_chat()
    await client.send_message(chatid,"Pong")

#PornHub
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ph', from_users='me'))
async def pornHub(update):
    chatid=await update.message.get_chat()
    await client.send_message(chatid,"⣿⣿⣿⣿⠉⠉⠉⠉⠉⠉⠉⢻⣿⣿⣿\n⣿⣿⣿⣿⣶⣶⡆⠀⣶⣶⠀⣿⣿⣿⣿\n⣿⣿⣿⣿⣿⣿⣧⡀⠙⠋⢀⣾⣿⣿⣿\n⣿⣿⣿⣿⣿⠟⠛⠛⢶⣶⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠁⣴⣶⣶⡀⢹⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣄⠈⠉⠉⢀⣼⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠿⠿⠶⠾⠿⢿⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣤⣤⣤⣤⠀⢺⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠛⠛⠛⠛⠒⢺⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⣶⣶⣶⣶⡄⢺⣿⣿⣿⣿⣿\n⣿⣿⣿⣿⠉⠉⠉⠉⣀⣼⣿⣿⣿⣿⣿\n⣿⡿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⢿⣿\n⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸\n⡇⠀⠀⠀⣶⣶⣶⣶⣶⣶⣶⡆⠀⠀⢸\n⡇⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢸\n⡇⠀⠀⠀⣤⣤⣤⣿⣧⣤⣤⡄⠀⠀⢸\n⡇⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢸\n⡇⠀⠀⠀⣾⡿⠿⠿⠿⠇⠀⠀⠀⠀⢸\n⡇⠀⠀⠀⣻⣦⣤⣤⣤⡄⠀⠀⠀⠀⢸\n⡇⠀⠀⠀⣛⣛⣛⣛⣛⣃⣀⡀⠀⠀⢸\n⡇⠀⠀⠀⣻⠿⠛⠻⣿⡛⠛⠃⠀⠀⢸\n⡇⠀⠀⠀⣿⣦⣤⣤⣿⡇⠀⠀⠀⠀⢸\n⡇⠀⠀⠀⠈⠉⠛⠋⠉⠀⠀⠀⠀⠀⢸\n⣷⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣾")

#Get ID
@client.on(events.NewMessage(outgoing=True, pattern=r'\.id', from_users='me'))
async def getId(event):
    if event.is_reply:
        sender=await event.get_reply_message()
        await client.send_message("me",str(sender.sender.id))

#Spam
@client.on(events.NewMessage(outgoing=True, pattern=r'\.spam',from_users='me'))
async def spam(update):
    global spamRepeat
    chatid=await update.message.get_chat()
    spamRepeat=True
    while spamRepeat:
        await client.send_message(chatid,'spam')
        await asyncio.sleep(config.intervalloSpam)

#Interrompi il comando spam
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ispam',from_users='me'))
async def ispam(update):
    global spamRepeat
    spamRepeat=False

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