import xml.etree.ElementTree as ET


def parse_xml(filename):
    tree = ET.parse(filename)
    if tree:
        return tree
    else:
        return "Error"

def get_songlist(tree):
    root = tree.getroot()
    songs = []
    for d in root.iter('dict'):
        name=d.find('string[1]')
        artist=d.find('string[2]')
        song_name = ""
        if name == None and artist==None:
            pass
        else:
            if name.text.find("(") != -1:
                index = name.text.find("(")
                song_name = name.text[:index-1]
                song_name = song_name.replace("'","")
                key = [song_name, artist.text]
            else:
                song_name = name.text.replace("'","")
                key = [song_name, artist.text]
            songs.append(key)
    songs.pop(0)
    songs.pop(len(songs)-1)
    return songs
