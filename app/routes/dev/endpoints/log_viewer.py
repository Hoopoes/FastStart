from datetime import datetime
from pydantic import BaseModel
from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse


from app.services.log_viewer_service import read_log_file



log_router = APIRouter()


class LogData(BaseModel):
    columns: list[str]
    logs: list[dict]
    date: datetime


@log_router.get("/logs/data")
def logs_data(date: str = Query("today", description="Date in YYYY-MM-DD format or 'today'")) -> LogData:
    
    logs, date = read_log_file(date)

    all_keys = set()
    for log in logs:
        all_keys.update(log.keys())
    columns = sorted(list(all_keys))  # Sort headers for consistency
    
    if date == "today":
        log_date = datetime.today().strftime("%Y-%m-%d")
    else:
        log_date = date  # Already in YYYY-MM-DD format
    
    return LogData(columns=columns, logs=logs, date=log_date)
    

@log_router.get("/logs", response_class=HTMLResponse)
def view_logs():

    with open("app/templates/log_viewer.html", 'r') as file:
        html_content = file.read()
        
    return HTMLResponse(content=html_content)