from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gilgates_api.database import create_tables
from gilgates_api.config import VERSION
from gilgates_api.api import api_router


def app_factory() -> FastAPI:
    app = FastAPI(title="GilGates API", version=VERSION)

    app.include_router(api_router)

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
    create_tables()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/")
async def index():
    return {"name": "GilGates API", "version": app.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
