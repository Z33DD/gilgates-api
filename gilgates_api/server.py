from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from gilgates_api import config as global_config, logger
from gilgates_api.settings import Settings
from gilgates_api.api import api_router


def app_factory(config: Settings) -> FastAPI:
    app = FastAPI(title=config.app_name, version=config.version)

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


app = app_factory(global_config)
logger.info(
    "Started!",
    env=global_config.env,
    database=global_config.database_url.split("://")[0],
    broker=global_config.celery_broker_url,
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/")
async def index():
    return {"name": "GilGates API", "version": app.version}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("gilgates_api.server:app", port=8000, log_level="info", reload=True)
