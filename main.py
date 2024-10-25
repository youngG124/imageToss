from typing import Union

from fastapi import FastAPI, Response, HTTPException
from pathlib import Path

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_DIRECTORY = Path("C:\pacsdata\imgs\imageExamples")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/image/{image_name}", responses={200: {"content": {"image/png": {}}}})
async def get_image(image_name : str) :
    image_name += ".png"
    image_path = IMAGE_DIRECTORY / image_name

    print(image_path)

    # Check if the image exists and is a PNG file
    if not image_path.exists() or not image_path.suffix == ".png":
        raise HTTPException(status_code=404, detail="Image not found")

    # Open the image in binary mode and return it as a response
    with open(image_path, "rb") as image_file:
        return Response(content=image_file.read(), media_type="image/png")

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}