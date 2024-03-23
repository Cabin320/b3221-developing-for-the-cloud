from http import HTTPStatus
from datetime import timedelta
from typing import Annotated, Optional

import uvicorn

from fastapi import FastAPI, Request, Depends, status, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from starlette.exceptions import HTTPException
from starlette.datastructures import MutableHeaders
from starlette.responses import JSONResponse, Response

from utils.base_models import User
from utils.env_vars import db, ACCESS_TOKEN_EXPIRE_MINUTES
from utils.authentication import authenticate_user, create_access_token, get_current_user

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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "error.html", {"request": request, "status_code": exc.status_code, "exc": exc}, status_code=exc.status_code
    )


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
async def dashboard_page(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
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

    print(form_data)

    return templates.TemplateResponse("registration.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
