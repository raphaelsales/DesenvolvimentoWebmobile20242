from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
import requests
from mostrarinfo.models import ToWatchList
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

# Main - Versão Web
def show_movie_info(request, movie_id):
    if 'Add' in request.GET:
        return add_to_watchlist(request, movie_id)
    
    url = f"{settings.API_SHOW_MOVIE_INFO_URL}"
    ondeInserirOID = url.find("/movie/") + len("/movie/")
    enderecoParaBuscarFilme = url[:ondeInserirOID] + str(movie_id) + url[ondeInserirOID:]
    filme = requests.get(enderecoParaBuscarFilme).json()
    
    # Convert release date to desired format
    release_date = filme.get('release_date')
    if release_date:
        release_date_obj = datetime.strptime(release_date, '%Y-%m-%d')
        filme['release_date'] = release_date_obj.strftime('%B %-d, %Y')
    
    context = {
        'filme': filme
    }
    return render(request, 'showinfo.html', context)

# Main - Versão API para App Mobile
def show_movie_info_api(request, movie_id):
    if request.method == 'GET':
        url = f"{settings.API_SHOW_MOVIE_INFO_URL}"
        ondeInserirOID = url.find("/movie/") + len("/movie/")
        enderecoParaBuscarFilme = url[:ondeInserirOID] + str(movie_id) + url[ondeInserirOID:]
        filme = requests.get(enderecoParaBuscarFilme).json()

        # Convert release date to desired format
        release_date = filme.get('release_date')
        if release_date:
            release_date_obj = datetime.strptime(release_date, '%Y-%m-%d')
            filme['release_date'] = release_date_obj.strftime('%B %-d, %Y')

        return JsonResponse(filme, safe=False)

# Adiciona o filme à lista de desejos - Versão Web
def add_to_watchlist(request, filme_id):
    if request.user.is_authenticated:
        if not ToWatchList.objects.filter(user=request.user, movie_id=filme_id).exists():
            ToWatchList.objects.create(user=request.user, movie_id=filme_id)
        return redirect(reverse('show_movie_info', args=[filme_id]))
    else:
        return redirect('Login')

# Adiciona o filme à lista de desejos - Versão API para App Mobile
@csrf_exempt
def add_to_watchlist_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Lê os dados enviados no corpo da requisição
            movie_id = data.get("movie_id")
            user = request.user

            # Verifica se o filme já está na watchlist
            if not ToWatchList.objects.filter(user=user, movie_id=movie_id).exists():
                ToWatchList.objects.create(user=user, movie_id=movie_id)
                return JsonResponse({"message": "Movie added to watchlist."}, status=201)
            else:
                return JsonResponse({"message": "Movie already in watchlist."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)

