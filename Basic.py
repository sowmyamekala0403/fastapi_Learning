from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def home()->dict:
    return {"key" : "value"}

@app.get('/about')
def about()->str:
    return " this is sample about page.this is returned after clicking the about endpoint"

@app.get("/about/{name}")
def Greeting(name:int)-> str:
    return f" hello {name} !!! happy to see you here"

