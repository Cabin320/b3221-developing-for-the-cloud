from http import HTTPStatus
from datetime import timedelta
from typing import Annotated, Optional

import uvicorn

from fastapi import FastAPI, Request, Depends, status, Cookie, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from starlette.exceptions import HTTPException
from starlette.datastructures import MutableHeaders
from starlette.responses import JSONResponse, Response

from utils.base_models import User, Dog
from utils.env_vars import ACCESS_TOKEN_EXPIRE_MINUTES, CONNECTION_STRING, DB_NAME

from utils.mongo_db_connect import connect_to_db
from utils.authentication import authenticate_user, create_access_token, get_current_user, get_password_hash

app = FastAPI(
    title="Waqq.ly Website",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

client = connect_to_db(CONNECTION_STRING)
database = client[DB_NAME]
owners_collection = database["owners"]
walkers_collection = database["walkers"]


@app.middleware("http")
async def authorization_middleware(request: Request, call_next):
    """
    Function to add access token to cookie
    :param request:
    :param call_next:
    :return: response
    """
    access_token = request.cookies.get("access_token")

    if access_token and "Authorization" not in request.headers.keys():
        new_header = MutableHeaders(request._headers)
        new_header["Authorization"] = f"Bearer {access_token}"
        request._headers = new_header
        request.scope.update(headers=request.headers.raw)

    response = await call_next(request)
    return response


@app.post("/token", response_class=JSONResponse)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> JSONResponse:
    """
    Function to check if user credentials are valid
    :param form_data:
    :return: 400 Response with validated access tokens
    """
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Incorrect username or password"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token, secure=True)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Custom exception
    :param request:
    :param exc:
    :return: HTTP Status Code
    """
    return templates.TemplateResponse(
        "error.html", {
            "request": request, "status_code": exc.status_code, "exc": exc
        }, status_code=exc.status_code
    )


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Loads the root index.html page
    :param request:
    :return: index.html
    """
    return templates.TemplateResponse(
        "index.html", {
            "request": request, "show_button": False
        }
    )


@app.get("/logout")
async def delete_cookie(response: Response):
    """
    Function to delete cookie on sign out
    :param response:
    """
    response.delete_cookie(key="access_token")


@app.get("/get_cookie", response_class=JSONResponse)
async def get_cookies(access_token: Optional[str] = Cookie(None)):
    """
    Test function for checking if an access token has been added
    :param access_token:
    :return: access token
    """
    try:
        return {"access_token": access_token}
    except Exception:
        raise HTTPException(detail="No cookie found", status_code=HTTPStatus.BAD_REQUEST)


@app.get("/dashboard", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def dashboard_page(request: Request, current_user: User = Depends(get_current_user)):
    """
    Function to load user data on dashboard page
    :param request:
    :param current_user:
    :return: dashboard.html with user information
    """
    owners_data = owners_collection.find_one({"user": current_user.username})
    walkers_data = walkers_collection.find_one({"user": current_user.username})

    all_walkers = walkers_collection.find()
    all_owners = owners_collection.find()

    user_data = None
    walkers_info = None
    owners_info = None

    if owners_data:
        user_data = owners_data
        walkers_info = [walker for walker in all_walkers]
    elif walkers_data:
        user_data = walkers_data
        owners_info = [owner for owner in all_owners]

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User data not found"
        )

    return templates.TemplateResponse(
        "dashboard.html", {
            "request": request,
            "show_button": True,
            "current_user": current_user.username,
            "user_data": user_data,
            "walkers_info": walkers_info,
            "owners_info": owners_info
        }
    )


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """
    Function to load registration.html template
    :param request:
    :return: registration.html
    """
    return templates.TemplateResponse(
        "registration.html", {
            "request": request, "show_button": False
        }
    )


@app.post("/submit", response_class=HTMLResponse)
async def submit_form(
        request: Request,
        user: str = Form(...),
        email: str = Form(...),
        location: str = Form(...),
        password: str = Form(...),
        password_check: str = Form(...),
        name: list[str] = Form(...),
        breed: list[str] = Form(...),
        age: list[str] = Form(...)
):
    """
    Function to submit user data to database
    :param request: User Information
    :param user: Username
    :param email: Email
    :param location: Location of user
    :param password: Password
    :param password_check: Re-type Password
    :param name: Name of Pet
    :param breed: Breed of Pet
    :param age: Age of Pet
    :return: Data sent to database collection
    """
    form_data = await request.form()

    dog_walker_selected = form_data.get('dog_walker')
    dog_owner_selected = form_data.get('dog_owner')

    existing_user_in_owners = owners_collection.find_one({"$or": [{"user": user}, {"email": email}]})
    existing_user_in_walkers = walkers_collection.find_one({"$or": [{"user": user}, {"email": email}]})

    if existing_user_in_owners or existing_user_in_walkers:
        existing_field = "user" if existing_user_in_owners and existing_user_in_owners.get("user") == user else "email"
        return templates.TemplateResponse(
            "registration.html", {
                "request": request, "existing": True, "existing_field": existing_field
            }
        )

    if password != password_check:
        return templates.TemplateResponse(
            "registration.html", {
                "request": request, "password_mismatch": True
            }
        )

    if dog_walker_selected:
        user_data = User(user=user, email=email, location=location, password=get_password_hash(password))
        walkers_collection.insert_one(user_data.dict())

    elif dog_owner_selected:
        dog_data = Dog(name=name, breed=breed, age=age)
        user_data = User(user=user, email=email, location=location, password=get_password_hash(password), dog=dog_data)
        owners_collection.insert_one(user_data.dict())

    return templates.TemplateResponse("registration.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
