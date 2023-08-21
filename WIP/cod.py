from cod_api import API, platforms
from dotenv import *
import os
import json

load_dotenv()
COD_TOKEN = os.getenv('COD_TOKEN')

api = API()

# print out the docstring
# print(api.ModernWarfare2.__doc__)

tamalego = 'tamalego#4116726'
khalos = 'Khalos#8742155'

"""
Your sso token can be found by longing in at callofduty, opening dev tools (ctr+shift+I), going to Applications > Storage > Cookies > 
https://callofduty.com, filter to search 'ACT_SSO_COOKIE' and copy the value.
"""
#https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/uno/gamer/tamalego%234116726/profile/type/mp
async def get_kd(username):
    api.login(COD_TOKEN)
    #bd = api.ModernWarfare.breakdown(platforms.Activision, 'tamalego#4116726')
    obj = await api.ModernWarfare.fullDataAsync(platforms.Activision, username)
    obj = obj['data']['lifetime']['all']['properties']['kdRatio']
    return obj

if __name__ == "__main__":
    user = tamalego

    api.login(COD_TOKEN)
    #bd = api.ModernWarfare.breakdown(platforms.Activision, 'tamalego#4116726')
    #obj = api.ModernWarfare.fullData(platforms.All, user)
    #obj = obj['data']['lifetime']['all']['properties']['kdRatio']
    #print(obj)
    obj = api.ModernWarfare2.breakdown(platforms.Activision, user)
    print(obj)