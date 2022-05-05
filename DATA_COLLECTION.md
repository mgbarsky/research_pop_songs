
# Data generation pipeline
### 1. Scrap top40 web site
Python script <em>scrap_top_charts.py</em>
scraps top40-charts.com for information about top 20 songs
in each country's top chart
and outputs four files in total, for example
for August 18, 2018 run:
<ol>
<li><em>2018-08-18charts_info.txt</em>: contains date when chart was compiled.</li>
<li><em>2018-08-18charts_info_pickle.txt</em>: binary version of dictionary 1.</li>
<li><em>2018-08-18songs_info.txt</em>: each song with unique id, and the place in charts of different countries.</li>
<li><em>2018-08-18songs_info_pickle.txt</em>: binary version of dictionary 3.</li>
</ol>

run:
<pre><code>python scrap_top_charts.py countries.txt</code></pre>


### 2. Search the web for song lyrics
<em>lyrics_web_search.py</em> takes
in <em>2018-08-18songs_info_pickle.txt</em> created
by <em>scrap_top_charts.py</em>,
and searches for lyrics of songs on Google
based on the information
in the given dictionary.
It outputs all the lyrics as text files
in folder lyricsSearchResults/lyricsUUID,
with file name being the UUID of the song.
It also outputs two dictionaries - lyrics_results.txt
(with the corresponding pickle version),
and summary_by_country.txt - as text files.
summary_by_country.txt contains number of songs per country,
for which lyrics was not found. The number of songs per country
can be estimated by subtracting this number from 20.

run:
<pre><code>python lyrics_web_search.py 2018-08-18songs_info_pickle.txt</code></pre>


### 3. Translation
All the lyrics files are uploaded to a google drive folder
and the google script is run to translate
each song into English.
The Translated songs replace the original songs in the folder.
The folder is then downloaded to the program directory and
serves as an input for word analysis.
Note: the files in this folder need to be converted to the plain text format.
For MAC users: From the terminal, run:
<pre>
<code>
textutil -convert txt /folder/path/*.docx
find /folder/path -name '*.docx' -delete
</code>
</pre>
For Windows users: The VBA script is located in a Microsoft document
Macro_from_docx_to_txt.docm. Open the document,
add developer tab, open Visual Basic editor,
and run the script by selecting directory of translated docx files,
then remove all *.docx files, leaving *.txt


### 4. Creating sqlite database

Run script <em>create_empty_db.py</em> to create songs.db.
It will either create a new database or replace
existing tables with empty tables.

Run:
<pre>
<code>
python create_empty_db.py
</code>
</pre>


### 5. Populate tables

Run script populate_data.py to populate database
tables. The script input files are pickle files
created in step 2.

Run:
<pre>
<code>
python populate_data.py 2018-08-18songs_info_pickle.txt
2018-08-18charts_info_pickle.txt lyrics_results_pickle.txt
</code>
</pre>


### 6. Create full vocabulary of words
Run script song_vocabulary.py, which will
parse each txt lyrics file in a given directory, clean it from non-alpha
characters, and generate file research_vocabulary.csv,
containing all song words minus stop words from song_stop_words.csv,
tested against english dictionary and lemmatized.

Run:
<pre>
<code>
python song_vocabulary.py 20180818_translated
</code>
</pre>


### 7. Insert song words into db
Run script insert_words.py with the input folder of translated songs as a parameter.
This parses each txt lyrics file in the same way as in step 6,
checks the parsed words against words in research_vocabulary.csv
and for each song, adds the following record to
the table word_count: (songUUID, word, count)

Run:
<pre>
<code>
python insert_words.py 20180818_translated
</pre>
</code>