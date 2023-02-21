import requests
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import random
from bs4 import BeautifulSoup
import html_to_json

whatwebhook = 'https://discord.com/api/webhooks/826443550396121109/Pac0A2581oR-Xu4-WjFhuMmzZuUP7oAvkJmqipSHEf15LjWx2Rb-vT9cEjNW912MSYHN'


def discordJoin(site, stock, link, image, allStonk):
    webhook = DiscordWebhook(url=whatwebhook, rate_limit_retry=True)
    embed = DiscordEmbed(title=site, description=("Instock"), color='0x2ecc71')
    print(link)
    embed.set_timestamp()
    if type(stock) == int:
        embed.add_embed_field(name='Total Stock left: ', value=(stock), inline=False)
    if type(allStonk) == dict:
        embed.add_embed_field(name='Size',
                              value='\n'.join(['**{}:** {}'.format(str(size), allStonk[size]) for size in allStonk]),
                              inline=False
                              )
        
    elif type(allStonk) == list:
        embed.add_embed_field(name='Sizes:',
                              value='\n'.join(
                                  ['{}'.format(str(size)) for
                                   size in allStonk]),
                              inline=False
                              )
    else:
        embed.add_embed_field(name='Stock left: ', value=(stock), inline=False)

    embed.add_embed_field(name='Link: ', value=(link))
    embed.set_image(url=image)
    webhook.add_embed(embed)
    response = webhook.execute()
    
        
def setHeaders(auth, ref, agent):
    return {'authority': auth, 'referer': ref, 'user-agent': agent}


def journeys(sku, agents, proxies):
    totalStock = {}
    for x in sku:
        totalStock[x] = 0
    agent = random.choice(agents)
    proxy = random.choice(proxies)
    s = requests.session()
    s.headers.update(setHeaders('www.journeys.ca', 'https://www.journeys.ca/', agent))
    s.proxies.update({"http": proxy, "https": proxy})

    cc = True
    while cc:
        for x in sku:
            try:
                a = s.post('https://www.journeys.ca/api/product/{}'.format(x))
                b = a.json()
                image = b['SimilarItems'][0]['SwatchImage']
                urlident = b['SimilarItems'][0]['UrlIdentifier']
                maSKUs = b['maSKUs']
                allStonk = {}
                thisStonk = 0
                for i in maSKUs:
                    allStonk[i['Size']] = i['QuantityInStock']
                    stonk = int(i['QuantityInStock'])
                    thisStonk += stonk

                if thisStonk == 0:
                    for j in b['Product']['SKUs']:
                        allStonk[j['Size1']] = 'BACKEND STOCK #: {}'.format(j['QuantityInStock'])
                        stonk = int(j['QuantityInStock'])
                        thisStonk += stonk

                link = 'https://www.journeys.ca/product/{}'.format(urlident)
                if int(thisStonk) != int(totalStock[x]):
                    totalStock[x] = thisStonk
                    discordJoin('Journeys', thisStonk, link, image, allStonk)
                else:
                    print('Journeys {} Not In Stock'.format(str(x)))
                time.sleep(3)

            except:
                print('Error sending request for {}'.format(x))
                agent = random.choice(agents)
                proxy = random.choice(proxies)
                s.headers.update(setHeaders('www.journeys.ca', 'https://www.journeys.ca/', agent))
                s.proxies.update({"http": proxy, "https": proxy})
                time.sleep(10)
           
          
