# Generated by Django 3.0.4 on 2020-07-03 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('b', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte', models.IntegerField(default=1)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='b.Commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes_commande', to='b.Produit')),
            ],
        ),
        migrations.AddConstraint(
            model_name='lignecommande',
            constraint=models.UniqueConstraint(fields=('produit', 'commande'), name='produit-commande'),
        ),
    ]
