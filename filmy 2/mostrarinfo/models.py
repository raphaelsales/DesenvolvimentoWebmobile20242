from django.db import models #  módulo do Django que permite criar classes para representar tabelas no banco de dados.
from django.contrib.auth.models import User

class ToWatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Esse campo cria uma relação entre a tabela ToWatchList e a tabela User.
    movie_id = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s watchlist - Movie ID: {self.movie_id}"

    def get_movie_ids(self): #Armazena o ID do filme que o usuário quer assistir.
        return list(ToWatchList.objects.filter(user=self.user).values_list('movie_id', flat=True))

