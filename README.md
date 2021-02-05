# MLB Pitch Locator
<h4>Interactive plot showing MLB pitch locations from Statcast using Pandas and SQLite, saving as HTML for viewing through plotly.</h4>


Supports both importing local Statcast .csv file and pulling data directly from Statcast using baseball_scraper.

Features:
* Left / Right batter splits per pitch type
* Single or multitple pitch selection
* Pitch velocity on hover
* Local .csv chunk import to Pandas dataframe and sqlite .db using sqlite3
* Direct pull from baseball-savant's Statcast API through baseball_scraper
* Save to HTML via Plotly libraries

Example plot of Yu Darvish's 2020 season. Each pitch is selectable on the right, with a double click function to clear or select all:

![Yu Darvish 2020](https://github.com/AaronHenry/MLB-Pitch-Locator/blob/main/PitchLocatorExample.png)



