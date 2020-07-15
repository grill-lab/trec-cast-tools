# Version 1.1
import os
import sys
import codecs
from trec_car.read_data import *
import argparse
import tqdm
from urllib import parse
import csv
import re

def writer(p, fp, meta_dict={}):

    """
    Writes each paragraph in the trecweb format
    """
    # Get the paragraph id and text
    para_id = 'CAR_' + str(p.para_id)
    text = p.get_text()

    content = (u'<DOC>\n')
    content += (u'<DOCNO>')
    content += (para_id)
    content += (u'</DOCNO>\n')
    content += (u'<DOCHDR>\n')
    content += (u'\n')
    content += (u'</DOCHDR>\n')
    if meta_dict and p.para_id in meta_dict:
        content += (u'<TITLE>\n')
        content += (meta_dict[p.para_id]["title"])
        content += (u'\n</TITLE>\n')
        content += (u'<TAG>\n')
        content += (meta_dict[p.para_id]["tag"])
        content += (u'\n</TAG>\n')
    content += (u'<BODY>\n')
    content += (text)
    content += (u'\n</BODY>\n')
    content += (u'</DOC>\n')
    fp.write(content)
    
def sanitize_string(s):
    s = parse.unquote(s)
    s = re.sub(r'\W+', ' ', s)
    return s
    
def create_metadata_dict(tsvfile):
    if tsvfile == None:
        return {}
    with open(args.metadata_file, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        metadata_dict = {}
        for row in tqdm.tqdm(reader, desc='loading metadata lines'):
            metadata_dict[row[0]] = {"title":sanitize_string(row[1]), "tag":sanitize_string(row[2])}
        return metadata_dict

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='"Usage: python car_treweb.py dedup.articles-paragraphs.cbor DUMP_DIR --metadata_file car_meta.tsv')
    parser.add_argument('filename', help='cbor file to process')
    parser.add_argument('dump_dir', help='duplicates file')
    parser.add_argument('--metadata_file', default=None, help='TSV file containing CAR para IDs and metadata')
    args = parser.parse_args()
    
    filename = args.filename
    dump_dir = args.dump_dir

    input_file = os.path.basename(filename)
    
    meta_dict = create_metadata_dict(args.metadata_file)

    dumper_file = os.path.join(dump_dir, input_file + '.xml')
    print("Writing output to: " + dumper_file)
    fp = codecs.open(dumper_file, 'w', 'utf-8')
    print("Starting processing.")
    print("Output directory: " + dump_dir)

    # Reads the file and iterates over paragraphs
    total = 0
    print("Reading ", filename)
    with open(filename, 'rb') as rp:
        for p in tqdm.tqdm(iter_paragraphs(rp), desc="casting to trecweb"):
            # Write to file
            writer(p, fp, meta_dict=meta_dict)
            total += 1
    print("Total paras written = ", total)
    print("Closing File")

    rp.close()
    fp.close()