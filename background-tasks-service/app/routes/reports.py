from fastapi import APIRouter, BackgroundTasks

router = APIRouter()

@router.post("/")
def generate_report(background_tasks: BackgroundTasks):
    # stub - real logic will come later
    return {"message": "Report generation task triggered"}