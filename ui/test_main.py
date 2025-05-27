from fastapi import FastAPI
from fastapi import Request
from pathlib import Path
from dicttoxml import dicttoxml
from fastapi.responses import Response, HTMLResponse

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

if __name__ == "__main__":
    import uvicorn
    app_path = Path(__file__).resolve().with_suffix('').name  # gets filename without .py
    uvicorn.run(f"{app_path}:app", host="0.0.0.0", port=8000, reload=True)