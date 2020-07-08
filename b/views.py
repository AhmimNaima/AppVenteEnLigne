from django.shortcuts import render, get_object_or_404
from b.models import Facture, LigneFacture,Client,Fournisseur,User,Admin,Produit,Commande,LigneCommande
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django_tables2 import SingleTableView
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Button
from django.urls import reverse
from django.db.models import Sum
from django.db.models import ExpressionWrapper,F,FloatField
from django.conf import settings
from bootstrap_datepicker_plus import DatePickerInput
import datetime
from jchart import Chart
from jchart.config import Axes, DataSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
# Create your views here.



def home(request):
    return render(request, 'bill/base.html')


def facture_detail_view(request, pk):
    facture = get_object_or_404(Facture, id=pk)
    context={}
    context['facture'] = facture
    return render(request, 'bill/facture_detail.html', context)


                    # Gestion client ##
class ClientTable(tables.Table):
    action= '<a href="{% url "client_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>\
             <a href="{% url "facture_table" pk=record.id %}" class="btn btn-primary">Factures</a>'   
    ca_client = tables.Column("ca_client") 
    edit   = tables.TemplateColumn(action) 

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields = [ 'nom','prenom','adresse','tel','sexe']

      
        
class ClientView(ListView):
    template_name = 'bill/listUser.html'
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        table = ClientTable(Client.objects.all().annotate(ca_client=Sum(ExpressionWrapper(F('facture__lignes__qte'),output_field=FloatField()) * F('facture__lignes__produit__prix'))))
        RequestConfig(self.request, paginate={"per_page": 8}).configure(table)
        context['table'] = table
        context['URLCreat']  = "/bill/client_create/"
        context['object'] = 'Client'
        context['title'] = 'La liste des clients :'

        return context

class ClientCreateView(CreateView):
    model = Client
    template_name = 'bill/create.html'
    fields = [ 'nom','prenom','adresse','tel','sexe']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client')
        return form

class ClientUpdateView(UpdateView):
    model =Client
    template_name = 'bill/update.html'
    fields = [ 'nom','prenom','adresse','tel','sexe']
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.fields['client']=forms.ModelChoiceField(queryset=Client.objects.all(), initial=0)
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('client')
        return form


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'bill/delete.html'
    
    def get_success_url(self):
        success_url = reverse('client')
        return success_url


#----------------- Gestion Facture----------------- ##

class FactureTable(tables.Table):
    action= '<a href="{% url "facture_table_detail" pk=record.id %}" class="btn btn-warning">Details</a>'
    Total=tables.Column("Total")
    Detail=tables.TemplateColumn(action)
    class Meta:
        model = Facture
        template_name = "django_tables2/bootstrap4.html"
        fields=['date']
                      

class FactureView(ListView):
    template_name = 'bill/commandes.html'
    model = Facture
    
    def get_context_data(self, **kwargs):
        context = super(FactureView, self).get_context_data(**kwargs)
        table = FactureTable(Facture.objects.filter(client_id=self.kwargs.get('pk')).annotate(Total=Sum(F("lignes__produit__prix") * F("lignes__qte"),output_field=FloatField())))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        context['object'] = 'Facture'
        context['title'] = 'La liste des factures:'
        return context
   


class LigneFactureTable(tables.Table):
    class Meta:
        model = LigneFacture
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__designation', 'produit__prix', 'qte' )


class FactureDetailView(DetailView):
    template_name = 'bill/facture_table_detail.html'
    model = Facture
    
    def get_context_data(self, **kwargs):
        context = super(FactureDetailView, self).get_context_data(**kwargs)
        
        table = LigneFactureTable(LigneFacture.objects.filter(facture=self.kwargs.get('pk')))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        return context


             # Gestion Fournisseurs 
class FournisseurTable(tables.Table):
    action=  '<a href="{% url "fournisseur_delete" pk=record.id %}" class="btn btn-danger">Supprimer</a>'
             
    edit   = tables.TemplateColumn(action) 

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
      
        
        

class FournisseurView(ListView):
    template_name = 'bill/listUser.html'
    model = Fournisseur

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        table = FournisseurTable(Fournisseur.objects.all())
        RequestConfig(self.request, paginate={"per_page": 8}).configure(table)
        context['table'] = table
        context['URLCreat']  = "/bill/fournisseur_create/"
        context['object'] = 'Fournisseur'
        context['title'] = 'La liste des fournisseurs :'

        return context

