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
    'cookie': 'TS01753cec=011d35fd7b7fc03df1fe60ad92072de05d6de5461a9cb1df75a8816a355a9a08fea0f2a00003651ae52a6ec2f9eaee24826534a2646ba66c4f77f2c41642060a997d39e33cef853f6c1b293f59bac6003296f1b837; TS01753cec030=01d23ba1732006902ae22246fc479b2745b27d5df33d25ac64436db81b9e1b560a6b1aeff5e3392cec6e2cf39562dee2604862fd7d; uc=init=%22H4sIAAAAAAAEAGWRX2%2bCMBTFvwvPkwgI6t5Qp5IJGFm2x%2bVSLrMJbU1L2b%2fsu6%2fdTI3x8Zzf7b3n3n57Kxwowazx7r0gjMJxMk0m2JI5tDPv7kwLYGh4WqwOZbZ63W%2fL4sHBp8%2bThfuj4OjMhQRuWypgSvM35%2beiwc74VT7azKPxowOlekapqOAGxn7gB46sqWTvIPHCw9DBLcjmGqojMH3Db0AOXLdAei1RXuXM1EGI3lgtdMouVBGJyCv6ZZskfmCHL086ranRH7PEydBokAyhpqNhCtYXnCPpTbDzkV6ydWb8UqWSHI2myd%2f7S%2fqJH%2flxHUf29suOIu8d47rrXOlC064pNKtt%2bn%2byQbETBOw0%2b5vxeBabZSXb4WBPbot%2bfgE4UqyP7wEAAA%3d%3d%22&uinf=k5%2fPtN0dS3rD62AQJtQDYgzBiTT1kNBO3mLxwgPFMo17NmghNN0c%2flI6MvX%2fCLRKdfA9moaNVIO6NB0Q8Ezh4iEDAYhPmJIu7a8Wy8cDU86oJqE%2bywU1z8pVgXABhxU85bxvQl2e1Guh300mIyePrD2M83dknUhA%2b8CbIGobU5R2r7sp3Yx1oOQhEaXxyExJG9VBFtiWQASOEWDpoVgoOCPYTrBfX1Ek%2fNs193AjXCA9hPvprc07FMyDy5g7kPsMjQMTA0s8FY5NkIL8dFeQbg%3d%3d; __RequestVerificationToken=VYp1XlulhmYxjH9KTe2kVcX31RvGV335JOWQzaBcu569sN5eCxtRsaugEa5dfj4JmlxR6dD2lmD6sQAeCC9VoO4XNIU1',
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


checkentitlement = req.post("https://mobileservice-smarttv-lg.beinconnect.com.tr/api/checkentitlement", headers=headers, json={"CmsContentId":selected_id,"IsPortrayal":"false"}).json()

if checkentitlement['errCode']== "NEEDAUTH":
    headers['cookie'] = req.get("https://reco31.vercel.app/loginbeinfilm").text
    checkentitlement = req.post("https://mobileservice-smarttv-lg.beinconnect.com.tr/api/checkentitlement", headers=headers, json={"CmsContentId":selected_id,"IsPortrayal":"false"}).json()
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
