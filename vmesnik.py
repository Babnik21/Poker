from model import Karta, Igra, Player, Hand, Runda, Peterka
import model

def pridobi_stack():
    stack = input('Vpišite stack igralca: ')
    if stack.count('.') > 1 or len(stack) == 0:
        print('Neveljaven vnos!')
        return pridobi_stack()
    for el in stack:
        if el not in '1234567890.':
            print('Neveljaven vnos!')
            return pridobi_stack()
    return float(stack)

def pridobi_igralce():
    seznam = []
    nadaljuj = True
    while nadaljuj and len(seznam) < 9:
        print('Ali želite dodati igralca?')
        print('1) Da')
        print('2) Ne')
        odgovor = input('> ')
        if odgovor == '2':
            nadaljuj = False
        elif odgovor == '1':
            ime = input('Vpišite ime igralca: ')
            stack = pridobi_stack()
            seznam.append(Player(ime, stack))
        else:
            print('Neveljaven odgovor!')
            pass
    return seznam

def poteza(igra, igralec):
    igralec.bil_na_potezi = True
    if igralec.stava == igra.maxBet:
        poteza_check(igralec)
    else:
        poteza_call(igralec)


def poteza_check(igralec):
    print('Vi ste na potezi. Kaj želite narediti?')
    print('1) Fold')
    print('2) Bet/Raise')
    print('3) Check')
    print('4) All in')
    odgovor = input('> ')
    if len(odgovor) != 1 or odgovor not in '1234':
        print('Neveljaven odgovor!')
        return poteza_check(igralec)
    else:
        return int(odgovor)

def poteza_call(igralec):
    print('Vi ste na potezi. Kaj želite narediti?')
    print('1) Fold')
    print('2) Bet/Raise')
    print('3) Call')
    print('4) All in')
    odgovor = input('> ')
    if len(odgovor) != 1 or odgovor not in '1234':
        print('Neveljaven odgovor!')
        return poteza_call(igralec)
    else:
        return int(odgovor)


def serija_stav(igra):
    for igralec in igra.igralci:
        if not igralec.odstopil:
            poteza(igra, igralec)

def game(igra):
    return None

def intro():
    print('Dobrodosli v moji igri!')

def program():
    intro()
    igralci = pridobi_igralce()
    igra = Igra(igralci)
    while True:
        game(igra)





program()
