from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('inventory', '0016_alter_suppliers_direccion_alter_suppliers_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialmovimiento',
            name='boleta_codigo',
            field=models.CharField(max_length=32, blank=True, null=True, help_text='Código de boleta chileno (opcional)'),
        ),
    ]
