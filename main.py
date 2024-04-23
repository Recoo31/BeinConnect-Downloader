from beinconnect_api import *
from getKey import *
import os
import headers as head


init()

query = input("Search->")

selected_id, selected_name, typ = search(query)
if typ == "Series":
    selected_season_id, episodeOrderField, episodeOrderMode = getproductdetails(selected_id)
    selected_id = getepisodes(selected_season_id, episodeOrderField, episodeOrderMode)
    
spec_id, asset_id = checkentitlement(selected_id)
has_drm, event_data, cdn_uri = get_event(selected_id,spec_id,asset_id)
drm_token, cdn_uri_with_ticket, ticket = get_url(selected_id,spec_id,cdn_uri, asset_id, event_data)

head.headers['X-ErDRM-Message'] = ticket
pssh = requests.get(cdn_uri_with_ticket, allow_redirects=True).text.split('<cenc:pssh>')[2].split('</cenc:pssh>')[0]

os.system("cls")

lic_url = "https://digiturk-drm.ercdn.com/widevine/api/erproxy"
correct, keys = WV_Function(pssh,lic_url)
print(pssh)
key = {}
for key in keys:
    print("KID:KEY: " + key)

os.system(os.getcwd()+f'\\bin\\N_m3u8DL-RE.exe --key {key} --save-name "{selected_name}" "{cdn_uri_with_ticket}" --live-real-time-merge --live-pipe-mux')
    