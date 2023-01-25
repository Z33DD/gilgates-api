from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gilgates_api.database import db, create_tables
from gilgates_api import __version__
from gilgates_api.api.login import router as login
from gilgates_api.api.signup import router as signup



def app_factory() -> FastAPI:
    app = FastAPI(title="GilGates API", version=__version__)

    app.include_router(login)
    app.include_router(signup)

    origins = [
        # settings.FRONTEND_URL
        "*"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = app_factory()


@app.on_event("startup")
async def startup():
    await db.connect()
    await create_tables()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.get("/")
async def index():
    return {"name": "GilGates API", "version": app.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
