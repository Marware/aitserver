
ait = ""
with open("wnsait_tmp.xml", "r") as f:
    ait = f.read()

pmt = ""
with open("wnspmt_tmp.xml", "r") as f:
    pmt = f.read()

channels = """AVA Series,2110,21
Iran International,7060,705
Iran International,1420,14
FX 1 HD,1610,16
FX 2 HD,2310,23
Iran International HD,3310,33
FX 1 HD,1910,19"""

def replacer(table, key, val):

    table = table.replace(f"[[{key}]]", val)
    return table

channel_name = "IRANINT"
app_path = "app/H36sP13t"
pid = "0x0582"

# channel_name = "AVAFAMILY"
# app_path = "index.html"
# pid = "0x0331"



l = channels.split("\n")

pcmds = ""
app_id = 0x00D2
for n in l:
    ns = n.split(",")
    
    channel_name = ns[0]
    app_path = "app/H36sP13t"
    pid = ns[1]
    sid = ns[2]
    pcrpid = "0x07D1"

    ait_pid = str(int(pid) + 3)
# <PMT version="3" current="true" service_id="[[SERVICE_ID]]" PCR_PID="[[PCR_PID]]">
#     <metadata PID="[[PMT_PID]]"/>
#     <component elementary_PID="[[PCR_PID]]" stream_type="0x02"/>
#     <component elementary_PID="[[AIT_PID]]" stream_type="0x05">
    ait = ""
    with open("wnsait_tmp.xml", "r") as f:
        ait = f.read()

    pmt = ""
    with open("wnspmt_tmp.xml", "r") as f:
        pmt = f.read()
    channel_name = channel_name.replace(" ", "_")
    pmt_dic = {
        "PMT_PID": pid,
        "SERVICE_ID": sid,
        "PCR_PID": pcrpid,
        "AIT_PID": ait_pid,
    }

    ait_dic = {
        "PID": ait_pid,
        "APP_ID": str(app_id+1),
        "APP_NAME": f"{channel_name}_{ait_pid}_AIT",
        "BASE_URL": "https://tait.wns.watch/",
        "APP_PATH": app_path,
    }
    

    for k, v in pmt_dic.items():
        pmt = replacer(pmt, k, v)

    for k, v in ait_dic.items():
        ait = replacer(ait, k, v)

    # print(pmt)
    # print(ait)
    # continue 
    pmt_file = f"wns_pmt_{channel_name}_{pid}.xml"
    with open(pmt_file, "w") as f:
        f.write(pmt)

    pcmds += f" -P inject -p {pid} --inter-packet 1000 --xml {pmt_file} "

    ait_file = f"wns_ait_{channel_name}_{pid}.xml"
    with open(ait_file, "w") as f:
        f.write(ait)
    
    pcmds += f" -P inject -p {ait_pid} --inter-packet 1000 --xml {ait_file} "

tsp_cmd = f"tsp -I null 1000 {pcmds} -O file tsout.ts"

print(tsp_cmd)

"""
pcr pid > 2001
transport stream id > 1
"""