# AnilistToMalExporter
Generates the .xml file from Anilist to be imported to MAL.

# Requirements
* Python 3.10 [ should work with most python version ]

# How to use?

* Clone the repo to your local machine.
* Create a virtual environment.
* Install the dependencies : 

      pip install -r requirements.txt
      
* Run the convertor.py file and pass your username as a parameter.

      python convertor.py Laevateinn
    
 _A file **\<anilistusername\>.xml** will be generated_

# How to import .xml file into your MAL account.

* Go to [MyAnimeList](https://myanimelist.net/) and log in with your MAL account.
* Click on _Add Entries_ : 

![image](https://user-images.githubusercontent.com/66104268/209352044-c71de3d9-dd86-45f2-a1b5-d4e175f26cc8.png)

* Click on _Import Lists_

![image](https://user-images.githubusercontent.com/66104268/209352265-9591203b-b9d0-4a33-b412-6613b3c28dec.png)

* Select _MyAnimeList Import_ and Upload the .xml file.

![image](https://user-images.githubusercontent.com/66104268/209352442-a8f6d230-0487-4e34-b3ab-078936084925.png)

* Finish and Click on Import Data.

## Watch Out.

There may be some entries that are not recognised by the APIs. These entries will be shown in the terminal with ERROR tag. Make sure to manually add them after the import is complete.

