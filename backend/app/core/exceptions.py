from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status
from typing import Any, Optional


class BaseAppException(Exception):
    def __init__(self, message: str, code: str = "app_error", http_status: int = status.HTTP_400_BAD_REQUEST, details: Optional[Any] = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.http_status = http_status
        self.details = details

    def to_response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.http_status,
            content={
                "error": {
                    "code": self.code,
                    "message": self.message,
                    "details": self.details,
                }
            },
        )


class DatabaseException(BaseAppException):
    def __init__(self, operation: str, details: Optional[Any] = None):
        super().__init__(
            message=f"Database error during {operation}",
            code="database_error",
            http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details,
        )


class ExceptionHandler:
    def __init__(self, logger):
        self.logger = logger

    async def handle_app_exception(self, request: Request, exc: BaseAppException):
        self.logger.warning(f"AppException {exc.code}: {exc.message}")
        return exc.to_response()

    async def handle_http_exception(self, request: Request, exc):
        self.logger.info(f"HTTPException {exc.status_code}: {exc.detail}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    async def handle_generic_exception(self, request: Request, exc: Exception):
        self.logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
