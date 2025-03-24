from string import Template
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Query, HTTPException
from app.service.log_viewer_service import generate_html_table, read_log_file



log_router = APIRouter()


@log_router.get("/logs", response_class=HTMLResponse)
def view_logs(date: str = Query("today", description="Date in YYYY-MM-DD format or 'today'")):
    try:
        logs, date = read_log_file(date)
        html_table = generate_html_table(logs)
        
        if date == "today":
            log_date = datetime.today().strftime("%Y-%m-%d")
        else:
            log_date = date  # Already in YYYY-MM-DD format
        print(log_date)
        
        with open("app/template/logger_view.html", 'r') as file:
            html_content = Template(file.read()).substitute(date=log_date, html_table=html_table)
        
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))