import json
from datetime import datetime
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Query, HTTPException
from app.services.log_viewer_service import read_log_file



log_router = APIRouter()


@log_router.get("/logs", response_class=HTMLResponse)
def view_logs(date: str = Query("today", description="Date in YYYY-MM-DD format or 'today'")):
    try:
        logs, date = read_log_file(date)

        all_keys = set()
        for log in logs:
            all_keys.update(log.keys())
        headers = sorted(list(all_keys))  # Sort headers for consistency
        
        if date == "today":
            log_date = datetime.today().strftime("%Y-%m-%d")
        else:
            log_date = date  # Already in YYYY-MM-DD format
        

        with open("app/template/logger_view.html", 'r') as file:
            html_content = file.read()
            html_content= html_content.replace("@{date}", json.dumps(log_date))\
                .replace("@{logs}", json.dumps(logs, ensure_ascii=False))\
                .replace("@{header_list}", json.dumps(headers, ensure_ascii=False))
            
                    
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))