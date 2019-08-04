from random import choice, randint

class Igra:
    def __init__(self, seznam, runda = Runda()):
        self.igralci = seznam
        self.runda = runda
        self.dealer = 0

class Runda:
    def __init__(self):
        self.usedcards = []
        self.pot = 0
        self.side_pots = {}
        self.maxBet = 0
        self.board = []

def nova_runda(igra):
    igra.runda = Runda()

def naslednja_serija_stav(igra):
    igra.runda.maxBet = 0
    for el in igra.igralci:
        el.stava = 0

class Karta:
    def __init__(self):
        self.suit = choice(['C', 'D', 'H', 'S'])
        self.value = choice(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])

    def __str__(self):
        return '{}{}'.format(self.suit, self.value)

    def __repr__(self):
        return '{}{}'.format(self.suit, self.value)

class Hand:
    def __init__(self):
        self.karte = []
    
    def __str__(self):
        odgovor = 'Vaš hand je'
        for el in self.karte:
            odgovor += ' ' + str(el)
        return odgovor
    
class Player:
    def __init__(self, ime, stack, karte = []):
        self.ime = ime
        self.stack = stack
        self.karte = karte
        self.stava = 0
        self.total_bet = 0
        self.odstopil = False
        self.all_in = False

    def __str__(self):
        karte = ''
        for el in self.karte:
            karte += str(el) + ' '
        return '{} ima {}€, njegove karte so {}'.format(self.ime, self.stack, karte)


def naredi_karto(igra):
    while True:
        karta = Karta()
        if karta not in igra.runda.usedcards:
            igra.runda.usedcards.append(karta)
            return karta

def razdeli_karte(igra):
    seznam = []
    while len(seznam) < 2*len(igra.igralci):
        karta = naredi_karto(igra)
        seznam.append(karta)
    for el in igra.igralci:
        el.karte.append(seznam.pop())
        el.karte.append(seznam.pop())

def naredi_board(igra):
    seznam = []
    while len(seznam) != 5:
        karta = naredi_karto(igra)
        seznam.append(karta)
    igra.runda.board = seznam

def player_bet(igra, igralec, odgovor):
    igra.runda.maxBet = odgovor
    igra.runda.pot += odgovor
    igralec.stava = odgovor
    igralec.stack -= odgovor

def veljaven_bet(igra, igralec, odgovor):
    if igra.runda.maxBet > odgovor or odgovor > igralec.stack:
        return False
    return True

def player_allin(igra, igralec):
    if igralec.stack > igra.runda.maxBet:
        igra.runda.maxBet = igralec.stack
    igra.pot += igralec.stack
    igralec.stack = 0
    igralec.stava += igralec.stack
    igralec.all_in = True

def player_call(igra, igralec):
    calling_amount = igra.runda.maxBet - igralec.stava
    igralec.stack -= calling_amount
    igralec.stava += calling_amount
    igra.runda.pot += calling_amount

def player_fold(igralec):
    igralec.odstopil = True