import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

def create_question(question_text, days):
    """
    Tworzymy puyanie z podanymi tsktami i przesunięciem w dniach
    Ujemna `days` to przeszłośc, dodatnie to przyszłośc
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelsTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30) #tworzymy czas z 30 dni w przyszłości
        future_question = Question(pub_date=time) #tworzymy wirtualne pytanie z tą datą z przyszłosci 
        self.assertIs(future_question.was_published_recently(), False) #sprwaedzamy i oczekujemy że funkcja zwróci false, bo pytanie jest z przyszłości

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1) #tworzymy czas z 1 dniem i 1 sekundą w przeszłości
        old_question = Question(pub_date=time) #tworzymy wirtualne pytanie z tą datą z przeszłości
        self.assertIs(old_question.was_published_recently(), False) #sprwaedzamy i oczekujemy że funkcja zwróci false, bo pytanie jest z przeszłości

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59) #tworzymy czas z 23 godzinami, 59 minutami i 59 sekundami w przeszłości
        recent_question = Question(pub_date=time) #tworzymy wirtualne pytanie z tą datą z przeszłości
        self.assertIs(recent_question.was_published_recently(), True) #sprwaedzamy i oczekujemy że funkcja zwróci true, bo pytanie jest z przeszłości ale nie jest stare, bo zostało opublikowane w ciągu ostatniego dnia

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        #jeśli nie ma żadnych pytań, to wyświetlamy odpowiedni komunikat
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        #jeśli pytanie jest z przeszłości, to jest wyświetlane na stronie
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        #jeśli pytanie jest z przyszłosći to nie jest wywiwtlne na stronie 
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        #jesli jest pytanie z przyszłości i z przeszłości to wyświtla tylko pytanie z przeszłości
        question= create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        #szczegóły pytania z datą w przyszłości powinny zwrócić 404
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        #szczegły pytania z datą w przeszłości powinny być wyświetlane jego treść
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

        