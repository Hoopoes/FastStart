import os
import json
from datetime import datetime
from app.core.logger import LOG_DIRECTORY



def read_log_file(date: str):
    # Format the date to match log file naming convention
    if date != "today":
        date = datetime.strptime(date, "%Y%m%d").strftime("%Y-%m-%d")
    

    # Check if the given date matches today's date
    current_date = datetime.now().strftime("%Y-%m-%d")
    if date == current_date:
        date = "today"

    log_file = os.path.join(LOG_DIRECTORY, f"{date}.log")
    
    # If the log file for the specified date does not exist, fallback to today's log
    if not os.path.exists(log_file):
        return [], date

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
    return logs, date


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