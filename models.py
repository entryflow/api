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
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"
        
    def __str__(self):
        return self.name

class Employee(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    middle_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    num_control = fields.CharField(max_length=255)
    avatar = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    #company = fields.ForeignKeyField('models.Company', related_name='employees')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "employees"
        
    def __str__(self):
        return self.name
    
class Company(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "companies"
        
    def __str__(self):
        return self.name