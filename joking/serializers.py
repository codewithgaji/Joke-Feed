from rest_framework import serializers 
from .models import JokesModel

class JokesSerializer(serializers.ModelSerializer):
  created_by = serializers.StringRelatedField()  # This will show the username instead of ID
  class Meta:
    model = JokesModel
    fields = ['id', 'content', 'upvotes', 'downvotes', 'created_at', 'created_by']
    read_only_fields = ['id', 'created_at', 'created_by', 'upvotes', 'downvotes']