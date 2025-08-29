from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routers.index import home_router
from routers.auth import auth_router
from routers.register import reg_router
from routers.portfolio import portfolio_route
import uvicorn


app = FastAPI()

@app.middleware("http")
async def dispatch(request: Request, call_next):
    try:
        response = await call_next(request)
        # Если пользователь зашёл на защищённый путь и не авторизован
        if request.url.path.startswith('/portfolio') and response.status_code == 401:
            return RedirectResponse(url="/login")
        return response
    except HTTPException as exc:
        if request.url.path.startswith('/portfolio') and exc.status_code == 401:
            return RedirectResponse(url="/login")
        raise exc

app.include_router(home_router, prefix="")
app.include_router(home_router, tags=["search"])
app.include_router(reg_router, prefix='')
app.include_router(portfolio_route, prefix='')
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8012 , reload=True)