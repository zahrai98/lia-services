from fastapi import Response
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import json
from app import routes
from app.core.dependencies.database import Database
from app.core.services.error_handler import APIException
from app.core.services.response_handler import JsonResponseEncoder
app = FastAPI(swagger_ui_parameters={"displayRequestDuration": True})


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_db():
    print('startup')
    await Database.init_db()

app.include_router(routes.router, prefix='')


@app.get('/')
async def home():
    return {"message": "hello!"}

#
# # TODO Uncomment this function
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print('RequestValidationError')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'success': False, 'errors': [
            {'message': str(exc), 'type': 'ValidationError', 'errorCode': 700, 'details': exc.errors()}]}),
    )

# # TODO Uncomment this function
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    print('RequestValidationError')
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({'success': False, 'errors': [
            {'message': str(exc), 'type': 'ValidationError', 'errorCode': 700, 'details': exc.errors()}]}),
    )


@app.exception_handler(APIException)
async def exception_handler(request: Request, exc: APIException):
    print('APIException')
    result = {'success': False, 'errors': exc.errors}
    return Response(json.dumps(result, sort_keys=True, indent=4, cls=JsonResponseEncoder), media_type="application/json",
                    status_code=exc.status_code)

