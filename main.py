from http.client import HTTPException
from fastapi import FastAPI, Request,status
from tortoise.contrib.fastapi import register_tortoise
from schemas import (EmailCreate, UserSchema,PersonSchema,EmployeeSchema,CompaniesSchema)
from models import Person,Users,Employees,Companies
from modules import create_mail
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    TORTOISE_ORM = {
        "connections": {"default": "postgres://root:pL98wvcPfs@entryflow-test.cifrirvwybqx.us-east-1.rds.amazonaws.com/entryflow"},
        "apps": {
        "models": {
        "models": ["models"],
        "default_connection": "default",
        },
        },
    }
    
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=True,
        add_exception_handlers=True,
    )
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

## CRUD COMPANIES
@app.post("/companies",response_model=CompaniesSchema,status_code=status.HTTP_201_CREATED)
async def create_company(company:CompaniesSchema) -> CompaniesSchema:
    company_Obj = await Companies.create(**company.dict())
    return CompaniesSchema.from_orm(company_Obj)

@app.get("/companies/{company_id}",response_model=CompaniesSchema)
async def get_company(company_id:int) -> CompaniesSchema:
    company_Obj = await Companies.get(id=company_id)
    if company_Obj is None:
        raise HTTPException(status_code=404, detail="Compañia no encontrada")
    return CompaniesSchema.from_orm(company_Obj)

@app.put("/companies/{company_id}",response_model=CompaniesSchema)
async def update_company(company_id:int,company:CompaniesSchema) -> CompaniesSchema:
    company_Obj = await Companies.get(id=company_id)
    await company_Obj.update_from_dict(company.dict()).save()
    return CompaniesSchema.from_orm(company_Obj)

@app.delete("/companies/{company_id}",response_model=CompaniesSchema)
async def delete_company(company_id:int) -> CompaniesSchema:
    company_obj= await Companies.get(id=company_id)
    await company_obj.delete()
    return CompaniesSchema.from_orm(company_obj)

## CRUD PERSONS

@app.post("/persons",response_model=PersonSchema,status_code=status.HTTP_201_CREATED)
async def create_person(person:PersonSchema) -> PersonSchema:
    person_Obj = await Person.create(**person.dict())
    return PersonSchema.from_orm(person_Obj)

@app.get("/persons/{person_id}",response_model=PersonSchema)
async def get_person(person_id:int) -> PersonSchema:
    person_Obj = await Person.get(id=person_id)
    if person_Obj is None:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return PersonSchema.from_orm(person_Obj)

@app.put("/persons/{person_id}",response_model=PersonSchema)
async def update_person(person_id:int,person:PersonSchema) -> PersonSchema:
    person_Obj = await Person.get(id=person_id)
    await person_Obj.update_from_dict(person.dict()).save()
    return PersonSchema.from_orm(person_Obj)

@app.delete("/persons/{person_id}",response_model=PersonSchema)
async def delete_person(person_id:int) -> PersonSchema:
    person_Obj = await Person.get(id=person_id)
    await person_Obj.delete()
    return PersonSchema.from_orm(person_Obj)

## CRUD USERS

@app.post("/users",response_model=UserSchema,status_code=status.HTTP_201_CREATED)
async def create_user(user:UserSchema) -> UserSchema:
    user_Obj = await User.create(**user.dict())
    return UserSchema.from_orm(user_Obj)

@app.get("/users/{user_id}",response_model=UserSchema)
async def get_user(user_id:int) -> UserSchema:
    user_Obj = await Users.get(id=user_id)
    if user_Obj is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserSchema.from_orm(user_Obj)

@app.put("/users/{user_id}",response_model=UserSchema)
async def update_user(user_id:int,user:UserSchema) -> UserSchema:
    user_Obj = await Users.get(id=user_id)
    await user_Obj.update_from_dict(user.dict()).save()
    return UserSchema.from_orm(user_Obj)

@app.delete("/users/{user_id}",response_model=UserSchema)
async def delete_user(user_id:int) -> UserSchema:
    user_Obj = await Users.get(id=user_id)
    await user_Obj.delete()
    return UserSchema.from_orm(user_Obj)

## Correo usuarios
@app.post("/email",status_code=status.HTTP_200_OK)
async def send_email(email: EmailCreate):
    print(email.dict())
    create_mail(**email.dict())
    return {"status": "ok"}


## CRUD EMPLOYEES
@app.post("/employees",response_model=EmployeeSchema,status_code=status.HTTP_201_CREATED)
async def create_employee(employee:EmployeeSchema) -> EmployeeSchema:
    employee_Obj = await Employees.create(**employee.dict())
    return EmployeeSchema.from_orm(employee_Obj)


@app.get("/employees/{employee_id}",response_model=EmployeeSchema)
async def get_employee(employee_id:int) -> EmployeeSchema:
    employee_Obj = await Employees.get(id=employee_id)
    if employee_Obj is None:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return EmployeeSchema.from_orm(employee_Obj)

@app.put("/employees/{employee_id}",response_model=EmployeeSchema)
async def update_employee(employee_id:int,employee:EmployeeSchema) -> EmployeeSchema:
    employee_Obj = await Employees.get(id=employee_id)
    await employee_Obj.update_from_dict(employee.dict()).save()
    return EmployeeSchema.from_orm(employee_Obj)

@app.delete("/employees/{employee_id}",response_model=EmployeeSchema)
async def delete_employee(employee_id:int) -> EmployeeSchema:
    employee_Obj = await Employees.get(id=employee_id)
    await employee_Obj.delete()
    return EmployeeSchema.from_orm(employee_Obj)
