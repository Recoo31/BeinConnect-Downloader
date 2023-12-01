import headers as head
from getKey import *
import os, time

try:
    import requests as req
    import ffmpeg
except:
    os.system("pip install requests")
    os.system("pip install ffmpeg-python")

search = input("Search-> ")

headers = {
    'authority': 'mobileservice-smarttv-lg.beinconnect.com.tr',
    'accept': 'text/plain, */*; q=0.01',
    'accept-language': 'tr-TR,tr;q=0.8',
    'Authorization': '%7b%22init%22%3a%22%2522H4sIAAAAAAAEAIVRy27CMBD8l5wb5MYhCb0FKigSD4lE3Df2RrXk2MiJqdqq%252f14jYUO4cJwZzc7O7m%252f0jmfBcM2jtyjLCSezNo%252bBz4oY0ryICUlonNEWAYCyaZJFL1fHDjp0nmpbHur6GOj6%252b%252bRoZaX0zNyA4mNqqznKMbXvj2h6oZWbGYYthem%252bwGCQ7h0fYPhT8SEXlG2BDdag8cq6P2g9eFQxg6gq8ROci5MtGzFGSYBaKWSDi7%252fvve9Lwz49uvWiEzohTZq%252buoILKVAND7tf4dwKyXe2a25brlBvNINL0uVVU1JQV8p0Gzz7S%252f79A0dpCyvMAQAA%2522%22%2c%22uinf%22%3a%22i0ZsKEo5nm6WSQ4qqz1NGAnaJ%252bqtN6gpQ0Lf6RVstI9%252b65TBdM1hCiqt3QwZjCR4ujivuAqEdRmV4E6cmzNq2wsEsYXipjuCf%252fJhBxYIlggKO1Uok%252blkhaq2ZtUc9bAeVkXFLrWTnH4yP34EPXsavoNDm0orU6eBObfA%252f2KYzUp1gTuAWVLnGibW7%252bSgoF44SXuyl5v1WGYbl%252b75Dx5Y6n%252fTnXMp2JEBatYkdeNJDZXgBo4RqefDg8Iic8WnSKrt%22%7d',
    'childroomactivated': 'false',
    'origin': 'https://smrtlg.beinconnect.com.tr',
    'referer': 'https://smrtlg.beinconnect.com.tr/',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}


try:
    search_post = req.post('https://mobileservice-smarttv-lg.beinconnect.com.tr/api/content/search2', headers=headers, json={'Keyword': search,'Page': 1,'Count': 50}).json()
    data = search_post['products']
    if not data:
        print("Movie Not Found!")
        search = input("Search-> ")
        
        search_post = req.post('https://mobileservice-smarttv-lg.beinconnect.com.tr/api/content/search2', headers=headers, json={'Keyword': search,'Page': 1,'Count': 50}).json()
        data = search_post['products']
except:
    pass
    
for i,movie in enumerate(data):
    if "PS" in movie['id']:
        typ = "Series"
    else:
        typ = "Movie"
    print(f"{i+1}: {movie['titleOriginal']} | {typ}")

selected = int(input("Select-> ")) - 1
selected_id = data[selected]['id']
if "PS" in selected_id:
        print("Series are not supported")
        time.sleep(2)
        exit()
    
selected_name = data[selected]['titleOriginal']


checkentitlement = req.post("https://mobileservice-smarttv-lg.beinconnect.com.tr/api/checkentitlement", headers=headers, json={"CmsContentId":selected_id,"StreamFormat":1,"IsPortrayal":"false"}).json()

if checkentitlement['errCode']== "NEEDAUTH":
    headers['Authorization'] = req.get("https://reco31.vercel.app/logintodfilmtoken").text
    checkentitlement = req.post("https://mobileservice-smarttv-lg.beinconnect.com.tr/api/checkentitlement", headers=headers, json={"CmsContentId":selected_id,"StreamFormat":1,"IsPortrayal":"false"}).json()
else:
    pass

pt = checkentitlement['Data']['Versions'][0]['Assets'][0]['AssetId']
usage_spec = checkentitlement['Data']['Versions'][0]['Assets'][0]['UsageSpecId']

get_cdn = req.get(f"https://mobileservice-smarttv-lg.beinconnect.com.tr/api/v2/vod/contents/{selected_id}/usages/{usage_spec}/assets/{pt}/cdn/1/alternate/3",headers=headers).json()

event_data = get_cdn["event_data"]
cdn_list = get_cdn["cdn_list"][0]["uri"]



ticket_data = {"cdn_type":0,"cms_content_id":selected_id,"usage_spec_id":usage_spec,"cdn_uri":cdn_list,"stream_format":"DASH","asset_id":pt,"drm_type":2,"event_data":event_data}

ticket = req.post("https://mobileservice-smarttv-lg.beinconnect.com.tr/api/v2/vod/contents/ticket",headers=headers,json=ticket_data)


responseArray = ticket.json()
ticket = responseArray['ticket_list'][1]['ticket']
cdn_list = cdn_list + "&" + ticket

pssh = req.get(cdn_list, allow_redirects=True).text.split('<cenc:pssh>')[2].split('</cenc:pssh>')[0]
print("PSSH: "+ pssh)
head.headers['X-ErDRM-Message']= ticket

try:
    lic_url = "https://digiturk-drm.ercdn.com/widevine/api/erproxy"
    correct, keys = WV_Function(pssh,lic_url)
    print()
    key = {}
    for key in keys:
        print("KID:KEY: " + key)

    os.system(os.getcwd()+f'\\bin\\N_m3u8DL-RE.exe --key {key} --save-name "{selected_name}" "{cdn_list}" --live-real-time-merge --live-pipe-mux --auto-select')
    
    lang = int(input("Turkish Lang -> 1\nEnglish Lang -> 2\n-> "))

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    if lang == 1:
        input_video = ffmpeg.input(f'{selected_name}.mp4')
        input_audio = ffmpeg.input(f'{selected_name}.tr.m4a')
        output_video = f'{desktop_path}/{selected_name}_out.mp4'

        ffmpeg.output(input_video, input_audio, output_video, c='copy').run()
    else:
        input_video = ffmpeg.input(f'{selected_name}.mp4')
        input_audio = ffmpeg.input(f'{selected_name}.en.m4a')
        output_video = f'{desktop_path}/{selected_name}_out.mp4'

        ffmpeg.output(input_video, input_audio, output_video, c='copy').run()
    print("Download Completed\n"*5)
except Exception as e:
    print("KEY or ffmpeg error. "+ str(e))
    exit()
