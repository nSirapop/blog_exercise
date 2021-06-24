from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blog(models.Model):
    """A blog type the user writing."""
    title = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Post(models.Model):
    """Posts that are in each blog."""
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string of model instead of entire model."""
        return self.title