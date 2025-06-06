import random 
import copy as c
from openpyxl import load_workbook

### ALAKITATLAN MEG
def niceprint(A, D, SWITCH):
    # D: NAPOK SZAMA
    # SWITCH 0: CSAK A DATUMHOZ TARTOZÓ ELEMEKET RAJZOLJA KI
    #        1: MINDEN ELEMET KIÍR PARAMÉTER SAVVAL EGYÜTT
    #        2: KÉRÉSEKHEZ ÍRJA KI A FIX NAPOKAT ÉS SZABADNAPOKAT
    #        3: SBO-S KIÍRAS
    P = len(A[0]) - D - 1  # PARAMÉTEREK SZAMA

    if SWITCH == 0:
        # NAPOK KEZD
        print('{:<18}{:<1}'.format(' ', '1'), end='  ')
        if len(A[0]) > 9:  # 9 FELETT 2 JEGYŰ SZAMOK MIATT MASKÉPP KELL KIÍRNI
            for i in range(2, 10):
                print(i, end='  ')
            for i in range(10, D + 1):
                print(i, end=' ')
        else:
            for i in range(2, D + 1):
                print(i, end='  ')
        print('')
        # NAPOK VÉGE
        # TÁBLAZAT KIÍRATASA KEZD
        for i in range(len(A)):
            print('{:<17}{:>1}'.format(A[i][0], '|'), end='')
            for j in range(len(A[i]) - D, len(A[i])):
                print(A[i][j], end='  ')
            print('')
        # TABLÁZAT KIÍRATÁSA VÉGE

    # TELJES TÁBLÁZATOT KIRAJZOLJA
    elif SWITCH == 1:
        # NAPOK KEZD     LIST a: ÁTMENETI DÁTUM TÖMB
        a = list(range(1, len(A[0])))
        if len(a) > D:
            for i in range(0, P):
                a[i] = 0
            for i in range(P, len(a)):
                a[i] = a[i] - P

        print('{:<18}{:<1}'.format(' ', a[0]), end='  ')
        if len(a) > P + 8:  # 9 FELETT 2 JEGYŰ SZÁMOK MIATT MÁSKÉPP KELL KIÍRNI
            for i in range(1, P + 8):
                print(a[i], end='  ')
            for i in range(P + 8, len(a)):
                print(a[i], end=' ')
        else:
            for i in range(1, len(a)):
                print(a[i], end='  ')
        print('')
        # NAPOK VÉGE
        # TÁBLÁZAT KIÍRATÁSA KEZD
        for i in range(len(A)):
            print('{:<17}{:>1}'.format(A[i][0], '|'), end=' ')

            for j in range(len(A[i]) - 1):
                print(A[i][j + 1], end='  ')
            print('')
        # TÁBLÁZAT KIÍRATÁSA VÉGE
        # KÉRÉSEK KIÍRATÁSA

    elif SWITCH == 2:
        # NAPOK KEZD
        print('{:<18}{:<1}'.format(' ', 'm'), end='  ')
        if len(A[0]) > 9:  # 9 FELETT 2 JEGYŰ SZÁMOK MIATT MÁSKÉPP KELL KIÍRNI
            for i in range(1, 10):
                print(i, end='  ')
            for i in range(10, D + 1):
                print(i, end=' ')
        else:
            for i in range(2, D + 1):
                print(i, end='  ')
        print('')
        # NAPOK VÉGE
        # TÁBLÁZAT KIÍRATÁSA KEZD
        for i in range(len(A)):
            print('{:<17}{:>1}'.format(A[i][0], '|'), end='')
            print(A[i][1], end='  ')
            for j in range(len(A[i]) - D, len(A[i])):
                if A[i][j] == 0:
                    print('x', end='  ')
                elif A[i][j] == 6:
                    print('n', end='  ')
                elif A[i][j] == 7:
                    print('e', end='  ')
                else:
                    print(' ', end='  ')
            print('')
        # TÁBLÁZAT KIÍRATÁSA VÉGE

    elif SWITCH == 3:
        time = list(range(len(A[0]) - D, len(A[0])))
        for i in time:
            print(i-1, end=' ')
            for j in range(len(A)):
                if A[j][i] == 6:
                    print('{:<17}{:>1}'.format(A[j][0], '|'), end='')
            for j in range(len(A)):
                if A[j][i] == 7:
                    print(A[j][0], end='')
            print('')


