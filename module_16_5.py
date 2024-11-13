from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from typing import Annotated, List
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

templates=Jinja2Templates(directory='templates')
app = FastAPI()

users = []

class User(BaseModel):
    id: int
    username: str
    age: int

# @app.get("/users")
@app.get("/")
async def get_userlist(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {'request': request, 'users': users})

@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: Annotated[int, Path(ge=0, le=100, description='Enter User ID', example='11')]) -> HTMLResponse:
    try:
        return templates.TemplateResponse("users.html", {'request': request, 'user': users[user_id]})
    except:
        raise HTTPException(status_code=404, detail='User not found')

@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    user_id = len(users) #50:30
    user = User(id=user_id,username=username,age=age)
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='11')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> str:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail='User not found')

@app.delete('/user/{user_id}')
async def delete_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='11')]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            users.remove(user_id)
            return templates.TemplateResponse("users.html", {'request': request, 'users': users})
    raise HTTPException(status_code=404, detail='User not found')