from django.shortcuts import redirect, render

from django.http import HttpResponse

from django.shortcuts import render

from datetime import datetime
from Serrurier import models

from Serrurier.models import Avis

from .utils import send_email_with_html_body

from .models import Avis, Contact
from .forms import AvisForm, ContactForm, UserRegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.urls import reverse

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  


def register_view(request):
    lang = request.session.get('lang', 'fr')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Envoyer l'email de bienvenue
            subject = "Bienvenue sur Notre Site"
            template = f'mail/welcome_email_{lang}.html'
            context = {
                'date': datetime.today().date(),
                'username': user.username,
                'email': user.email
            }
            receivers = [user.email]
            send_email_with_html_body(
                subjet=subject,
                receivers=receivers,
                template=template,
                context=context
            )
            # Connecter l'utilisateur directement après l'inscription
            login(request, user)
            messages.success(request, 'compte crée avec succès!')
            return redirect('Serrurier:home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def contact_view(request):
    lang = request.session.get('lang', 'fr')
    template_name = f"accueil/contact_{lang}.html"

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Vous devez enregistrer le formulaire avant d'envoyer l'email pour avoir accès aux données sauvegardées
            contact = form.save()

            # Envoyer un email de confirmation au client
            subject_client = "Confirmation de réception de votre message"
            template_client = 'mail/confirmation_email_client.html'
            context_client = {
                'full_name': contact.full_name,  # Utilisez l'instance sauvegardée pour récupérer le nom complet
                'date': datetime.today().date(),

            }
            send_email_with_html_body(
                subjet=subject_client,
                receivers=[contact.email],  # Utilisez l'instance sauvegardée pour récupérer l'email
                template=template_client,
                context=context_client
            )

            # Envoyer un email de notification au gérant
            subject_manager = "Nouvelle demande de contact"
            template_manager = 'mail/notification_email_manager.html'
            context_manager = {
                'full_name': contact.full_name,  # Utilisez l'instance sauvegardée pour récupérer les données
                'email': contact.email,
                'phone_number': contact.phone_number,
                'message': contact.message,
                'date': datetime.today().date(),
            }
            send_email_with_html_body(
                subjet=subject_manager,
                receivers=['rochdi53sami@gmail.com'],
                template=template_manager,
                context=context_manager
            )

            messages.success(request, 'Votre demande a été envoyé avec succès!')
            # Rediriger vers une page de succès après l'envoi des emails
            return redirect('Serrurier:home')

    else:
        form = ContactForm()

    return render(request, template_name, {'form': form})


def home(request):
    lang = request.session.get('lang', 'fr')
    avis_list = Avis.objects.all()    
    template_name = f"accueil/home_{lang}.html"
    return render(request, template_name, {'avis_list': avis_list})


def service(request):
    lang = request.session.get('lang', 'fr')
    template_name = f"accueil/services_{lang}.html"

    return render(request,template_name)

@login_required
def soumettre_avis(request):
    lang = request.session.get('lang', 'fr')
    template_name = f"avis/AvisForm_{lang}.html"

    if request.method == 'POST' and request.user.is_authenticated:
        # if avis:  # If an avis already exists
        #     form = AvisForm(request.POST, instance=avis)
        # else:
        form = AvisForm(request.POST)
        
        if form.is_valid():
            avis = form.save(commit=False)
            avis.user = request.user
            avis.save()
            messages.success(request, 'Votre Avis a été envoyé avec succès!')
            return redirect('Serrurier:home')
    else:
        form = AvisForm()
    return render(request, template_name, {'form': form})



def create_view(request, *args, **kwargs):
    """ This view help to create and account for testing sending mails."""
    cxt = {}
    if request.method == "POST":
        email = request.POST.get('email')
        print(email)
        subjet = "Test Email"
        template = 'mail/email.html'
        context = {
            'date': datetime.today().date,
            'email': email
        }

        receivers = [email]

        has_send = send_email_with_html_body(
            subjet=subjet,
            receivers=receivers,
            template=template,
            context=context
            )

        if has_send:
           cxt =  {"msg":"mail envoyee avec success."}
        else:
            cxt = {'msg':'email envoie echoue.'}

    return render(request, 'index.html', cxt)       


@staff_member_required  # Ceci garantit que seul un utilisateur staff (admin) peut accéder à cette vue
def admin_contact(request):
    contacts = Contact.objects.all()  # Récupérer toutes les demandes de contact
    return render(request, 'admin/contact_requests.html', {'contacts': contacts})


def change_language(request, lang):
    request.session['lang'] = lang
    return redirect(request.META.get('HTTP_REFERER', reverse('Serrurier:home')))