from litestar import Litestar, get, head
from datetime import datetime
import json
#2024-05-12 14:23:15.300767 {'host': 'tait.wns.watch', 'accept-encoding': 'gzip, br', 'cf-ray': '882b10c8791f2bc1-FRA', 'x-forwarded-proto': 'https', 'cf-visitor': '{"scheme":"https"}', 'upgrade-insecure-requests': '1', 'user-agent': 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36 HbbTV/1.5.1 (+DRM; LGE; 75UP81003LR; WEBOS6.0 03.40.82; W60_K7LP; DTV_W21P;)', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'sec-fetch-site': 'cross-site', 'sec-fetch-mode': 'navigate', 'accept-language': 'en-GB,en', 'cf-connecting-ip': '5.232.194.253', 'cdn-loop': 'cloudflare', 'cf-ipcountry': 'IR', 'x-forwarded-for': '5.232.194.253', 'x-forwarded-host': 'tait.wns.watch', 'x-forwarded-server': 'tait.wns.watch', 'connection': 'Keep-Alive'}

channel_hits = None

async def save_data(data, output_file=None):
    """Saves the (potentially updated) JSON data.

    Args:
        output_file: Optional path to save data to a new file. If not provided, overwrites the original.
    """
    output_file = "channel_hits.json"
    try:
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)  # Pretty-print with indentation
    except IOError:
        print(f"Error: Could not write to file '{output_file}'.")

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
        "method": "GET"
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
        "method": "HEAD"
    }
    
    channel_hits.append(data)
    await save_data(channel_hits)
    return

@get("/app/logs")
async def get_log_handler(headers: dict) -> str:

    # html = ""
    # for k, v in channel_hits.items():
    #     html += f"{k} {v} \n"

    html_text = ""

    ips = []
    for c in reversed(channel_hits):
        html_text += f'Timestamp: {c["timestamp"]}\nIP: {c["ip"]}\nCountry: {c["country"]}\nUser Agent: {c["user_agent"]}\nMethod: {c["method"]}\n'
        html_text += "--------------------------------------------------------------------------------------"
        ips.append(c["ip"])

    uniq_cnt = len(set(ips))
    html = ""
    html += f"Viewership count: {len(channel_hits)} | Unique count: {uniq_cnt}\n"
    html += html_text

    return html

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
    #return {"hello": "world"}

# @get("/index.html")
# def index_page(headers: dict) -> dict[str, str]:
#     print("GET", datetime.utcnow(), headers)
#     return {"hello": "world"}

# @head("/index.html")
# def s(headers: dict) -> dict[str, str]:
#     print("HEAD", datetime.utcnow(), headers)
#     #return {"hello": "world"}

app = Litestar(route_handlers=[get_handler, head_handler, get_log_handler], debug=False)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=43223)