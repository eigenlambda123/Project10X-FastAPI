from fastapi import APIRouter, BackgroundTasks

router = APIRouter()

@router.post("/")
def notify_user(background_tasks: BackgroundTasks):
    # stub - real logic will come later
    return {"message": "Notification task triggered"}
