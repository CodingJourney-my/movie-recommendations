from django.shortcuts import render
from django.views import generic
from django.utils import timezone

from .models import Movie

# Create your views here.

class IndexView(generic.ListView):
    template_name = "movies/index.html"
    context_object_name = "latest_movies_list"

    def get_queryset(self):
        return Movie.objects.filter(pub_date__lte=timezone.now())
