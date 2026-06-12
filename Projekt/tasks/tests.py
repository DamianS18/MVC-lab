import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import TicketEvent, TicketPurchase


def create_event(
    event_name="Koncert",
    days=1,
    seats=100,
    location="Warszawa",
    category=TicketEvent.Category.MUSIC,
    subcategory="pop",
):
    return TicketEvent.objects.create(
        event_name=event_name,
        event_date=timezone.localdate() + datetime.timedelta(days=days),
        location=location,
        category=category,
        subcategory=subcategory,
        seats=seats,
    )


class TicketEventModelTests(TestCase):
    def test_event_with_seats_has_available_seats(self):
        event = create_event(seats=10)
        self.assertIs(event.has_available_seats(), True)

    def test_event_without_seats_has_no_available_seats(self):
        event = create_event(seats=0)
        self.assertIs(event.has_available_seats(), False)

    def test_string_representation_returns_event_name(self):
        event = create_event(event_name="Spektakl")
        self.assertEqual(str(event), "Spektakl")


class TicketEventViewTests(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Znajdz wydarzenie")
        self.assertContains(response, "Na czasie")
        self.assertContains(response, "Zaplanuj wakacje juz teraz")
        self.assertContains(response, "Wybrane dla Ciebie")
        self.assertContains(response, "Kategorie wydarzen")
        self.assertContains(response, reverse("tasks:category", args=[TicketEvent.Category.MUSIC]))
        self.assertContains(response, 'aria-label="Zaloguj"')
        self.assertContains(response, reverse("tasks:login"))
        self.assertNotContains(response, ">Zaloguj</a>")
        self.assertNotContains(response, "Panel administracyjny")
        self.assertNotContains(response, "/admin/")
        self.assertNotContains(response, "Wydarzenia</a>")
        self.assertNotContains(response, "Dodaj</a>")

    def test_header_account_icon_goes_to_profile_for_logged_user(self):
        user = get_user_model().objects.create_user(username="profilowy", password="test12345")
        self.client.force_login(user)

        response = self.client.get(reverse("tasks:index"))

        self.assertContains(response, 'aria-label="Profil uzytkownika"')
        self.assertContains(response, reverse("tasks:profile"))
        self.assertNotContains(response, ">Profil</a>")

    def test_signup_uses_email_instead_of_username(self):
        response = self.client.get(reverse("tasks:signup"))

        self.assertContains(response, "Imie")
        self.assertContains(response, "Nazwisko")
        self.assertContains(response, "Email")
        self.assertContains(response, "Od 8 do 32 znakow")
        self.assertContains(response, "Wymagana cyfra oraz mala i wielka litera")
        self.assertNotContains(response, "Nazwa użytkownika")
        self.assertNotContains(response, "Nazwa uzytkownika")

    def test_signup_creates_user_with_email_login(self):
        response = self.client.post(
            reverse("tasks:signup"),
            {
                "first_name": "Jan",
                "last_name": "Kowalski",
                "email": "nowy@example.com",
                "password1": "MocneHaslo123",
                "password2": "MocneHaslo123",
            },
        )
        user = get_user_model().objects.get(email="nowy@example.com")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.first_name, "Jan")
        self.assertEqual(user.last_name, "Kowalski")
        self.assertEqual(user.username, "nowy@example.com")
        self.assertEqual(user.email, "nowy@example.com")

    def test_signup_rejects_password_without_required_rules(self):
        response = self.client.post(
            reverse("tasks:signup"),
            {
                "first_name": "Slabe",
                "last_name": "Haslo",
                "email": "slabe@example.com",
                "password1": "samehaslo",
                "password2": "samehaslo",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(email="slabe@example.com").exists())
        self.assertContains(response, "Haslo musi zawierac przynajmniej jedna cyfre.")

    def test_login_uses_email_label(self):
        response = self.client.get(reverse("tasks:login"))

        self.assertContains(response, "Email")
        self.assertNotContains(response, "Nazwa użytkownika")

    def test_list_without_events(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brak wydarzen.")
        self.assertQuerySetEqual(response.context["event_list"], [])

    def test_list_with_event(self):
        event = create_event(event_name="Festiwal", days=2)
        response = self.client.get(reverse("tasks:list"))
        self.assertContains(response, event.event_name)
        self.assertQuerySetEqual(response.context["event_list"], [event])

    def test_detail_view(self):
        event = create_event(event_name="Kino plenerowe", days=3)
        response = self.client.get(reverse("tasks:detail", args=[event.pk]))
        self.assertContains(response, "Kino plenerowe")
        self.assertContains(response, "Home")
        self.assertContains(response, "O wydarzeniu")
        self.assertContains(response, "Artysci")
        self.assertContains(response, "Lokalizacja")
        self.assertContains(response, "Kup bilet")

    def test_reserve_event_decreases_seats(self):
        event = create_event(event_name="Koncert z rezerwacja", seats=2)
        user = get_user_model().objects.create_user(username="jan", password="test12345")
        self.client.force_login(user)

        response = self.client.post(reverse("tasks:reserve", args=[event.pk]), follow=True)
        event.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(event.seats, 1)
        self.assertTrue(TicketPurchase.objects.filter(user=user, event=event).exists())
        self.assertContains(response, "Potwierdzenie")
        self.assertContains(response, "Bilet zostal kupiony.")

    def test_reserve_event_requires_login(self):
        event = create_event(event_name="Koncert dla zalogowanych", seats=2)

        response = self.client.post(reverse("tasks:reserve", args=[event.pk]))
        event.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("tasks:login"), response["Location"])
        self.assertEqual(event.seats, 2)
        self.assertFalse(TicketPurchase.objects.exists())

    def test_reserve_event_does_not_go_below_zero(self):
        event = create_event(event_name="Wyprzedane", seats=0)
        user = get_user_model().objects.create_user(username="anna", password="test12345")
        self.client.force_login(user)

        response = self.client.post(reverse("tasks:reserve", args=[event.pk]))
        event.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(event.seats, 0)

    def test_profile_shows_user_data_and_tickets(self):
        user = get_user_model().objects.create_user(
            username="ola",
            password="test12345",
            email="ola@example.com",
            first_name="Ola",
            last_name="Nowak",
        )
        event = create_event(event_name="Bilet w profilu", days=3)
        TicketPurchase.objects.create(user=user, event=event)
        self.client.force_login(user)

        response = self.client.get(reverse("tasks:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profil uzytkownika")
        self.assertContains(response, "ola@example.com")
        self.assertContains(response, "Bilet w profilu")
        self.assertContains(response, "Moje bilety")
        self.assertContains(response, "Historia wydarzen")

    def test_profile_paginates_and_sorts_tickets_by_nearest_date(self):
        user = get_user_model().objects.create_user(username="sortowany", password="test12345")
        events = [
            create_event(event_name=f"Bilet {days}", days=days)
            for days in [9, 1, 7, 2, 5, 3]
        ]
        for event in events:
            TicketPurchase.objects.create(user=user, event=event)
        self.client.force_login(user)

        response = self.client.get(reverse("tasks:profile"))

        tickets = list(response.context["tickets"])
        self.assertEqual(len(tickets), 5)
        self.assertEqual([purchase.event.event_name for purchase in tickets], [
            "Bilet 1",
            "Bilet 2",
            "Bilet 3",
            "Bilet 5",
            "Bilet 7",
        ])
        self.assertTrue(response.context["tickets"].has_next())
        self.assertContains(response, "Nastepna")

    def test_profile_paginates_and_sorts_history_by_nearest_past_date(self):
        user = get_user_model().objects.create_user(username="historia", password="test12345")
        events = [
            create_event(event_name=f"Historia {abs(days)}", days=days)
            for days in [-9, -1, -7, -2, -5, -3]
        ]
        for event in events:
            TicketPurchase.objects.create(user=user, event=event)
        self.client.force_login(user)

        response = self.client.get(reverse("tasks:profile"))

        history = list(response.context["history"])
        self.assertEqual(len(history), 5)
        self.assertEqual([purchase.event.event_name for purchase in history], [
            "Historia 1",
            "Historia 2",
            "Historia 3",
            "Historia 5",
            "Historia 7",
        ])
        self.assertTrue(response.context["history"].has_next())

    def test_create_event(self):
        response = self.client.post(
            reverse("tasks:add"),
            {
                "event_name": "Teatr",
                "event_date": timezone.localdate().isoformat(),
                "location": "Krakow",
                "category": TicketEvent.Category.THEATER,
                "subcategory": "spektakle",
                "seats": 80,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TicketEvent.objects.filter(event_name="Teatr").exists())

    def test_category_page_shows_subcategory_sections_and_events(self):
        event = create_event(
            event_name="Rockowy wieczor",
            category=TicketEvent.Category.MUSIC,
            subcategory="rock",
        )

        response = self.client.get(reverse("tasks:category", args=[TicketEvent.Category.MUSIC]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Muzyka")
        self.assertContains(response, "Nowosci")
        self.assertContains(response, "Rock")
        self.assertContains(response, event.event_name)
        self.assertIn("subcategory_sections", response.context)

    def test_category_page_groups_events_by_subcategory_sections(self):
        rock_event = create_event(
            event_name="Rockowy wieczor",
            category=TicketEvent.Category.MUSIC,
            subcategory="rock",
        )
        jazz_event = create_event(
            event_name="Jazzowy wieczor",
            category=TicketEvent.Category.MUSIC,
            subcategory="jazz",
        )

        response = self.client.get(reverse("tasks:category", args=[TicketEvent.Category.MUSIC]))

        sections = {section["slug"]: list(section["events"]) for section in response.context["subcategory_sections"]}
        self.assertEqual(sections["rock"], [rock_event])
        self.assertEqual(sections["jazz"], [jazz_event])
        self.assertContains(response, "Rockowy wieczor")
        self.assertContains(response, "Jazzowy wieczor")

    def test_search_by_name_location_and_date_range(self):
        matching_event = create_event(event_name="Koncert jazzowy", days=3, location="Gdansk")
        create_event(event_name="Spektakl", days=3, location="Gdansk")
        create_event(event_name="Koncert rockowy", days=20, location="Krakow")

        response = self.client.get(
            reverse("tasks:list"),
            {
                "q": "koncert",
                "location": "gdan",
                "date_from": (timezone.localdate() + datetime.timedelta(days=1)).isoformat(),
                "date_to": (timezone.localdate() + datetime.timedelta(days=5)).isoformat(),
            },
        )

        self.assertQuerySetEqual(response.context["event_list"], [matching_event])
        self.assertContains(response, "Koncert jazzowy")
        self.assertNotContains(response, "Spektakl")
        self.assertNotContains(response, "Koncert rockowy")

    def test_search_with_one_date_matches_exact_day(self):
        matching_event = create_event(event_name="Koncert dzisiaj", days=4, location="Poznan")
        create_event(event_name="Koncert pozniej", days=5, location="Poznan")

        response = self.client.get(
            reverse("tasks:list"),
            {
                "date_from": (timezone.localdate() + datetime.timedelta(days=4)).isoformat(),
            },
        )

        self.assertQuerySetEqual(response.context["event_list"], [matching_event])
        self.assertContains(response, "Koncert dzisiaj")
        self.assertNotContains(response, "Koncert pozniej")

    def test_home_search_filters_events_on_same_page(self):
        matching_event = create_event(event_name="Koncert domowy", days=2, location="Lodz")
        create_event(event_name="Spektakl domowy", days=2, location="Lodz")

        response = self.client.get(
            reverse("tasks:index"),
            {
                "q": "koncert",
                "location": "lodz",
                "date_from": (timezone.localdate() + datetime.timedelta(days=2)).isoformat(),
            },
        )

        sections = {section["slug"]: list(section["events"]) for section in response.context["result_sections"]}
        self.assertEqual(sections[TicketEvent.Category.MUSIC], [matching_event])
        self.assertContains(response, "Koncert domowy")
        self.assertNotContains(response, "Spektakl domowy")

    def test_home_search_groups_results_by_category(self):
        music_event = create_event(
            event_name="Letni koncert",
            days=2,
            category=TicketEvent.Category.MUSIC,
            subcategory="pop",
        )
        theater_event = create_event(
            event_name="Letni spektakl",
            days=2,
            category=TicketEvent.Category.THEATER,
            subcategory="spektakle",
        )

        response = self.client.get(
            reverse("tasks:index"),
            {
                "date_from": (timezone.localdate() + datetime.timedelta(days=2)).isoformat(),
                "date_to": (timezone.localdate() + datetime.timedelta(days=2)).isoformat(),
            },
        )

        sections = {section["slug"]: list(section["events"]) for section in response.context["result_sections"]}
        self.assertTrue(response.context["search_active"])
        self.assertEqual(sections[TicketEvent.Category.MUSIC], [music_event])
        self.assertEqual(sections[TicketEvent.Category.THEATER], [theater_event])
        self.assertContains(response, "Home")
        self.assertContains(response, "Wydarzenia")
        self.assertContains(response, "Wyniki wyszukiwania")
        self.assertContains(response, "Muzyka")
        self.assertContains(response, "Teatr")
        self.assertNotContains(response, "Kategorie wydarzen")
