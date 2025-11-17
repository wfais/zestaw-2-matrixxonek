import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify
import math

ZMIENNA = 'x'

def parse_wejscie(wejscie: str):
    try:
        wzor, zakres = wejscie.split(',')
        x_min, x_max = map(float, zakres.strip().split())
        return wzor.strip(), x_min, x_max
    except ValueError:
        raise ValueError("Niepoprawny format wejścia. Oczekiwano: 'wzór, x_min x_max'")
    
# Funkcja rysująca wykres na podstawie eval()
def rysuj_wielomian(wejscie):
    # Generowanie wartości x i y przy użyciu eval()
    wzor, x_min, x_max = parse_wejscie(wejscie)

    x_val = np.linspace(x_min, x_max, 200)
    if ZMIENNA not in wzor:
        wynik_skalarny = eval(wzor, {}, {})
        y_val = np.full_like(x_val, wynik_skalarny)
    else:
        y_val = eval(wzor, {ZMIENNA: x_val})
    # Rysowanie wykresu ale bez show()

    plt.figure("Wielomian - Porównanie Eval vs SymPy", figsize=(12, 5))
    plt.subplot(1, 2, 1) # Tworzenie pierwszego subwykresu
    plt.plot(x_val, y_val, label="Metoda eval()")

    # Dodanie podpisów i siatki
    plt.title(f"Funkcja: {wzor} (Eval)")
    plt.xlabel(ZMIENNA)
    plt.ylabel("f(x)")
    plt.grid(True)
    
    # Zwracanie wartości na granicach przedziału
    return y_val[0], y_val[-1]

# Funkcja rysująca wykres na podstawie SymPy i lambdify()
def rysuj_wielomian_sympy(wejscie):
    wzor, x_min, x_max = parse_wejscie(wejscie)
    
    x = symbols(ZMIENNA)
    
    try:
        wyrazenie_sympy = sympify(wzor)
    except (SyntaxError, TypeError):
        raise ValueError(f"Błąd parsowania wzoru SymPy: {wzor}")

    funkcja_numeryczna = lambdify(x, wyrazenie_sympy, 'numpy')

    x_val_sympy = np.linspace(x_min, x_max, 200)
    y_val_sympy = funkcja_numeryczna(x_val_sympy)

    plt.subplot(1, 2, 2) 
    plt.plot(x_val_sympy, y_val_sympy, color='red', label="Metoda SymPy")

    plt.title(f"Funkcja: {wzor} (SymPy)")
    plt.xlabel(ZMIENNA)
    plt.ylabel("f(x)")
    plt.grid(True)
    
    # Zwracanie wartości na granicach przedziału
    return y_val_sympy[0], y_val_sympy[-1]

if __name__ == '__main__':
    # Przykładowe wywołanie pierwszej funkcji
    wejscie1 = "x**3 + 3*x + 1, -10 10"
    
    # Pierwszy wykres z eval
    wynik_eval = rysuj_wielomian(wejscie1)
    print("Wynik (eval):", wynik_eval)
    
    # Drugie wejście dla funkcji SymPy - bardziej złożona funkcja 
    wejscie2 = "x**4 - 5*x**2 + 3*sin(x), -10 10"  
    
    # Drugi wykres z SymPy
    wynik_sympy = rysuj_wielomian_sympy(wejscie2)
    print("Wynik (SymPy):", wynik_sympy)
    
    # Wyświetlanie obu wykresów
    plt.show()
