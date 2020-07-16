# Generated by Django 2.2.10 on 2020-07-16 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20200716_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='surveys.Survey'),
        ),
        migrations.AlterField(
            model_name='responseoption',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='response_options', to='surveys.Question'),
        ),
        migrations.AlterField(
            model_name='surveyresponse',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='survey_responses', to='surveys.Survey'),
        ),
    ]
