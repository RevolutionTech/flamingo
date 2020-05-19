import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Photo",
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
                ("title", models.CharField(max_length=30)),
                ("img", models.ImageField(upload_to=b"photo")),
                ("description", models.TextField(null=True, blank=True)),
                (
                    "user_profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.UserProfile",
                    ),
                ),
            ],
        )
    ]
