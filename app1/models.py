from django.db import models
from django.conf import settings



class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_year = models.IntegerField()
    duration = models.IntegerField()
    rating = models.FloatField(default=0.0)
    poster = models.URLField(blank=True)
    
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="movies"
    )
    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name="movies"
    )

    def __str__(self):
        return self.title




class MyList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="my_list"
    )

    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE,
        related_name="saved_by_users"
    )

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                name="unique_user_saved_movie"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.movie.title}"
