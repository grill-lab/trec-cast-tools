import json
from tqdm import tqdm
import os
import sys
import codecs
from src.helpers import convert_to_trecweb
from src.PassageChunker import RegexPassageChunker, SpacyPassageChunker

    
if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("USAGE: python kilt_trecweb.py path_to_kilt_file path_to_dumpdir")
        exit(0)
    
    kilt_file_path = sys.argv[1]
    dump_dir = sys.argv[2]
    
    input_file = os.path.basename(kilt_file_path)

    print("Starting processing.")
    print("Output directory: " + dump_dir)
    dumper_file = os.path.join(dump_dir, input_file + '.xml')
    print("Writing output to: " + dumper_file)
    fp = codecs.open(dumper_file, 'w', 'utf-8')
                        
    with open(kilt_file_path, 'r') as kilt_file:
        #num_lines = kilt_file.readlines()
        for line in tqdm(kilt_file, total=5903530):
            doc = json.loads(line)
            doc_id = 'KILT_' + doc['wikipedia_id']
            doc_title = doc['wikipedia_title']
            doc_text = ' '.join(doc['text'])
            doc_url = doc['history']['url']
            
            passageChunker = RegexPassageChunker(doc_id, doc_title, doc_text, doc_url)
            passages = passageChunker.create_passages()
            
            for passage in passages:
                trecweb_passage = convert_to_trecweb(passage['id'], passage['title'], passage['body'], passage['url'])
                fp.write(trecweb_passage)

    fp.close()