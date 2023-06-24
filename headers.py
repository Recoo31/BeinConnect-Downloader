import requests

headers = {
    'Accept': '*/*',
    'Accept-Language': 'tr-TR,tr;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.beinconnect.com.tr',
    'Referer': 'https://www.beinconnect.com.tr/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-ErDRM-Message': 'HnlkFGOMZM25DCHDHFEpMAOvj-8JTYvvrgr6qFaOxGt1pGi2AVwjniQhfEdBLbYxejpzwNmxtgm6DG46vUu00a9rnG9WnBvLl4zz1RqPbiObwvZuCCdB8sJC3arUhJLsUjwp2C3M_-JcJxpD-qVoTx-4lnsF_ienLD6fFUUBbut0Nndu69bQGKEkECroa5g7oeYDSywdg_khtt7td_8stw2',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '\b\x04'

response = requests.post('https://digiturk-drm.ercdn.com/widevine/api/erproxy', headers=headers, data=data)