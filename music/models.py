"""Define the Song model."""
from django.db import models
from django.utils.translation import pgettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.
class Songs(models.Model):
    """The Song model."""
    user = models.ForeignKey(
        User(),
        related_name='artist',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None
    )
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of the artist or group/band
    artist = models.CharField(max_length=255, null=False)
    # name of the album
    album = models.CharField(max_length=255, null=False, default='New Album') 
    image = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(
        _('Songs field', 'created at'),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        _('Songs field', 'updated at'),
        auto_now=True
    )

    class Meta:
        """define metadata."""
        app_label = 'music'

    def __str__(self):
        """Print out title and artist."""
        return "{} - {}".format(self.title, self.artist)
