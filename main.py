from fastapi import FastAPI, HTTPException,APIRouter
from models import Todo
from fastapi.middleware.cors import CORSMiddleware
from configurations import collection
from schema import all_tasks
from bson.objectid import ObjectId
from datetime import datetime


app = FastAPI()
router = APIRouter()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

@router.get("/api/tasks")
async def get_all_todos():
    data = collection.find()
    return all_tasks(data)

@router.get("/api/tasks/{task_id}")


async def get_task_by_id(task_id: str):
    try:
        try:
            id = ObjectId(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task ID format")

        task = collection.find_one({"_id": id, "deleted": False})

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task = convert_object_id(task) 
        return task

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


def convert_object_id(task: dict):
    task["_id"] = str(task["_id"]) 
    return task

app.include_router(router)


@router.post('/api/tasks')
async def create_task(new_task: Todo):
    try:
        resp = collection.insert_one(dict(new_task))
        return {"status_code": 200, "id": str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(status_code=500, detail=f"An error occurred: {e}")
    
@router.put("/api/tasks/{task_id}")
async def update_task(task_id: str, updated_task: Todo):
    try:
        try:
            id = ObjectId(task_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        existing_doc = collection.find_one({"_id": id, "deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Task does not exist")

        updated_task.updated_at = datetime.now()

        resp = collection.update_one(
            {"_id": id}, 
            {"$set": updated_task.dict(exclude_unset=True)}
        )
        if resp.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to update task")

        return {"status_code": 200, "message": "Task updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    

@router.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        try:
            id = ObjectId(task_id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid task ID format")
        
        task = collection.find_one({"_id": id})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        resp = collection.delete_one({"_id": id})
        if resp.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete task")

        return {"status_code": 200, "message": "Task deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")




app.include_router(router)


