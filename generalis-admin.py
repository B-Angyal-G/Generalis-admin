import random
import copy as c
from openpyxl import load_workbook


### SIMPLE GRAF (EJJELES MUSZAKOK) GENERALASA
def graph_bipart_init(G):
    for i in range(len(G)):
        if sum(item[1] for item in G[i]) == 0:
            tmp = list()
            for j in range(len(G[i])):
                if G[i][j] == [1, 0] and sum(rows[j][1] for rows in G) == 0:
                    tmp.append(j)
            if len(tmp) > 0:
                rand_item = random.choice(tmp)
                G[i][rand_item][1] = 1

def hun_repair_init(G, A, B):
    ### UA SIMPLE ES DOUBLE ESETEKBEN
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

def hun_repair(G):
    A = list(-1 for i in range(len(G)))
    B = list(-1 for i in range(len(G[0])))

    OK = hun_repair_init(G, A, B)
    IFEND = OK
    enum = 1
    FIND = 0

    ### MINDEN 2. LEPES UTAN VIZSGALUNK
    while OK:
        enum += 1
        OK = 0
        for j in range(len(B)):
            if B[j] == enum - 1:
                for i in range(len(G)):
                    ### VAN EL ES MEG NEM JELOLTUK MEG A HOZZA TARTOZO CSUCSOT
                    if G[i][j] == [1, 1] and A[i] == -1:
                        A[i] = enum
                        OK = 1

        if OK:
            enum += 1
            OK = 0
            for i in range(len(A)):
                if A[i] == enum - 1:
                    for j in range(len(G[0])):
                        ### VAN EL ES MEG NEM JELOLTUK MEG A HOZZA TARTOZO CSUCSOT
                        if G[i][j] == [1, 0] and B[j] == -1:
                            B[j] = enum
                            OK = 1

                            ### VIZSGALAT, HOGY VEGE LESZ-E AZ ALGORITMUSNAK
                            FIND = 1
                            for k in range(len(G)):
                                if G[k][j] == [1, 1] or G[k][j] == [1, 4]:
                                    FIND = 0
                                    break
                            if FIND == 1:
                                last = j
                                break
                if FIND:
                    break

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

    if IFEND:
        return -1
    else:
        return 0

def graph_max_match(G):
    graph_bipart_init(G)
    REPAIR = hun_repair(G)
    while REPAIR == 1:
        REPAIR = hun_repair(G)
    if REPAIR == -1:
        return 0
    return 1



### DOUBLE GRAF (NAPPALOS MUSZAKOK) GENERALASA
def graph_bipart_double_init(G, shifts, admins):
    for row in range(len(G)):
        SKIP = 0
        tmp = list()
        for col in range(len(G[0])):
            if G[row][col][1] in {1, 4}:
                SKIP = 1
                admins[col].add(whois(row, shifts))
            if len(admins[col]) < 2 and G[row][col] == [1, 0]:
                if whois(row, shifts) not in admins[col]:
                    tmp.append(col)
        if not SKIP:
            if len(tmp) != 0:
                day = random.choice(tmp)
                G[row][day][1] = 1
                admins[day].add(whois(row, shifts))

def hun_repair_double_init(G, A, B, shifts, admins):
    ### MAS MINT A SIMPLE ESET, MERT A KIMARADT 0-AS INDEXU CSUCSOKBOL
    ### OLYAN CSUCSBA NEM HUZHATUNK ELT, AMELYIKKEL OSSZE VAN KOTVE OLYAN EL,
    ### AMELYIK UGYANAHHOZ AZ ADMINHOZ TARTOZIK, VAGYIS WHOIS() BENNE VAN ADMINS-BAN
    OK = 0
    ### 0-AS INDEXU CSUCSOK KIJELOLESE
    for i in range(len(G)):
        if sum(item[1] for item in G[i]) == 0:
            A[i] = 0
            OK = 1

    ### 1-ES INDEXU CSUCSOK KIJELOLESE (MEG NEM LEHET JAVITO UT!)
    if OK:
        OK = 0
        for row in range(len(A)):
            if A[row] == 0:
                for col in range(len(G[0])):
                    if G[row][col] == [1, 0] and B[col] == -1 and whois(row, shifts) not in admins[col]:
                        B[col] = 1
                        OK = 1
    if OK:
        return 1
    else:
        return 0

