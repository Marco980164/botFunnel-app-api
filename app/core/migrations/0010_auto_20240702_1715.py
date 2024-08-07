# Generated by Django 3.2.25 on 2024-07-02 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20240625_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configbot',
            name='descripcionNegocio',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='configbot',
            name='proposito',
            field=models.TextField(),
        ),
        migrations.CreateModel(
            name='InstanciaConversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preguntaRealizada', models.TextField()),
                ('respuestaCliente', models.TextField()),
                ('conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.conversacion')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.pregunta')),
            ],
        ),
    ]
