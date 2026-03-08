from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_slot_delete_timeslot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrole',
            name='available_timings',
        ),
    ]
