from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Any, Dict, Optional
from datetime import datetime
import json
import uvicorn

app = FastAPI()

channel_hits = []
channels_ids = {
    "dsd": "ddds",
}

id_channel_hits = {}

async def save_data(data, output_file=None):
    """Saves the (potentially updated) JSON data.

    Args:
        output_file: Optional path to save data to a new file. If not provided, overwrites the original.
    """
    if not output_file:
        output_file = "channel_hits.json"
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)  # Pretty-print with indentation
    except IOError:
        print(f"Error: Could not write to file '{output_file}'.")

# Load initial data
with open("id_channel_hits.json", "r") as f:
    id_channel_hits = json.load(f)

with open("channel_hits.json", "r") as f:
    channel_hits = json.load(f)

@app.get("/index.html")
async def get_handler(request: Request) -> Dict[str, str]:
    headers = request.headers

    ip = headers.get("cf-connecting-ip")
    country = headers.get("cf-ipcountry")
    useragent = headers.get("user-agent")

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "country": country,
        "user_agent": useragent,
        "method": "GET",
    }

    channel_hits.append(data)
    await save_data(channel_hits)
    return {"s": "s"}

@app.head("/index.html")
async def head_handler(request: Request) -> None:
    headers = request.headers

    ip = headers.get("cf-connecting-ip")
    country = headers.get("cf-ipcountry")
    useragent = headers.get("user-agent")

    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "country": country,
        "user_agent": useragent,
        "method": "HEAD",
    }

    channel_hits.append(data)
    await save_data(channel_hits)
    return

@app.get("/app/logs", response_class=HTMLResponse)
async def get_log_handler() -> str:
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Viewership Logs</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 800px; margin: auto; }
            .header { background-color: #f4f4f4; padding: 10px; border-radius: 5px; text-align: center; }
            .log-entry { border-bottom: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
            .log-entry:last-child { border-bottom: none; }
            .title { font-size: 1.2em; font-weight: bold; }
            .subtitle { color: #555; }
            .log-entry pre { background-color: #f9f9f9; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Viewership Logs</h1>
            </div>
            <div class="content">
    """

    html += f'<div class="title">AVAFAMILY | Viewership count: {len(channel_hits)} | Unique count: {len(set(c["ip"] for c in channel_hits))}</div>'

    for c in reversed(channel_hits):
        html += f'''
        <div class="log-entry">
            <div class="subtitle">Timestamp: {c["timestamp"]}</div>
            <pre>
IP: {c["ip"]}
Country: {c["country"]}
User Agent: {c["user_agent"]}
Method: {c["method"]}
            </pre>
        </div>
        '''
    
    html += """
            </div>
        </div>
    </body>
    </html>
    """

    return html

@app.get("/sstracker", response_class=HTMLResponse)
async def sstracker_handle() -> str:
    html_text = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script defer src="https://dd.com/script.js" data-website-id="471b9af5-391e-42fe-8ed2-3e0dff5c1761"></script>
        <title>Success</title>
    </head>
    <body>
    </body>
    </html>
    """

    return html_text

@app.get("/viewership")
async def get_viewership() -> list[dict[str, Any]]:
    for i, c in enumerate(channel_hits):
        c["id"] = i + 1

    return channel_hits

async def get_by_channel_id(headers, channel_id, method):
    if channel_id is None or channel_id not in channels_ids:
        return "success"
    
    ip = headers.get("cf-connecting-ip")
    country = headers.get("cf-ipcountry")
    useragent = headers.get("user-agent")

    if "HbbTV".lower() not in useragent.lower() and country != "EG":
        print("Bad Request", headers)
        return "success"
    
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "ip": ip,
        "country": country,
        "user_agent": useragent,
        "method": method,
    }

    if channel_id not in id_channel_hits:
        id_channel_hits[channel_id] = []

    id_channel_hits[channel_id].append(data)
    await save_data(id_channel_hits, output_file="id_channel_hits.json")

    html_text = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script defer src="https://dd.com/script.js" data-website-id="471b9af5-391e-42fe-8ed2-3e0dff5c1761"></script>
        <title>Success</title>
    </head>
    <body>
    </body>
    </html>
    """

    return html_text

#@app.head("/app/{channel_id}", response_class=HTMLResponse)
@app.get("/app/{channel_id}", response_class=HTMLResponse)
async def get_id_handler(request: Request, channel_id: Optional[str] = None):
    headers = request.headers
    resp = await get_by_channel_id(headers, channel_id, "GET")
    return resp


# async def head_id_handler(request: Request, channel_id: Optional[str] = None):
#     headers = request.headers
#     resp = await get_by_channel_id(headers, channel_id, "HEAD")
#     return resp

@app.get("/app/viewership/{channel_id}", response_class=HTMLResponse)
async def get_viewership_handler(channel_id: Optional[str] = None):
    if channel_id is None or id_channel_hits.get(channel_id) is None:
        return {"status": "success"}
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Viewership Logs</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 800px; margin: auto; }
            .header { background-color: #f4f4f4; padding: 10px; border-radius: 5px; text-align: center; }
            .log-entry { border-bottom: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
            .log-entry:last-child { border-bottom: none; }
            .title { font-size: 1.2em; font-weight: bold; }
            .subtitle { color: #555; }
            .log-entry pre { background-color: #f9f9f9; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Viewership Logs</h1>
            </div>
            <div class="content">
    """

    html += f'<div class="title">{channels_ids[channel_id]} | Viewership count: {len(id_channel_hits[channel_id])} | Unique count: {len(set(c["ip"] for c in id_channel_hits[channel_id]))}</div>'

    for c in reversed(id_channel_hits[channel_id]):
        html += f'''
        <div class="log-entry">
            <div class="subtitle">Timestamp: {c["timestamp"]}</div>
            <pre>
IP: {c["ip"]}
Country: {c["country"]}
User Agent: {c["user_agent"]}
Method: {c["method"]}
            </pre>
        </div>
        '''
    
    html += """
            </div>
        </div>
    </body>
    </html>
    """

    return html

if __name__ == "__main__":
    uvicorn.run(app, port=43223)
