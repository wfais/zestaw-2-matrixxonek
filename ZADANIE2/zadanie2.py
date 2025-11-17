import re
from itertools import groupby

liczby_rzymskie_dic={'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

def rzymskie_na_arabskie(rzymskie):
    if not rzymskie:
        return 0
        
    klucze = liczby_rzymskie_dic.keys()
    for znak in rzymskie:
        if znak not in klucze:
            raise ValueError("Niepoprawna liczba rzymska!")
        
    wzorzec = r'(.)\1{4}'
    znalezione = re.findall(wzorzec, rzymskie)

    if len(znalezione) > 0:
        raise ValueError("Niepoprawna liczba rzymska!")
    
    ciągi = []
    for key, group in groupby(rzymskie):
        run = "".join(group)
        ciągi.append(run) 

    for ciag in ciągi:
        znak = ciag[0]
        dlugosc = len(ciag)
        if znak in 'VLD' and dlugosc > 1:
            raise ValueError("Niepoprawna liczba rzymska: V, L, D nie mogą być powtarzane.")
        if znak in 'IXCM' and dlugosc > 3: 
             raise ValueError("Niepoprawna liczba rzymska: I, X, C, M więcej niż 3 razy.")
    
    for i in range (len(ciągi) - 1):
        wartosc_odjemnika = liczby_rzymskie_dic[ciągi[i][0]]
        wartosc_odejmowana = liczby_rzymskie_dic[ciągi[i+1][0]]
        
        if wartosc_odjemnika < wartosc_odejmowana:
            
            if len(ciągi[i]) > 1:
                raise ValueError("Niepoprawna liczba rzymska: odjęto więcej niż jeden znak.")
                
            if ciągi[i][0] not in 'IXC':
                raise ValueError("Niepoprawna liczba rzymska: nie można odejmować V, L, D.")
            
            if wartosc_odejmowana > wartosc_odjemnika * 10:
                raise ValueError("Niepoprawna liczba rzymska: zbyt duża różnica potęg (np. IC).")

            if (ciągi[i][0] == 'I' and ciągi[i+1][0] not in ('V', 'X')) or \
               (ciągi[i][0] == 'X' and ciągi[i+1][0] not in ('L', 'C')) or \
               (ciągi[i][0] == 'C' and ciągi[i+1][0] not in ('D', 'M')):
                raise ValueError("Niepoprawna liczba rzymska: niedozwolona para odejmowania.")

            if i < len(ciągi) - 2:
                wartosc_po_odjeciu = liczby_rzymskie_dic[ciągi[i+2][0]]
                
                if wartosc_po_odjeciu > wartosc_odejmowana:
                     raise ValueError("Niepoprawna liczba rzymska: Naruszony porządek po odejmowaniu (np. IXL).")
            
    wartosc = 0
    
    for i in range(len(ciągi) - 1):
        wartosc_akt = liczby_rzymskie_dic[ciągi[i][0]]
        ilosc_akt = len(ciągi[i])
        wartosc_nast = liczby_rzymskie_dic[ciągi[i+1][0]]
        
        if wartosc_akt < wartosc_nast:
            wartosc -= wartosc_akt * ilosc_akt
        else:
            wartosc += wartosc_akt * ilosc_akt
            
    ostatni_znak = ciągi[-1][0]
    wartosc_ost = liczby_rzymskie_dic[ostatni_znak]
    ilosc_ost = len(ciągi[-1])
    wartosc += wartosc_ost * ilosc_ost
    
    return wartosc

def arabskie_na_rzymskie(arabskie):
    if arabskie not in range(1,4000):
        raise ValueError("Liczba spoza zakresu")
    mapa_rzymska = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), 
        (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), 
        (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    wynik = ""
    
    for wartosc, symbol in mapa_rzymska:
        ile_razy = arabskie // wartosc
        
        wynik += symbol * ile_razy
        
        arabskie -= ile_razy * wartosc
        
        if arabskie == 0:
            break
            
    return wynik

if __name__ == '__main__':
    try:
        # Przykłady konwersji rzymskiej na arabską
        rzymska = "MCMXCIV"
        print(f"Liczba rzymska {rzymska} to {rzymskie_na_arabskie(rzymska)} w arabskich.")
        
        # Przykłady konwersji arabskiej na rzymską
        arabska = 1994
        print(f"Liczba arabska {arabska} to {arabskie_na_rzymskie(arabska)} w rzymskich.")
        
    except ValueError as e:
        print(e)
