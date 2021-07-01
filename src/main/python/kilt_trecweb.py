import multiprocessing
import json
from tqdm import tqdm
import os
import sys
import codecs
from src.helpers import convert_to_trecweb, add_passage_ids
from src.PassageChunker import SpacyPassageChunker

    
# if __name__ == "__main__":
    
#     if len(sys.argv) < 3:
#         print("USAGE: python kilt_trecweb.py path_to_kilt_file path_to_dumpdir")
#         exit(0)
    
#     kilt_file_path = sys.argv[1]
#     dump_dir = sys.argv[2]
    
#     input_file = os.path.basename(kilt_file_path)

#     print("Starting processing.")
#     print("Output directory: " + dump_dir)
#     dumper_file = os.path.join(dump_dir, input_file + '.xml')
#     print("Writing output to: " + dumper_file)
#     fp = codecs.open(dumper_file, 'w', 'utf-8')
                        
#     with open(kilt_file_path, 'r') as kilt_file:
#         #num_lines = kilt_file.readlines()
#         for line in tqdm(kilt_file, total=5903530):
#             doc = json.loads(line)
#             idx = 'KILT_' + doc['wikipedia_id']
#             title = doc['wikipedia_title']
#             body = ' '.join(doc['text'])
#             url = doc['history']['url']
            
#             passageChunker = SpacyPassageChunker(body)
#             # passageChunker = RegexPassageChunker(body)
#             passages = passageChunker.create_passages()
            
#             passage_splits = add_passage_ids(passages)

#             trecweb_format = convert_to_trecweb(idx, title, passage_splits, url)
#             fp.write(trecweb_format)

#     fp.close()

def write_kilt_to_trecweb(path_to_kilt_file, path_to_dumpdir):
    
    kilt_file_path = path_to_kilt_file
    dump_dir = path_to_dumpdir
    
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
            idx = 'KILT_' + doc['wikipedia_id']
            title = doc['wikipedia_title']
            body = ' '.join(doc['text'])
            url = doc['history']['url']
            
            passageChunker = SpacyPassageChunker(body)
            # passageChunker = RegexPassageChunker(body)
            passages = passageChunker.create_passages()
            
            passage_splits = add_passage_ids(passages)

            trecweb_format = convert_to_trecweb(idx, title, passage_splits, url)
            fp.write(trecweb_format)

    fp.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: python kilt_trecweb.py path_to_kilt_file path_to_dumpdir")
        exit(0)
    
    kilt_file_path = sys.argv[1]
    dump_dir = sys.argv[2]

    p1 = multiprocessing.Process(target=write_kilt_to_trecweb, args=(kilt_file_path, dump_dir, ))
    p1.start()

    print("Done!")