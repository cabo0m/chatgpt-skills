---
name: faithful-product-photo
description: Edycja fotografii produktowych do e-commerce z zachowaniem rzeczywistego produktu i opakowania. Używaj, gdy trzeba usunąć tło, poprawić światło, kolor, perspektywę i kadr bez tworzenia nowego produktu.
---

# Faithful Product Photo

## Cel

Przekształć fotografię produktu w czyste zdjęcie ofertowe. **Edytuj oryginalne piksele. Nie generuj ponownie produktu ani opakowania.** Domyślnym wynikiem jest PNG z rzeczywiście przezroczystym kanałem alfa (RGBA).

## Niezmienne elementy

- Zachowaj dokładną liczbę przedmiotów, kolorów, przewodów, końcówek, wtyków, opasek, zawieszek i elementów opakowania.
- Zachowaj widoczny kształt, proporcje, powierzchnię, logo, etykiety, napisy i symbole. Nie odtwarzaj napisów generatywnie.
- Zachowaj oryginalne połączenia między przewodami a końcówkami. **Nie przypisuj końcówki jednego przewodu do innego.**
- Nie dodawaj wtyczek niewidocznych na zdjęciu. Jeśli widoczna jest tylko jedna końcówka białego kabla, nie domalowuj drugiej. Brak widoczności nie dowodzi braku elementu w rzeczywistym produkcie.
- Nie wymieniaj ani nie symetryzuj części produktu wyłącznie dlatego, że taki układ wygląda estetyczniej.
- Dopuszczalna jest korekta ekspozycji, balansu bieli i perspektywy, o ile nie zmienia to informacji o produkcie.

## Procedura

1. **Inwentaryzacja referencji.** Zanotuj wszystkie widoczne elementy i niepewności. Oddziel elementy potwierdzone od zasłoniętych.
2. **Segmentacja.** Utwórz maskę produktu wraz z opakowaniem na podstawie zdjęcia źródłowego. Usuń tło sklepowe, cenówkę, półkę i inne obiekty niezwiązane z produktem. Jeśli granica między produktem i obcym przedmiotem jest niepewna, zgłoś to.
3. **Korekta niedestrukcyjna.** Popraw globalne światło, balans bieli i kadr. Zachowaj drobne detale, oryginalne faktury i ostre krawędzie.
4. **Eksport.** Zapisz PNG RGBA z realnym kanałem alfa. Alternatywne białe tło utwórz przez kompozycję z wyciętym produktem, nie przez narysowanie imitacji szachownicy.
5. **Porównanie.** Porównaj źródło i rezultat punkt po punkcie. Jeśli zmieniła się liczba lub przynależność wtyków, napis, logo, typ złącza albo kolor, wynik odrzuć.

## Testy akceptacyjne

- [ ] Nie widać fragmentów sklepu, półki ani cenówki.
- [ ] Opakowanie i widoczne elementy produktu pozostały autentyczne.
- [ ] Liczba **widocznych** końcówek każdego kabla zgadza się ze źródłem; części zasłoniętych nie dopowiedziano.
- [ ] Kształty, połączenia i kolory odpowiadają źródłu.
- [ ] Czytelne napisy i znaki nie zostały wymyślone ani zmienione.
- [ ] Piksele poza maską mają alfa = 0, a nie wzór szachownicy; format obrazu obsługuje alfa.
- [ ] Krawędzie wycięcia nie zawierają dużych resztek tła ani sztucznej poświaty.
- [ ] Przynajmniej raz obejrzano zdjęcie wyjściowe obok wejściowego w dużym powiększeniu.

## Zasada odmowy fałszywej poprawności

Jeśli dostępne narzędzie potrafi wyłącznie tworzyć nowy obraz, a nie wiarygodnie maskować oryginalne piksele, **nie oznaczaj rezultatu jako wiernej obróbki**. Wyraźnie nazwij go rekonstrukcją poglądową i wskaż brakujący krok maskowania.

## Przykład testowy: 3-pack USB-C

Fotografia sklepowa trzech przewodów na opakowaniu (biały, czarny, jasnoszary). W jednej z prób model zmienił przynależność końcówek: biały przewód miał tylko jedną widoczną wtyczkę, a wynik wyglądał na poprawny. Weryfikacja musi badać **widoczne końcówki i ich przynależność**, nie tylko ogólną liczbę wtyków na zdjęciu. Ten przykład jest regresją jakościową; nie należy interpretować go jako pewnej informacji o niewidocznej stronie fizycznego produktu.
