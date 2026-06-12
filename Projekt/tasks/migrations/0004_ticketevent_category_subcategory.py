from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0003_ticketevent_location"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketevent",
            name="category",
            field=models.CharField(
                choices=[
                    ("muzyka", "Muzyka"),
                    ("teatr", "Teatr"),
                    ("rodzina", "Rodzina"),
                    ("sport", "Sport"),
                    ("festiwale", "Festiwale"),
                    ("kultura", "Kultura"),
                    ("stand-up", "Stand-up"),
                    ("plenery", "Plenery"),
                    ("kino", "Kino"),
                    ("klasyka", "Klasyka"),
                    ("inne", "Inne"),
                ],
                default="inne",
                max_length=30,
                verbose_name="kategoria",
            ),
        ),
        migrations.AddField(
            model_name="ticketevent",
            name="subcategory",
            field=models.CharField(blank=True, max_length=60, verbose_name="podkategoria"),
        ),
    ]
