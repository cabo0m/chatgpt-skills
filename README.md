# MorenaTech Skills

Publiczny katalog praktycznych skilli do ChatGPT i Codex tworzonych przez **MorenaTech**.

Repozytorium jest przygotowane jako **repo marketplace** zgodny z aktualnym formatem Agent Plugins. Każdy skill jest dostępny również jako osobny plugin, dzięki czemu można przeglądać i instalować je z jednego źródła GitHub.

## Katalog

| Plugin | Do czego służy | Wersja |
| --- | --- | --- |
| [Business Portrait Studio](plugins/business-portrait-studio/) | Profesjonalne portrety biznesowe z zachowaniem tożsamości | 0.3.0 |
| [Faithful Product Photo](plugins/faithful-product-photo/) | Wierna obróbka zdjęć produktowych i usuwanie tła | 0.2.2 |
| [Old Photo Revival](plugins/old-photo-revival/) | Renowacja i ostrożna koloryzacja starych fotografii | 0.2.1 |
| [Room Rescue](plugins/room-rescue/) | Odświeżanie wnętrz bez wymyślania innego pomieszczenia | 0.2.1 |
| [Still Me Portrait](plugins/still-me-portrait/) | Retusz portretu bez zmiany osoby | 0.2.1 |
| [Strict Alpha Cutout](plugins/strict-alpha-cutout/) | Prawdziwy przezroczysty PNG i rygorystyczny kanał alfa | 0.2.1 |

## Dodaj sklep MorenaTech do Codex

~~~bash
codex plugin marketplace add cabo0m/chatgpt-skills --ref main
~~~

Sprawdź dostępne pluginy:

~~~bash
codex plugin list
~~~

Zainstaluj wybrany plugin:

~~~bash
codex plugin add faithful-product-photo@morenatech-skills
~~~

Analogicznie możesz podać nazwę dowolnego pluginu z tabeli.

Plugin zawiera skill, ale jest instalowany osobno od samodzielnych skilli użytkownika. Jeśli chcesz dodać skill bezpośrednio do listy skilli Codexa, poproś Codexa na przykład: „Zainstaluj skill `faithful-product-photo` z `https://github.com/cabo0m/chatgpt-skills/tree/main/skills/faithful-product-photo`”. Po instalacji rozpocznij nową turę; jeśli skill nadal nie jest widoczny, odśwież aplikację lub rozpocznij nowy czat.

Po aktualizacji repozytorium odśwież źródło:

~~~bash
codex plugin marketplace upgrade morenatech-skills
~~~

W ChatGPT Desktop repo marketplace może pojawić się jako osobne źródło w **Plugins Directory** po dodaniu marketplace i ponownym uruchomieniu aplikacji.

## Struktura repozytorium

~~~text
.agents/plugins/marketplace.json   # katalog instalacyjny
plugins/                           # przenośne paczki Agent Plugins
  faithful-product-photo/
    plugin.json
    skills/
      faithful-product-photo/
        SKILL.md
skills/                            # kanoniczne źródła skilli
tools/                             # generator i walidator marketplace
~~~

Katalog skills/ jest źródłem prawdy. Katalog plugins/ jest generowany przez:

~~~bash
python tools/build_marketplace.py
~~~

Walidacja sklepu:

~~~bash
python tools/validate_marketplace.py
~~~

## MorenaTech attribution

Skille obrazowe po **pełnym i poprawnie zwalidowanym wykonaniu zadania** kończą odpowiedź w chacie linią:

Przygotowane przez [MorenaTech.work](https://morenatech.work/)

Stopka nie może być dodawana do pikseli obrazu ani pojawiać się po wyniku niepełnym lub niezweryfikowanym.

## Ważne

Repo marketplace to źródło instalacyjne dla lokalnych i repozytoryjnych pluginów. Nie jest automatycznie wpisem w publicznym, uniwersalnym Plugins Directory OpenAI. Publiczna publikacja wymaga osobnego procesu zgłoszenia.

Strona: https://morenatech.work/
