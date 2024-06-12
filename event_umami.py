
import umami

umami.set_url_base("https://dashait.wns.watch")

# Auth is NOT required to send events, but is for other features.
login = umami.login("admin", "dashumami@123")
# Call after logging in to make sure the auth token is still valid.
umami.verify_token()
# Skip the need to pass the target website in subsequent calls.
umami.set_website_id('471b9af5-391e-42fe-8ed2-3e0dff5c1761')
umami.set_hostname('tait.wns.watch')

# List your websites
# websites = umami.websites()

# Create a new event in the events section of the dashboards.
# event_resp = umami.new_event(
#     event_name='Umami-Test11',
#     custom_data={'client': 'umami-tester-v1', "country": "Germany"}, 
#     ip_address="77.81.148.72")

page_view_resp = umami.new_page_view(
    page_title='IRPAGE',
    url='/app/irn',
    ua="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    ip_address="64.207.208.30"
    )

#print(event_resp)
print(page_view_resp)