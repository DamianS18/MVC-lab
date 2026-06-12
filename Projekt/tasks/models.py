from django.conf import settings
from django.db import models
from django.urls import reverse


class TicketEvent(models.Model):
    class Category(models.TextChoices):
        MUSIC = "muzyka", "Muzyka"
        THEATER = "teatr", "Teatr"
        FAMILY = "rodzina", "Rodzina"
        SPORT = "sport", "Sport"
        FESTIVALS = "festiwale", "Festiwale"
        CULTURE = "kultura", "Kultura"
        STAND_UP = "stand-up", "Stand-up"
        OUTDOOR = "plenery", "Plenery"
        CINEMA = "kino", "Kino"
        CLASSICAL = "klasyka", "Klasyka"
        OTHER = "inne", "Inne"

    event_name = models.CharField("nazwa wydarzenia", max_length=200)
    event_date = models.DateField("data")
    location = models.CharField("lokalizacja", max_length=120, blank=True)
    category = models.CharField(
        "kategoria",
        max_length=30,
        choices=Category.choices,
        default=Category.OTHER,
    )
    subcategory = models.CharField("podkategoria", max_length=60, blank=True)
    description = models.TextField("opis wydarzenia", blank=True)
    artists = models.TextField("artysci", blank=True)
    seats = models.PositiveIntegerField("liczba miejsc")

    class Meta:
        ordering = ["event_date", "event_name"]
        verbose_name = "wydarzenie"
        verbose_name_plural = "wydarzenia"

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse("tasks:detail", args=[self.pk])

    def has_available_seats(self):
        return self.seats > 0


class TicketPurchase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ticket_purchases",
        verbose_name="uzytkownik",
    )
    event = models.ForeignKey(
        TicketEvent,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="wydarzenie",
    )
    purchased_at = models.DateTimeField("data zakupu", auto_now_add=True)

    class Meta:
        ordering = ["-purchased_at"]
        verbose_name = "kupiony bilet"
        verbose_name_plural = "kupione bilety"

    def __str__(self):
        return f"{self.user} - {self.event}"
