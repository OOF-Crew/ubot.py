#Configurazione base
apiId=2705234
apiHash="004c9c7cca4e1e9abc26daa1c1d924c8"
nomeSessione="sessione"
nomeUtente="doggycheems"

#Variabili
intervalloSpam=6


#Funzioni

##Funzione che serve a impostare il nome utente
def setNome(nome):
    global nomeUtente
    nomeUtente=nome

##Funzione che serve a impostare l'API ID
def setApiId(numero):
    global apiId
    try:
        apiId=int(numero)
        return 0
    except:
        print("\nNon è stato possibile impostare il valore in quanto non è stato inserito un numero.\n")
        return 1

##Funzione che serve ad impostare l'API hash
def setApiHash(inputHash):
    global apiHash
    apiHash=str(inputHash)

##Funzione che serve ad impostare il nome della sessione
def setNomeSessione(nome):
    global nomeSessione
    nomeSessione=str(nome)

##Funzione che serve a impostare l'intervallo di spam
def setIntervalloSpam(numero):
    global intervalloSpam
    try:
        intervalloSpam=int(numero)
        return 0
    except:
        print("\nNon è stato possibile impostare il valore in quanto non è stato inserito un numero\n")
        return 1
