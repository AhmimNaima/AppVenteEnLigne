from django.contrib import admin
from b.models import User,Client,Fournisseur,Produit,Facture, LigneFacture,Fournisseur,Categorie,Admin,Commande,LigneCommande


# Register your models here.

admin.site.register(Produit)
admin.site.register(LigneFacture)
admin.site.register(Fournisseur)
admin.site.register(Categorie)
admin.site.register(Client)
admin.site.register(Facture)
admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Commande)
admin.site.register(LigneCommande)