def hun_repair_double(G, shifts, admins):
    A = list(-1 for i in range(len(G)))
    B = list(-1 for i in range(len(G[0])))

    ### UA MINT SIMPLE ESETBEN
    OK = hun_repair_double_init(G, A, B, shifts, admins)
    enum = 1
    FIND = 0

    ### MINDEN 2. LEPES UTAN VIZSGALUNK
    while OK:
        enum += 1
        OK = 0
        for j in range(len(B)):
            if B[j] == enum - 1:
                for i in range(len(G)):
                    ### VAN EL ES MEG NEM JELOLTUK MEG A HOZZA TARTOZO CSUCSOT
                    if G[i][j] == [1, 1] and A[i] == -1:
                        A[i] = enum
                        OK = 1

        if OK:
            enum += 1
            OK = 0
            for row in range(len(A)):
                if A[row] == enum - 1:
                    for col in range(len(G[0])):
                        ### VAN EL ES MEG NEM JELOLTUK MEG A HOZZA TARTOZO CSUCSOT
                        if G[row][col] == [1, 0] and B[col] == -1:
                            B[col] = enum
                            OK = 1

                            ### VIZSGALAT, HOGY VEGE LESZ-E AZ ALGORITMUSNAK
                            FIND = 0
                            s_edge = 0
                            for k in range(len(G)):
                                if G[k][col] == [1, 1] or G[k][col] == [1, 4]:
                                    s_edge += 1
                            if s_edge < 2:
                                FIND = 1
                                last = col
                                break
                    if FIND:
                        break

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

def graph_double_max_match(G, shifts, admins):
    graph_bipart_double_init(G, shifts, admins)
    while hun_repair_double(G, shifts, admins):
        pass


### KOZOS HASZNALATU FUGGVENYEK
def make_graph(ORIG_TABLE, admins, shifts, SHIFT, DAYS):
    ### GRAFOK LETREHOZASA
    ### ### TABLAZATBA IRHATO JELEK CSOPORTOSITASA
    day_exception_current = {'x', 'X', 'y', 'Y', 'xn', 'xN', 'XN', 'Xn', 'nx', 'nX', 'Nx', 'NX', 'e', 'E', 'é', 'É'}
    day_exception_prev = {'e', 'E', 'é', 'É'}
    night_exception_current = {'x', 'X', 'y', 'Y', 'xe', 'xE', 'XE', 'Xe', 'ex', 'eX', 'Ex', 'EX', 'n', 'N',
                               'xé', 'xÉ', 'XÉ', 'Xé', 'éx', 'éX', 'Éx', 'ÉX'}
    night_exception_next = {'x', 'X', 'xn', 'xN', 'XN', 'Xn', 'nx', 'nX', 'Nx', 'NX', 'n', 'N'}

    ### ORIG_TABLE_REQ AZ ADOTT MUSZAKRA VONATKOZO KERESEKET TARTALMAZZA
    ### ### NEM LEHET NAPPALOS, HA AZNAP VAGY ELOTTE NAP EJSZAKAS
    ### ### NEM LEHET EJSZAKAS, HA AZNAP VAGY UTANA NAP NAPPALOS
    ORIG_TABLE_REQ = list(range(len(ORIG_TABLE)))
    if SHIFT == 'DAY':
        for row in range(len(ORIG_TABLE_REQ)):
            ORIG_TABLE_REQ[row] = [[1, 0] for j in range(DAYS)]
            for col in range(DAYS):
                if ORIG_TABLE[row][col + 3] in day_exception_current:
                    ORIG_TABLE_REQ[row][col][0] = 0
                if ORIG_TABLE[row][col + 3] in {'n', 'N'}:
                    ORIG_TABLE_REQ[row][col][1] = 4
                    admins[col].add(row)
                if ORIG_TABLE[row][col + 2] in day_exception_prev:
                    ORIG_TABLE_REQ[row][col][0] = 0
    if SHIFT == 'NIGHT':
        for i in range(len(ORIG_TABLE_REQ)):
            ORIG_TABLE_REQ[i] = [[1, 0] for j in range(DAYS)]
            for j in range(DAYS):
                if ORIG_TABLE[i][j + 3] in night_exception_current:
                    ORIG_TABLE_REQ[i][j][0] = 0
                if ORIG_TABLE[i][j + 3] in {'e', 'E'}:
                    ORIG_TABLE_REQ[i][j][1] = 4
                if j + 4 < len(ORIG_TABLE[0]):
                    if ORIG_TABLE[i][j + 4] in night_exception_next:
                        ORIG_TABLE_REQ[i][j][0] = 0

    ### ORIG_GRAPH AZ ADOTT MUSZAKNAK MEGFELELO GRAF
    ### AMIBEN MINDEN EMBER ANNYISZOR SZEREPEL MAR, AHANY MUSZAKJA VAN
    ### ### shifts A MUSZAKNAK MEGFELELO BEOSZTASSZAMOKAT TARTALMAZZA
    index = 0
    ORIG_GRAPH = list(range(sum(shifts)))
    for i in range(len(ORIG_TABLE_REQ)):
        for j in range(shifts[i]):
            ORIG_GRAPH[index] = c.deepcopy(ORIG_TABLE_REQ[i])
            index += 1

    ### ### FIX NAPOK BEIRASA/JAVITASA
    admin_index = 0
    for s in range(len(shifts)):
        serial_num = 0
        for col in range(len(ORIG_GRAPH[0])):
            if ORIG_GRAPH[admin_index][col][1] == 4:
                for row in range(admin_index, admin_index + shifts[s]):
                    if row != serial_num + admin_index:
                        ORIG_GRAPH[row][col][1] = 0
                serial_num += 1
        ### ### HA A LEGUTOLSO ADMINNAL 0 SZEREPEL MUSZAKSZAMNAK,
        ### ### AKKOR MAR NEM KELL NOVELNI, KULONBEN KIINDEXEL A GRAFBOL
        if s < len(shifts) - 1:
            if shifts[s + 1] != 0:
                admin_index += shifts[s]

    return ORIG_GRAPH

