import os
from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import shutil
import uvicorn

from database import engine, Base, get_db
import crud
from schemas import CategoryCreate, CategoryResponse, NewsResponse

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# CATEGORY API -----------------------------------------------------------------------
@app.post("/categories/", response_model=CategoryResponse)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_category(db, data)


@app.get("/categories/", response_model=list[CategoryResponse])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db)


@app.put("/categories/{id}", response_model=CategoryResponse)
async def update_category(id: int, data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    category = await crud.update_category(db, id, data)
    if not category:
        raise HTTPException(404, "Not found")
    return category


@app.delete("/categories/{id}")
async def delete_category(id: int, db: AsyncSession = Depends(get_db)):
    category = await crud.delete_category(db, id)
    if not category:
        raise HTTPException(404, "Not found")
    return {"message": "Deleted"}


# NEWS API ------------------------------------------------------------------
@app.post("/news/", response_model=NewsResponse)
async def create_news(
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    video: UploadFile = File(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    data = {
        "title": title,
        "content": content,
        "category_id": category_id
    }

    for field, upload in {"image": image, "video": video, "file": file}.items():
        if upload:
            path = f"{UPLOAD_DIR}/{upload.filename}"
            with open(path, "wb") as buffer:
                shutil.copyfileobj(upload.file, buffer)
            data[field] = path

    return await crud.create_news(db, data)


@app.get("/news/", response_model=list[NewsResponse])
async def get_news(db: AsyncSession = Depends(get_db)):
    return await crud.get_news(db)


@app.put("/news/{id}", response_model=NewsResponse)
async def update_news(id: int, db: AsyncSession = Depends(get_db), title: str = Form(...), content: str = Form(...), category_id: int = Form(...)):
    data = {
        "title": title,
        "content": content,
        "category_id": category_id
    }

    news = await crud.update_news(db, id, data)
    if not news:
        raise HTTPException(404, "Not found")
    return news


@app.delete("/news/{id}")
async def delete_news(id: int, db: AsyncSession = Depends(get_db)):
    news = await crud.delete_news(db, id)
    if not news:
        raise HTTPException(404, "Not found")
    return {"message": "Deleted"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)