class FournisseurCreateView(CreateView):
    model = Fournisseur
    template_name = 'bill/create.html'
    fields = [ 'nom','prenom','adresse','tel','sexe']
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur')
        return form
    
    def get_context_data(self, **kwargs):
        context = super(FournisseurCreateView, self).get_context_data(**kwargs)
        context['object'] = 'Fournisseur'
        context['title'] = "Création d'un fournisseur"

        return context
class FournisseurUpdateView(UpdateView):
    model =Fournisseur
    template_name = 'bill/update.html'
    fields = [ 'nom','prenom','adresse','tel','sexe']
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('fournisseur')
        return form



class FournisseurDeleteView(DeleteView):
    model = Fournisseur
    template_name = 'bill/delete.html'
    
    def get_success_url(self):
        success_url = reverse('fournisseur')
        return success_url
 

class ClientTableDash(tables.Table):   
    ca_client = tables.Column("ca_client")  

    class Meta:
        model = Client
        template_name = "django_tables2/bootstrap4.html"
        fields=('facture__client__nom','facture__client__prenom')


class FournisseurTableDash(tables.Table):   
    ca_fournisseur = tables.Column("ca_fournisseur")  

    class Meta:
        model = Fournisseur
        template_name = "django_tables2/bootstrap4.html"
        fields=('produit__fournisseur__nom','produit__fournisseur__prenom')

def Dash(request):
    context = {}
    fournisseur = FournisseurTableDash(LigneFacture.objects.all().values('produit__fournisseur__nom','produit__fournisseur__prenom').
    annotate(ca_fournisseur=Sum(ExpressionWrapper(F('qte'),output_field=FloatField())*F('produit__prix'))))
    client = ClientTableDash(LigneFacture.objects.all().values('facture__client__nom','facture__client__prenom').
    annotate(ca_client=Sum(ExpressionWrapper(F('qte'),output_field=FloatField())*F('produit__prix'))))
    RequestConfig(request, paginate={"per_page": 10}).configure(client)
    context['client'] = client
    RequestConfig(request, paginate={"per_page": 10}).configure(fournisseur)
    context['fournisseur'] = fournisseur
    context['LineChart']=LineChart()
    context['radar']=RadarChart()

    return render(request, 'bill/Dash.html',context)

    
class LineChart(Chart):
    chart_type = 'line'
    scales = {
        'xAxes': [Axes(type='time', position='bottom')],
    }
    def get_datasets(self, **kwargs):
     factures = Facture.objects.all().values('date').annotate(y=Sum(F("lignes__produit__prix")*F("lignes__qte"),output_field=FloatField()))
     data=factures.annotate(x=F('date')).values('x','y') 
     return[DataSet(
                    type='line',
                    label='Evaluation du chiffre d\'affaire par jour',
                    data=list(data)
                    )]
        
        

class RadarChart(Chart):
    chart_type = 'radar'
    labels = []
    data = []
    produits = LigneFacture.objects.all().values('produit__categorie').annotate(total=Sum(F("produit__prix") * F("qte"),output_field=FloatField()),Categorie=F("produit__categorie__nom"))
    for f in produits:
          labels.append(f['Categorie'])
          data.append(f['total'])
          
    def get_labels(self):
        return self.labels

    

    def get_datasets(self, **kwargs):
        return [
                DataSet(label="le chiffre d'affaire réparti par catégorie de Produit",
                        color=(255, 99, 132),
                        data=self.data )
               ]

###############l'authentification, inscription des utilisateurs##########

class SignUp(UserCreationForm):
    nom = forms.CharField(required=False)
    prenom = forms.CharField(required=False)
    email = forms.EmailField(help_text='A valid email address, please.')
    SEXE = (
        ('M', 'Masculin'),
        ('F', 'Feminin')
    )
    adresse = forms.CharField(required=False)
    tel = forms.CharField(required=False)
    sexe = forms.ChoiceField(choices=SEXE)
    class Meta:
        model = User
        fields = ('username', 'nom', 'prenom', 'email','adresse' , 'tel','sexe', 'password1', 'password2' , 'user_type')
        

