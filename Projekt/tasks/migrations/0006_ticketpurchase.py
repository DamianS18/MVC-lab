from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("tasks", "0005_ticketevent_artists_ticketevent_description"),
    ]

    operations = [
        migrations.CreateModel(
            name="TicketPurchase",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("purchased_at", models.DateTimeField(auto_now_add=True, verbose_name="data zakupu")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchases",
                        to="tasks.ticketevent",
                        verbose_name="wydarzenie",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_purchases",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="uzytkownik",
                    ),
                ),
            ],
            options={
                "verbose_name": "kupiony bilet",
                "verbose_name_plural": "kupione bilety",
                "ordering": ["-purchased_at"],
            },
        ),
    ]
