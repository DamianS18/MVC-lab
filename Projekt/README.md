# System rezerwacji biletow na wydarzenia

## Spis tresci

1. Opis projektu
2. Zgodnosc z lista zadan projektowych
3. Funkcjonalnosci
4. Struktura MVC
5. Struktura plikow
6. Dokumentacja techniczna
7. Uruchomienie
8. Przykladowe dane
9. Testy

## Opis projektu

Projekt zaliczeniowy w Django. Aplikacja realizuje temat z listy zadan projektowych z pliku PDF:

**Zadanie 5 - System rezerwacji biletow na wydarzenia**.

## Zgodnosc z lista zadan projektowych

Wymaganie z PDF-a:

- **Model**: nazwa wydarzenia, data, liczba miejsc.
- **Kontroler**: obsluga zadan HTTP, interakcja z modelem, przekazywanie danych do widoku.
- **Widok**: lista widokow, formularz dodawania i edycji.

Realizacja w projekcie:

- **Model**: `TicketEvent` w `tasks/models.py` ma pola wymagane w PDF-ie: `event_name`, `event_date`, `seats`. Dodatkowo ma pole `location`, ktore obsluguje wyszukiwanie po lokalizacji.
- **Kontroler**: `tasks/views.py` obsluguje liste, szczegoly, dodawanie i edycje wydarzen.
- **Widok**: `tasks/templates/tasks/` zawiera liste wydarzen, szczegoly oraz formularz dodawania/edycji.

## Funkcjonalnosci

- strona glowna z wyszukiwarka wydarzen,
- wyszukiwanie wydarzen po nazwie, lokalizacji oraz dacie lub zakresie dat,
- wyswietlanie wydarzen w sekcjach i kategoriach,
- osobne strony kategorii z podkategoriami,
- szczegoly pojedynczego wydarzenia,
- zakup biletu przez zalogowanego uzytkownika,
- komunikat potwierdzajacy zakup biletu,
- profil uzytkownika z danymi, biletami i historia wydarzen,
- rejestracja i logowanie uzytkownika przez email,
- panel administracyjny Django do zarzadzania wydarzeniami i kupionymi biletami,
- formularz dodawania wydarzenia,
- formularz edycji wydarzenia,
- testy modelu, widokow i najwazniejszych funkcjonalnosci.

## Struktura MVC

- **Model**: `TicketEvent` w aplikacji `tasks`, pola: nazwa wydarzenia, data, liczba miejsc oraz dodatkowa lokalizacja.
- **Kontroler**: widoki w `tasks/views.py`, ktore obsluguja zadania HTTP i przekazuja dane do szablonow.
- **Widok**: szablony HTML w `tasks/templates/tasks/`.

Django nazywa ten wzorzec MVT, ale w projekcie odpowiada on wymaganiom MVC: model przechowuje dane, widoki Django obsluguja logike zadania HTTP, a template'y odpowiadaja za prezentacje.

## Struktura plikow

- `manage.py` - glowny plik uruchamiajacy komendy Django.
- `homework_site/` - konfiguracja calego projektu Django, m.in. ustawienia i glowne adresy URL.
- `tasks/` - aplikacja z logika systemu rezerwacji biletow.
- `tasks/models.py` - modele bazy danych: wydarzenia i kupione bilety.
- `tasks/views.py` - widoki obslugujace strony, wyszukiwanie, profil, rejestracje i zakup biletu.
- `tasks/forms.py` - formularze rejestracji, logowania oraz wydarzenia.
- `tasks/urls.py` - adresy URL aplikacji.
- `tasks/admin.py` - konfiguracja panelu administracyjnego Django.
- `tasks/templates/tasks/` - szablony HTML wyswietlane uzytkownikowi.
- `tasks/tests.py` - testy automatyczne projektu.
- `tasks/fixtures/sample_events.json` - przykladowe dane wydarzen.
- `requirements.txt` - lista wymaganych paczek.
- `.gitignore` - pliki pomijane przy dodawaniu projektu do repozytorium.

## Dokumentacja techniczna

Pelna dokumentacja projektowa znajduje sie w pliku:

```text
DOKUMENTACJA_TECHNICZNA.md
```

Zawiera opis projektu, funkcjonalnosci, moduly, harmonogram, kosztorys, ryzyka, przypadki uzycia, diagramy, strategie bezpieczenstwa oraz harmonogram testow.

## Uruchomienie

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata sample_events
python manage.py createsuperuser
python manage.py runserver
```

Aplikacja bedzie dostepna pod adresem:

```text
http://127.0.0.1:8000/
```

Panel admina:

```text
http://127.0.0.1:8000/admin/
```

## Przykladowe dane

Projekt zawiera plik z przykladowymi wydarzeniami:

```text
tasks/fixtures/sample_events.json
```

Po wykonaniu migracji mozna go wczytac komenda:

```powershell
python manage.py loaddata sample_events
```

Plik `db.sqlite3` nie powinien byc dodawany do repozytorium, poniewaz baza moze zostac odtworzona z migracji oraz danych przykladowych.

## Testy

```powershell
python manage.py test
```
