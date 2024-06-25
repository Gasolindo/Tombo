import time
from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from tombo import routes

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    # "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    print(request.headers)
    response.headers["X-Process-Time"] = str(time.time() - start_time)
    return response


# @app.get("/user",dependencies=[Depends(verify_token)] )
# def teste():
#     print("hello")


app.include_router(routes.user.router, prefix="/user")
app.include_router(routes.tombo.router, prefix="/tombo")
app.include_router(routes.material.router, prefix="/materials")
app.include_router(routes.login.router, prefix="/login")

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.0", port=8000)