def graph_merge(graph_day, graph_night, day_shifts, night_shifts, admins, DAYS):
    ### VEGSO TABLAZAT, ELSO OSZLOPA AZ ADMINOK NEVEI
    final_table = [[admin] for admin in admins]
    for i in range(len(final_table)):
        final_table[i] += (list('' for j in range(DAYS)))

    ### NAPPALOS MUSZAKOK EGYBE IRASA
    for row in range(len(graph_day)):
        for col in range(len(graph_day[row])):
            if graph_day[row][col][1] in {1, 4}:
                final_table[whois(row, day_shifts)][col + 1] = 'N'

    ### EJSZAKAS MUSZAKOK EGYBE IRASA
    for row in range(len(graph_night)):
        for col in range(len(graph_night[row])):
            if graph_night[row][col][1] in {1, 4}:
                final_table[whois(row, night_shifts)][col + 1] = 'E'

    return final_table

def whois(row, shifts):
    s = 0
    for i in range(len(shifts)):
        s += shifts[i]
        if s > row:
            return i



### ELLENORZESEK
def request_check(ORIG_TABLE):
    DAYS = len(ORIG_TABLE[0]) - 3
    ERROR = 0

    ### ### ELLENORZES, HOGY PONTOSAN ANNYI KIOSZTANDO MUSZAK VAN-E AHANY NAP
    day_shift = 0
    night_shift = 0
    for i in range(len(ORIG_TABLE)):
        day_shift += ORIG_TABLE[i][1]
        night_shift += ORIG_TABLE[i][2]

    ### ### FELTETELEK NAPPALRA ES EJSZAKARA KULON
    if day_shift < 2 * DAYS:
        print('ALERT!!! Nappalra kevesebb műszak van beírva, mint szükséges!')
        ERROR = 1
    elif day_shift > 2 * DAYS:
        print('ALERT!!! Nappalra több műszak van beírva, mint szükséges!')
        ERROR = 1

    if night_shift < DAYS:
        print('ALERT!!! Éjszakára kevesebb műszak van beírva, mint szükséges!')
        ERROR = 1
    elif night_shift > DAYS:
        print('ALERT!!! Éjszakára több műszak van beírva, mint szükséges!')
        ERROR = 1

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
    for day in range(3, len(ORIG_TABLE[0])):
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
def result_check(GRAPH, SCALE):
    OK = 1
    for row in range(len(GRAPH)):
        s = 0
        for col in GRAPH[row]:
            if col[1] != 0:
                s += 1
        if s > 1:
            OK = 0
            print('ALERT:', row, 'sorban tobb el lett kivalasztva', s)
        elif s < 1:
            OK = 0
            print('ALERT:', row, 'sorban kevesebb lett kivalasztva', s)

    for col in range(len(GRAPH[0])):
        s = 0
        for row in GRAPH:
            if row[col][1] != 0:
                s += 1
        if s > SCALE:
            OK = 0
            print('ALERT:', col, 'col tobb el lett kivalasztva', s)
        elif s < SCALE:
            OK = 0
            print('ALERT:', col, 'col kevesebb lett kivalasztva', s)

    if OK:
        if SCALE == 2:
            print('ELLENORZES RENDBEN: DAYS')
        if SCALE == 1:
            print('ELLENORZES RENDBEN: NIGHTS')

