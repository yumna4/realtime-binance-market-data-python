from fastapi import FastAPI, status
import uvicorn
from init import COMMON_API_PREFIX
from router import market_data
from fastapi.requests import Request
from starlette.responses import JSONResponse
from exceptions.custom_exceptions import CustomAPIException
from fastapi.encoders import jsonable_encoder
from apimodel.response_models import APIError
from common.config_manager import get_config

app = FastAPI(
    title="Binance Demo API",
    version="1.0.0",
    description="Binance Demo APIs documentation"
)


@app.exception_handler(CustomAPIException)
async def custom_exception_handler(request: Request, exception: CustomAPIException):
    return JSONResponse(
        status_code=exception.status_code if hasattr(exception, "status_code") else status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(APIError(type=exception.name, message=exception.message))
    )

app.include_router(market_data.router, prefix=f"{COMMON_API_PREFIX}/market_data", tags=["Market Data"])
if __name__== "__main__":
   uvicorn.run(app, host="127.0.0.1", port=get_config("api_host_port"))