from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contest",
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
                ("name", models.CharField(max_length=100, db_index=True)),
                ("slug", models.SlugField(max_length=100)),
                ("description", models.TextField(null=True, blank=True)),
                ("submission_open", models.DateTimeField(null=True, blank=True)),
                ("submission_close", models.DateTimeField(null=True, blank=True)),
                ("end", models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Sponsor",
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
                ("name", models.CharField(max_length=30, db_index=True)),
                ("slug", models.SlugField(max_length=30)),
                ("bio", models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name="contest",
            name="sponsor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="contest.Sponsor"
            ),
        ),
    ]
