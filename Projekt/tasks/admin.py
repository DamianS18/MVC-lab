from django.contrib import admin

from .models import TicketEvent, TicketPurchase


admin.site.site_header = "Panel administracyjny biletow"
admin.site.site_title = "Bilety admin"
admin.site.index_title = "Zarzadzanie wydarzeniami"


@admin.register(TicketEvent)
class TicketEventAdmin(admin.ModelAdmin):
    list_display = [
        "event_name",
        "event_date",
        "location",
        "category",
        "subcategory",
        "seats",
        "has_available_seats",
    ]
    list_display_links = ["event_name"]
    list_filter = ["event_date", "location", "category", "subcategory"]
    search_fields = ["event_name", "location", "subcategory", "description", "artists"]
    date_hierarchy = "event_date"
    ordering = ["event_date", "event_name"]
    fieldsets = [
        (
            "Podstawowe informacje",
            {
                "fields": [
                    "event_name",
                    "event_date",
                    "location",
                    "category",
                    "subcategory",
                ]
            },
        ),
        (
            "Opis strony wydarzenia",
            {
                "fields": [
                    "description",
                    "artists",
                ]
            },
        ),
        (
            "Sprzedaz biletow",
            {
                "fields": [
                    "seats",
                ]
            },
        ),
    ]


@admin.register(TicketPurchase)
class TicketPurchaseAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "purchased_at"]
    list_filter = ["purchased_at", "event__category", "event__location"]
    search_fields = ["user__username", "user__email", "event__event_name"]
    date_hierarchy = "purchased_at"
    ordering = ["-purchased_at"]