def register(response):
        if response.method == "POST":
           form = SignUp(response.POST)
           if form.is_valid():
              user = form.save()
              sexe = form.cleaned_data.get('sexe')
              tel = form.cleaned_data.get('tel')
              adresse = form.cleaned_data.get('adresse')
              nom = form.cleaned_data.get('nom')
              prenom = form.cleaned_data.get('prenom')
              user_type = form.cleaned_data.get('user_type')
              
              if user_type==1:
                  Client.objects.create(user=user,sexe=sexe,tel=tel,adresse=adresse,nom=nom,prenom=prenom)
                  login(response, user)
                  messages.info(response, "Votre compte Client a été créé")
                  return redirect('home')
              elif user_type==2:
                   Fournisseur.objects.create(user=user,sexe=sexe,tel=tel,adresse=adresse,nom=nom,prenom=prenom)
                   login(response, user)
                   messages.info(response, "Votre compte Fournisseur a été créé")
                   return redirect('home')
              else:
                   Admin.objects.create(user=user,sexe=sexe,tel=tel,adresse=adresse,nom=nom,prenom=prenom)
                   login(response, user) 
                   messages.info(response, "Votre compte Administrateur a été créé")                                                                                                       
                   return redirect('home')
        else:
          form = SignUp()

        return render(response, "registration/signup.html", {"form":form})


#------------------Gestion Produits-------------------------------

class ProduitTable(tables.Table):

    add_panier = '<a href="{% url "add_produit_panier" pk=record.id %}" class="btn btn-info">Ajouter</a>'
    photo =  '<img src="{{ record.photo.url }}" alt="produit" width="200" height="200">'
    photo = tables.TemplateColumn(photo)

    Panier   = tables.TemplateColumn(add_panier)

    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"
        fields = ('designation','categorie', 'prix')

class ProduitTableAdmin(tables.Table):
    action= '<a href="{% url "produit_update" pk=record.id  %}" class="btn btn-warning">Modifier</a>\
             <a href="{% url "produit_delete" pk=record.id  %}" class="btn btn-danger">Supprimer</a>'
    photo =  '<img src="{{ record.photo.url }}" alt="produit" width="200" height="200">'
    photo = tables.TemplateColumn(photo)
    edit   = tables.TemplateColumn(action) 
   
    class Meta:
        model = Produit
        template_name = "django_tables2/bootstrap4.html"
        fields = ('designation','categorie', 'prix')

class ProduitListViewAdmin(ListView):
    template_name = 'bill/list.html'
    model = Produit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produits = Produit.objects.all()
        table = ProduitTableAdmin(produits)
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        context['URLCreat']  = "/bill/produit_table_create/"
        context['object'] = 'produit'
        context['title'] = 'La liste des produits :'

        return context

class ProduitListViewClient(ListView):
    template_name = 'bill/produits.html'
    model = Produit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produits = Produit.objects.all()
        table = ProduitTable(produits)
        RequestConfig(self.request, paginate={"per_page": 5}).configure(table)
        context['table'] = table
        context['object'] = 'produit'
        context['title'] = 'La liste des produits :'

        return context


