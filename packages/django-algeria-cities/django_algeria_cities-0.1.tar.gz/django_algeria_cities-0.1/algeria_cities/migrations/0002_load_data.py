from django.db import migrations
from django.core.management import call_command


def load_fixture_data(apps, schema_editor):
    call_command("loaddata", "data.json")


class Migration(migrations.Migration):
    dependencies = [
        ("algeria_cities", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(load_fixture_data),
    ]

