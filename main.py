from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse

app = FastAPI(title ="Task Manager API")


#Defines the structure of a task
class TaskCreate(BaseModel):
    title: str
    description : str
   

#Temporary storage
tasks = []
next_id = 1

# Welcome endpoint
@app.get("/", include_in_schema=False)
async def home():
    return FileResponse("static/index.html")

@app.get("/tasks")
async def get_tasks():
    return {"tasks": tasks}

@app.post("/tasks", status_code=201)
async def create_task(task: TaskCreate):
    global next_id

    next_task = {
        "id": next_id,
        "title" : task.title,
        "description": task.description,
        "completed" : False
    }

    tasks.append(next_task)
    next_id += 1

    return next_task

@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task

        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return {"message": "Task deleted successfully"}

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )



