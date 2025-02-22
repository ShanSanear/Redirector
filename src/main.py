from fastapi import FastAPI
from fastapi.responses import RedirectResponse
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/discord")
async def redirect_discord():
    return RedirectResponse("https://discord.gg/xDPWqhSj")