def graph_bipart_init (G, RANDOM):
    if RANDOM:
        for i in range(len(G)):
            if sum(item[1] for item in G[i]) == 0:
                tmp = list()
                for j in range(len(G[i])):
                    if G[i][j] == [1, 0] and sum(rows[j][1] for rows in G) == 0:
                        tmp.append(j)
                if len(tmp) > 0:
                    rand_item = random.choice(tmp)
                    G[i][rand_item][1] = 1
    else:
        for i in range(len(G)):
            if sum(item[1] for item in G[i]) == 0:
                for j in range(len(G[i])):
                    if G[i][j] == [1, 0] and sum(rows[j][1] for rows in G) == 0:
                        G[i][j][1] = 1
                        break


def hun_repair_init (G, A, B):
    OK = 0
    ### 0-AS INDEXU CSUCSOK KIJELOLESE
    for i in range(len(G)):
        if sum(item[1] for item in G[i]) == 0:
            A[i] = 0
            OK = 1

    ### 1-ES INDEXU CSUCSOK KIJELOLESE (MEG NEM LEHET JAVITO UT!)
    if OK:
        OK = 0
        for i in range(len(A)):
            if A[i] == 0:
                for j in range(len(G[0])):
                    if G[i][j] == [1, 0] and B[j] == -1:
                        B[j] = 1
                        OK = 1
    if OK:
        return 1
    else: 
        return 0


def hun_repair (G):
    A = list(-1 for i in range(len(G)))
    B = list(-1 for i in range(len(G[0])))

    OK = hun_repair_init(G, A, B)
    enum = 1
    FIND = 0

    ### MINDEN 2. LEPES UTAN VIZSGALUNK
    while OK:
        enum += 1
        OK = 0
        for j in range(len(B)):
            if B[j] == enum - 1:
                for i in range(len(G)):
                    if G[i][j] == [1, 1] and A[i] == -1:
                        A[i] = enum
                        OK = 1

        if OK:
            enum += 1
            OK = 0
            for i in range(len(A)):
                if A[i] == enum - 1:
                    for j in range(len(G[0])):
                        if G[i][j] == [1, 0] and B[j] == -1:
                            B[j] = enum
                            OK = 1

                            ### VIZSGALAT, HOGY VEGE LESZ-E AZ ALGORITMUSNAK
                            FIND = 1
                            for k in range(len(G)):
                                if G[k][j] == [1,1]:
                                    FIND = 0
                                    break
                            if FIND == 1:
                                last = j
        
        ### LEALLAS
        if FIND == 1:
            break


    ### JAVITAS VEGREHAJTASA
    ### ### MIVEL PARATLAN SOK ELET KELL ATIRNI,
    ### ### EZERT AZ ELSOT KIVUL, MAJD WHILE CILUSBAN 2-ESEVEL
    ### ### ATIRANDO EL MEGTALALASA A TOMB SEGITSEGEVEL TORTENIK
    if FIND:
        enum -= 1
        for i in range(len(A)):
            if G[i][last] == [1, 0] and A[i] == enum:
                G[i][last][1] = 2
                last = i
                break

        while enum > 0:
            ### GRAF MATRIXABAN VIZSZINTESEN CSAK 1 EL LEHET KIVALASZTVA, AZT ATIRJUK
            for j in range(len(G[last])):
                if G[last][j] == [1, 1]:
                    G[last][j][1] = 0
                    last_new = j
                elif G[last][j] == [1, 2]:
                    G[last][j][1] = 1
            last = last_new
            
            ### AZ ELOBB MEGTALALT EL OSZLOPABAN MEGKERESSUK A JAVITOELT A TOMB SEGITSEGEVEL
            enum -= 2
            for i in range(len(A)):
                if G[i][last] == [1, 0] and A[i] == enum:
                    G[i][last][1] = 2
                    last = i
                    break

        for i in range(len(G[last])):
            if G[last][i] == [1, 2]:
                G[last][i][1] = 1
        return 1

    return 0


def graph_max_match (G, RANDOM):
    graph_bipart_init(G, RANDOM)
    print("INIT")
    for i in G:
        print(i)
    print()
    while hun_repair(G):
        pass

