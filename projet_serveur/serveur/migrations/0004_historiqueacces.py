# Generated by Django 2.1.15 on 2025-05-03 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serveur', '0003_auto_20250427_0109'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriqueAcces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entree', models.DateTimeField()),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serveur.Employe')),
            ],
        ),
    ]
