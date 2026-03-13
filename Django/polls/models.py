import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone

class Question(models.Model): # Tworenie tabeli na pytania
    question_text = models.CharField(max_length=200) # kolumna na tekst pytania maks 200 zanków
    pub_date = models.DateTimeField("date published") # kolumna na datę publikacji pytania

    def __str__(self): #dunder method, który zwraca tekst pytania, gdy obiekt jest wyświetlany jako string
        return self.question_text 

    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )

    def was_published_recently(self): # metoda, która sprawdza, czy pytanie zostało opublikowane w ciągu ostatniego dnia
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model): # Tworzenie tabeli na odpowiedzi do pytania
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # odpowiedzi przypisujemy do pytań, jak zostanie usunięte pytanie to usuwamy też odpowiedzi
    choice_text = models.CharField(max_length=200) # kolumna na tekst odpowiedzi maks 200 zanków
    votes = models.IntegerField(default=0) # licznik głosów 

    def __str__(self): #dunder method, który zwraca tekst odpowiedzi, gdy obiekt jest wyświetlany jako string
        return self.choice_text