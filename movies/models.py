from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    video_release_date = models.DateField(null=True, blank=True)
    imdb_url = models.URLField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title

class User(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    occupation = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    timestamp = models.DateTimeField()