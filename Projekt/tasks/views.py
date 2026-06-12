from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import EmailSignUpForm, TicketEventForm
from .models import TicketEvent, TicketPurchase


CATEGORY_PAGES = {
    TicketEvent.Category.MUSIC: {
        "title": "Muzyka",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-teal"),
            ("pop", "Pop", "category-wide category-coral"),
            ("rock", "Rock", "category-mint"),
            ("jazz", "Jazz", "category-blue"),
            ("elektroniczna", "Elektroniczna", "category-wide category-amber"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.THEATER: {
        "title": "Teatr",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-coral"),
            ("spektakle", "Spektakle", "category-wide category-teal"),
            ("musicale", "Musicale", "category-mint"),
            ("balet", "Balet", "category-blue"),
            ("komedia", "Komedia", "category-wide category-rose"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.FAMILY: {
        "title": "Rodzina",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-mint"),
            ("dla-dzieci", "Dla dzieci", "category-wide category-coral"),
            ("warsztaty", "Warsztaty", "category-blue"),
            ("pikniki", "Pikniki", "category-wide category-amber"),
            ("familijne", "Familijne", "category-teal"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.SPORT: {
        "title": "Sport",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-blue"),
            ("pilka-nozna", "Pilka nozna", "category-wide category-teal"),
            ("biegi", "Biegi", "category-mint"),
            ("koszykowka", "Koszykowka", "category-coral"),
            ("motorsport", "Motorsport", "category-wide category-amber"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.FESTIVALS: {
        "title": "Festiwale",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-amber"),
            ("muzyczne", "Muzyczne", "category-wide category-teal"),
            ("lato", "Lato", "category-coral"),
            ("plener", "Plener", "category-mint"),
            ("podroze", "Podroze", "category-wide category-blue"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.CULTURE: {
        "title": "Kultura",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-rose"),
            ("wystawy", "Wystawy", "category-wide category-teal"),
            ("targi", "Targi", "category-mint"),
            ("spotkania", "Spotkania", "category-blue"),
            ("iluzja", "Iluzja", "category-wide category-coral"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.STAND_UP: {
        "title": "Stand-up",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-coral"),
            ("solowe", "Solowe", "category-wide category-teal"),
            ("kabaret", "Kabaret", "category-mint"),
            ("open-mic", "Open mic", "category-blue"),
            ("plener", "Plener", "category-wide category-amber"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.OUTDOOR: {
        "title": "Plenery",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-teal"),
            ("koncerty", "Koncerty", "category-wide category-coral"),
            ("kino", "Kino", "category-mint"),
            ("pikniki", "Pikniki", "category-blue"),
            ("food", "Food", "category-wide category-amber"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.CINEMA: {
        "title": "Kino",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-blue"),
            ("plenerowe", "Plenerowe", "category-wide category-teal"),
            ("retro", "Retro", "category-coral"),
            ("familijne", "Familijne", "category-mint"),
            ("maratony", "Maratony", "category-wide category-rose"),
            ("inne", "Inne", "category-forest"),
        ],
    },
    TicketEvent.Category.CLASSICAL: {
        "title": "Klasyka",
        "tiles": [
            ("nowosci", "Nowosci", "category-large category-teal"),
            ("symfoniczne", "Symfoniczne", "category-wide category-blue"),
            ("opera", "Opera", "category-coral"),
            ("balet", "Balet", "category-mint"),
            ("kameralne", "Kameralne", "category-wide category-amber"),
            ("inne", "Inne", "category-forest"),
        ],
    },
}


def get_category_tiles():
    return [
        {
            "slug": TicketEvent.Category.MUSIC,
            "label": "Muzyka",
            "style": "category-large category-teal",
        },
        {
            "slug": TicketEvent.Category.THEATER,
            "label": "Teatr",
            "style": "category-wide category-coral",
        },
        {"slug": TicketEvent.Category.FAMILY, "label": "Rodzina", "style": "category-mint"},
        {"slug": TicketEvent.Category.SPORT, "label": "Sport", "style": "category-tall category-blue"},
        {
            "slug": TicketEvent.Category.FESTIVALS,
            "label": "Festiwale",
            "style": "category-wide category-amber",
        },
        {"slug": TicketEvent.Category.CULTURE, "label": "Kultura", "style": "category-rose"},
        {
            "slug": TicketEvent.Category.STAND_UP,
            "label": "Stand-up",
            "style": "category-forest",
        },
        {
            "slug": TicketEvent.Category.OUTDOOR,
            "label": "Plenery",
            "style": "category-wide category-mint",
        },
        {"slug": TicketEvent.Category.CINEMA, "label": "Kino", "style": "category-coral"},
        {"slug": TicketEvent.Category.CLASSICAL, "label": "Klasyka", "style": "category-blue"},
    ]


def search_is_active(params):
    return bool(params["q"] or params["date_from"] or params["date_to"] or params["location"])


def build_category_result_sections(events):
    sections = []
    for tile in get_category_tiles():
        category_events = events.filter(category=tile["slug"])
        if category_events:
            sections.append(
                {
                    "slug": tile["slug"],
                    "title": tile["label"],
                    "events": category_events,
                }
            )
    return sections


def build_subcategory_sections(category_slug):
    sections = []
    for slug, label, style in CATEGORY_PAGES[category_slug]["tiles"]:
        events = TicketEvent.objects.filter(category=category_slug)
        if slug == "nowosci":
            events = events.order_by("-id")[:11]
        else:
            events = events.filter(subcategory=slug)[:11]

        sections.append(
            {
                "slug": slug,
                "title": label,
                "style": style,
                "events": events,
            }
        )
    return sections


def get_subcategory_label(category_slug, subcategory_slug):
    for slug, label, style in CATEGORY_PAGES.get(category_slug, {}).get("tiles", []):
        if slug == subcategory_slug:
            return label
    return subcategory_slug.replace("-", " ").title() if subcategory_slug else "Inne"


def get_search_params(request):
    return {
        "q": request.GET.get("q", "").strip(),
        "date_from": request.GET.get("date_from", "").strip(),
        "date_to": request.GET.get("date_to", "").strip(),
        "location": request.GET.get("location", "").strip(),
    }


def filter_events(queryset, params):
    if params["q"]:
        queryset = queryset.filter(event_name__icontains=params["q"])
    if params["location"]:
        queryset = queryset.filter(location__icontains=params["location"])
    if params["date_from"] and params["date_to"]:
        queryset = queryset.filter(event_date__gte=params["date_from"])
        queryset = queryset.filter(event_date__lte=params["date_to"])
    elif params["date_from"]:
        queryset = queryset.filter(event_date=params["date_from"])
    elif params["date_to"]:
        queryset = queryset.filter(event_date=params["date_to"])
    return queryset


class HomeView(generic.TemplateView):
    template_name = "tasks/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = get_search_params(self.request)
        events = filter_events(TicketEvent.objects.all(), context["search"])
        context["search_active"] = search_is_active(context["search"])
        if context["search_active"]:
            context["result_sections"] = build_category_result_sections(events)
        else:
            context["featured_events"] = events[:11]
            context["summer_events"] = events[11:22]
            context["selected_events"] = events[22:33]
        context["category_tiles"] = get_category_tiles()
        return context


class CategoryView(generic.TemplateView):
    template_name = "tasks/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = kwargs["category_slug"]
        if category_slug not in CATEGORY_PAGES:
            raise Http404("Nie ma takiej kategorii.")

        context["category_slug"] = category_slug
        context["category_title"] = CATEGORY_PAGES[category_slug]["title"]
        context["subcategory_sections"] = build_subcategory_sections(category_slug)
        return context


class EventListView(generic.ListView):
    model = TicketEvent
    template_name = "tasks/task_list.html"
    context_object_name = "event_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_events(queryset, get_search_params(self.request))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = get_search_params(self.request)
        return context


class EventDetailView(generic.DetailView):
    model = TicketEvent
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        context["category_title"] = CATEGORY_PAGES.get(event.category, {}).get(
            "title",
            event.get_category_display(),
        )
        context["subcategory_title"] = get_subcategory_label(event.category, event.subcategory)
        return context


class SignUpView(generic.CreateView):
    form_class = EmailSignUpForm
    template_name = "tasks/signup.html"
    success_url = reverse_lazy("tasks:profile")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Konto zostalo utworzone.")
        return response


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = "tasks/profile.html"
    login_url = "tasks:login"
    page_size = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = TicketPurchase.objects.filter(user=self.request.user).select_related("event")
        today = timezone.localdate()
        tickets = purchases.filter(event__event_date__gte=today).order_by("event__event_date", "event__event_name")
        history = purchases.filter(event__event_date__lt=today).order_by("-event__event_date", "event__event_name")
        context["tickets"] = Paginator(tickets, self.page_size).get_page(
            self.request.GET.get("tickets_page")
        )
        context["history"] = Paginator(history, self.page_size).get_page(
            self.request.GET.get("history_page")
        )
        context["all_purchases"] = purchases
        return context


@require_POST
def reserve_event(request, pk):
    event = get_object_or_404(TicketEvent, pk=pk)
    if not request.user.is_authenticated:
        messages.error(request, "Zaloguj sie, aby kupic bilet.")
        login_url = reverse("tasks:login")
        detail_url = reverse("tasks:detail", args=[event.pk])
        return redirect(f"{login_url}?next={detail_url}")

    if event.has_available_seats():
        event.seats -= 1
        event.save(update_fields=["seats"])
        TicketPurchase.objects.create(user=request.user, event=event)
        messages.success(request, "Bilet zostal kupiony.")
    else:
        messages.error(request, "Brak wolnych miejsc na to wydarzenie.")
    return redirect("tasks:detail", pk=event.pk)


class EventCreateView(generic.CreateView):
    model = TicketEvent
    form_class = TicketEventForm
    template_name = "tasks/task_form.html"


class EventUpdateView(generic.UpdateView):
    model = TicketEvent
    form_class = TicketEventForm
    template_name = "tasks/task_form.html"