class ProduitCreateView(CreateView):
    model = Produit
    template_name = 'bill/create.html'
    fields = '__all__'
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()

        form.helper.add_input(Submit('submit','Créer', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('produits')
        return form

    def get_context_data(self, **kwargs):
        ctx = super(ProduitCreateView, self).get_context_data(**kwargs)
        ctx['object'] = 'Produit'
        ctx['title'] = "Création d'un Produit :"
        return ctx

class ProduitUpdateView(UpdateView):
    model =Produit
    template_name = 'bill/update.html'
    fields = '__all__'
    
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.add_input(Submit('submit','Modifier', css_class='btn-primary'))
        form.helper.add_input(Button('cancel', 'Annuler', css_class='btn-secondary', onclick="window.history.back()"))
        self.success_url = reverse('produits')
        return form


class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = 'bill/delete.html'
    
    def get_success_url(self):
        success_url = reverse('produits')
        return success_url
 



@login_required
def ajouter_panier_view(request, pk):
    context={}
    if request.method == 'GET':
        produit = get_object_or_404(Produit, id=pk)
        context['produit'] = produit
        return render(request, 'bill/Add_panier.html', context)
    elif request.method == 'POST':
        produit = get_object_or_404(Produit, id=pk)
        if 'qte' not in request.POST:
            qte = 1
        else:
            qte = int(request.POST['qte'])
            if qte < 0:
                qte = 1

        if 'panier' not in request.session:
            request.session['panier'] = {}
        request.session['panier'][int(pk)] = qte
        request.session.modified = True
        return HttpResponseRedirect(reverse('produits_client'))


class PanierTable(tables.Table):

    produit = tables.Column()
    qte = tables.Column()
    prix= tables.Column()

    class Meta:
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit','qte','prix')

@login_required
def panier_detail_view(request):
    panier = []
    context = {}

    if 'panier' in request.session:
        for pk,qte in request.session['panier'].items():
            produit = get_object_or_404(Produit, id=pk)
            panier.append({"produit":produit,"qte":qte,"prix":produit.prix})

    table = PanierTable(panier)
    RequestConfig(request, paginate={"per_page": 5}).configure(table)
    context['table'] = table
    context['title'] = 'Mon panier'

    return render(request, 'bill/panier.html', context)


@login_required
def confirme_panier_view(request):

    if 'panier' in request.session and len(request.session['panier']) > 0:
        commande = Commande.objects.create(client=request.user.client)
        for pk,qte in request.session['panier'].items():
            produit = get_object_or_404(Produit, id=pk)
            LigneCommande.objects.create(produit=produit,qte=qte,commande=commande)
        request.session['panier'] = {}
        request.session.modified = True
    
    return HttpResponseRedirect(reverse('commandes'))
    

#----------------Gestion Commandes ------------------------------

class CommandeTable(tables.Table):

    lignes = '<a href="{% url "commande_table_detail" pk=record.id %}" class="btn btn-info">Details</a>'
    Details   = tables.TemplateColumn(lignes)

    class Meta:
        model = Commande
        template_name = "django_tables2/bootstrap4.html"
        fields = ('date', 'valide')

class CommandeTableAdmin(CommandeTable):

    valider = '<a href="{% url "valider_commande" pk=record.id %}" class="btn btn-info">Valider </a>'
    valider   = tables.TemplateColumn(valider)
    class Meta:
        model = Commande
        template_name = "django_tables2/bootstrap4.html"
        fields = ('client','date', 'valide')

#Commande list view
class CommandeListView(ListView):

    template_name = 'bill/commandes.html'
    model = Commande

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        filter = {}
        if self.request.user.is_authenticated:
            if self.request.user.user_type == 1:
                filter['client'] = self.request.user.client
        commandes = Commande.objects.filter(**filter)

        if self.request.user.user_type == 0:
            table = CommandeTableAdmin(commandes)
        elif self.request.user.user_type == 1:
            table = CommandeTable(commandes)

        RequestConfig(self.request, paginate={"per_page": 8}).configure(table)
        context['table'] = table
        context['object'] = 'Commande'
        context['title'] = 'La liste des commandes :'

        return context


class LigneCommandeTable(tables.Table):
    class Meta:
        model = LigneCommande
        template_name = "django_tables2/bootstrap4.html"
        fields = ('produit__id','produit__designation', 'produit__prix', 'qte')



class CommandeDetailView(DetailView):
    template_name = 'bill/commandes.html'
    model = Commande

    def get_context_data(self, **kwargs):
        context = super(CommandeDetailView, self).get_context_data(**kwargs)
        commande = Commande.objects.get(id=self.kwargs.get('pk'))
        table = LigneCommandeTable(LigneCommande.objects.filter(commande=commande))
        RequestConfig(self.request, paginate={"per_page": 2}).configure(table)
        context['table'] = table
        context['object'] = 'LigneCommande'
        context['title'] = 'La liste des produits de la commande :'

        return context

@login_required
def valider_commande_view(request, pk):
    
    commande = Commande.objects.filter(id=pk)
    
    if commande[0].valide == False:
        commande.update(valide = True)
        commande = commande[0]
        facture = Facture.objects.create(client=commande.client,commande=commande)
        for ligne in commande.lignes.all():
            LigneFacture.objects.create(produit=ligne.produit,qte=ligne.qte,facture=facture)

    return HttpResponseRedirect(reverse('commandes'))

            

        