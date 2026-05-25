from fastapi import FastAPI
from contextlib import asynccontextmanager
from rich import print, panel

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[green]Starting up...[/green]")
    print(panel.Panel("Starting up", border_style="blue"))
    yield
    print("[red]Shutting down...[/red]")
    print(panel.Panel("Shutting down", border_style="red"))

app = FastAPI(lifespan=lifespan)
@app.get("/")
def read_root():
    return {"detail": "Server Started"}