def sportinglife(skus, agents, proxies):
    from bs4 import BeautifulSoup
    import html_to_json

    agent = random.choice(agents)
    proxy = random.choice(proxies)
    s = requests.session()
    s.headers.update(setHeaders('www.sportinglife.ca', 'https://www.sportinglife.ca', agent))
    s.proxies.update({"http": proxy, "https": proxy})

    allSku = {}
    for sku in skus:
        allSku[sku] = []

    OOS = True
    while OOS:
        for sku in skus:
            try:
                link = 'https://www.sportinglife.ca/en-CA/shoes/-{}.html'.format(sku)
                image = 'https://www.sportinglife.ca/dw/image/v2/BCLQ_PRD/on/demandware.static/-/Sites-spl-master/default/images/default/{}_ONE_COLOUR_3.JPG'.format(
                    sku)
                linkk = 'https://www.sportinglife.ca/on/demandware.store/Sites-SportingLife-Site/en_CA/Product-Variation?pid={}&dwvar_{}&dwvar_{}_color=000&Quantity=1&format=ajax&productlistid=undefined'.format(
                    sku, sku, sku)
                a = s.get(linkk)
                a = a.text
                soup = BeautifulSoup(a, 'html.parser')
                all_class_topsection = soup.findAll('div', {'class': 'tfc-fitrec-product tfc-product-main-widget'})
                for para in all_class_topsection:
                    para = para

                output_json = html_to_json.convert(str(para))
                finddd = output_json['div'][0]['_attributes']['data-availablesizes']

                if finddd:
                    sizes = finddd.split(':')
                    if allSku[sku] != sizes:
                        allSku[sku] = sizes
                        discordJoin('Sportinglife', None, link, image, sizes)

                    else:
                        print('Sportinglife {} Same Sizes'.format(str(sku)))
                    time.sleep(10)
                else:
                    print('Sportinglife {} Not In Stock'.format(str(sku)))
                    time.sleep(10)

            except:
                print('Error sending Sportinglife request')
                agent = random.choice(agents)
                proxy = random.choice(proxies)
                s.headers.update(setHeaders('www.sportinglife.ca', 'https://www.sportinglife.ca', agent))
                s.proxies.update({"http": proxy, "https": proxy})
                time.sleep(10)
                
       
      
def holtRenfrew(skus, agents, proxies):
    totalStock = {}
    for x in skus:
        totalStock[x] = 0
    agent = random.choice(agents)
    proxy = random.choice(proxies)
    s = requests.session()
    s.headers.update(setHeaders('www.holtrenfrew.com', 'https://www.holtrenfrew.com', agent))
    s.proxies.update({"http": proxy, "https": proxy})

    cc = True
    while cc:
        for x in skus:
            try:
                a = s.get('https://www.holtrenfrew.com/en/p/{}/getSwatches'.format(x))
                b = a.json()
                for prod in b:
                    if prod['swatchData']['color'] == 'Chestnut' or prod['swatchData']['color'] == 'Driftwood':
                        image = (prod['swatchData']['swatch']['url']).replace('_S1', '_01')
                        image = 'https:{}'.format(image)
                        link = 'https://www.holtrenfrew.com/en/Products/joshbeyer/p/{}'.format(x)

                        allStonk = {}
                        thisStonk = 0

                        for i in prod['productVariantDataList']:
                            size = i['size']
                            stock = i['stock']['stockLevel']
                            allStonk[size] = stock
                            thisStonk += int(stock)

                        if int(thisStonk) != int(totalStock[x]):
                            totalStock[x] = thisStonk
                            discordJoin('Holt Renfrew', thisStonk, link, image, allStonk)

                        else:
                            print('Holt Renfrew {} Not In Stock'.format(str(x)))
                        time.sleep(3)

            except:
                print('Holt Renfrew Error sending request for {}'.format(x))

                agent = random.choice(agents)
                proxy = random.choice(proxies)
                s.headers.update(setHeaders('www.holtrenfrew.com', 'https://www.holtrenfrew.com', agent))
                s.proxies.update({"http": proxy, "https": proxy})
                time.sleep(10)
                
                
