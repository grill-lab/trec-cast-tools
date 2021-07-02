# Year 3 Trecweb scripts

The scripts in this directory help with creating trecweb files (from the Marco document, KILT, and WaPo collections) that can be used for creating indexes. As part of the trecweb creation process, each document in a collection is chunked into smaller passages. 

Each document has an ID, url, title, and body. You can refer to http://www.treccast.ai/ to learn more about the Document ID format used for CAsT. Passage Number is based on the position of a passage within a document. 

Below is an example of the trecweb file that will be generated for MARCO:

```
<DOC>
<DOCNO>MARCO_D1555982</DOCNO>
<DOCHDR>
</DOCHDR>
<HTML>
<TITLE>The hot glowing surfaces of stars emit energy in the form of electromagnetic radiation.?</TITLE>
<URL>https://answers.yahoo.com/question/index?qid=20071007114826AAwCFvR</URL>
<BODY>
<PASSAGE 0>
Science & Mathematics Physics The hot glowing surfaces of stars emit energy in the form of electromagnetic radiation.? It is a good approximation to assume that the emissivity e is equal to 1 for these surfaces. Find the radius of the star Rigel, the bright blue star in the constellation Orion that radiates energy at a rate of 2.7 x 10^32 W and has a surface temperature of 11,000 K. Assume that the star is spherical. Use σ =... show more Follow 3 answers Answers Relevance Rating Newest Oldest Best Answer: Stefan-Boltzmann law states that the energy flux by radiation is proportional to the forth power of the temperature: q = ε · σ · T^4 The total energy flux at a spherical surface of Radius R is Q = q·π·R² = ε·σ·T^4·π·R² Hence the radius is R = √ ( Q / (ε·σ·T^4·π) ) = √ ( 2.7x10+32 W / (1 · 5.67x10-8W/m²K^4 · (1100K)^4 · π) ) 
</PASSAGE>
<PASSAGE 1>
= 3.22x10+13 m Source (s):http://en.wikipedia.org/wiki/Stefan_bolt...schmiso · 1 decade ago0 18 Comment Schmiso, you forgot a 4 in your answer. Your link even says it: L = 4pi (R^2)sigma (T^4). Using L, luminosity, as the energy in this problem, you can find the radius R by doing sqrt (L/ (4pisigma (T^4)). Hope this helps everyone. Caroline · 4 years ago4 1 Comment (Stefan-Boltzmann law) L = 4pi*R^2*sigma*T^4 Solving for R we get: => R = (1/ (2T^2)) * sqrt (L/ (pi*sigma)) Plugging in your values you should get: => R = (1/ (2 (11,000K)^2)) *sqrt ( (2.7*10^32W)/ (pi * (5.67*10^-8 W/m^2K^4))) R = 1.609 * 10^11 m? · 3 years ago0 1 Comment Maybe you would like to learn more about one of these? 
</PASSAGE>
<PASSAGE 2>
Want to build a free website? Interested in dating sites? Need a Home Security Safe? How to order contacts online?
</PASSAGE>
</BODY>
</HTML>
</DOC>
```

## How to use

1. Create and Activate a Python Virtual Environment using `python3 -m venv env` and `source env/bin/activate`
2. Install the required modules using `pip install -r requirements.txt`

### Creating the Trecweb scripts:

Ensure you have a copy of the Marco document, KILT, and WaPo collections and any relevant duplicate files (duplicates file for Marco can be found in the `duplicate_files` folder). Then:

Generate the **trecweb file for the Marco document collection** by running:

`python marco_trecweb.py path-to-msmarco-docs.tsv path-to-dump-directory path-to-duplicates-file`

Generate the **trecweb file for KILT** by running:

`python kilt_trecweb.py path-to-kilt_knowledgesource.json path-to-dump-directory`

Generate the **trecweb file for WaPo** by running:

`python wapo_trecweb.py path-to-TREC_Washington_Post_collection.v4.jl path-to-dump-directory path-to-wapo-near-duplicates`