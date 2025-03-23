import os
import json
from string import Template
from datetime import datetime
from app.core.logger import LOG_DIRECTORY
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Query, HTTPException


log_router = APIRouter()


def read_log_file(date: str):
    if date != "today":
        date = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_DIRECTORY, f"{date}.log")
    if not os.path.exists(log_file):
        raise HTTPException(status_code=404, detail="Log file not found")

    logs = []
    buffer = ""
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            buffer += line
            try:
                log_entry = json.loads(buffer)
                logs.append(log_entry)
                buffer = ""  # Reset buffer after successful load
            except json.JSONDecodeError:
                buffer += " "  # Add a space and continue accumulating
    return logs


def generate_html_table(logs):
    # Collect all unique keys from all log entries
    all_keys = set()
    for log in logs:
        all_keys.update(log.keys())
    headers = sorted(list(all_keys))  # Sort headers for consistency

    # Start building the HTML table
    table = """
    <table id='logTable' class='min-w-full bg-gray-800 text-gray-200 shadow-md rounded-lg'>
        <thead class='bg-gray-700'>
            <tr>
    """
    for header in headers:
        table += f"""
            <th class='py-3 px-4 border-b border-gray-600'>
                {header}<br>
                <input type='text' onkeyup='filterColumn({headers.index(header)})' placeholder='Filter...'
                    class='mt-1 p-1 w-full bg-gray-900 text-gray-300 border border-gray-600 rounded'>
            </th>
        """
    table += "</tr></thead><tbody>"

    for idx, log in enumerate(logs):
        # Zebra striping for rows
        row_class = "bg-gray-800 hover:bg-gray-700" if idx % 2 == 0 else "bg-gray-900 hover:bg-gray-800"
        table += f"<tr class='{row_class}'>"
        for header in headers:
            value = log.get(header, "")  # Get the value or an empty string if not present
            table += f"<td class='py-2 px-4 border-b border-gray-700'>{json.dumps(value, ensure_ascii=False)}</td>"
        table += "</tr>"

    table += "</tbody></table>"
    return table




@log_router.get("/logs", response_class=HTMLResponse)
def view_logs(date: str = Query("today", description="Date in YYYY-MM-DD format or 'today'")):
    try:
        logs = read_log_file(date)
        html_table = generate_html_table(logs)
        with open("app/assets/logger_view.html", 'r')as file:
            html_content = Template(file.read()).substitute(date=date, html_table=html_table)
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))