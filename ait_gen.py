
ait = ""
with open("wnsait_tmp.xml", "r") as f:
    ait = f.read()

    # <metadata PID="[[PID]]"/>
    # <application control_code="0x01">
    #   <application_identifier organization_id="0x00000007" application_id="[[APP_ID]]"/>
    #   <application_descriptor service_bound="true" visibility="3" application_priority="1">
    #     <profile application_profile="0x0000" version="1.1.1"/>
    #     <transport_protocol label="0x01"/>
    #   </application_descriptor>
    #   <application_name_descriptor>
    #     <language code="eng" application_name="[[APP_NAME]]"/>
    #   </application_name_descriptor>
    #   <transport_protocol_descriptor transport_protocol_label="0x01">
    #     <http>
    #       <url base="[[BASE_URL]]"/>
    #     </http>
    #   </transport_protocol_descriptor>
    #   <simple_application_location_descriptor initial_path="[[APP_PATH]]"/>

def replacer(key, val):

    global ait

    ait = ait.replace(f"[[{key}]]", val)
    return ait

channel_name = "IRANINT"
app_path = "app/H36sP13t"
pid = "0x0582"

# channel_name = "AVAFAMILY"
# app_path = "index.html"
# pid = "0x0331"

val_dic = {
    "PID": pid,
    "APP_ID": "0x00D2",
    "APP_NAME": f"{channel_name}_AIT",
    "BASE_URL": "http://tait.wns.watch/",
    "APP_PATH": app_path,
}

for k, v in val_dic.items():
    ait = replacer(k, v)

print(ait)
with open(f"wnsait_{channel_name}.xml", "w") as f:
    f.write(ait)