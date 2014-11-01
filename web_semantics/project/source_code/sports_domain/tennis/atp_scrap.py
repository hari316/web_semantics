__author__ = 'Hari'
import requests
import bs4
from collections import OrderedDict
import re
import json


root_url = 'http://www.atpworldtour.com'
player_ranking = root_url + '/Rankings/Singles.aspx'


def web_scrap():

    response = requests.get(player_ranking)

    soup = bs4.BeautifulSoup(response.text)
    results = [(profile.get_text().encode('utf-8').replace('\xc2\xa0', ' '), profile.attrs.get('href'))
               for profile in soup.select('td.first a[href^=/Tennis]')]

    players = OrderedDict()
    name = dict()

    result = results[2]

    val = result[0].split(',')
    url = result[1]
    player_dict = {}
    name['firstname'] = val[1].strip()
    name['lastname'] = val[0].strip()
    player_id = val[1].strip().lower()+val[0].strip().lower()
    player_dict['fullname'] = name
    player_dict['url'] = url
    player_dict['bio_data'] = get_player_details(url)
    players[player_id] = player_dict

    # for result in results:
    #     val = result[0].split(',')
    #     url = result[1]
    #     player_dict = {}
    #     name['firstname'] = val[1].strip()
    #     name['lastname'] = val[0].strip()
    #     player_id = val[1].strip().lower()+val[0].strip().lower()
    #     player_dict['fullname'] = name
    #     player_dict['url'] = url
    #     player_dict['bio_data'] = get_player_details(url)
    #     players[player_id] = player_dict

    print players.keys()
    print players['rafaelnadal']['bio_data'].keys()


def get_player_details(player_url):

    response = requests.get(root_url+player_url)
    soup = bs4.BeautifulSoup(response.text)
    #p = s.select('div#playerBioInfoCardMain')
    bio_info = soup.select('ul#playerBioInfoList > li')
    player_bio = dict()
    info_details = [info.get_text().encode('utf-8') for info in bio_info]
    for detail in info_details:
        data = detail.split(':')
        player_bio[data[0].strip().lower()] = ''.join(data[1:]).strip()

    # Personal History.
    player_history = soup.select('div#personal')
    player_bio['history'] = player_history[0].get_text().encode('utf-8')

    # Player ranking.
    rank = soup.select('div#playerBioInfoRank > span')
    player_bio['ranking'] = rank[0].get_text()

    # Player titles.
    title_url = [player_title.attrs.get('href').encode('utf-8')
                 for player_title in soup.select('li#playerBionav_finals a[href^=/Tennis/Players/Top-Players]')]
    player_title_url = root_url+title_url[0]
    print player_title_url
    #player_bio['titles'] = get_title_details(player_title_url)

    return player_bio

def get_title_details(player_title_url):

    response = requests.get(player_title_url)
    soup = bs4.BeautifulSoup(response.text)
    titles = soup.select('h5.profileSecondaryTitle')
    print titles[0].text
    r = re.search(r'\(\*\)', titles[0].text, re.M|re.I)
    print r.group()
    return player_title_url

if __name__ == '__main__':

    web_scrap()