# Generated by Django 5.0.1 on 2025-06-10 12:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scolarite', '0003_alter_note_options_note_semestre_note_type_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='etudiant',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='etudiant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etudiant',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
