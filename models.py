from tortoise.models import Model
from tortoise import fields


class Person(Model):
    id  = fields.IntField(pk=True,autoincrement=True)
    first_name = fields.CharField(max_length=255)
    middle_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=255)
    address = fields.CharField(max_length=255)
    
    class Meta:
        table = "persons" 
        
    def __str__(self):
        return self.first_name
    
class Users(Model):
    id = fields.IntField(pk=True,autoincrement=True)
    person = fields.ForeignKeyField('models.Person', related_name='users', null=False)
    email = fields.CharField(max_length=255, unique=True)
    password = fields.CharField(max_length=255)
    avatar = fields.CharField(max_length=255)
    access_token = fields.CharField(max_length=255)
    
    class Meta:
        table = "users" 
        
    def __str__(self):
        return self.person.first_name
    
class Employees(Model):
    id = fields.IntField(pk=True,autoincrement=True)
    id_company = fields.ForeignKeyField('models.Companies', related_name='employees', null=False)
    person = fields.ForeignKeyField("models.Person", related_name='employees', null=False)
    salary = fields.FloatField()
    position = fields.CharField(max_length=255)
    department = fields.CharField(max_length=255)
    status = fields.BooleanField()
    date_joined = fields.DateField(auto_now_add=True)
    date_left = fields.DateField(null = True)
    
    class Meta:
        table = "employees"
    def __str__(self):
        return self.person.first_name
    
class Companies(Model):
    id = fields.IntField(pk=True,autoincrement=True)
    nombre = fields.CharField(max_length=255)