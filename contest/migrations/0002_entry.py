import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("photo", "0001_initial"), ("contest", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "contest",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contest.Contest",
                    ),
                ),
                (
                    "photo",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="photo.Photo"
                    ),
                ),
            ],
            options={"verbose_name_plural": "Entries"},
        )
    ]
