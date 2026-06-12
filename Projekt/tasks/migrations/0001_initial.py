# Generated for the project starter.

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HomeworkTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.CharField(max_length=200, verbose_name="opis")),
                ("due_date", models.DateField(verbose_name="termin wykonania")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("todo", "Do zrobienia"),
                            ("in_progress", "W trakcie"),
                            ("done", "Zrobione"),
                        ],
                        default="todo",
                        max_length=20,
                        verbose_name="status",
                    ),
                ),
            ],
            options={
                "verbose_name": "zadanie domowe",
                "verbose_name_plural": "zadania domowe",
                "ordering": ["due_date", "description"],
            },
        ),
    ]
