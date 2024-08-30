import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.v1.router import router as v1_router
from configs.config import app_settings
from constants.backend import BACKEND_ENTRYPOINT


app = FastAPI(
    title="KODE",
    openapi_url=f"/{BACKEND_ENTRYPOINT}/openapi.json/",
    docs_url=f"/{BACKEND_ENTRYPOINT}/docs/",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router, prefix=f"/{BACKEND_ENTRYPOINT}")


if __name__ == "__main__":
    host = "0.0.0.0"  # noqa: S104
    if app_settings.ENVIRONMENT == "local":
        uvicorn.run(
            "main:app",
            host=host,
            port=app_settings.SERVICE_PORT,
            reload=True,
            forwarded_allow_ips="*",
        )
    else:
        uvicorn.run(
            "main:app",
            host=host,
            port=8000,
            forwarded_allow_ips="*",
            workers=app_settings.UVICORN_WORKERS,
        )
