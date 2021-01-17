import json
from bs4 import BeautifulSoup
import requests
from urllib3 import PoolManager
import re

def track_stock():
    cards = ['3080','3070','3060ti']

    url_dict = {"3070":"https://rptechindia.in/nvidia-geforce-rtx-3070.html",
                "3060ti":"https://rptechindia.in/nvidia-geforce-rtx-3060-ti.html",
                "3080":"https://rptechindia.in/nvidia-geforce-rtx-3080.html"}
    
    hdr = {'User-Agent':
        ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
        '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
        'Accept':
        ('text/html,application/xhtml+xml,'
        'application/xml;q=0.9,*/*;q=0.8'),
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'close'}
    
    chat_id = YOUR_CHAT_ID
    bot_secret = YOUR_BOT_SECRET
    
    http = PoolManager()
    err_code = 0
    
    for card in cards:
        try:
            response = http.request('GET', url_dict[card], hdr, timeout=3, retries=2)
            soup = BeautifulSoup(response.data, 'html.parser')
            span_text = soup.find_all('span', {'class' :'rs2'})[0].text
            if 'Out of stock' not in span_text:
                div_text = soup.find_all('div', {'class' :'pull-left retail'})
                qty =''
                for divs in div_text:
                    if divs.find(text=re.compile("Available Quantity")):
                        qty = divs.text
                        break
                text = card + " is in stock. "+ qty +". BUY @ " + url_dict[card]
                data = {'text': f"{text}", 'chat_id': f"{chat_id}"}
                requests.post(f"https://api.telegram.org/bot{bot_secret}/sendMessage", data = data)
        except:
            text = "Response error looking for "+ card
            data = {'text': f"{text}", 'chat_id': f"{chat_id}"}
            requests.post(f"https://api.telegram.org/bot{bot_secret}/sendMessage", data = data)
            err_code = 1
            continue
    
    return err_code

def lambda_handler(event, context):
    res = track_stock()
    if res == 0:
        return {
            'statusCode': 200,
            'body': json.dumps('Scaping success')
        }
    return {
        'statusCode': 500,
        'body': json.dumps('Response blocked by website')
    }
