from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class JokesModel(models.Model):
  content  = models.TextField()
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jokes')
  created_at = models.DateTimeField(auto_now_add=True)
  upvotes = models.IntegerField(default=0)
  downvotes = models.IntegerField(default=0)

  def __str__(self):
    return self.content[:50]
  


# Tracking Users that have voted

class TrackVote(models.Model):
  VOTE_TYPES = (
    ('upvote', 'Upvote'),
    ('downvote', 'Downvote'),
  )
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  joke = models.ForeignKey(JokesModel, on_delete=models.CASCADE, related_name='votes')
  vote_type = models.CharField(max_length=10, choices=VOTE_TYPES)

  class Meta:
    unique_together = ('user', 'joke') # This makes sure one vote per user per joke

  def __str__(self):
    return f"{self.user.email} - {self.vote_type} on joke {self.joke.id}"



