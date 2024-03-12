from typing import List, Optional

from fastapi import FastAPI, Request
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


class RegistryInfo(BaseModel):
    dog_walker: str
    dog: str
    add_dog: Optional[List[str]] = None


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_registry_info(request: Request):
    form_data = await request.form()
    dog_walker = form_data.get("dog_walker")
    dog = form_data.get("dog")
    add_dog = form_data.getlist("add_dog")

    if not dog_walker or not dog:
        return templates.TemplateResponse("index.html", {"request": request, "missing": True})

    registry_info = RegistryInfo(dog_walker=dog_walker, dog=dog, add_dog=add_dog)

    print(registry_info.dog_walker, registry_info.dog, registry_info.add_dog)
    return templates.TemplateResponse("index.html", {"request": request, "submitted": True})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", port=8000, reload=True)
