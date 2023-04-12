# Generated by Django 4.2 on 2023-04-12 04:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MajorItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='DetailItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.CharField(max_length=20)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_id', to='chamberlain.majoritem')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_created=True)),
                ('content', models.CharField(max_length=20)),
                ('end_time', models.DateTimeField(blank=True)),
                ('spend_time', models.FloatField(default=0)),
                ('items', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_item', to='chamberlain.detailitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]