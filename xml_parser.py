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
        artist_name = ""
        if name == None or artist == None:
            pass
        else:
            if name.text.find("(") != -1:
                index = name.text.find("(")
                song_name = name.text[:index-1]
                song_name = song_name.replace("'","")
                song_name = song_name.replace("&", "")
                artist_name = artist.text
                artist_name = artist_name.replace("'","")
                artist_name = artist_name.replace("&","")
                artist_name = artist_name.replace(",","")
                key = [song_name, artist_name]
            else:  
                song_name = name.text.replace("'","")
                song_name = song_name.replace("&", "")
                artist_name = artist.text
                if artist_name != None:
                    artist_name = artist_name.replace("'","")
                    artist_name = artist_name.replace("&","")
                    artist_name = artist_name.replace(",","")
                key = [song_name, artist_name]
            songs.append(key)
    songs.pop(0)
    songs.pop(len(songs)-1)
    return songs


#tree = parse_xml('rocktheboat.xml')
#songs = get_songlist(tree)
#print(songs)