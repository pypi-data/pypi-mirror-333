#by hso
class instagram:
    @staticmethod
    def info(user):
        try:
            import requests
            import uuid
            import time
            import random
            import base64
        except ImportError:
            h=["requests","uuid","time","base64"]
            for l in h:
                import os
                os.system("pip install {}".format(l))
        oo = f"-1::{user}"
        ee = base64.b64encode(oo.encode('utf-8')).decode('utf-8')
        headers = {
		'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
		}
        try:
            rr = requests.get(f'https://instanavigation.net/api/v1/stories/{ee}', headers=headers).json()
            ids = rr['user_info']['id']
            full_name = rr['user_info']['full_name']
            is_private = rr['user_info']['is_private']
            media_count = rr['user_info']['posts']
            followers = rr['user_info']['followers']
            following = rr['user_info']['following']
            return {"data":{"id":ids,"full_name":full_name,"is_private":is_private,"post":media_count,"followers":followers,"following":following,"programer":"@ii33cc"}}
        except Exception as e:
            return{"status":False,"no info user":user}
    @staticmethod
    def checkEmail(email):
        try:
            import requests
            import uuid
            import time
            import hashlib
            import secrets
            from random import choice,randint,randrange
        except ImportError:
            h=["requests","uuid","time","secrets","hashlib"]
            for l in h:
                import os
                os.system("pip install {}".format(l))
        rnd=str(randint(150, 999))
        user_agent = "Instagram 311.0.0.32.118 Android (" + ["23/6.0", "24/7.0", "25/7.1.1", "26/8.0", "27/8.1", "28/9.0"][randint(0, 5)] + "; " + str(randint(100, 1300)) + "dpi; " + str(randint(200, 2000)) + "x" + str(randint(200, 2000)) + "; " + ["SAMSUNG", "HUAWEI", "LGE/lge", "HTC", "ASUS", "ZTE", "ONEPLUS", "XIAOMI", "OPPO", "VIVO", "SONY", "REALME"][randint(0, 11)] + "; SM-T" + rnd + "; SM-T" + rnd + "; qcom; en_US; 545986"+str(randint(111,999))+")"   
        files=[
    ]
        headers = {
    }        
        try:
            response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers,files=files)
        except Exception as e:
            return e
        try:
            device_id = f"android-{secrets.token_hex(8)}",
            csrf = hashlib.md5(str(time.time()).encode()).hexdigest()
            mid = response.cookies["mid"]
            ig_did = response.cookies["ig_did"]
            ig_nrcb = response.cookies["ig_nrcb"]
            app = ''.join(choice('1234567890')for i in range(15))

        except Exception as f:""
        choice_ = choice("143")
        if choice_ == "1":
                data = {        'signed_body':'ef02f559b04e8d7cbe15fb8cf18e2b48fb686dafd056b7c9298c08f3e2007d43.{"_csrftoken":"dG4dEIkWvAWpIj1B2M2mutWtdO1LiPCK","adid":"5e7df201-a1ff-45ec-8107-31b10944e25c","guid":"b0382b46-1663-43a7-ba90-3949c43fd808","device_id":"android-71a5d65f74b8fcbc","query":"'f'{email}''"}',

            'ig_sig_key_version':'4',
        }	
                headers = {
            'X-Pigeon-Session-Id':'2b712457-ffad-4dba-9241-29ea2f472ac5',
            'X-Pigeon-Rawclienttime':'1707104597.347',
            'X-IG-Connection-Speed':'-1kbps',
            'X-IG-Bandwidth-Speed-KBPS':'-1.000',
            'X-IG-Bandwidth-TotalBytes-B':'0',
            'X-IG-Bandwidth-TotalTime-MS':'0',
            'X-IG-VP9-Capable':'false',
            'X-Bloks-Version-Id':'009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0',
            'X-IG-Connection-Type':'WIFI',
            'X-IG-Capabilities':'3brTvw==',
            'X-IG-App-ID':'567067343352427',
            'User-Agent':str(user_agent.generate_user_agent()),
            'Accept-Language':'ar-IQ, en-US',
            'Cookie':'mid=Zbu4xQABAAE0k2Ok6rVxXpTD8PFQ; csrftoken=dG4dEIkWvAWpIj1B2M2mutWtdO1LiPCK',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept-Encoding':'gzip, deflate',
            'Host':'i.instagram.com',
            'X-FB-HTTP-Engine':'Liger',
            'Connection':'keep-alive',
            'Content-Length':'364',
        }
                try:
                    re = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',headers=headers,data=data)
                    if ('"can_recover_with_code"')in re.text:
                        return {"data":{"status":True,"programmer":"@ii33cc"}}
                    elif "ip"in re.text:
                        return  {"data":{"status":"ip_block run vpn or use proxy","programmer":"@ii33cc"}}            	             
                    else:
                        return {"data":{"status":False,"programmer":"@ii33cc"}}
                except Exception as e:""    
        elif choice_ == "3":
                url = 'https://www.instagram.com/api/v1/web/accounts/check_email/'
                headers = {	
                'Host': 'www.instagram.com',
                'origin': 'https://www.instagram.com',
                'referer': 'https://www.instagram.com/accounts/signup/email/',	
                'sec-ch-ua-full-version-list': '"Android WebView";v="119.0.6045.163", "Chromium";v="119.0.6045.163", "Not?A_Brand";v="24.0.0.0"',
                'user-agent': str(user_agent)}
                data = {
            'email': str(email)
            }
                try:
                    response = requests.post(url,headers=headers,data=data)
                    if 'email_is_taken' in response.text:
                        return {"data":{"status":True,"programmer":"@ii33cc"}}
                    elif '"spam":true' or "Please wait a few minutes before you try again"in response.text:
                        return  {"data":{"status":"ip_block run vpn or use proxy","programmer":"@ii33cc"}}
                    else:
                        return {"data":{"status":False,"programmer":"@ii33cc"}}
                except Exception as e:
                    ""
        elif choice_ == "4":
                url='https://i.instagram.com/api/v1/accounts/create/'
                headers={
                'Host': 'i.instagram.com',
                'cookie': f'mid={mid}',
                'x-ig-capabilities': 'AQ==',
                'cookie2': '$Version=1',
                'x-ig-connection-type': 'WIFI',
                'user-agent': "Instagram 136.0.0.34.124 Android (24/7.0; 640dpi; 1440x2560; HUAWEI; LON-L29; HWLON; hi3660; en_US; 208061712)",
                'content-type': 'application/x-www-form-urlencoded',
                'content-length': '159'
                }
                data={
    'password':'Topython',
    'device_id':str(uuid.uuid4()),
    'guid':str(uuid.uuid4()),
    'email': str(email),
    'username':email,}
                try:
                    response = requests.post(url,headers=headers,data=data)
                    if "Another account is using the same email" in response.text:
                    
                        return {"data":{"status":True,"programmer":"@ii33cc"}}
                    elif "ip" or "Please wait a few minutes before you try again" in response.text:
                        return {"data":{"status":"ip_block run vpn or use proxy","programmer":"@ii33cc"}}
                    else:
                        return {"data":{"status":False,"programmer":"@ii33cc"}}
                except Exception as e:""

