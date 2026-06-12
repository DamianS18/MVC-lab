from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0004_ticketevent_category_subcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticketevent",
            name="artists",
            field=models.TextField(blank=True, verbose_name="artysci"),
        ),
        migrations.AddField(
            model_name="ticketevent",
            name="description",
            field=models.TextField(blank=True, verbose_name="opis wydarzenia"),
        ),
    ]