def final_check(table_fin, day_shifts, night_shifts):
    OK = 1
    for col in range(1, len(table_fin[0])):
        d = 0
        e = 0
        for row in range(len(table_fin)):
            if table_fin[row][col] == 'N':
                d += 1
            elif table_fin[row][col] == 'E':
                e += 1
        if d < 2:
            OK = 0
            # print('ALERT', col, 'napon nincs eleg nappalos!')
        elif d > 2:
            OK = 0
            # print('ALERT', col, 'napon tul sok a nappalos!')
        if e < 1:
            OK = 0
            # print('ALERT', col, 'napon nincs eleg ejszakas!')
        elif e > 1:
            OK = 0
            # print('ALERT', col, 'napon tul sok az ejszakas!')
    for row in range(len(table_fin)):
        d = 0
        e = 0
        for col in range(1, len(table_fin[0])):
            if table_fin[row][col] == 'N':
                d += 1
            elif table_fin[row][col] == 'E':
                e += 1
        if d != day_shifts[row]:
            # print('ALERT', table_fin[row][0], 'adminnak kevesebb lett a nappalja.')
            OK = 0
        if e != night_shifts[row]:
            # print('ALERT', table_fin[row][0], 'adminnak kevesebb lett az ejszakaja.')
            OK = 0

    if OK:
        # print('Minden rendben!')
        return 1
    else:
        return 0