def uggCa(skus, agents, proxies):
    import secrets
    import string
    import cloudscraper
    
    allSizes = {}

    for sku in skus:
        allSizes[sku] = []

    while True:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(10))

        agent = random.choice(agents)
        proxy = random.choice(proxies)
        print('Ugg CA Getting Session')

        s = cloudscraper.create_scraper()
        s.proxies.update({"http": proxy, "https": proxy})
        s.headers.update({
            "Sec-Ch-Ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "User-Agent": agent,
            "Referer": "https://www.ugg.com/ca",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Dest": "empty",
            "Accept-Encoding": "gzip, deflate",
            "Sec-Fetch-Mode": "cors",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua-Mobile": "?0"
        })
        cookieing = True
        while cookieing:
            try:
                a = s.get('https://www.ugg.com/ca/')

                s.cookies.update({
                    "forterToken": password,
                    "dwsid": a.cookies['dwsid'],
                })
                cookieing = False
            except:
                print('Ugg Ca Error getting session')
                s = cloudscraper.create_scraper()
                s.proxies.update({"http": proxy, "https": proxy})
                agent = random.choice(agents)
                s.headers.update({
                    "Sec-Ch-Ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\"",
                    "Accept": "*/*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Sec-Ch-Ua-Platform": "\"Windows\"",
                    "User-Agent": agent,
                    "Referer": "https://www.ugg.com/ca",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-Dest": "empty",
                    "Accept-Encoding": "gzip, deflate",
                    "Sec-Fetch-Mode": "cors",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Sec-Ch-Ua-Mobile": "?0"
                })
                time.sleep(2)

        run = True
        while run:
            for x in skus:
                try:
                    skuSplit = x.split(':')
                    code = skuSplit[0]
                    color = skuSplit[1]

                    link = 'https://www.ugg.com/ca/joshbeyer/{}.html'.format(code)
                    s.headers.update({
                        'Accept': '*/*',
                        'Referer':'https://www.ugg.com/ca/{}/{}.html?dwvar_{}_color={}'.format(password, code, code, color),
                        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
                    })

                    paramsGet = {"pid": "{}".format(code), "dwvar_{}_color".format(code): color, "dwvar_{}_size".format(code): "7"}
                    atc = s.get("https://www.ugg.com/on/demandware.store/Sites-UGG-CA-Site/en_CA/Product-Variation",
                        params=paramsGet)
                    print(atc)
                    atcJson = atc.json()
                    
                    try:
                        image = atcJson['product']['images']['default']['small'][0]['url']

                        sizes = []
                        stockSize = {}
                        for i in atcJson['product']['variationAttributes'][1]['values']:
                            if 'isMaster' in i:
                                pass
                            elif i['available'] == True:
                                if i['availability']['type'] != 'backorder':
                                    if (x == '1135092:MSG' and (i['id'] == '12' or i['id'] == '11' or i['id'] == '10' or i['id'] == '09')):
                                        pass
                                    elif (x == '1135092:BLK' and i['id'] == '10'):
                                        pass
                                    else:
                                        if i['availability']['messages'] != ['In Stock']:
                                            stock = ((i['availability']['messages'][0]).replace(", don’t miss out!", ''))
                                            stock = stock.replace("Only ", '')
                                        else:
                                            stock = '10+'
                                        sizes.append(i['id'])
                                        stockSize[i['id']] = stock
                                else:

                                    if (x == '1135092:BLK' and i['id'] == '10') or (x == '1122550:CHE' and (i['id'] == '08' or i['id'] == '06' or i['id'] == '07')):
                                        pass

                                    else:
                                        sizes.append('{} - Backorder: Instock Date {}'.format(i['id'], i['availability']['inStockDate']))

                                        stockSize[i['id']] = 'Backorder: Instock Date {}'.format(i['availability']['inStockDate'])
                        print(sizes)
                        print(allSizes[x])

                        if sizes == allSizes[x]:
                            print('Ugg Canada {} {} Not In Stock'.format(str(code), color))
                        else:
                            print(sizes)
                            print(allSizes[x])
                            print('Ugg Canada {} {} INSTOCK'.format(code, color))
                            print(atcJson)
                            allSizes[x] = sizes
                            discordJoin('Ugg Canada', 'testingg', link, image, stockSize)
                    except:
                        print('{} {} Product Not Loaded'.format(code, color))

                    time.sleep(5)
                except:
                    if atc.status_code == 429:

                        print('{} {} Product Not Loaded'.format(code, color))

                        time.sleep(5)
                    else:

                        print('Ugg CA {} Error Sending Request'.format(x))

                        time.sleep(5)
                        run = False
                        break
