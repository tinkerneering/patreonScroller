#!/usr/bin/python
#
# patreonScroll.py 
# Written by Rob Clarke @ Tinkerneering.uk
#
# Connect to Patreon using the client credentials from the developer console
# obtain details on your primary campaign, 
# extract the users in that relationship then
# string their vanity names together into a thank you message.
#
import scrollphathd as sphd
import patreon
import json
import time

xcludeuser = 'tinkerneering'
access_token = '#### INSERT YOU CREATOR ACCESS KEY HERE ####'
api_client = patreon.API(access_token)

# Get the campaign ID
campaign_response = api_client.fetch_campaign()
campaign_id = campaign_response.data()[0].id()

list = ""
user_count=0

# Fetch all pledges
pledges = []
pledgesIncl = []
cursor = None
while True:
    pledges_response = api_client.fetch_page_of_pledges(campaign_id, 25, cursor=cursor)
    pledges += pledges_response.data()
    pledgesIncl += pledges_response._all_resource_json_data()

    sep = ""
    for i in pledgesIncl:
        if "relationships" in i:
            r = i["relationships"]
            if r:
                a = i["attributes"]
                if a:
                    t = i["type"]
                    if t == "user":
                       n = a["vanity"]
                       if n != xcludeuser:
                           list += sep + n
                           user_count += 1
                           sep = ",  "

    cursor = api_client.extract_cursor(pledges_response)
    if not cursor:
        break

msg = "   Thank you Patreons.   " + str(user_count) + " supporters : " + list
print msg

sphd.write_string(msg, brightness=0.3);

while True:
    sphd.show()
    sphd.scroll(1)
    time.sleep(0.02)

sphd.clear()
