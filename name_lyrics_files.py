import sys
import os
import codecs
from db_utils import *

def main():
    if len(sys.argv) < 3:
        print("Please specify input and output directories")
        return

    songs_dir = sys.argv[1]
    output_dir_name = sys.argv[2]
    conn = db_connect()
    try:
        directory = os.fsencode(songs_dir)
    except (FileNotFoundError, IOError):
        print("No such directory", songs_dir)
        return

    try:
        output_dir = os.fsencode(output_dir_name)
    except (FileNotFoundError, IOError):
        print("No such directory", output_dir)
        return

    for file in os.listdir(directory):

        file_path = os.path.join(directory, file)
        with codecs.open(file_path, "r", encoding='utf-8', errors='replace') as data:
            raw_text = data.read()

        file_uuid = file.decode("utf-8")[:-4]
        title,artist = get_song_name_author_byid(conn,file_uuid)
        m = map(lambda x: x.lower() if x.isalpha() or x.isdigit() else '_', title)
        # convert from list of letters to string
        title = "".join(list(m))
        m = map(lambda x: x.lower() if x.isalpha() else '_', artist)
        # convert from list of letters to string
        artist = "".join(list(m))
        song_name = title+artist
        output_file_path = output_dir_name +"/" + song_name +".txt"
        output = open(output_file_path,"w", encoding='utf-8', errors='replace')
        output.write(raw_text)


if __name__ == "__main__":
    main()