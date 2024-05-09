import requests, subprocess, os
from colorama import Fore, Style

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'tr-TR,tr;q=0.6',
    'authorization': '%7b%22init%22%3a%22%2522H4sIAAAAAAAEAIVRy07DMBD8l5xJlcROTbilRUClPqQm6t2PRVhK7GoTFwHi33Gl2m164Tgzmp2d3Z%252fkGU5awkolTwlRgha8ZCkp5ixl%252bVykWV4VaS4qoKwirOQ0ebg4trwH72k29b5tD5Fuv46eNq7rArNAbtSU2lgF3ZTaDQfAQVvjZ8ZhLxr7T44QpVvHG0f1r3iXy41753J0CBiU1bC3dgyokQhgGv0dncujq4WeoiJCawzI0cff9t4NNcqPgK69yIzMMkFp7gsuOw1mvNv9AhdOd2rrenHd8hXs2kp%252bTjq%252fqsweiS%252bF%252fRpO4ZK%252ffzmPdojMAQAA%2522%22%2c%22uinf%22%3a%22MUV0HfEfQZh3wG74y%252bWjmwy4PtFrrF4TvhY85CmPnFRTdcTCBbkQhCEvPRMJFEXom0FxYiNhfBS9GKpt3FDn2eEnsI3s%252byt1HNphaq1eocexjZUviF2vGmhledRlAnd98yNbFw2E3IYFtBUZuyaAoLFp4RPfQbglJmQXjfeaDf%252fSww9i77IlD%252fal3eu8XpMBgGagSgAl4JMv3AAvNjfdX29RtT25%252bUQh0pqfIkBjgTf19nlr%252bdSgQq8CyLGqaeWlcyQegms98luL0sp%252ft1fhRg%253d%253d%22%7d',
    'childroomactivated': 'false',
    'content-type': 'application/json',
    'origin': 'https://smrtsg.beinconnect.com.tr',
    'referer': 'https://smrtsg.beinconnect.com.tr/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
}

def handle_error(response):
    if response["errCode"] != "OK":
        err = response["message"]
        err_code = response["ErrorMessage"]
        print(f"{Fore.RED} {err} \n {err_code} {Style.RESET_ALL}")
        exit()


def get_pssh(cdn_uri_with_ticket):
    process = subprocess.Popen([os.getcwd() + '\\bin\\N_m3u8DL-RE.exe', '--save-name', 'test', cdn_uri_with_ticket, '--auto-select'], stdout=subprocess.PIPE)

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode('utf-8').strip())
            if "PSSH(WV):" in output.decode('utf-8'):
                pssh_index = output.decode('utf-8').find("PSSH(WV):")
                pssh_key = output.decode('utf-8')[pssh_index+10:].strip()
                process.terminate()
                return pssh_key
    process.wait()

            
def init():
    json_data = {"DeviceName":"SMARTTV","uuid":"34255485-a88c-994a-8745-69be49d1268a","device":"TV","device_type":"SMARTTV","os":"Windows10","ClientVersion":"3.3.0b441","username":"","jailbroken":False,"DeviceLanguage":"TR","DeviceId":"34255485-a88c-994a-8745-69be49d1268a","DeviceOsVersion":""}

    response = requests.post('https://mobileservice-smarttv.beinconnect.com.tr/api/init2?rnd=0.25646692375601043',headers=headers,json=json_data).json()
    handle_error(response)

    
    headers["authorization"] == response["accessToken"]
    return


def search(query):
    url = "https://mobileservice-smarttv.beinconnect.com.tr/api/content/search2?rnd=0.6792948073898692"
    post_data = {"Keyword":query,"Page":1,"Count":50}
    
    response = requests.post(url, json=post_data, headers=headers).json()
    handle_error(response)

    products =  response["products"]

    for i,item in enumerate(products):
        if "PS" in item['id']:
            typ = "Series"
        else:
            typ = "Movie"
        print(f"{Fore.MAGENTA}{i+1} : {Fore.LIGHTMAGENTA_EX}{item['titleOriginal']} | {typ} {Style.RESET_ALL}")

    selected = int(input("Select->")) - 1
    selected_id = products[selected]
    return selected_id["id"], selected_id["titleOriginal"], typ

