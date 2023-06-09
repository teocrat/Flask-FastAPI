from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

tasks = []
for i in range(10):
    tasks.append({f'title': f'name{i}', 'description': f'description{i}'})


app = FastAPI()


class Tasks(BaseModel):
    title: str = Field(max_length=20)
    description: str = Field(max_length=200)
    status: bool = Field(default=False)


@app.get('/tasks/', response_model=List[Tasks])
async def read_tasks():
    return tasks


@app.get('/task/{task_id}', response_model=Tasks)
async def read_task(task_id: int):
    return tasks[task_id]


@app.post('/tasks', response_model=Tasks)
async def create_task(task: Tasks):
    tasks.append(task)
    return task


@app.put('/tasks/{task_id}', response_model=Tasks)
async def update_task(task_id: int, new_task: Tasks):
    tasks[task_id] = new_task
    return new_task


@app.delete('/tasks/{task_id}', response_model=Tasks)
async def delete_task(task_id: int):
    return tasks.pop(task_id)
