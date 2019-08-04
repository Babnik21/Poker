from random import choice, randint

class Igra:
    def __init__(self, seznam, runda = Runda()):
        self.igralci = seznam
        self.runda = runda
        self.dealer = 0

    def nova_runda(self):
        self.runda = Runda()

class Runda:
    def __init__(self):
        self.usedcards = []
        self.pot = 0
        self.side_pots = {}
        self.maxBet = 0
        self.board = []

def naslednja_serija_stav(igra):
    igra.runda.maxBet = 0
    for el in igra.igralci:
        el.stava = 0

slovar_vrednosti = {
    '2' : 2,
    '3' : 3,
    '4' : 4,
    '5' : 5,
    '6' : 6,
    '7' : 7,
    '8' : 8,
    '9' : 9,
    'T' : 10,
    'J' : 11,
    'Q' : 12,
    'K' : 13,
    'A' : 14
    }

class Karta:
    def __init__(self):
        self.suit = choice(['C', 'D', 'H', 'S'])
        self.value = choice(['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'])

    def __str__(self):
        return '{}{}'.format(self.suit, self.value)

    def __repr__(self):
        return '{}{}'.format(self.suit, self.value)

    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

    def __gt__(self, other):
        return slovar_vrednosti[self.value] > slovar_vrednosti[other.value]

    def __lt__(self, other):
        return slovar_vrednosti[self.value] < slovar_vrednosti[other.value]

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
        self.peterka = []

    def __str__(self):
        karte = ''
        for el in self.karte:
            karte += str(el) + ' '
        return '{} ima {}€, njegove karte so {}'.format(self.ime, self.stack, karte)


class Peterka:
    def __init__(self, seznam):
        self.karte = seznam
        self.jakost = 0

    def pridobi_vrednosti(self):
        seznam = []
        for el in self.karte:
            seznam.append(slovar_vrednosti[el.value])
        return seznam

    def update_jakost(self):
        self.jakost = pridobi_jakost(self)

    def je_par(self):
        sez_vrednosti = self.pridobi_vrednosti()
        for el in sez_vrednosti:
            if sez_vrednosti.count(el) == 2:
                return True
        return False

    def je_dva_para(self):
        sez_vrednosti = self.pridobi_vrednosti()
        st_parov = 0
        for el in sez_vrednosti:
            if sez_vrednosti.count(el) == 2:
                st_parov += 1
        return st_parov == 4

    def je_tris(self):
        sez_vrednosti = self.pridobi_vrednosti()
        for el in sez_vrednosti:
            if sez_vrednosti.count(el) == 3:
                return True
        return False

    def je_lestvica(self):
        sez_vrednosti = self.pridobi_vrednosti()
        sez_vrednosti.sort()
        i = 0
        for el in sez_vrednosti:
            if el != sez_vrednosti[0] + i:
                return sez_vrednosti == [2, 3, 4, 5, 14]
            i += 1
        return True

    def je_barva(self):
        barva = self.karte[0].suit
        for el in self.karte:
            if el.suit != barva:
                return False
        return True

    def je_full_house(self):
        sez_vrednosti = self.pridobi_vrednosti()
        for el in sez_vrednosti:
            if sez_vrednosti.count(el) not in [2, 3]:
                return False
        return True
        
    def je_quads(self):
        sez_vrednosti = self.pridobi_vrednosti()
        for el in sez_vrednosti:
            if sez_vrednosti.count(el) == 4:
                return True
        return False

    def je_straight_flush(self):
        return self.je_barva() and self.je_lestvica()
    
    def je_royal_flush(self):
        return self.je_straight_flush() and 14 in self.pridobi_vrednosti()

    def rangiraj(self):
        if self.je_royal_flush():
            self.jakost = 10
        elif self.je_straight_flush():
            self.jakost = 9
        elif self.je_quads():
            self.jakost = 8
        elif self.je_full_house():
            self.jakost = 7
        elif self.je_barva():
            self.jakost = 6
        elif self.je_lestvica():
            self.jakost = 5
        elif self.je_tris():
            self.jakost = 4
        elif self.je_dva_para():
            self.jakost = 3
        elif self.je_par():
            self.jakost = 2
        else:
            self.jakost = 1

    def __eq__(self, other):
        sez_vrednosti_self = self.pridobi_vrednosti()
        sez_vrednosti_other = other.pridobi_vrednosti()
        return self.jakost == other.jakost and sez_vrednosti_self == sez_vrednosti_other

    def __gt__(self, other):
        if not self.jakost == other.jakost:
            return self.jakost > other.jakost
        else:
            if self.jakost in [9, 1, 5, 6]:
                return boljsi_nista(self, other)
            elif self.jakost == 2:
                return boljsi_par(self, other)
            elif self.jakost == 3:
                return boljsi_dva_para(self, other)
            elif self.jakost in [4, 7]:
                return boljsi_tris(self, other)
            else:
                return boljsi_quads(self, other)
            assert False

    def __lt__(self, other):
        if not self.jakost == other.jakost:
            return self.jakost < other.jakost
        else:
            if self.jakost in [9, 1, 5, 6]:
                return boljsi_nista(other, self)
            elif self.jakost == 2:
                return boljsi_par(other, self)
            elif self.jakost == 3:
                return boljsi_dva_para(other, self)
            elif self.jakost in [4, 7]:
                return boljsi_tris(other, self)
            else:
                return boljsi_quads(other, self)
            assert False

