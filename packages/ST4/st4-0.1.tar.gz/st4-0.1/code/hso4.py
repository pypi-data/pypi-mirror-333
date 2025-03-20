#by hso
class HOTMAIL:
    @staticmethod
    def CheckEmail(email):
        if not "@"in email:
            return {"data":{"status":None,"message":"use @hotmail.com or @outlook.com in email","error_code":3,"programmer":"@ii33cc"}}
        import requests,re
        reqz=requests.Session()
        try:
            headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            "Host": "signup.live.com",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
            }
            url="https://signup.live.com/signup.aspx?lic=1"
            response=reqz.get(url, headers=headers)
            apiCanary = re.search("apiCanary\":\"(.+?)\",", str(response.content)).group(1)
            apiCanary = str.encode(apiCanary).decode("unicode_escape").encode("ascii").decode("unicode_escape").encode("ascii").decode("ascii");url  = "https://signup.live.com/API/CheckAvailableSigninNames";json = {
            "signInName": email,
            "includeSuggestions": True}
            res = reqz.post(url, headers={
            "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
            "canary":apiCanary
            }, json=json)
            if res.json()['isAvailable']==False:
                return {"data":{"status":False,"email":email,"error_code":0,"programmer":"@ii33cc"}}
            


            elif res.json()['isAvailable']==True:



                return {"data":{"status":True,"email":email,"error_code":1,"programmer":"@ii33cc"}}
        except:""
