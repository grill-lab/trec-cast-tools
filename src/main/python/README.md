# Year 3 Trecweb scripts

The scripts in this directory help with creating trecweb files (from the Marco document, KILT, and WaPo collections) that can be used for indexing with tools like Anserini or Solr. As part of the trecweb creation process, each document in a collection is chunked into passages of at most 250 words. 

Each passage has an ID, url, title, and body. The passage ID is of the form <Document ID>:<Passage Number>. You can refer to http://www.treccast.ai/ to learn more about the Document ID format used for CAsT. Passage Number simply is the position of a passage within a document. Passages from the same document have the same url and title.

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