from fastapi import FastAPI
from .routes import topics, posts, comments
from .database import engine, Base

app = FastAPI(title="Forum API", docs_url="/docs", redoc_url="/redoc")

app.include_router(topics.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
