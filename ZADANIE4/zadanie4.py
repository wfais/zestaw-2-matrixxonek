import os
import time
import threading
import sys
import math

# Stałe konfiguracyjne
LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    # Funkcja oblicza częściową sumę przybliżenia liczby pi metodą prostokątów.
    # Argumenty:
    #     pocz, kon - zakres iteracji (indeksy kroków całkowania),
    #     krok      - szerokość pojedynczego prostokąta (1.0 / LICZBA_KROKOW),
    #     wyniki    - lista, do której należy wpisać wynik dla danego wątku na pozycji indeks,
    #     indeks    - numer pozycji w liście 'wyniki' do zapisania rezultatu.

    # Każdy wątek powinien:
    #   - obliczyć lokalną sumę dla przydzielonego przedziału,
    #   - wpisać wynik do wyniki[indeks].
    wynik_lokalny = 0.0
    for i in range(pocz, kon):
        x_i = (i + 0.5) * krok
        wynik_lokalny += 4.0/(1 + (x_i * x_i))

    wyniki[indeks] = wynik_lokalny


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW:,}\n")

    # Wstępne uruchomienie w celu stabilizacji środowiska wykonawczego
    krok = 1.0 / LICZBA_KROKOW

    czas_bazowy = 0.0
    max_watkow = max(LICZBA_WATKOW)

    # ---------------------------------------------------------------
    # Tu zaimplementować:
    #   - utworzenie wielu wątków (zgodnie z LICZBY_WATKOW),
    #   - podział pracy na zakresy [pocz, kon) dla każdego wątku,
    #   - uruchomienie i dołączenie wątków (start/join),
    #   - obliczenie przybliżenia π jako sumy wyników z poszczególnych wątków,
    #   - pomiar czasu i wypisanie przyspieszenia.
    # ---------------------------------------------------------------
    
    for N_watkow in LICZBA_WATKOW:
        watki = []
        wyniki_czesciowe = [0.0] * N_watkow 
        
        # Obliczanie bloku pracy 
        rozmiar_bloku = LICZBA_KROKOW // N_watkow
        
        start_time = time.perf_counter()
        
        # Utworzenie i uruchomienie wątków (podział pracy)
        for i in range(N_watkow):
            pocz = i * rozmiar_bloku
            kon = pocz + rozmiar_bloku 
            
            # Ostatni wątek musi obsłużyć resztę
            if i == N_watkow - 1:
                kon = LICZBA_KROKOW
            
            w = threading.Thread(
                target=policz_fragment_pi, 
                args=(pocz, kon, krok, wyniki_czesciowe, i)
            )
            watki.append(w)
            w.start()
            
        # Poczekanie na zakończenie wszystkich wątków
        for w in watki:
            w.join()
            
        end_time = time.perf_counter()
        czas = end_time - start_time
        
        wynik_pi = sum(wyniki_czesciowe)
        
        # Ustalenie czasu bazowego (dla N=1)
        if N_watkow == 1:
            czas_bazowy = czas
            
        przyspieszenie = czas_bazowy / czas if czas > 0 else 0.0

        # Wypisanie wyniku
        print(f"{N_watkow:<6}{czas:<12.4f}{przyspieszenie:<20.2f}{wynik_pi:.10f}")

    print(f"\nPi (z biblioteki math): {math.pi:.10f}")
    print(f"Błąd przybliżenia: {abs(wynik_pi - math.pi):.2e}")

if __name__ == "__main__":
    main()
