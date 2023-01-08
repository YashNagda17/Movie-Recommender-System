from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
class movies(models.Model):
    movieId = models.IntegerField(_("movieId"),primary_key=True)
    title = models.CharField( _("title"), max_length=511)
    adult = models.BooleanField(_("adult"), default=False)
    imdbid = models.CharField(_("imdbid"), max_length = 511)
    backdrop = models.CharField(_("backdrop"), max_length=255, blank=True, null=True)
    genres = models.CharField(_("genres"), max_length=511, blank = True, null=True)
    overviews = models.CharField(_("overviews"), max_length=1024, blank = True, null=True)
    
    def __str__(self) -> str:
        return self.title
    
    
    