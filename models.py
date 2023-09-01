from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    middle_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    avatar = fields.CharField(max_length=255)
    access_token = fields.CharField(max_length=255)
    
    class Meta:
        table = "users"
        
    def __str__(self):
        return self.name
