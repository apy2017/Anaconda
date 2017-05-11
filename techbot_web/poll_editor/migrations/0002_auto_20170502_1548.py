# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-02 12:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('poll_editor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=128, verbose_name='Answer caption')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'ordering': ['-caption'],
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Poll name')),
                ('passes', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
                'ordering': ['-name'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=128, verbose_name='Question caption')),
                ('from_poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_editor.Poll')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['-caption'],
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='register_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data registration'),
        ),
        migrations.AddField(
            model_name='poll',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_editor.User'),
        ),
        migrations.AddField(
            model_name='answer',
            name='from_question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll_editor.Question'),
        ),
    ]