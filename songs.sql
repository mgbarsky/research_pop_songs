DROP TABLE IF EXISTS songs;

CREATE TABLE songs
(uuid TEXT PRIMARY KEY,
 name TEXT,
 artist_id INT,
 lyrics INT);


DROP TABLE IF EXISTS ratings;

CREATE TABLE ratings
(uuid TEXT,
country_id INT,
rating INT,
chart_date INT,
PRIMARY KEY(uuid, country_id, chart_date));


DROP TABLE IF EXISTS countries;

CREATE TABLE countries
(country_id INT PRIMARY KEY,
 country_name TEXT);


 DROP TABLE IF EXISTS artists;

 CREATE TABLE artists
 (artist_id INT PRIMARY KEY,
  artist_name TEXT);

DROP TABLE IF EXISTS word_count;

  CREATE TABLE word_count
  (songUUID TEXT,
  word TEXT,
  frequency INT,
  PRIMARY KEY(songUUID, word));
