import json
from tqdm import tqdm
import os
import sys
import codecs
from trecweb_utils import convert_to_trecweb, add_passage_ids
from passage_chunker import SpacyPassageChunker


def write_document(line, fp, passageChunker):
    """Writes a KILT document to Trecweb

    Args:
        line (json str): KILT document
        fp (file path): path to trecweb file
    """
    doc = json.loads(line)
    idx = 'KILT_' + doc['wikipedia_id']
    title = doc['wikipedia_title']
    body = ' '.join(doc['text'])
    url = doc['history']['url']
    
    passageChunker.sentence_tokenization(body)

    passages = passageChunker.create_passages()
    
    passage_splits = add_passage_ids(passages)

    trecweb_format = convert_to_trecweb(idx, title, passage_splits, url)
    fp.write(trecweb_format)
    


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: python kilt_trecweb.py path_to_kilt_file path_to_dumpdir")
        exit(0)
    
    kilt_file_path = sys.argv[1]
    dump_dir = sys.argv[2]
    
    input_file = os.path.basename(kilt_file_path)

    passageChunker = SpacyPassageChunker()

    # Create the directory (for dumping files) if it doesn't exists
    if not os.path.exists(dump_dir):
        os.mkdir(dump_dir)

    print("Starting processing.")
    print("Output directory: " + dump_dir)
    dumper_file = os.path.join(dump_dir, input_file + '.trecweb')
    print("Writing output to: " + dumper_file)
    fp = codecs.open(dumper_file, 'w', 'utf-8')

                 
    with open(kilt_file_path, 'r') as kilt_file:
        
        for line in tqdm(kilt_file, total=5903530):
            write_document(line, fp, passageChunker)

    fp.close()