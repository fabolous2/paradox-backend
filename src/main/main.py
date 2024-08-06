from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from sqlalchemy.exc import DBAPIError

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from src.api.http import product, profile, promo, referral_system, supercell_auth, feedback
from src.main.ioc import DALProvider, DatabaseProvider, ServiceProvider


app = FastAPI()


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.exception_handler(DBAPIError)
async def validation_exception_handler(request: Request, exc: DBAPIError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": "Wrong SQL statement."}),
    )


app.include_router(product.router)
app.include_router(profile.router)
app.include_router(promo.router)
app.include_router(referral_system.router)
app.include_router(supercell_auth.router)
app.include_router(feedback.router)

container = make_async_container(DALProvider(), DatabaseProvider(), ServiceProvider())
setup_dishka(container, app)
