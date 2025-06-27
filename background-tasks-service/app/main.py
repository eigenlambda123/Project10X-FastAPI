from fastapi import FastAPI
from app.routes import notify, reports, status, filegen

app = FastAPI(title="Background Tasks Service")

app.include_router(notify.router, prefix="/notify", tags=["Notify"]) # register notification routes
app.include_router(reports.router, prefix="/report", tags=["Reports"]) # register report generation routes
app.include_router(status.router, prefix="/status", tags=["Status"]) # register task status routes
app.include_router(status.router, prefix="/retry", tags=["Retry"]) # register retry routes
app.include_router(filegen.router, prefix="/file", tags=["File Generator"]) # register file generation routes
