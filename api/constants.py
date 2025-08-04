# api/constants.py

# Base URLs
BASE_URL = "https://howlongtobeat.com"
SEARCH_ENDPOINT = "/api/seek/5e05cccac2c36e68"  # Note: This hash may change
GAME_DETAILS_ENDPOINT = "/_next/data/{build_id}/game/{game_id}.json"

# Build ID (will need to be dynamic eventually)
DEFAULT_BUILD_ID = "xIwqd28bXtKyx4Rz29__L"

# Headers for requests
HEADERS = {
   "accept": "*/*",
   "accept-language": "en-US,en;q=0.9",
   "content-type": "application/json",
   "origin": BASE_URL,
   "referer": f"{BASE_URL}/",
   "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

# Additional headers for game details endpoint
GAME_DETAILS_HEADERS = {
   **HEADERS,  # Include all base headers
   "x-nextjs-data": "1",
   "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
   "sec-ch-ua-mobile": "?0",
   "sec-ch-ua-platform": '"Windows"',
   "sec-fetch-dest": "empty",
   "sec-fetch-mode": "cors",
   "sec-fetch-site": "same-origin",
   "priority": "u=1, i"
}

# Cookies (GDPR/privacy consent - public data)
COOKIES = {
   "zdconsent": "optin",
   "OptanonAlertBoxClosed": "2025-07-27T18:56:50.330Z",
   "OTGPPConsent": "DBABLA~BVQqAAAAAAKA.QA",
   "usprivacy": "1YNY",
   "OptanonConsent": "isGpcEnabled=0&datestamp=Sat+Aug+02+2025+17%3A32%3A13+GMT%2B0530+(India+Standard+Time)&version=202507.1.0&browserGpcFlag=0&isIABGlobal=false&consentId=844dce7b-c212-4752-b3f6-af68f7f51429&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&GPPCookiesCount=1&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2COSSTA_BG%3A1&hosts=H36%3A1%2CH1%3A1%2CH2%3A1%2Clie%3A1%2CH4%3A1%2CH205%3A1%2CH185%3A1%2CH12%3A1%2CH283%3A1%2CH17%3A1%2CH18%3A1%2CH23%3A1%2CH26%3A1%2CH32%3A1%2CH35%3A1%2CH140%3A1%2CH38%3A1%2CH1191%3A1%2CH43%3A1%2CH1002%3A1%2CH45%3A1%2CH47%3A1%2CH290%3A1%2CH49%3A1%2CH51%3A1%2CH54%3A1%2CH57%3A1%2CH58%3A1%2CH198%3A1%2CH894%3A1%2CH66%3A1%2CH67%3A1%2CH1352%3A1%2CH73%3A1%2Cfgs%3A1%2CH78%3A1%2CH184%3A1%2CH298%3A1%2CH79%3A1%2CH83%3A1%2CH85%3A1%2CH302%3A1%2CH177%3A1%2CH86%3A1%2Cyyf%3A1%2CH89%3A1%2CH90%3A1%2CH547%3A1%2CH425%3A1%2CH970%3A1%2CH93%3A1%2CH94%3A1%2CH95%3A1%2CH657%3A1&genVendors=&intType=1&geolocation=IN%3BMH&AwaitingReconsent=false&gppSid=7"
}

# Default search options payload
DEFAULT_SEARCH_OPTIONS = {
   "games": {
       "userId": 0,
       "platform": "",
       "sortCategory": "popular",
       "rangeCategory": "main",
       "rangeTime": {"min": None, "max": None},
       "gameplay": {
           "perspective": "",
           "flow": "",
           "genre": "",
           "difficulty": ""
       },
       "rangeYear": {"min": "", "max": ""},
       "modifier": ""
   },
   "users": {"sortCategory": "postcount"},
   "lists": {"sortCategory": "follows"},
   "filter": "",
   "sort": 0,
   "randomizer": 0
}