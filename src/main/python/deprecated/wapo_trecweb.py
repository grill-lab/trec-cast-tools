
# Version 1.0
# Python 3
import json
import sys
import os
import codecs
from tqdm import tqdm
from trecweb_utils import convert_to_trecweb, add_passage_ids
from passage_chunker import SpacyPassageChunker


def get_document(data, dup_dict):
    """Extracts the ID, title, url, and body of each document

    Args:
        data (dictionary): Contianer for a WaPo document
        dup_dict (dictionary): A lookup dictionary for duplicates in the WaPo collection

    Returns:
        str: ID of the WaPo document
        str: Contents of the WaPo document
        str: Title of the WaPo document
        str: Url of the WaPo document
    """
    
    if dup_dict.get(data["id"]) == 1:
        print("duplicate found -> {}!".format(data["id"]))
        return
    
    if dup_dict.get(data["id"]) == 2:
        dup_dict[data["id"]] = 1

    idx = 'WAPO_' + str(data['id'])
    url = ''
    
    if data["article_url"]:
        if "www.washingtonpost.com" not in data["article_url"]:
            url = "https://www.washingtonpost.com" + data['article_url']
        else:
            url = data['article_url']
    else:
        url = '/#'
    
    body = ''
    contents = data['contents']
    title = 'No Title'
    
    try:
        for item in contents:
            if 'subtype' in item and item['subtype'] == 'paragraph':
                body += ' ' + item['content']
    except:
        body += 'No body'
    
    if data['title'] != None:
        title = data['title'].replace("\n", " ")

    
    return idx, body, title, url


def create_duplicate_dictionary(duplicate_file):
    """Creates a lookup dictionary from the WaPo duplicates file

    Args:
        duplicate_file (file): WaPo duplicates file

    Returns:
        dict: duplicates lookup dictionary
    """
    dup_dict = {}
    data_dups = open(duplicate_file).readlines()
    for each in data_dups:
        idxs = each.strip().split(' ') #source duplicate title
        if idxs[0] == idxs[1]:
            dup_dict[idxs[1]] = 2 #the duplicate has the same id as the original
        else:
            dup_dict[idxs[1]] = 1 #the duplicate has a different id from the original
    
    return dup_dict


def write_document(data, fp, dup_dict, passageChunker):
    """Writes a WaPo document to trecweb

    Args:
        data (json str): Wapo document
        fp (str): File path
        dup_dict (dict): Duplicates dictionary
    """
    data1 = data.strip()
    data1 = json.loads(data1)

    try:
        idx, body, title, url = get_document(data1, dup_dict)

        passageChunker.sentence_tokenization(body)
        passages = passageChunker.create_passages()

        passage_splits = add_passage_ids(passages)

        trecweb_format = convert_to_trecweb(idx, title, passage_splits, url)
        fp.write(trecweb_format)
        

    except:
        return

    

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python3 wapo_trecweb.py DATAPATH DUMP_PATH DUPLICATE_FILE")
        print("Example: python wapo_clean_parser.py ../wapo_path ../wapo_dump_dir wapo-near-duplicates")
        exit(0)


    duplicate_file = sys.argv[3]
    dumper = sys.argv[2] 
    file_path = sys.argv[1]


    dup_dict = create_duplicate_dictionary(duplicate_file)
    
    input_file = os.path.basename(file_path)

    if not os.path.exists(dumper):
        os.mkdir(dumper)
    
    dumper_file = os.path.join(dumper, input_file + '.trecweb')
    fp = codecs.open(dumper_file, 'w', 'utf-8')
    print("Opening ", file_path)
    lines = open(file_path, 'r').readlines()
    print("Read ", file_path)
    tl = len(lines)

    passageChunker = SpacyPassageChunker()


    for i, data in tqdm(enumerate(lines), total=tl):
        write_document(data, fp, dup_dict, passageChunker)        
        
    fp.close()