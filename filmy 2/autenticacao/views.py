from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import RegistrationForm
import json

class Login(View):
    # Classe para autenticação da versão web
    def get(self, request):
        contexto = {'mensagem': ''}
        if request.user.is_authenticated:
            return redirect('/')  # Redirect to the homepage if user is already authenticated
        else:
            return render(request, 'login.html', contexto)

    def post(self, request):
        # Obtém as credenciais de autenticação do formulário
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        # Verifica as credenciais de autenticação fornecidas
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            # Verifica se o usuário ainda está ativo no sistema
            if user.is_active:
                login(request, user)
                return redirect('/')  # Redirect to the homepage upon successful login

            return render(request, 'login.html', {'mensagem': 'Usuário inativo.'})

        return render(request, 'login.html', {'mensagem': 'Usuário ou senha inválidos.'})

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def mobile_post(self, request):
        try:
            data = json.loads(request.body)
            usuario = data.get('usuario')
            senha = data.get('senha')

            # Verifica as credenciais de autenticação fornecidas
            user = authenticate(request, username=usuario, password=senha)
            if user is not None:
                # Verifica se o usuário ainda está ativo no sistema
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'mensagem': 'Login realizado com sucesso.'}, status=200)

                return JsonResponse({'mensagem': 'Usuário inativo.'}, status=403)

            return JsonResponse({'mensagem': 'Usuário ou senha inválidos.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'mensagem': 'Erro no formato dos dados.'}, status=400)

class Logout(View):
    # Classe para logout da versão web
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def mobile_post(self, request):
        logout(request)
        return JsonResponse({'mensagem': 'Logout realizado com sucesso.'}, status=200)

class Register(View):
    # Classe para registro da versão web
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            form = RegistrationForm()
            return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
        return render(request, 'register.html', {'form': form})

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def mobile_post(self, request):
        try:
            data = json.loads(request.body)
            form = RegistrationForm(data)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return JsonResponse({'mensagem': 'Cadastro realizado com sucesso.'}, status=201)
            return JsonResponse({'mensagem': 'Erro no cadastro.', 'erros': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'mensagem': 'Erro no formato dos dados.'}, status=400)

# Classes dedicadas para API mobile
class LoginMobile(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            usuario = data.get('usuario')
            senha = data.get('senha')

            # Verifica as credenciais de autenticação fornecidas
            user = authenticate(request, username=usuario, password=senha)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return JsonResponse({'mensagem': 'Login realizado com sucesso.'}, status=200)
                return JsonResponse({'mensagem': 'Usuário inativo.'}, status=403)
            return JsonResponse({'mensagem': 'Usuário ou senha inválidos.'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'mensagem': 'Erro no formato dos dados.'}, status=400)

class LogoutMobile(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        logout(request)
        return JsonResponse({'mensagem': 'Logout realizado com sucesso.'}, status=200)

class RegisterMobile(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = RegistrationForm(data)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                login(request, user)
                return JsonResponse({'mensagem': 'Cadastro realizado com sucesso.'}, status=201)
            return JsonResponse({'mensagem': 'Erro no cadastro.', 'erros': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'mensagem': 'Erro no formato dos dados.'}, status=400)