def getproductdetails(selected_id):
    url = "https://mobileservice-smarttv.beinconnect.com.tr/api/v2/getproductdetails?rnd=0.43724332814885214"
    post_data = {"ProductId":selected_id}
    response = requests.post(url, headers=headers, json=post_data).json()
    handle_error(response)

    details = response["ProductDetails"]
    episodeOrderField = details["episodeOrderField"]
    episodeOrderMode = details["episodeOrderMode"]

    season = details["season"]

    for item in season:
        name = item["name"]
        print(Fore.MAGENTA+name+Style.RESET_ALL)
    selected = int(input("Select->")) - 1
    selected_season_id = season[selected]["id"]
    return selected_season_id, episodeOrderField, episodeOrderMode

def getepisodes(selected_season_id, episodeOrderField, episodeOrderMode):
    url = "https://mobileservice-smarttv.beinconnect.com.tr/api/getepisodes?rnd=0.24435242265543322"
    post_data = {"seasonId":selected_season_id,"episodeOrderField":episodeOrderField,"episodeOrderMode":episodeOrderMode,"page":1,"count":150}
    response = requests.post(url, headers=headers, json=post_data).json()
    handle_error(response)
    products =  response["products"]

    for item in products:
        print(f"{Fore.MAGENTA}{item['titleOriginal']} {Style.RESET_ALL}")
    selected = int(input("Select->")) - 1
    selected_item = products[selected]["id"]
    return selected_item




def checkentitlement(selected_id):
    url = "https://mobileservice-smarttv.beinconnect.com.tr/api/checkentitlement?rnd=0.9283716413245446"
    post_data = {"CmsContentId":selected_id,"StreamFormat":1,"IsPortrayal":False}
    response = requests.post(url, headers=headers, json=post_data).json()
    handle_error(response)

    data = response["Data"]["Versions"][0]["Assets"][0]
    # for i, item in enumerate(data):
    #     asset_label = item["AssetLabel"]
    #     print(f"{i+1}-> {asset_label}")
    # selected = int(input("Select->")) - 1
    # selected_item = data[selected]

    # url = "https://mobileservice-smarttv.beinconnect.com.tr/api/checkentitlement?rnd=0.9283716413245446"
    # post_data = {"CmsContentId":selected_id,"StreamFormat":selected_item,"IsPortrayal":False}
    # response = requests.post(url, headers=headers, json=post_data).json()
    # handle_error(response)
    # data = response["Data"]["Versions"][0]["Assets"][0]
    
    return data["UsageSpecId"], data["AssetId"]

def get_event(_id,spec_id,asset_id):
    url = f"https://mobileservice-smarttv.beinconnect.com.tr/api/v2/vod/contents/{_id}/usages/{spec_id}/assets/{asset_id}/cdn/1/alternate/3?rnd=0.9604823708960291"
    response = requests.get(url, headers=headers).json()
    handle_error(response)

    event_data = response["event_data"]
    cdn_list = response["cdn_list"][0]

    has_drm = cdn_list["has_drm"]
    cdn_uri = cdn_list["uri"]

    return has_drm, event_data, cdn_uri

def get_url(selected_id, spec_id, cdn_uri, asset_id, event_data):
    url = "https://mobileservice-smarttv.beinconnect.com.tr/api/v2/vod/contents/ticket?rnd=0.7637453031302732"
    json_data = {
        'cdn_type': 0,
        'cms_content_id': selected_id,
        'usage_spec_id': spec_id,
        'cdn_uri': cdn_uri,
        'stream_format': 'DASH',
        'asset_id': asset_id,
        'drm_type': 2,
        'event_data': event_data,
    }


    response = requests.post(url,json=json_data,headers=headers).json()
    handle_error(response)

    drm_token = response["drm_token"]

    ticket_list = response["ticket_list"][0]
    ticket = ticket_list["ticket"]
    cdn_uri_with_ticket = ticket_list["cdn_uri_with_ticket"]
    return drm_token, cdn_uri_with_ticket, ticket

