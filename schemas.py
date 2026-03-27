from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str


class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


class NewsCreate(BaseModel):
    title: str
    content: str
    category_id: int


class NewsResponse(NewsCreate):
    id: int
    image: str | None = None
    video: str | None = None
    file: str | None = None

    class Config:
        from_attributes = True