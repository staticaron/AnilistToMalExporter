import sys
import requests
import xml.etree.ElementTree as ET

ANILIST_BASE = "https://graphql.anilist.co/"

status_mappings = {
    "CURRENT" : "Reading",
    "PLANNING" : "Plan to Read",
    "DROPPED" : "Dropped",
    "COMPLETED" : "Completed",
    "PAUSED" : "Paused"
}

manga_list_fetch = """

query($username:String){
  MediaListCollection(userName:$username, type:MANGA, sort:STATUS){
    lists{
      entries{
        progress
        status
        score
        startedAt {
            year
            month
            day
        }
        completedAt{
            year
            month
            day
        }
        media{
          id
          idMal
          title{
            english
            romaji
          }
        }
      }
    }
  }
}

"""

def convert(anilist_username:str) -> None:
    manga_list_response = requests.post(
        url=ANILIST_BASE, 
        json={
            "query" : manga_list_fetch,
            "variables" : {
                "username" : anilist_username
            }
        }
    )

    manga_list_data = manga_list_response.json()

    manga_list = manga_list_data.get("data").get("MediaListCollection").get("lists")

    root = ET.Element("myanimelist")

    """Boilerplate XML"""
    my_info = ET.SubElement(root, "myinfo")
    user_export_type = ET.SubElement(my_info, "user_export_type")
    user_export_type.text = "1"

    for list in manga_list:
        list_entries = list.get("entries")

        """Populating Manga"""
        for manga_info in list_entries:

            mal_id = manga_info.get("media").get("idMal")
            manga_title = manga_info.get("media").get("title").get("english") or manga_info.get("media").get("title").get("romaji")
            manga_status = status_mappings.get(manga_info.get("status"))
            manga_score = manga_info.get("score")
            manga_progress  = manga_info.get("progress")
            manga_startDate = "{y}-{m}-{d}".format(y=manga_info.get("startedAt").get("year"), m=manga_info.get("startedAt").get("month"), d=manga_info.get("startedAt").get("day"))
            manga_endDate = "{y}-{m}-{d}".format(y=manga_info.get("completedAt").get("year"), m=manga_info.get("completedAt").get("month"), d=manga_info.get("completedAt").get("day"))

            if manga_title == "None" or manga_title is None:
                manga_title = manga_info.get("media").get("title").get("english") or manga_info.get("media").get("title").get("romaji")

            manga_container = ET.SubElement(root, "manga")

            ET.SubElement(manga_container, "manga_mangadb_id").text = str(mal_id)
            ET.SubElement(manga_container, "my_read_chapters").text = str(manga_progress)
            ET.SubElement(manga_container, "my_score").text = str(manga_score)
            if manga_status != "Plan to Read":
                ET.SubElement(manga_container, "my_start_date").text = manga_startDate
            if manga_status == "Completed":
                ET.SubElement(manga_container, "my_finish_date").text = manga_endDate
            ET.SubElement(manga_container, "my_status").text = manga_status
            ET.SubElement(manga_container, "update_on_import").text = "1"

            print("ADDED : {} > {} ".format(manga_status, manga_title))

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
