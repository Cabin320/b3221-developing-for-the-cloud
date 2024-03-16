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


class DogOwnerInfo(BaseModel):
    email: str
    password: str
    dog: str
    add_dog: Optional[List[str]] = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_registry_info(request: Request):
    form_data = await request.form()
    email = form_data.get("inputEmail")
    password = form_data.get("inputPassword")
    dog = form_data.get("dog")
    add_dog = form_data.getlist("add_dog")

    dog_walker_info = DogWalkerInfo(email=email, password=password)

    dog_owner_info = DogOwnerInfo(email=email, password=password, dog=dog, add_dog=add_dog)

    return templates.TemplateResponse("registration.html", {"request": request, "submitted": True})


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
