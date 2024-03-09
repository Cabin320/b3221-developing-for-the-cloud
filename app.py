from typing import List, Optional

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Waqq.ly Website",
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_registry_info(request: Request, dog_walker: str = Form(...), dog: str = Form(...),
                               add_dog: List[str] = Form(...)):
    print(dog_walker, dog, add_dog)

    if not dog_walker or not dog:
        raise HTTPException(status_code=400, detail="Incomplete form data")

    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", port=8000, reload=True)
