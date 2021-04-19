import requests, threading, json, random, string, time

with open('settings.json', 'r') as settings:
    settings = json.loads(settings.read())

publickey = settings['public_key']
website = settings['site']
cap2 = settings['2captcha_key']

emailDomains = ['gmail', 'yahoo', 'outlook']

with open('proxies.txt', 'r') as proxies:
    proxies = proxies.read().splitlines()

threads = settings['threads']
prefix = settings['prefix']


def solveCaptcha():
    try:
        with requests.session() as session:
            requestCaptcha = session.post(f'http://2captcha.com/in.php?key={cap2}&method=funcaptcha&publickey={publickey}&surl=https://client-api.arkoselabs.com&pageurl={website}')
            captchaKey = requestCaptcha.text.split('|')[1]
        time.sleep(30)
        with requests.session() as session:
            getSolved = session.get(f'http://2captcha.com/res.php?key={cap2}&action=get&id={captchaKey}')
        return getSolved.text.split('OK|')[1]
    except:
        pass

def getForums():
    username = f'{prefix}' + ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=7))
    password = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
    email = f'{username}@{random.choice(emailDomains)}.com'
    day = random.randint(1,29)
    month = random.randint(1,12)
    year = random.randint(1990, 2006)
    birthday = {'day':day, 'month':month, 'year':year}
    RegisterForum = [username, password, email, birthday]
    return RegisterForum

def getClientId():
    with requests.session() as session:
        client_id = session.get('https://www.twitch.tv/').text.split('"Client-ID":')[1].split('","Content-Type"')[0]
    return client_id

def create_account():
    try:
        with requests.session() as session:
            form = getForums()
            username = form[0]
            password = form[1]
            email = form[2]
            birthday = form[3]
            token = solveCaptcha()
            clientId = getClientId()
            register = session.post('https://passport.twitch.tv/register', json={'arkose':{'token':token}, 'username':username, 'password':password, 'birthday':birthday, 'include_verification_code':False, 'client_id':clientId, 'email':email}, proxies={'http':random.choice(proxies), 'https':random.choice(proxies)}, headers={'accept-language''origin':'https://www.twitch.tv','sec-fetch-dest':'empty', 'sec-fetch-mode':'cors', 'sec-fetch-site':'same-site','referer':'https://www.twitch.tv/','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.57' ,'content-type':'text/plain;charset=UTF-8', 'accept-encoding':'gzip, deflate, br'})
            token = register.json()['access_token']
            print(register.json())
            created = {'username':username, 'password':password, 'token':token}
            token = f'{username}:{password}:{token}'
            with open(r'Logs\UPT.txt', 'a') as UPC:
                UPC.write(token + '\n')
            with open(r'Logs\tokens.txt', 'a') as tokens:
                tokens.write(token + '\n')
            print(created)
    except:
        return

def handle():
    while True:
        create_account()

print(f'Twitch Gen / 2captcha')
print(f'Developed by: SSL#4813 or https://github.com/sslprograms')
print(f'-> Starting {threads} threads..')
for thread in range(threads):
    threading.Thread(target=handle,).start()