def eval_table(table_fin, sat_orig, sun_orig):
    PRINT = 0
    ### ERTEKEK FINOMHANGOLASA
    VALUE = 100000
    #                    2   3    4    5     6     7     8
    penalty_val = [0, 0, 50, 200, 1000, 3000, 4000, 8000, 10000]

    #                          2    3     4     5
    penalty_night_val = [0, 0, 100, 2500, 5000, 10000]
    
    #                    2   3   4    5    6
    reward_val = [0, 0, 80, 200, 350, 500, 800] 

    table_string = ['.' for i in range(len(table_fin))]
    admin_shifts = [[[], [], 0] for i in range(len(table_fin))]

    for admin in range(len(table_fin)):
        for day in range(1, len(table_fin[0])):
            if table_fin[admin][day] == '':
                table_string[admin] += '.'
            elif table_fin[admin][day] in {'N', 'E'}:
                table_string[admin] += table_fin[admin][day]
        table_string[admin] += '.'
        
    if PRINT:
        for st in table_string:
            print(st)
        print()

    ### BUNTETOPONTOK LEVONASA A TUL SURU MUSZAKOKERT
    if PRINT:
        print('Buntetopontok:')
    admin = -1
    for st in table_string:
        s = 0
        admin += 1
        sat = 0
        sun = 0
        while s < len(st) - 1:
            if st[s] == '.':
                c = 0
                if s + c + 1 < len(st):  
                    while st[s + c + 1] != '.':
                        c += 1
                        if s + c + 1 in sat_orig:
                            sat += 1
                        elif s + c + 1 in sun_orig:
                            sun += 1
                    if c > 0:
                        # if c >= 8:
                        #     VALUE -= penalty_val[8]
                        # else:
                        #     VALUE -= penalty_val[c]
                        admin_shifts[admin][0].append(c)
                        if PRINT:
                            print(c, end=' ')
                    s = s + c + 1
        admin_shifts[admin][2] += sat
        admin_shifts[admin][2] += sun
        if PRINT:
            print()

    ### BUNTETOPONTOK LEVONASA A TUL SURU EJJELEKERT
    if PRINT:
        print('Buntetopontok a suru ejjelekert:')
    admin = -1
    for st in table_string:
        s = 1
        admin += 1
        while s < len(st) - 1:
            c = 1
            if st[s] == 'E':
                while s + c < len(st) - 1:
                    if st[s + c] == 'E':
                        c += 1
                    else:
                        break
                if c > 0:
                    # if c >= 5:
                    #     VALUE -= penalty_val[5]
                    # else:
                    #     VALUE -= penalty_val[c]
                    admin_shifts[admin][1].append(c)
                if PRINT:
                    print(c, end=' ')
            s += c
        if PRINT:
            print()
    
    ### ERTEKELES KISZAMITASA
    weekend = 0
    weekend += len(sat_orig)
    weekend += len(sun_orig)
    weekend *= weekend
    sum_shifts = 3 * (len(table_fin[0]) - 1)
    for admin in admin_shifts:
        for s in admin[0]:
            if s > 8:
                VALUE -= penalty_val[8]
            else:
                VALUE -= penalty_val[s]
        for s in admin[1]:
            if s > 5:
                VALUE -= penalty_night_val[5]
            else:
                VALUE -= penalty_night_val[s]
        opt_weekend = sum(admin[0])*weekend/sum_shifts
        w = abs(admin[2] - opt_weekend)
        if w > 2:
            VALUE -= 10000
        elif w > 1:
            VALUE -= 3000
        elif w > 0:
            VALUE -= 200

    ### JUTALOMPONTOK HOZZAADASA A SZABADNAPOKERT
    # print('Jutalom pontok:')
    # for st in table_string:
    #     s = 1
    #     while s < len(st) - 1:
    #         c = 1
    #         if st[s] == '.':
    #             while s + c < len(st) - 1:
    #                 if st[s + c] == '.':
    #                     c += 1
    #                 else:
    #                     break
    #             if c > 0:
    #                 if c >= 6:
    #                     VALUE += reward_val[6]
    #                 else:
    #                     VALUE += reward_val[c]
    #             print(c, end=' ')
    #         s += c
    #     print()
    if PRINT:
        print(VALUE)
        print()
        for i in admin_shifts:
            print(i)
        print()
        print('-'*100)
        print()

    return VALUE



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
    # BEOLVASOTT TABLAZAT
    ORIG_TABLE = [row[0:DAYS + 3] for row in row_list[3:len(row_list)]]
    admins_name = [row[0] for row in ORIG_TABLE]

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

    ### GRAFOK LETREHOZASA
    ORIG_ADMINS = [set() for i in range(DAYS)]
    day_shifts = [ORIG_TABLE[i][1] for i in range(len(ORIG_TABLE))]
    night_shifts = [ORIG_TABLE[i][2] for i in range(len(ORIG_TABLE))]
    ORIG_GRAPH_DAY = make_graph(ORIG_TABLE, ORIG_ADMINS, day_shifts,  'DAY', DAYS)
    ORIG_GRAPH_NIGHT = make_graph(ORIG_TABLE, ORIG_ADMINS, night_shifts,  'NIGHT', DAYS)

    ### GENERALAS KEZDESE
    SZUMMA = 0
    best_gen_value = -100000
    best_gen_table = list()
    SUM_GEN = 25
    for i in range(SUM_GEN):
        GENERATION = 1
        while GENERATION:
            GENERATION = 0
            admins = c.deepcopy(ORIG_ADMINS)
            ### EREDETI GRAFOKAT NEM MODOSITJUK,
            ### AZ ALABBI GRAFOKKAL FOGUNK TOVABB DOLGOZNI
            graph_day = c.deepcopy(ORIG_GRAPH_DAY)
            graph_night = c.deepcopy(ORIG_GRAPH_NIGHT)

            ### NAPPALI BEOSZTAS GENERALASA
            graph_double_max_match(graph_day, day_shifts, admins)

            ### EJSZAKAI MUSZAKOKHOZ TARTOZO GRAF MODOSITASA
            ### A GENERALASNAK MEGFELELOEN
            for row in range(len(graph_day)):
                for col in range(len(graph_day[row])):
                    if graph_day[row][col][1] == 1:
                        admin = whois(row, day_shifts)
                        admin_index = sum(night_shifts[:admin])
                        for row_mod in range(admin_index, admin_index + night_shifts[admin]):
                            graph_night[row_mod][col][0] = 0
                            if col - 1 >= 0:
                                graph_night[row_mod][col - 1][0] = 0
                        break

            ### EJSZAKAI MUSZAKOK GENERALASA
            gen_night = graph_max_match(graph_night)
            if gen_night == 0:
                GENERATION = 1
            else:
                final_table = graph_merge(graph_day, graph_night, day_shifts, night_shifts, admins_name, DAYS)
                if final_check(final_table, day_shifts, night_shifts):
                    GENERATION = 0
                    current_value = eval_table(final_table, sat_orig, sun_orig)
                    if current_value > best_gen_value:
                        best_gen_value = current_value
                        best_gen_table = c.deepcopy(final_table)
                else:
                    GENERATION = 1

    e = 0
    n = 0
    print(SUM_GEN, 'generálásból a legjobbnak vélt beosztás:')
    print()
    print('NAME'.center(21, ' '), end='\t ')
    for i in range(DAYS):
        if i < 9:
            print(i + 1, end='  ')
        else:
            print(i + 1, end=' ')
    print()
    for i in best_gen_table:
        for j in range(len(i)):
            if j == 0:
                print(i[j].ljust(21, ' '), end='\t|')
            else:
                if i[j] != '':
                    print(i[j], end='  ')
                    if i[j] == 'E':
                        e += 1
                    if i[j] == 'N':
                        n += 1
                else:
                    print(' ', end='  ')
        print()
    print('\nÉrtékelés:', best_gen_value)


main()
