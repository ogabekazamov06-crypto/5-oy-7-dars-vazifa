from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import Category, News
from schemas import CategoryCreate


# CATEGORY CRUD ----------------------------------------------------------------
async def create_category(db: AsyncSession, data: CategoryCreate):
    category = Category(**data.model_dump())
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category


async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def update_category(db: AsyncSession, category_id: int, data: CategoryCreate):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        return None

    category.name = data.name
    await db.commit()
    await db.refresh(category)
    return category


async def delete_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        return None

    await db.delete(category)
    await db.commit()
    return category


# NEWS CRUD -------------------------------------------------------------------
async def create_news(db: AsyncSession, data: dict):
    news = News(**data)
    db.add(news)
    await db.commit()
    await db.refresh(news)
    return news


async def get_news(db: AsyncSession):
    result = await db.execute(select(News))
    return result.scalars().all()


async def update_news(db: AsyncSession, news_id: int, data: dict):
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()

    if not news:
        return None

    for key, value in data.items():
        setattr(news, key, value)

    await db.commit()
    await db.refresh(news)
    return news


async def delete_news(db: AsyncSession, news_id: int):
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()

    if not news:
        return None

    await db.delete(news)
    await db.commit()
    return news