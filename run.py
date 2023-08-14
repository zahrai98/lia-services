import uvicorn
from app.core.config import Setting


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=Setting.BACK_PORT, reload=True)