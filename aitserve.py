from litestar import Litestar, get, head, MediaType
from datetime import datetime
from typing import Any
import json
import requests
from litestar.response import Redirect
# 2024-05-12 14:23:15.300767 {'host': 'tait.wns.watch', 'accept-encoding': 'gzip, br', 'cf-ray': '882b10c8791f2bc1-FRA', 'x-forwarded-proto': 'https', 'cf-visitor': '{"scheme":"https"}', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36 HbbTV/1.5.1 (+DRM; LGE; 75UP81003LR; WEBOS6.0 03.40.82; W60_K7LP; DTV_W21P;)', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'navigate', 'accept-language': 'en-GB,en', 'cf-connecting-ip': '5.232.194.253', 'cdn-loop': 'cloudflare', 'cf-ipcountry': 'IR', 'x-forwarded-for': '5.232.194.253', 'x-forwarded-host': 'tait.wns.watch', 'x-forwarded-server': 'tait.wns.watch', 'connection': 'Keep-Alive'}

channel_hits = None

channels_ids = {
    "H36sP13t": "Iran International",
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


with open("id_channel_hits.json", "r") as f:
    id_channel_hits = json.load(f)


with open("channel_hits.json", "r") as f:
    channel_hits = json.load(f)

@get("/index.html")
async def get_handler(headers: dict) -> dict[str, str]:
    print("GET", datetime.utcnow(), headers)

    ip = headers.get("cf-connecting-ip")
    country = headers.get("cf-ipcountry")
    useragent = headers.get("user-agent")

    print(ip)
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


@head("/index.html")
async def head_handler(headers: dict) -> None:
    print("GET", datetime.utcnow(), headers)

    ip = headers["cf-connecting-ip"]
    country = headers["cf-ipcountry"]
    useragent = headers["user-agent"]

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


@get("/app/logs",  media_type=MediaType.HTML)
async def get_log_handler(headers: dict) -> str:
    # html = ""
    # for k, v in channel_hits.items():
    #     html += f"{k} {v} \n"

    # HTML structure for the response
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

    # html_text = ""

    # ips = []
    # for c in reversed(channel_hits):
    #     html_text += f'\nTimestamp: {c["timestamp"]}\nIP: {c["ip"]}\nCountry: {c["country"]}\nUser Agent: {c["user_agent"]}\nMethod: {c["method"]}\n'
    #     html_text += "\n--------------------------------------------------------------------------------------\n"
    #     ips.append(c["ip"])

    # uniq_cnt = len(set(ips))
    # html = ""
    # html += f"Viewership count: {len(channel_hits)} | Unique count: {uniq_cnt}\n\n"
    # html += html_text

    return html

@get("/sstracker", media_type=MediaType.HTML)
async def sstracker_handle(headers: dict) -> str:
    print("GET sstracker", datetime.utcnow(), headers)

    html_text = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script defer src="https://dashait.wns.watch/script.js" data-website-id="471b9af5-391e-42fe-8ed2-3e0dff5c1761"></script>
        <title>Success</title>
    </head>
    <body>
    </body>
    </html>
    """

    return html_text

@get("/viewership")
async def get_viewership(headers: dict) -> dict[str, Any]:

    i = 1
    for c in channel_hits:
        c["id"] = i
        i += 1

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
    
    print(ip)
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
    #print(id_channel_hits)
    await save_data(id_channel_hits, output_file="id_channel_hits.json")

    # html_text = """
    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    #     <meta charset="UTF-8">
    #     <meta name="viewport" content="width=device-width, initial-scale=1.0">
    #     <script defer src="https://dashait.wns.watch/script.js" data-website-id="471b9af5-391e-42fe-8ed2-3e0dff5c1761"></script>
    #     <title>Success</title>
    # </head>
    # <body>
    # </body>
    # </html>
    # """

    #r = requests.get("/")
    Redirect(path="/sstracker")

    return {"status": "success"}

@get("/app/{channel_id:str}")
async def get_id_handler(headers: dict, channel_id: str = None) -> dict[str, str]:
    print("GET", datetime.utcnow(), channel_id, headers)

    resp = await get_by_channel_id(headers, channel_id, "GET")

    return resp

@head("/app/{channel_id:str}")
async def head_id_handler(headers: dict, channel_id: str = None) -> None:
    print("HEAD", datetime.utcnow(), channel_id, headers)

    resp = await get_by_channel_id(headers, channel_id, "HEAD")

    return 

@get("/app/viewership/{channel_id:str}",  media_type=MediaType.HTML)
async def get_viewership_handler(headers: dict, channel_id: str = None) -> dict[str, str]:
    #print(id_channel_hits)
    if channel_id is None or id_channel_hits.get(channel_id) is None:
        return {"status": "success"}
    
    # HTML structure for the response
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

# async def get_viewership_handler(headers: dict, channel_id: str = None)-> dict[str, str]:
#     # html = ""
#     # for k, v in channel_hits.items():
#     #     html += f"{k} {v} \n"

#     if channel_id is None or id_channel_hits.get(channel_id) is None:
#         return {"status": "success"}
    
#     html_text = ""

#     ips = []
#     for c in reversed(id_channel_hits[channel_id]):
#         html_text += f'\nTimestamp: {c["timestamp"]}\nIP: {c["ip"]}\nCountry: {c["country"]}\nUser Agent: {c["user_agent"]}\nMethod: {c["method"]}\n'
#         html_text += "\n--------------------------------------------------------------------------------------\n"
#         ips.append(c["ip"])

#     uniq_cnt = 1 #len(ips)
#     html = ""
#     html += f"{channels_ids[channel_id]} | Viewership count: {len(id_channel_hits[channel_id])} | Unique count: {uniq_cnt}\n\n"
#     html += html_text

#     return html

# @get("/app/{channel_id:str}")
# async def get_handler(headers: dict, channel_id: str = None) -> dict[str, str]:
#     print("GET", datetime.utcnow(), channel_id, headers)
#     new_data = {"new_key": "new_value", "existing_key": "updated_value"}
#     channel_hits.update(new_data)

#     ip = headers["cf-connecting-ip"]
#     country = headers["cf-ipcountry"]
#     useragent = headers["user-agent"]

#     return {"hello": "world"}

# @head("/app/{channel_id:str}")
# async def head_handler(headers: dict, channel_id: str = None) -> None:
#     print("GET", datetime.utcnow(), channel_id, headers)
# return {"hello": "world"}

# @get("/index.html")
# def index_page(headers: dict) -> dict[str, str]:
#     print("GET", datetime.utcnow(), headers)
#     return {"hello": "world"}

# @head("/index.html")
# def s(headers: dict) -> dict[str, str]:
#     print("HEAD", datetime.utcnow(), headers)
#     #return {"hello": "world"}

app = Litestar(
    route_handlers=[get_handler, head_handler, get_log_handler, get_viewership,
                    get_id_handler, head_id_handler, get_viewership_handler, sstracker_handle],
    debug=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=43223)