def request_check (ORIG_TABLE):
    DAYS = len(ORIG_TABLE[0]) - 3
    ERROR = 0
    print('ELLENORZESEK')
    for i in ORIG_TABLE:
        print(i)
    print()
    ### ### ELLENORZES, HOGY PONTOSAN ANNYI KIOSZTANDO MUSZAK VAN-E AHANY NAP
    day_shift = 0
    night_shift = 0
    OK_day = 0
    OK_night = 0
    ### ### HA SZEREPEL A TABLAZATBAN -1, AKKOR AZT A PROGRAM FOGJA KITOLTENI
    ### ### UGYHOGY AKKOR AZ NEM LEHET BAJ, HOGY KEVESEBB MUSZAK VAN MEGADVA
    for i in range(len(ORIG_TABLE)):
        if ORIG_TABLE[i][1] != -1:
            day_shift += ORIG_TABLE[i][1]
        else:
            OK_day = 1
            
        if ORIG_TABLE[i][2] != -1:
            night_shift += ORIG_TABLE[i][2]
        else:
            OK_night = 1

    ### ### FELTETELEK NAPPALRA ES EJSZAKARA KULON
    if OK_day and day_shift <= 2*DAYS:
        pass
    elif !OK_day and day_shift == 2*DAYS:
        OK_day = 1
    elif !OK_day and day_shift != 2*DAYS:
        pass

    if OK_night and night_shift <= DAYS:
        pass
    elif !OK_night and night_shift == DAYS:
        OK_night = 1
    elif !OK_night and night_shift != DAYS:
        pass


    ### ### ELLENORZES, HOGY NEM ADTAK-E EGY EMBERNEK TOBB FIX NAPOT
    ### ### NAPPALRA VAGY EJSZAKARA, MINT AMENNYIT LEHETNE
    ### ### ES 
    ### ### ELLENORZES, HOGY NEM ADTAK-E VALAKINEK
    ### ### EJSZAKA UTAN NAPPALT 
    for row in range(len(ORIG_TABLE)):
        s = 0
        for day in range(DAYS):
            if ORIG_TABLE[row][day + 3] in {'n', 'N'}:
                s += 1
                if ORIG_TABLE[row][day + 2] in {'é', 'É'}:
                    ERROR = 1
                    print(ORIG_TABLE[row][0], day + 1, 'DATE: ALERT DAY AFTER NIGHT!!!')
        if s > ORIG_TABLE[row][1]:
            ERROR = 1
            print(ORIG_TABLE[row][0], ': ALERT DAY!!!')

        s = 0
        for night in range(DAYS):
            if ORIG_TABLE[row][night + 3] in {'é', 'É'}:
                s += 1
        if s > ORIG_TABLE[row][2]:
            ERROR = 1
            print(ORIG_TABLE[row][0], ': ALERT NIGHT!!!')

    ### ### ELLENORZES, HOGY NEM OSZTOTTAK-E BE TOBB EMBERT EGY NAPON
    ### ### NAPPALRA VAGY EJSZAKARA, MINT AMENNYIT LEHETNE
    for day in range(3,len(ORIG_TABLE[0])):
        s_day = 0
        s_night = 0
        for people in range(len(ORIG_TABLE)):
            if ORIG_TABLE[people][day] in {'n', 'N'}:
                s_day += 1
            if ORIG_TABLE[people][day] in {'é', 'É'}:
                s_night += 1
        if s_day > 2:
            ERROR = 1
            print(day - 2, 'ALERT DAY SHIFT!!!')
        if s_night > 1:
            ERROR = 1
            print(day - 2, 'ALERT NIGHT SHIFT!!!')

    if ERROR:
        return 0
    return 1


def main():
    ### XLSX IMPORTALASA
    workbook = load_workbook(filename="./requests_admin.xlsx")
    
    # ELSO SHEET
    worksheet = workbook.worksheets[0]

    # 2D-S LISTAVA KONVERTALAS
    row_list = []
    for r in worksheet.rows:
        column = [cell.value for cell in r]
        row_list.append(column)

    # NAPOK SZAMA
    DAYS = row_list[0][1]
    ORIG_TABLE = [row[0:DAYS + 3] for row in row_list[3:len(row_list)]]

    # HETVEGEK DATUMAINAK GENERALESA KEZD.
    SATURDAY = row_list[1][1]
    sat = []
    sun = []
    if SATURDAY == 7:
        sun.append(1)
    while SATURDAY <= DAYS:
        sat.append(SATURDAY)
        if SATURDAY != DAYS:
            sun.append(SATURDAY + 1)
        SATURDAY += 7

    # HETVEGEK EREDETI DATUMAHOZ!!! HALMAZOK LETREHOZASA
    sat_orig = set(sat)
    sun_orig = set(sun)

    # TIME (DATUMOK) LISTABAN INDEXELES!!! MIATT 1-GYEL CSOKKENTES
    for i in range(len(sat)):
        sat[i] -= 1
    for i in range(len(sun)):
        sun[i] -= 1
    # HETVEGEK DATUMAINAK GENERALASA VEGE


    ### ELLENORZESEK
    if request_check(ORIG_TABLE) == 0:
        return 0

    ### GRAF LETREHOZASA
    G_ORIG = 0
main()