def pridobi_jakost(peterica):
    if peterica.je_royal_flush():
        return 10
    elif peterica.je_straight_flush():
        return 9
    elif peterica.je_quads():
        return 8
    elif peterica.je_full_house():
        return 7
    elif peterica.je_barva():
        return 6
    elif peterica.je_lestvica():
        return 5
    elif peterica.je_tris():
        return 4
    elif peterica.je_dva_para():
        return 3
    elif peterica.je_par():
        return 2
    else:
        return 1

def boljsi_nista(self, other):
    sez_vrednosti_self = self.pridobi_vrednosti()
    sez_vrednosti_other = other.pridobi_vrednosti()
    sez_vrednosti_self.sort()
    sez_vrednosti_other.sort()
    i = -1
    while i > -6:
        if sez_vrednosti_self[i] > sez_vrednosti_other[i]:
            return True
        elif sez_vrednosti_self[i] < sez_vrednosti_other[i]:
            return False
        i -= 1
    assert False
        
def boljsi_par(self, other):
    sez_vrednosti_self = self.pridobi_vrednosti()
    sez_vrednosti_other = other.pridobi_vrednosti()
    self_par = 0
    other_par = 0
    for el in sez_vrednosti_self:
        if sez_vrednosti_self.count(el) == 2:
            self_par = el
            break
    for el in sez_vrednosti_other:
        if sez_vrednosti_other.count(el) == 2:
            other_par = el
            break
    if self_par > other_par:
        return True
    elif self_par < other_par:
        return False
    else:
        return boljsi_nista(self, other)

def boljsi_dva_para(self, other):
    sez_vrednosti_self = sorted(self.pridobi_vrednosti())
    sez_vrednosti_other = sorted(other.pridobi_vrednosti())
    self_par_nizji = sez_vrednosti_self[1]
    self_par_visji = sez_vrednosti_self[3]
    other_par_nizji = sez_vrednosti_other[1]
    other_par_visji = sez_vrednosti_other[3]
    if self_par_visji > other_par_visji:
        return True
    elif self_par_visji < other_par_visji:
        return False
    if self_par_nizji > other_par_nizji:
        return True
    elif self_par_nizji < other_par_nizji:
        return False
    else:
        return boljsi_nista(self, other)

def boljsi_tris(self, other):
    sez_vrednosti_self = self.pridobi_vrednosti()
    sez_vrednosti_other = other.pridobi_vrednosti()
    self_tris = 0
    other_tris = 0
    for el in sez_vrednosti_self:
        if sez_vrednosti_self.count(el) == 3:
            self_tris = el
            break
    for el in sez_vrednosti_other:
        if sez_vrednosti_other.count(el) == 3:
            other_tris = el
            break
    if self_tris > other_tris:
        return True
    elif self_tris < other_tris:
        return False
    else:
        return boljsi_nista(self, other)

def boljsi_quads(self, other):
    sez_vrednosti_self = self.pridobi_vrednosti()
    sez_vrednosti_other = other.pridobi_vrednosti()
    self_quads = 0
    other_quads = 0
    for el in sez_vrednosti_self:
        if sez_vrednosti_self.count(el) == 4:
            self_quads = el
            break
    for el in sez_vrednosti_other:
        if sez_vrednosti_other.count(el) == 4:
            other_quads = el
            break
    if self_quads > other_quads:
        return True
    elif self_quads < other_quads:
        return False
    else:
        return boljsi_nista(self, other)




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
    if igra.runda.maxBet - igralec.stava > odgovor or odgovor > igralec.stack:
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