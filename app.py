import uvicorn
from typing import List, Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(
    title="Waqq.ly Website",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class DogWalkerInfo(BaseModel):
    email: str
    password: str


class AdditionalPetInfo(BaseModel):
    name: str
    breed: str
    age: int


class DogOwnerInfo(BaseModel):
    email: str
    password: str
    dog: str
    breed: str
    age: int
    add_pet: Optional[List[AdditionalPetInfo]] = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_registry_info(request: Request):
    form_data = await request.form()

    email = form_data.get("email")
    password = form_data.get("password")

    if form_data.get("dog_walker") is not None:
        if email and password:
            dog_walker_info = DogWalkerInfo(email=email, password=password)

            print(dog_walker_info)
            return templates.TemplateResponse("dashboard.html", {"request": request, "submitted": True})

    if form_data.get("dog_owner") is not None:
        dog = form_data.get("dog")
        breed = form_data.get("breed")
        age = form_data.get("age")

        add_dog = form_data.getlist("add_dog")
        add_breed = form_data.getlist("add_breed")
        add_age = form_data.getlist("add_age")

        additional_pets = []
        for pet_name, pet_breed, pet_age in zip(add_dog, add_breed, add_age):
            AdditionalPetInfo(name=pet_name, breed=pet_breed, age=int(pet_age))

        if email and password and dog and breed and age:
            dog_owner_info = DogOwnerInfo(
                email=email,
                password=password,
                dog=dog,
                breed=breed,
                age=int(age),
                add_pet=additional_pets
            )

            print(dog_owner_info)
            return templates.TemplateResponse("dashboard.html", {"request": request, "submitted": True})

    return templates.TemplateResponse("registration.html", {"request": request, "submitted": False})


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
