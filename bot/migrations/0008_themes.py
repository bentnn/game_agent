# Generated by Django 4.0.4 on 2022-05-24 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_merge_0013_sessions_0015_alter_articles_options'),
        ('bot', '0007_settingsbot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.IntegerField(verbose_name='IDS')),
                ('theme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.articles', verbose_name='Тема')),
            ],
            options={
                'verbose_name': 'Тема',
                'verbose_name_plural': 'Темы',
            },
        ),
    ]
