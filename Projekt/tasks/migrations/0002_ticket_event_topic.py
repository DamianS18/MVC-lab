from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="HomeworkTask",
            new_name="TicketEvent",
        ),
        migrations.RenameField(
            model_name="ticketevent",
            old_name="description",
            new_name="event_name",
        ),
        migrations.RenameField(
            model_name="ticketevent",
            old_name="due_date",
            new_name="event_date",
        ),
        migrations.RemoveField(
            model_name="ticketevent",
            name="status",
        ),
        migrations.AddField(
            model_name="ticketevent",
            name="seats",
            field=models.PositiveIntegerField(default=50, verbose_name="liczba miejsc"),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name="ticketevent",
            options={
                "ordering": ["event_date", "event_name"],
                "verbose_name": "wydarzenie",
                "verbose_name_plural": "wydarzenia",
            },
        ),
        migrations.AlterField(
            model_name="ticketevent",
            name="event_name",
            field=models.CharField(max_length=200, verbose_name="nazwa wydarzenia"),
        ),
        migrations.AlterField(
            model_name="ticketevent",
            name="event_date",
            field=models.DateField(verbose_name="data"),
        ),
    ]
