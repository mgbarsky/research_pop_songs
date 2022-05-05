import requests
from bs4 import BeautifulSoup
import sys
import linecache
import datetime
import pprint
import uuid
import pickle

'''
This program takes in a list of countries and scraps the information about the top 20
rated songs based on the website top40-charts.com. It outputs the dictionary all_songs
as text file.
The most popular digital singles on the Web compiled from an internet sample
by Top Internet Singles Downloads/Sales from providers/sites:
iTunes Apple, Amazon, ArtistDirect, EBay.
The chart provided by Top40-Charts.com every Saturday.
'''

#dict with key being name and artist of songs and value being a list[UUID, artist_id, country, rank_in_that_country]
global all_songs
#dict with key being each artist and value being an id of the artist
global artists_id_dict
#int that represents the artist id
global artist_id
#dict with key being each country and value being a list[country_id, country_chart_date]
global country_chart_info


'''
Iterate through all charts that are of a country in the input file.
'''
def get_all_charts(soup, country_file):
    global country_chart_info
    chart_links = soup.find_all("select", {"name": "cid"})
    line_num = 1
    for link in chart_links:
        for i in range(len(link.contents)):
            cid = link.contents[i]
            cid_num = cid.get("value")
            url = "http://top40-charts.com/chart.php?cid="+ str(cid_num)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, "html.parser")
            country = linecache.getline(country_file, line_num)
            country = linecache.getline(country_file, line_num).replace('\n', '')
            if str(country) not in str(cid.text.replace(u'\xa0', ' ').encode("ascii")):
                continue
            elif str(country) == '': continue
            else:
                date = soup.find("select", {"name": "date"}).contents[-1].text
                country_chart_info.update({str(country): [int(cid_num), date]})
                #get each song in the chart
                song_box = soup.find_all("tr", {"class": "latc_song"})
                get_names_artists_ranks(song_box, country)
                line_num += 1
    return all_songs


'''
Scrap information for each song, assign each song with an UUID, and update all_songs.
'''
def get_names_artists_ranks(song_box, country):
    global all_songs, artists_id_dict, artist_id
    rank = 0
    top = 1
    for song in song_box:
        if top <= 20:
            temp = song.find_all("b")
            for i in temp:
                if i.find_all("a") == []:
                    rank += 1
                else:
                    names = i.find_all("a")
                    for n in names:
                        name = str(n.text.replace(u'\xa0', ' '))
                        if n != None:
                            artist = str(n.find_next("a").text.replace(u'\xa0', ' '))
                            if (name, artist) in all_songs.keys():
                                all_songs[(name, artist)].append(country)
                                all_songs[(name, artist)].append(rank)
                            else:
                                if artist in artists_id_dict:
                                    all_songs.update({(name, artist): [uuid.uuid4(), artists_id_dict[artist], country, rank]})
                                else:
                                    artists_id_dict.update({artist: artist_id})
                                    all_songs.update({(name, artist): [uuid.uuid4(), artists_id_dict[artist], country, rank]})
                                    artist_id += 1
            top += 1


'''
Output the dictionary all_songs
'''
def output_file(dict_name, details):
    global all_songs
    #output the pickle version of all_songs
    with open(str(datetime.datetime.today().strftime('%Y-%m-%d')) + details + '_pickle.txt', 'wb') as handle:
        pickle.dump(dict_name, handle)

    #output all_songs in a form that is easy to read
    orig_stdout = sys.stdout
    f = open(str(datetime.datetime.today().strftime('%Y-%m-%d')) + details + '.txt', 'w')
    sys.stdout = f

    pprint.pprint(dict_name)

    sys.stdout = orig_stdout
    f.close()


if __name__ == "__main__":
    global all_songs, artists_id_dict, artist_id, country_chart_info
    all_songs = {}
    artists_id_dict = {}
    artist_id = 0
    country_chart_info = {}
    url = "http://top40-charts.com/chart.php?cid=16"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    get_all_charts(soup, sys.argv[1])
    output_file(all_songs, "songs_info")
    output_file(country_chart_info, "charts_info")
