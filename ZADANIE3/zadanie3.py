import requests, re, time, sys
from collections import Counter

URL = "https://pl.wikipedia.org/api/rest_v1/page/random/summary"
N = 100  # liczba losowań
HEADERS = {
    "User-Agent": "wp-edu-wiki-stats/0.1 (kontakt: twoj-email@domena)",
    "Accept": "application/json",
}

# przygotowanie wyrażenia regularnego wyłapującego słowa (litery)
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def selekcja(text: str):
    WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)
    wszystkie_slowa = WORD_RE.findall(text)
    lista_slow = [
        slowo.lower() for slowo in wszystkie_slowa
        if len(slowo) >= 4
    ]
    return lista_slow

def ramka(text: str, width: int = 80) -> str:
    max_content_width = width - 2
    
    if len(text) > max_content_width:
        content = text[:width - 3] + "…"
    else:
        content = text
        
    if max_content_width <= 0:
        return ""
        
    centered_content = content.center(max_content_width)
    
    return f"[{centered_content}]"


def main():
    cnt = Counter()
    licznik_slow = 0
    pobrane = 0

    # linia statusu
    print(ramka("Start"), end="", flush=True)

    while pobrane < N:
        try:
            data = requests.get(URL, headers=HEADERS, timeout=10).json()
        except Exception:
            # timeout / brak JSON → spróbuj ponownie
            time.sleep(0.1)
            continue

        title = data.get("title") or ""
        line = "\r" + ramka(title, 80)
        print(line, end="", flush=True)

        extract = data.get("extract") or ""
        lista_slow = selekcja(extract)
        licznik_slow += len(lista_slow)
        pobrane += 1
        cnt.update(lista_slow)
        time.sleep(0.05)

    print(f"Pobrano wpisów: {pobrane}")
    print(f"Słów (≥4) łącznie:{licznik_slow}")
    print(f"Unikalnych (≥4):{len(cnt)}\n")

    print("Top 15 słów (≥4):")
    for slowo in cnt.most_common(15):
        print(slowo)

if __name__ == "__main__":
    main()