#"spam":true

    @staticmethod
    def generateUsername2011() -> str:
        try:
            import requests
            import string
            import random
            import json
        except ImportError:
            li=["requests","user_agent"]
            import os
            for o in li:
                os.system("pip install {}".format(o))
        data = {
            "lsd": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "variables": json.dumps({"id": int(random.randrange(10000, 17699999)), "render_surface": "PROFILE"}),
            "doc_id": "25618261841150840"
        }
        try:
            response = requests.post(
                "https://www.instagram.com/api/graphql",
                headers={"X-FB-LSD": data["lsd"]},
                data=data
            )
            username = response.json().get('data', {}).get('user', {}).get('username')
            fol= response.json().get("data",{}).get("user",{}).get("follower_count")
            return {"data":{"message":"ok","username":username,"follower_count":fol,"programmer":"@ii33cc"}}
        except:
            return{"data":{"Errur":"try agin"}}
    @staticmethod
    def generateUsername2012() -> str:
        try:
            import requests
            import string
            import random
            import json
        except ImportError:
            li=["requests","user_agent"]
            import os
            for o in li:
                os.system("pip install {}".format(o))
        data = {
            "lsd": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "variables": json.dumps({"id": int(random.randrange(17699999, 263014407)), "render_surface": "PROFILE"}),
            "doc_id": "25618261841150840"
        }
        try:
            response = requests.post(
                "https://www.instagram.com/api/graphql",
                headers={"X-FB-LSD": data["lsd"]},
                data=data
            )
            username = response.json().get('data', {}).get('user', {}).get('username')
            fol= response.json().get("data",{}).get("user",{}).get("follower_count")
            return {"data":{"message":"ok","username":username,"follower_count":fol,"programmer":"@ii33cc"}}
        except:
            return{"data":{"Errur":"try agin"}}
    @staticmethod
    def generateUsername2013() -> str:
        try:
            import requests
            import string
            import random
            import json
        except ImportError:
            li=["requests","user_agent"]
            import os
            for o in li:
                os.system("pip install {}".format(o))
        data = {
            "lsd": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "variables": json.dumps({"id": int(random.randrange(263014407, 361365133)), "render_surface": "PROFILE"}),
            "doc_id": "25618261841150840"
        }
        try:
            response = requests.post(
                "https://www.instagram.com/api/graphql",
                headers={"X-FB-LSD": data["lsd"]},
                data=data
            )
            username = response.json().get('data', {}).get('user', {}).get('username')
            fol= response.json().get("data",{}).get("user",{}).get("follower_count")
            return {"data":{"message":"ok","username":username,"follower_count":fol,"programmer":"@ii33cc"}}
        except:
            return{"data":{"Errur":"try agin"}}
    @staticmethod
    def generateUsername() -> str:
        try:
            import requests
            import string
            import random
            import json
        except ImportError:
            li=["requests","user_agent"]
            import os
            for o in li:
                os.system("pip install {}".format(o))
        data = {
            "lsd": ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            "variables": json.dumps({"id": int(random.randrange(361365133, 1629010000)), "render_surface": "PROFILE"}),
            "doc_id": "25618261841150840"
        }
        try:
            response = requests.post(
                "https://www.instagram.com/api/graphql",
                headers={"X-FB-LSD": data["lsd"]},
                data=data
            )
            username = response.json().get('data', {}).get('user', {}).get('username')
            fol= response.json().get("data",{}).get("user",{}).get("follower_count")
            return {"data":{"message":"ok","username":username,"follower_count":fol,"programmer":"@ii33cc"}}
        except:
            return{"data":{"Errur":"try agin"}}
    @staticmethod
    def generateUsername():
        try:
            import random
            import requests
            import user_agent
        except:
            k=["requests","user_agent"]
            for l in k:
                import os
                os.system("pip install {}".format(l))
        g=random.choice(
            [
                'azertyuiopmlkjhgfdsqwxcvbn', 
                'azertyuiopmlkjhgfdsqwxcvbn',
                'azertyuiopmlkjhgfdsqwxcvbn',
                'azertyuiopmlkjhgfdsqwxcvbn',
                'azertyuiopmlkjhgfdsqwxcvbn',
                'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',  
                'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',
                'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',
                
'abcdefghijklmnopqrstuvwxyzéèêëàâäôùûüîïç',                'abcdefghijklmnopqrstuvwxyzñ',  
                'abcdefghijklmnopqrstuvwxyzñ',
                'abcdefghijklmnopqrstuvwxyzñ',
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',  
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
                'абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
                '的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之',  
                '的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之',
                '的一是不了人我在有他这为之大来以个中上们到说时国和地要就出会可也你对生能而子那得于着下自之',
                'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン',  
                'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン',
                'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん', 
                'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん',
                'אבגדהוזחטיכלמנסעפצקרשת',
                'אבגדהוזחטיכלמנסעפצקרשת',
                'αβγδεζηθικλμνξοπρστυφχψω',  
                'αβγδεζηθικλμνξοπρστυφχψω',
                'abcdefghijklmnopqrstuvwxyzç', 
                'abcdefghijklmnopqrstuvwxyzç',
                'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤฤลฦวศษสหฬอฮ',  
                'กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรฤฤลฦวศษสหฬอฮ',
                'अआइईउऊऋएऐओऔअंअःकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ',  
                'अआइईउऊऋएऐओऔअंअःकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञ',
            ]

        )
        keyword=''.join((random.choice(g) for i in range(random.randrange(4,9))))
        cookies = {
            'rur': '"LDC\\05467838469205\\0541758153066:01f72be7578ed09a57bfe3e41c19af58848e0e965e0549f6d1f5a0168a652d2bfa28cd9a"',
        }

        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'sec-ch-ua-full-version-list': '"Chromium";v="128.0.6613.138", "Not;A=Brand";v="24.0.0.0", "Google Chrome";v="128.0.6613.138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(user_agent.generate_user_agent()),
            'x-asbd-id': '129477',
            'x-bloks-version-id': '235c9483d007713b45fc75b34c76332d68d579a4300a1db1da94670c3a05089f',
            'x-csrftoken': 'mf3zd6qWxnKgh9BaNRI5Ldpms2NrH62X',
            'x-fb-friendly-name': 'PolarisSearchBoxRefetchableQuery',
            'x-fb-lsd': 'BslibIYRWxn19hyIaPyrZV',
            'x-ig-app-id': '936619743392459',
        }

        data = {
            'variables': '{"data":{"context":"blended","include_reel":"true","query":"'+keyword+'","rank_token":"","search_surface":"web_top_search"},"hasQuery":true}',
            'doc_id': '7935512656557707',
        }
        try:
            response = requests.post('https://www.instagram.com/graphql/query', cookies=cookies, headers=headers, data=data).json()['data']['xdt_api__v1__fbsearch__topsearch_connection']['users']
            for i in response:
                us=i['user']['username']
                return {"data":{"message":"ok","username":us,"programmer":"@ii33cc"}}
        except:
            return{"data":{"Errur":"try agin"}}
    @staticmethod
    def Reset(email):
        try:
            import requests
            import user_agent
        except:
            o=["requests","user_agent"]
            for i in o:
                import os
                os.system("pip install {}".format(i))
        data = {
        'signed_body':'ef02f559b04e8d7cbe15fb8cf18e2b48fb686dafd056b7c9298c08f3e2007d43.{"_csrftoken":"dG4dEIkWvAWpIj1B2M2mutWtdO1LiPCK","adid":"5e7df201-a1ff-45ec-8107-31b10944e25c","guid":"b0382b46-1663-43a7-ba90-3949c43fd808","device_id":"android-71a5d65f74b8fcbc","query":"'f'{email}''"}',

        'ig_sig_key_version':'4',
    }	
        headers = {
        'X-Pigeon-Session-Id':'2b712457-ffad-4dba-9241-29ea2f472ac5',
        'X-Pigeon-Rawclienttime':'1707104597.347',
        'X-IG-Connection-Speed':'-1kbps',
        'X-IG-Bandwidth-Speed-KBPS':'-1.000',
        'X-IG-Bandwidth-TotalBytes-B':'0',
        'X-IG-Bandwidth-TotalTime-MS':'0',
        'X-IG-VP9-Capable':'false',
        'X-Bloks-Version-Id':'009f03b18280bb343b0862d663f31ac80c5fb30dfae9e273e43c63f13a9f31c0',
        'X-IG-Connection-Type':'WIFI',
        'X-IG-Capabilities':'3brTvw==',
        'X-IG-App-ID':'567067343352427',
        'User-Agent':str(user_agent.generate_user_agent()),
        'Accept-Language':'ar-IQ, en-US',
        'Cookie':'mid=Zbu4xQABAAE0k2Ok6rVxXpTD8PFQ; csrftoken=dG4dEIkWvAWpIj1B2M2mutWtdO1LiPCK',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'i.instagram.com',
        'X-FB-HTTP-Engine':'Liger',
        'Connection':'keep-alive',
        'Content-Length':'364',
    }
        res = requests.post('https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/',headers=headers,data=data)
        print(res.text)
        if ('"can_recover_with_code"')in res.text:
            sdd=res.json()["email"]
            return {"data":{"status":True,"email_or_user":email,"reset":sdd,"programmer":"@ii33cc"}}
        elif "user_not_found"in res.text:
            return {"data":{"status":True,"email_or_user":email,"reset":"user_not_found","programmer":"@ii33cc"}} 	       
        elif "ip" or "Please wait a few minutes before you try again"in  res.text:  
            return {"data":{"status":False,"result":"ip block run vpn or use proxy","programmer":"@ii33cc"}} 	 
        else:
            return {"data":{"status":None,"email_or_user":email,"reset":None,"programmer":"@ii33cc"}}
    @staticmethod
    def GetData(Id):
        try:
            if int(Id) >1 and int(Id)<1279000:
                d= 2010
            elif int(Id)>1279001 and int(Id)<17750000:
                d= 2011
            elif int(Id) > 17750001 and int(Id)<279760000:
                d= 2012
            elif int(Id)>279760001 and int(Id)<900990000:
                d= 2013
            elif int(Id)>900990001 and int(Id)< 1629010000:
                d= 2014
            elif int(Id)>1900000000 and int(Id)<2500000000:
                d= 2015
            elif int(Id)>2500000000 and int(Id)<3713668786:
                d= 2016
            elif int(Id)>3713668786 and int(Id)<5699785217:
                d= 2017
            elif int(Id)>5699785217 and int(Id)<8507940634:
                d= 2018
            elif int(Id)>8507940634 and int(Id)<21254029834:
                d= 2019
            else:
                d= "2020-2025"
            return {"message":{"status":True,"data":d,"programmer":"@ii33cc"}}
        except:
            return {"message":{"status":False,"data":False,"programmer":"@ii33cc"}}
    @staticmethod
    def loginweb(username,password):
        try:
            import requests
            import time
            import user_agent
        except:
            p=["requests","time","user_agent"]
            for i in p:
                import os
                os.system("pip install {}".format(i))
        a=str(time.time()).split(".")[1]
        headers = {
            'accept': '*/*',
            'accept-language': 'ar,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.instagram.com',
            'priority': 'u=1, i',
            'referer': 'https://www.instagram.com/',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Microsoft Edge";v="133.0.3065.92", "Chromium";v="133.0.6943.142"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': str(user_agent.generate_user_agent()),
            'x-asbd-id': '359341',
            'x-csrftoken': 'JwprPHIEz6Ay9speTWqA0wCqFw9hHARt',
            'x-ig-app-id': '936619743392459',
            'x-ig-www-claim': '0',
            'x-instagram-ajax': '1020778632',
            'x-requested-with': 'XMLHttpRequest',
            'x-web-session-id': 'rhcefi:mkhs1v:b6t13o',
        }
        data = {
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{a}:{password}',
            'caaF2DebugGroup': '0',
            'loginAttemptSubmissionCount': '0',
            'optIntoOneTap': 'false',
            'queryParams': '{}',
            'trustedDeviceRecords': '{}',
            'username': username,
        }

        response = requests.post('https://www.instagram.com/api/v1/web/accounts/login/ajax/', headers=headers, data=data)
        if "userId" and '"authenticated":true' in response.text:
            ses=response.cookies.get_dict()['sessionid']
            return {"data":{"status":True,"username":username,"paswerd":password,"login":True,"sessionId":ses,"programmer":"@ii33cc"}}
        elif '{"user":true,"authenticated":false,"error_type":"UserInvalidCredentials","status":"ok"}'in response.text:
            return {"data":{"status":True,"username":username,"paswerd":password,"login":"bad_password","programmer":"@ii33cc"}}
        elif "two_factor_required"in response.text:
            return {"data":{"status":True,"username":username,"paswerd":password,"login":"two_factor_required","programmer":"@ii33cc"}}
        elif "challenge_required" or "checkpoint_required"in response.text:
            return {"data":{"status":True,"username":username,"paswerd":password,"login":"sceure","programmer":"@ii33cc"}}
        elif '"spam":true'or "ip" or "Please wait a few minutes before you try again"in response.text:
            return {"data":{"status":False,"username":username,"paswerd":password,"login":"ip block run vpn or use proxy","programmer":"@ii33cc"}}
        else:
            return response.text
