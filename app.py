from datetime import timedelta
from http import HTTPStatus
from typing import Annotated, Optional

import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.datastructures import MutableHeaders
from starlette.responses import JSONResponse, Response

from utils.authentication import authenticate_user, create_access_token, get_current_user
from utils.base_models import DogWalkerInfo, AdditionalPetInfo, DogOwnerInfo, User
from utils.env_vars import db, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(
    title="Waqq.ly Website"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.middleware("http")
async def authorization_middleware(request: Request, call_next):
    access_token = request.cookies.get("access_token")

    if access_token and "Authorization" not in request.headers.keys():
        new_header = MutableHeaders(request._headers)
        new_header["Authorization"] = f"Bearer {access_token}"
        request._headers = new_header
        request.scope.update(headers=request.headers.raw)

    response = await call_next(request)
    return response


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "show_button": False})


@app.post("/token", response_class=JSONResponse)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, secure=True)
    return response


@app.get("/logout")
async def delete_cookie(response: Response):
    response.delete_cookie(key="access_token")


@app.get("/get_cookie", response_class=JSONResponse)
async def get_cookies(access_token: Optional[str] = Cookie(None)):
    try:
        return {"access_token": access_token}
    except Exception:
        raise HTTPException(detail="No cookie found", status_code=HTTPStatus.BAD_REQUEST)


@app.get("/dashboard", response_class=HTMLResponse, status_code=HTTPStatus.OK)
async def dashoard_page(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    return templates.TemplateResponse(
        "dashboard.html", {
            "request": request, "show_button": True, "current_user": current_user.username
        }
    )


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request, "show_button": False})


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
