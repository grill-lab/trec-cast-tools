# Corpus Processing

Utility tools to create trecweb and jsonlines files from the MARCO, KILT, and WaPo collections can be found in this directory. During the file creation process, each document in a collection is chunked into smaller passages. 

Each document has an ID, url, title, and body. You can refer to http://www.treccast.ai/ to learn more about the Document ID format used for CAsT. Passage ID is based on the position of a passage within a document. 

Below is a sample document in `trecweb` format that is generated from KILT after running the utility:

```
<DOC>
<DOCNO>KILT_20988744</DOCNO>
<DOCHDR>
</DOCHDR>
<HTML>
<TITLE>Worlingworth</TITLE>
<URL>https://en.wikipedia.org/w/index.php?title=Worlingworth&oldid=895384908</URL>
<BODY>
<PASSAGE id=1>
Worlingworth  Worlingworth is a village and civil parish in the Mid Suffolk district of Suffolk in eastern England, located around ten miles south-east of Diss. In 2011 it had a total population of 802 people.  The village has a primary school called Worlingworth CEVC Primary School. The school was judged by Ofsted to be 'Outstanding' in all areas in March 2016. The school's motto is "Cherish All, Achieve Together". The local church of St. Mary is a grade I listed building and the chancel, the oldest surviving part, dates to the late 13th century.   Between 1908 and 1952 the village was served by Worlingworth railway station on the Mid-Suffolk Light Railway.  Section::::History.  In Old English, the meaning of Worlingworth is an 'enclosure of the followers of Wilhere'. Broken down, 'Wilhere' is a personal name, '-ingas' means 'the people of' or 'the people called after' and 'worð' is for 'an enclosure'.  The Domesday book states Worlingworth to be "quite large", with a population of 32 households, made up from 16 villagers, 14 smallholders, 1 slave and 1 freeman. 
</PASSAGE>
<PASSAGE id=2>
The livestock of Worlingworth in 1066 included 8 cattle, 24 pigs, 25 sheep, 35 goats and 2 horses, this remained the same by 1086 however the village had gained 6 beehives and lost the 2 horses.  John Marius Wilson wrote about Worlingworth in 1870 and described it as:  In 1801 the village had the facilities of a blacksmith, a wheelwright, a shoemaker, a dressmaker, a brewers and malsters, a general tradesman, a general store, a beerhouse and coaching inn, a workhouse, a school, a church and a stately hall.  The workhouse was founded in 1730, after the village guild hall was converted. It was able to accommodate 35 people up until it was closed in 1836, shortly after outbreaks of typhus in 1820.  By 2014 the village amenities have changed considerably compared to those available in 1801. There is now a church, a community centre, and a primary school. The village had a public house called The Swan Inn, which closed in 2016. The building is still standing as it is a grade II listed building.  Section::::Demographics.  Section::::Demographics.:Population.   The earliest records for population in Worlingworth date back to the 1801 census where there was a total population of 729. 
</PASSAGE>
<PASSAGE id=3>
There has been a steady decline in Worlingworth's total population from 1851 where the population total was 811 to 460 in 1961, possibly due to the migration of people and families to towns or cities to find work in factories rather than as farm labourers.By 2011 the population had increased to 802, and was made up of 390 females and 412 males.  In 1831 the majority of Worlingworth's population, 78 people, were classed as Labourers and Servants, the lowest social class, compared to just 27 people who were in the highest being Employers and Professionals. 43 people were of the Middling Sorts which includes masters, skilled workers and small farmers who do not employ labourers and just 21 classified as Other. This suggests that Worlingworth was a small rural community which was strongly based around agriculture.    Section::::Demographics.:Employment.  The enumeration of 1831 shows Worlingworth to have a total population of 729, split between 145 families. 86 people were "chiefly employed in agriculture", the biggest employer as only 30 people were working in trade, manufacturing and handicraft and just 29 in other classes.  In the 1881 census, 324 people were counted in the occupation section in Worlingworth. 
</PASSAGE>
<PASSAGE id=4>
The main occupation for the villagers at this time was in agriculture which employed 103 males, 81 of these worked as an agricultural labourer, farm servant or cottager.30 females were employed as domestic indoor servants,  although the majority of females, 75, were without specified occupations, the second biggest employment sector within Worlingworth in 1881.  The 2001 census shows that there are 487 economically active people, ages 16 to 74, in Worlingworth. The majority, 181 of these were in full-time employment, compared to only 67 who were in part-time employment.  In 2011, the occupations of the villagers was almost equally mixed between employment sectors. The biggest employing sector was Wholesale and Retail Trade which employed 52 people. The second largest sector was Agriculture, Forestry and Fishing which employed 47 people, this includes L.E Tuckwell Ltd. who is an agricultural supplier and a major employer within Worlingworth. 
</PASSAGE>
</BODY>
</HTML>
</DOC>
```

and here is a `jsonlines` sample

