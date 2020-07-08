from django.urls import  path, re_path, include
from b import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    re_path(r'^facture_detail/(?P<pk>\d+)/$', views.facture_detail_view, name='facture_detail'),
    re_path(r'^facture_table/(?P<pk>\d+)/$', views.FactureView.as_view(), name='facture_table'),
    re_path(r'^facture_table_detail/(?P<pk>\d+)/$', views.FactureDetailView.as_view(), name='facture_table_detail'),
    re_path(r'^client_table', views.ClientView.as_view(), name='client'),
    re_path(r'^client_create', views.ClientCreateView.as_view(), name='client_create'),
    re_path(r'^client_delete/(?P<pk>\d+)/$', views.ClientDeleteView.as_view(), name='client_delete'),
    re_path(r'^client_update/(?P<pk>\d+)/$', views.ClientUpdateView.as_view(), name='client_update'),
    re_path(r'^fournisseur_table', views.FournisseurView.as_view(), name='fournisseur'),
    re_path(r'^fournisseur_create', views.FournisseurCreateView.as_view(), name='fournisseur_create'),
    re_path(r'^fournisseur_delete/(?P<pk>\d+)/$', views.FournisseurDeleteView.as_view(), name='fournisseur_delete'),
    re_path(r'^fournisseur_update/(?P<pk>\d+)/$', views.FournisseurUpdateView.as_view(), name='fournisseur_update'),
    re_path(r'^Dash/', views.Dash, name='Dash'),
    re_path(r'^register/', views.register, name='register'),
    re_path(r'^home/', views.home, name='home'),
    re_path(r'produits/', views.ProduitListViewAdmin.as_view(), name='produits'),
    re_path(r'produitsClient/', views.ProduitListViewClient.as_view(), name='produits_client'),
    re_path(r'produit_table_create/', views.ProduitCreateView.as_view(), name='produit_table_create'),
    re_path(r'^produit_delete/(?P<pk>\d+)/$', views.ProduitDeleteView.as_view(), name='produit_delete'),
    re_path(r'^produit_update/(?P<pk>\d+)/$', views.ProduitUpdateView.as_view(), name='produit_update'),
    re_path(r'add_produit_panier/(?P<pk>\d+)/$', views.ajouter_panier_view, name='add_produit_panier'),
    re_path(r'confirme_panier/', views.confirme_panier_view, name='confirme_panier'),
    re_path(r'panier/', views.panier_detail_view, name='panier'),
    re_path(r'commandes/',login_required(views.CommandeListView.as_view()), name='commandes'),
    re_path(r'commande_table_detail/(?P<pk>\d+)/$', views.CommandeDetailView.as_view(), name='commande_table_detail'),
    re_path(r'valider_commande/(?P<pk>\d+)/$', views.valider_commande_view, name='valider_commande'),
    

    ] 