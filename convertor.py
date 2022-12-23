import sys
import requests
import xml.etree.ElementTree as ET

ANILIST_BASE = "https://graphql.anilist.co/"
FINDMYLIST_BASE = "https://find-my-anime.dtimur.de/api?id={id}&provider=MyAnimeList&includeAdult=true"

status_mappings = {
    "CURRENT" : "Watching",
    "PLANNING" : "Plan to Watch",
    "DROPPED" : "Dropped",
    "COMPLETED" : "Completed",
    "PAUSED" : "Paused"
}

anime_list_fetch = """

query($username:String){
  MediaListCollection(userName:$username, type:ANIME, sort:STATUS){
    lists{
      entries{
        progress
        status
        media{
          id
          idMal
          title{
            english
            romaji
          }
          startDate {
            year
            month
            day
          }
        }
      }
    }
  }
}

"""

def convert(anilist_username:str) -> None:
    anime_list_response = requests.post(
        url=ANILIST_BASE, 
        json={
            "query" : anime_list_fetch,
            "variables" : {
                "username" : anilist_username
            }
        }
    )

    anime_list_data = anime_list_response.json()

    anime_list = anime_list_data.get("data").get("MediaListCollection").get("lists")

    root = ET.Element("myanimelist")

    """Boilerplate XML"""
    my_info = ET.SubElement(root, "myinfo")
    user_export_type = ET.SubElement(my_info, "user_export_type")
    user_export_type.text = "1"

    for list in anime_list:
        list_entries = list.get("entries")

        """Populating Anime"""
        for anime_info in list_entries:

            anilist_id = anime_info.get("media").get("id")
            mal_id = anime_info.get("media").get("idMal")
            anime_title = anime_info.get("media").get("title").get("english") or anime_info.get("media").get("title").get("romaji")
            anime_startDate = "{y}-{m}-{d}".format(y=anime_info.get("media").get("startDate").get("year"), m=anime_info.get("media").get("startDate").get("month"), d=anime_info.get("media").get("startDate").get("day"))
            anime_progress  = anime_info.get("progress")
            anime_status = status_mappings.get(anime_info.get("status"))

            if anime_title == "None" or anime_title is None:
                anime_info.get("media").get("title").get("english")
                anime_info.get("media").get("title").get("romaji")

            try:
                anime_sources = requests.get(url=FINDMYLIST_BASE.format(id=mal_id)).json()[0].get("sources")
            except:
                print(">>>>>>>>")
                print("ERROR : \nTITLE : {}\nANILIST ID : {}".format(anime_title, anime_id))
                print(">>>>>>>>")
                continue

            anime_id = 0

            for source in anime_sources:
                source = str(source)

                if "anidb" in source:
                    anime_id = source.split("/")[-1]

            anime_container = ET.SubElement(root, "anime")

            ET.SubElement(anime_container, "series_animedb_id").text = str(anime_id)
            ET.SubElement(anime_container, "anilist_id").text = str(anilist_id)
            ET.SubElement(anime_container, "title").text = anime_title
            ET.SubElement(anime_container, "my_watched_episodes").text = str(anime_progress)
            ET.SubElement(anime_container, "my_start_date").text = anime_startDate
            ET.SubElement(anime_container, "my_status").text = anime_status
            ET.SubElement(anime_container, "update_on_import").text = "1"

            print("ADDED : {} > {} ".format(anime_status, anime_title))

    with open("{}_MAL.xml".format(anilist_username), "wb") as xml_in:
        
        tree = ET.ElementTree(root)
        tree.write(xml_in)

def main():

    if len(sys.argv) < 2:
        print("Please provide a valid Anilist Username")
        anilist_username = input()
    else:
        anilist_username = sys.argv[1]

    convert(anilist_username)

if __name__ == "__main__":
    main()