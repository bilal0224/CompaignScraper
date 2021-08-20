import mechanicalsoup
from bs4 import BeautifulSoup
import json
import pprint
import argparse
from getpass import getpass
import random

def getKickStartData(proj_name,user_email,user_password):
    try:
        browser = mechanicalsoup.StatefulBrowser()

        browser.open(f"https://www.kickstarter.com/projects/imag1/{proj_name}/dashboard?ref=creator_nav")

        browser.select_form('form[action="/user_sessions"]')

        browser["user_session[email]"] = user_email
        browser["user_session[password]"] = user_password

        after_login = browser.submit_selected()
        soup = BeautifulSoup(after_login.text, 'html.parser')

        all_money = soup.find_all("span", class_="money")
        pleged, avg_pleged, pleged_via_kickstarter, pleged_via_external, pleged_via_custom = (money.text for money in all_money)

        top_page_stats = soup.find("div", class_="stats-numbers").find_all("h1")[1:]
        funded, backers, sec_to_go = (stat.text for stat in top_page_stats)

        project_followers_div = soup.find("div", class_="flex mr2").find_all("span",class_="block type-38 soft-black bold")
        proj_followers, converted_followers, conversion_rate = (follower.text for follower in project_followers_div)

        proj_video_plays = soup.find("h5", class_="stats_num").text

        project_id = json.loads(soup.find_all("div", attrs={'data-attrs' : True})[0]['data-attrs'])["projectId"]

#         refrerrers = browser.open(f"https://www.kickstarter.com/project_referrers/refs/stats?page=1&project_id={project_id}").json()

        return {
            "Pleged" : pleged,
            "average_Pleged" : avg_pleged,
            "pleged_via_kickstarter" : pleged_via_kickstarter,
            "pleged_via_external" : pleged_via_external,
            "pleged_via_custom" : pleged_via_custom,
            "funded" : funded,
            "backers" : backers,
            "sec_to_go" : sec_to_go,
            "proj_followers" : proj_followers,
            "converted_followers" : converted_followers,
            "conversion_rate" : conversion_rate,
            "proj_video_plays" : proj_video_plays,
            "project_id" : project_id,
#             "Referrers" : refrerrers
        }
    
    except Exception as e:
        return {
            "error" : e
        }

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Scrape Kickstarter Campaign Data')
    parser.add_argument('-c', '--campaign', type=str,help="The name of campaign from url like '2-in-1-wireless-charging-dock-and-power-bank' from dashboard url 'https://www.kickstarter.com/projects/imag1/2-in-1-wireless-charging-dock-and-power-bank/dashboard' ")
    parser.add_argument('-u', '--user', type=str,help="Kickstarter username, the account belongs to.")
    parser.add_argument('-p', '--password', type=str,help="Password for the kickstarter account, you can also enter hidden if you don't use this flag.")

    args = parser.parse_args()

    if not args.campaign:
        parser.error("Campaign Url required.")

    if not args.user:
        parser.error("User name required.")

    if not args.password:
        args.password = getpass("Enter Password: ")

    data = getKickStartData(args.campaign,args.user,args.password)

    pprint.pprint(data)

    filename = f"run_{random.randint(1000,10000)}.json"

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("\n\n")
    pprint.pprint(f"Output saved in {filename}!")
