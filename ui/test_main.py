from fastapi import FastAPI
from fastapi import Request
from pathlib import Path
from dicttoxml import dicttoxml
from fastapi.responses import Response, HTMLResponse, JSONResponse
from fastapi import Query

app = FastAPI()

@app.get("/")
def root():
    return "Hello, World!"

@app.get("/user/{username}")
def get_user(username: str):
    return {"username": username}

@app.get("/echo")
def echo(request: Request):
    query_params = dict(request.query_params)
    print(query_params)
    return {"received": query_params}

@app.get("/xml-auto")
def auto_xml():
    data = {"user": "Alice", "message": "Hello from FastAPI"}
    xml = dicttoxml(data)
    return Response(content=xml, media_type="application/xml")

@app.get("/html-auto", response_class=HTMLResponse)
def auto_html():
    return "<h1>This is HTML</h1>"

@app.get("/html-auto2")
def auto_html():
    content = "<h1>This is HTML</h1>"
    return Response(content=content, media_type="text/html") 

@app.get("/html-auto3")
def auto_html():
    return HTMLResponse("<h1>This is HTML</h1>")

@app.get("/search")
def search(q: str = Query(..., min_length=3, max_length=50)):
    return {"query": q}

from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

@app.get("/profile", response_model=User)
def profile():
    return {"name": "Alice", "age": 30, "password": "secret"}

from fastapi import HTTPException

@app.get("/user_login/{username}")
def get_user(username: str):
    if username != "admin":
        raise HTTPException(status_code=404, detail="User not found")
    return {"username": username}

@app.get("/user_login_v2/{username}")
def get_user(username: str):
    if username != "admin":
        raise HTTPException(status_code=403, detail="User not found", headers={"X-Error": "You are not authorized"})
    return {"username": username}

@app.get("/custom")
def custom_response():
    return JSONResponse(content={"msg": "Welcome to the App"}, status_code=202, headers={"X-Custom": "App reached"})

if __name__ == "__main__":
    import uvicorn
    app_path = Path(__file__).resolve().with_suffix('').name  # gets filename without .py
    uvicorn.run(f"{app_path}:app", host="0.0.0.0", port=8000, reload=True)