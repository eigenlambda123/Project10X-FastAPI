from fastapi import FastAPI
from app.routes import notify, reports

app = FastAPI(title="Background Tasks Service")

app.include_router(notify.router, prefix="/notify", tags=["Notify"]) # register notification routes
app.include_router(reports.router, prefix="/report", tags=["Reports"]) # register report generation routes