```
{
   "id":"KILT_20988744",
   "url":"https://en.wikipedia.org/w/index.php?title=Worlingworth&oldid=895384908",
   "title":"Worlingworth",
   "contents":[
      {
         "body":"Worlingworth  Worlingworth is a village and civil parish in the Mid Suffolk district of Suffolk in eastern England, located around ten miles south-east of Diss. In 2011 it had a total population of 802 people.  The village has a primary school called Worlingworth CEVC Primary School. The school was judged by Ofsted to be 'Outstanding' in all areas in March 2016. The school's motto is \"Cherish All, Achieve Together\". The local church of St. Mary is a grade I listed building and the chancel, the oldest surviving part, dates to the late 13th century.   Between 1908 and 1952 the village was served by Worlingworth railway station on the Mid-Suffolk Light Railway.  Section::::History.  In Old English, the meaning of Worlingworth is an 'enclosure of the followers of Wilhere'. Broken down, 'Wilhere' is a personal name, '-ingas' means 'the people of' or 'the people called after' and 'worð' is for 'an enclosure'.  The Domesday book states Worlingworth to be \"quite large\", with a population of 32 households, made up from 16 villagers, 14 smallholders, 1 slave and 1 freeman. ",
         "id":1
      },
      {
         "body":"The livestock of Worlingworth in 1066 included 8 cattle, 24 pigs, 25 sheep, 35 goats and 2 horses, this remained the same by 1086 however the village had gained 6 beehives and lost the 2 horses.  John Marius Wilson wrote about Worlingworth in 1870 and described it as:  In 1801 the village had the facilities of a blacksmith, a wheelwright, a shoemaker, a dressmaker, a brewers and malsters, a general tradesman, a general store, a beerhouse and coaching inn, a workhouse, a school, a church and a stately hall.  The workhouse was founded in 1730, after the village guild hall was converted. It was able to accommodate 35 people up until it was closed in 1836, shortly after outbreaks of typhus in 1820.  By 2014 the village amenities have changed considerably compared to those available in 1801. There is now a church, a community centre, and a primary school. The village had a public house called The Swan Inn, which closed in 2016. The building is still standing as it is a grade II listed building.  Section::::Demographics.  Section::::Demographics.:Population.   The earliest records for population in Worlingworth date back to the 1801 census where there was a total population of 729. ",
         "id":2
      },
      {
         "body":"There has been a steady decline in Worlingworth's total population from 1851 where the population total was 811 to 460 in 1961, possibly due to the migration of people and families to towns or cities to find work in factories rather than as farm labourers.By 2011 the population had increased to 802, and was made up of 390 females and 412 males.  In 1831 the majority of Worlingworth's population, 78 people, were classed as Labourers and Servants, the lowest social class, compared to just 27 people who were in the highest being Employers and Professionals. 43 people were of the Middling Sorts which includes masters, skilled workers and small farmers who do not employ labourers and just 21 classified as Other. This suggests that Worlingworth was a small rural community which was strongly based around agriculture.    Section::::Demographics.:Employment.  The enumeration of 1831 shows Worlingworth to have a total population of 729, split between 145 families. 86 people were \"chiefly employed in agriculture\", the biggest employer as only 30 people were working in trade, manufacturing and handicraft and just 29 in other classes.  In the 1881 census, 324 people were counted in the occupation section in Worlingworth. ",
         "id":3
      },
      {
         "body":"The main occupation for the villagers at this time was in agriculture which employed 103 males, 81 of these worked as an agricultural labourer, farm servant or cottager.30 females were employed as domestic indoor servants,  although the majority of females, 75, were without specified occupations, the second biggest employment sector within Worlingworth in 1881.  The 2001 census shows that there are 487 economically active people, ages 16 to 74, in Worlingworth. The majority, 181 of these were in full-time employment, compared to only 67 who were in part-time employment.  In 2011, the occupations of the villagers was almost equally mixed between employment sectors. The biggest employing sector was Wholesale and Retail Trade which employed 52 people. The second largest sector was Agriculture, Forestry and Fishing which employed 47 people, this includes L.E Tuckwell Ltd. who is an agricultural supplier and a major employer within Worlingworth. ",
         "id":4
      }
   ]
}
```

## How to use

1. Create and activate a Python Virtual Environment using `python3 -m venv env` then `source env/bin/activate`
2. Install the dependencies using `pip install -r requirements.txt`

### Processing the Collection:

1. First, use the `download_collection.sh` bash script to download the raw collection and blacklisted document ids
2. Next, run `python3 main.py --output_type trecweb` or `python3 main.py --output_type jsonlines` to generate .trecweb or .jsonl files you can use for indexing

### Notes

1. If you downloaded the raw collection without the `download_collection.sh` script, you may need to pass in the path to your files as argument while using the scripts:
- use `--wapo_collection` to specify the path to your downloaded WaPo collection
- use `--duplicates_file` to specify the path to your downloaded duplicates file
- use `--marco_v2_collection` to specify the path to your downloaded MARCO V2 collection
- use `--kilt_collection` to specify the path to your downloaded KILT collection

2. You can specify a directory to write the output trecweb/jsonlines file to by using `--output_dir`

3. If you want to process a subset of the three collections, you can skip processing the other collections you're not interested. For example, if you just wanted to generate trecweb files for MARCO V2, then you would do `python3 main.py --output_type trecweb --skip_process_kilt --skip_process_wapo`

4. Documents are processed in batches to take advange of Spacy's multiprocessing capabilities. You may want to reduce or increase the `--batch_size` argument (default of 100000) depending on the compute resources available to you. Please note that the `--batch_size` argument also determines the number of document entries that are written out per output file.

5. The `download_collection.sh` script asks for a password to download the Washington Post corpus. This is the same password NIST provides to download the collection after filing the "Organizational agreement" with NIST. For more information, visit the [Washington Post Web page](https://trec.nist.gov/data/wapost/)

6. If you want to write out the output trecweb/jsonlines file to a different directory than the default, then pass in the `--output-dir` argument when running the utility.

7. This utility also generates csv files with all passage ids and their corresponding passage md5 hashes. You may compare the hashes in this file with the hashes in the [master version](https://cast-y4-collection.s3.amazonaws.com/all_hashes.csv) to ensure that you have the right passage splits.


## Other Notes
1. The utility was built and tested with Python 3.8.10
