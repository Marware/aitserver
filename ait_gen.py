
ait = ""
with open("wnsait_tmp.xml", "r") as f:
    ait = f.read()

pmt = ""
with open("wnspmt_tmp.xml", "r") as f:
    pmt = f.read()

patf = ""
with open("wnspat_tmp.xml", "r") as f:
    patf = f.read()

sdtf = ""
with open("wnssdt_tmp.xml", "r") as f:
    sdtf = f.read()

nitf = ""
with open("wnsnit_tmp.xml", "r") as f:
    nitf = f.read()

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

pat_tmp = """<service service_id="{}" program_map_PID="{}"/>"""
pat_tmp_t = pat_tmp

sdt_tmp = """<service service_id="{}" EIT_schedule="{}" EIT_present_following="{}" CA_mode="{}" running_status="{}">
      <service_descriptor service_type="{}" service_provider_name="{}" service_name="{}"/>
    </service>"""
sdt_tmp_t = sdt_tmp

nit_tmp = """<service service_id="{}" service_type="{}"/>"""
nit_tmp_t = nit_tmp

nit_log_tmp = """<service service_id="{}" logical_channel_number="{}" visible_service="{}"/>"""
nit_log_tmp_t = nit_log_tmp

l = channels.split("\n")

pats = ""
sdts = ""
nits = ""
nits_logs = ""

lcn = 1
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
    
    o_channel_name = channel_name
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

# nit_tmp = """<service service_id="{}" service_type="{}"/>"""
# nit_tmp_t = nit_tmp

# nit_log_tmp = """<service service_id="{}" logical_channel_number="{}" visible_service="{}"/>"""
    service_type = "0x19"

    pats += pat_tmp.format(sid, pid)
    sdts += sdt_tmp.format(sid, "true", "true", "false", "running", service_type, "Wide Network Solutions", o_channel_name)
    nits += nit_tmp.format(sid, service_type)
    nits_logs += nit_log_tmp.format(sid, str(lcn), "true")
    
    lcn += 1

    for k, v in pmt_dic.items():
        pmt = replacer(pmt, k, v)

    for k, v in ait_dic.items():
        ait = replacer(ait, k, v)

    # reg = "--inter-packet 1000"
    reg = "--bitrate 5000000"
    # print(pmt)
    # print(ait)
    # continue
    pmt_file = f"wns_pmt_{channel_name}_{pid}.xml"
    with open(pmt_file, "w") as f:
        f.write(pmt)

    pcmds += f" -P inject -p {pid} {reg} --xml {pmt_file} "

    ait_file = f"wns_ait_{channel_name}_{pid}.xml"
    with open(ait_file, "w") as f:
        f.write(ait)
    
    pcmds += f" -P inject -p {ait_pid} {reg} --xml {ait_file} "

patf = patf.replace("[[PAT_SERVICES]]", pats)
pat_file = "wns_pat.xml"
with open(pat_file, "w") as f:
    f.write(patf)

sdtf = sdtf.replace("[[SERVICES]]", sdts)
sdt_file = "wns_sdt.xml"
with open(sdt_file, "w") as f:
    f.write(sdtf)


nitf = nitf.replace("[[NIT_SERVICES]]", nits)
nitf = nitf.replace("[[NIT_LOGICAL_SERVICES]]", nits_logs)
nitf = nitf.replace("[[ACTUAL]]", "true")
print(nitf)
nit_file = "wns_nit.xml"
with open(nit_file, "w") as f:
    f.write(nitf)

# nitf_other = nitf.replace("[[NIT_SERVICES]]", nits)
# nitf_other = nitf.replace("[[NIT_LOGICAL_SERVICES]]", nits_logs)
# nitf_other = nitf.replace("[[ACTUAL]]", "false")
# nit_file_other = "wns_nit_other.xml"
# with open(nit_file_other, "w") as f:
#     f.write(nitf_other)

pcmds = f" -P inject -p 0 {reg} --xml {pat_file} " + pcmds
pcmds = f" -P inject -p 17 {reg} --xml {sdt_file} " + pcmds

pcmds += f" -P inject -p 16 {reg} --xml {nit_file} "
#pcmds += f" -P inject -p 16 --inter-packet 1000 --xml {nit_file_other} "

tsp_cmd = f"tsp --bitrate 30000000 --max-flushed-packets 70 -I null 10000 -P regulate --packet-burst 14 {pcmds} -O file tsout.ts"

print(tsp_cmd)

"""
pcr pid > 2001
transport stream id > 1
"""