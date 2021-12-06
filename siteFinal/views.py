from braces.views import JsonRequestResponseMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import FormView, View, TemplateView, DetailView
from django.contrib import messages

from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import get_object_or_404

from django.contrib.auth.forms import AuthenticationForm

from .models import Ternos, Atividade
from .forms import ContatoForm
from .utils import GeraPDFMixin


class IndexView(TemplateView):
    template_name = 'index.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context[
            'ternos'] = Ternos.objects.all()  # .order_by('?').all() -Usar caso queira embaralhar como os icones aparecer na tela
        context['atividades'] = Atividade.objects.all()
        return context


class DetalheView(DetailView):
    template_name = 'detalhe.html'
    success_url = reverse_lazy('detalhe')
    model = Ternos

    def terno_detail_view(request, primary_key):
        terno = get_object_or_404(Ternos, pk=primary_key)

        return render(request, 'detalhe/detalhe.html', context={'terno': terno})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


class DetalhePDFView(View, GeraPDFMixin):
    def get(self, request, *args, **kwargs):
        ternos = Ternos.objects.all()
        dados = {
            'ternos': ternos,
        }
        pdf = GeraPDFMixin()
        return pdf.reder_to_pdf('PDF/ternos.html', dados)
