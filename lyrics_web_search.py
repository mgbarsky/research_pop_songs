import os
import sys
import time
import string
import pprint
import pickle
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

'''
This program uses Selenium and Chrome driver. It takes in the dictionary created by
scrap_top_charts.py (pickle version), and search for lyrics of songs based on the
infomation in the given dictionary. It can output all the lyrics as text files with
file name being either the UUID of the song, or the name and artist of the songs.
It also outputs the two dictionaries - google_lyrics and country_sum - as text files.

As of 20180601, success = 249, total number of songs = 317
'''

#dict with key being name and artist of songs and value being a list[0/1, UUID]
#0 indicates the lyrics for the song is not found and 1 indicates can be found
global google_lyrics
#dict with key being name and artist of songs and value being a list[UUID, country, rank_in_that_country]
global all_songs
#number of songs that lyrics are found
global success
#dict with key being countries and value being the number of songs which lyrics cannot be found
global country_sum


'''
Read the dictionary created by scrap_top_charts.py. Initialize google_lyrics, set the first
element in the value list to be 0.
'''
def read_as_dict():
    global all_songs, google_lyrics
    with open(sys.argv[1], 'rb') as handle:
        all_songs = pickle.loads(handle.read())
    for key in all_songs.keys():
        google_lyrics.update({key:[0, all_songs[key][0]]})


'''
Performs a google search with the name and artist of the song. Scrap lyrics if it's the top resultself.
Otherwise, click on the website Genius Lyrics if applicable.
'''
def google_search():
    global google_lyrics, success
    success = 0
    count = 0

    for key in google_lyrics.keys():

        #restarts driver once every 50 searches
        if count%50 == 0:
            if count != 0:
                driver.close()
            capa = DesiredCapabilities.CHROME
            capa["pageLoadStrategy"] = "none"
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            # chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
            #this is the headless version, Chrome window will not jump out
            driver = webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=capa)
            #use this driver when debugging, Chrome window will jump out
            # driver = webdriver.Chrome(desired_capabilities=capa)
        count += 1
        print(count)
        #get the input ready for google search
        translator = str.maketrans('', '', string.punctuation)
        newKey = str(key).translate(translator).replace(" ", "+").replace("++", "+")
        input = newKey+"+lyrics"
        url = "https://www.google.com/search?q="+input+"&rlz=1C5CHFA_enUS763US768&oq="+input+"&aqs=chrome..69i57.6636j0j1&sourceid=chrome&ie=UTF-8"
        driver.get(url)
        time.sleep(2)
        #see if lyrics is the top result, if not, try Genius
        try:
            driver.find_element_by_class_name("kp-header")
        except NoSuchElementException:
            genius_search(driver, key)
            continue
        #click on the expansion button to show full lyrics
        try:
            element = driver.find_element_by_xpath('//div[@data-fbevent="fastbutton"]')
        except NoSuchElementException:
            genius_search(driver, key)
            continue

        element.click()
        time.sleep(1)
        #scrap the lyrics
        try:
            lyrics = driver.find_element_by_class_name("Kvw2ac").text
            # .encode('ascii')
        except NoSuchElementException:
            genius_search(driver, key)
            continue

        time.sleep(0.1)
        #output lyrics with file name being name and artist of song
        # output_file(str(key).encode('utf-8'), lyrics, False, "lyricsNameArtist")
        #output lyrics with filename being UUID of song
        output_file(str(google_lyrics[key][1]), lyrics, False, "lyricsUUID")
        #update dict
        google_lyrics[key][0] = 1
        success += 1
    print ("Found", str(success), "out of", str(len(google_lyrics)), "songs")
    driver.quit()


'''
When Google search fails, see if the website Genius Lyrics is in the top three result
of the google search, results further down can be inaccurate.
'''
def genius_search(driver, key):
    global google_lyrics, success
    links = driver.find_elements_by_xpath("//div/h3/a")
    for i in range(len(links)):
        if i > 2: break
        link = links[i]
        if "Lyrics | Genius Lyrics" in link.text:
                driver.execute_script("arguments[0].click();", link)
                try:
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "section"))
                        )
                    driver.execute_script("window.stop();")
                except:
                    driver.refresh()

                time.sleep(1)

                try:
                    lyrics = driver.find_element_by_tag_name("section").text
                    # .encode("utf-8")
                except NoSuchElementException:
                    continue
                # output_file(str(key).encode('utf-8'), lyrics, False, "lyricsNameArtist")
                output_file(str(google_lyrics[key][1]), lyrics, False, "lyricsUUID")
                google_lyrics[key][0] = 1
                success += 1
                break
    return


'''
Update country_sum dict based on the google search results. The higher the value,
the more songs that lyrics cannot be found. Success rate can be calculated by
value/20.
'''
def summary_lyrics():
    global google_lyrics, all_songs, country_sum
    for key in google_lyrics.keys():
        if google_lyrics[key][0] == 0:
            for i in range(len(all_songs[key])):
                if i != 0 and i%2 == 0:
                    if all_songs[key][i] not in country_sum.keys():
                        country_sum.update({all_songs[key][i]: 1})
                    else:
                        country_sum[all_songs[key][i]] += 1
    output_file('lyrics_results', google_lyrics, True, None)
    output_file('summary_by_country', country_sum, True, None)


'''
Output lyrics and dictionaries as text files in designated directories.
'''
def output_file(fileName, content, pretty, newDir):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if newDir != None:
        dest_dir = os.path.join(script_dir, 'lyricsSearchResults', newDir)
    else:
        dest_dir = os.path.join(script_dir, 'lyricsSearchResults')
    try:
        os.makedirs(dest_dir)
    except OSError:
        pass
    path = os.path.join(dest_dir, fileName)
    orig_stdout = sys.stdout
    f = open(path + '.txt', 'w',encoding='utf-8', errors='replace')
    sys.stdout = f
    if pretty == False:
        print (content)
    else:
        pprint.pprint(content)
    sys.stdout = orig_stdout
    f.close()
    if fileName == 'lyrics_results':
        with open(path + '_pickle.txt', 'wb') as handle:
            pickle.dump(google_lyrics, handle)


if __name__ == "__main__":
    global google_lyrics, all_songs, country_sum
    google_lyrics = {}
    all_songs = {}
    country_sum = {}
    read_as_dict()
    google_search()
    summary_lyrics()
