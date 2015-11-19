#Wrangling-OpenStreetMap-Data
In this project, I wrangle the OpenStreetMap XML Data for the city of Atlanta. A link to the XML data used can be found [here](https://s3.amazonaws.com/metro-extracts.mapzen.com/atlanta_georgia.osm.bz2). The XML data is programmatically audited using the functions written in **audit.py**.  The auditing task is focused on *nodes* and *way* objects and we focus on the tags with:
- address information
- user/location info

After iteratively auditing the data, I perform my data cleaning process using the functions in **data_cleaning.py**. The XML data is restructured into *JSON* documents and then placed into a MongoDB data based where Data Analysis is performed using the MongoDB Aggregation framework Information about the MongoDB Aggregation Framework can be found at this [link](https://docs.mongodb.org/manual/applications/aggregation/).  Documentation on this project can be found by clicking on **OpenStreetMap Project.ipynb** in this repository.
