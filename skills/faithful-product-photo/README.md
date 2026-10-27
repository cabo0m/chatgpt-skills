# Faithful Product Photo

Skill do wiernej obróbki zdjęć produktów: usuwanie tła i poprawa jakości bez generatywnego odtwarzania produktu.

Główna instrukcja: [SKILL.md](./SKILL.md).

## Jak testować

Prześlij oryginalne zdjęcie i poproś o usunięcie tła z zachowaniem opakowania i wszystkich widocznych detali. Po obróbce porównaj przewody, końcówki, opaski, logo i napisy. Wynik musi być PNG z prawdziwym kanałem alfa.

**Ograniczenie:** sam prompt nie gwarantuje wiernej edycji. Potrzebne jest narzędzie do segmentacji oryginalnych pikseli i kontrola efektu. Przypadek testowy z przewodami USB-C wykazał ryzyko przesuwania i dopowiadania wtyczek.
