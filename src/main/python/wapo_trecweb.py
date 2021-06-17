
# Version 1.0
# Python 3

import json
import sys
import os
import codecs
import re
from tqdm import tqdm
from bs4 import BeautifulSoup
from src.helpers import convert_to_trecweb
from src.PassageChunker import RegexPassageChunker, SpacyPassageChunker


def get_document(data, dup_dict):
    """ 
    Writes item to a file in trecweb format
   
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
    '''
    Creates a duplicate dictionary to help with removing duplicates from the collection
    '''
    dup_dict = {}
    data_dups = open(duplicate_file).readlines()
    for each in data_dups:
        idxs = each.strip().split(' ') #source duplicate title
        if idxs[0] == idxs[1]:
            dup_dict[idxs[1]] = 2 #the duplicate has the same id as the original
        else:
            dup_dict[idxs[1]] = 1 #the duplicate has a different id from the original
    
    return dup_dict
    

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
    
    #for file in os.listdir(file_path):
    dumper_file = os.path.join(dumper, input_file + '.xml')
    fp = codecs.open(dumper_file, 'w', 'utf-8')
    print("Opening ", file_path)
    lines = open(file_path, 'r').readlines()
    print("Read ", file_path)
    tl = len(lines)
    for i, data in tqdm(enumerate(lines), total=tl):
        data1 = data.strip()
        data1 = json.loads(data1)
        
        try:
            idx, body, title, url = get_document(data1, dup_dict)
            passageChunker = RegexPassageChunker(idx, title, body, url)
            passages = passageChunker.create_passages()
            
            for passage in passages:
                trecweb_passage = convert_to_trecweb(passage['id'], passage['title'], passage['body'], passage['url'])
                fp.write(trecweb_passage)
            
        except:
            continue
        
    fp.close()