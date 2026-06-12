from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0002_ticket_event_topic"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketevent",
            name="location",
            field=models.CharField(blank=True, max_length=120, verbose_name="lokalizacja"),
        ),
    ]
