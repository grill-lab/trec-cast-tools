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
import logging


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
        title = meta_dict[p.para_id]["title"]
        headings = meta_dict[p.para_id]["headings"]
        if title and not title.isspace():
            content += (u'<TITLE>\n')
            content += (title)
            content += (u'\n</TITLE>\n')
        if headings and not headings.isspace():
            content += (u'<HEADINGS>\n')
            content += (headings)
            content += (u'\n</HEADINGS>\n')
    elif meta_dict and p.para_id not in meta_dict:
        logging.warning(f'No metadata for ID: {p.para_id}')
    content += (u'<BODY>\n')
    content += (text)
    content += (u'\n</BODY>\n')
    content += (u'</DOC>\n')
    fp.write(content)
    
def sanitize_string(s):
    s = parse.unquote(s)
    s = re.sub(r'\W+', ' ', s)
    s = s.replace("enwiki","")
    return s
    
def create_metadata_dict(tsvfile):
    if tsvfile == None:
        return {}
    num_lines = sum(1 for line in open(tsvfile))
    assert num_lines == 36005581, f"Number of metadata records ({num_lines}) number is unexpected, expected 36005581. Ensure you are using the correct file."
    with open(args.metadata_file, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        metadata_dict = {}
        for row in tqdm.tqdm(reader, desc='Loading metadata lines', total=num_lines):
            assert len(row)==3, f"Row is not formatted correctly: {row}"
            metadata_dict[row[0]] = {"title":sanitize_string(row[1]), "headings":sanitize_string(row[2])}
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

    dumper_file = os.path.join(dump_dir, input_file + '.xml')
    print("Writing output to: " + dumper_file)
    fp = codecs.open(dumper_file, 'w', 'utf-8')
    print("Starting processing.")
    print("Output directory: " + dump_dir)
    
    meta_dict = create_metadata_dict(args.metadata_file)

    # Reads the file and iterates over paragraphs
    total = 0
    print("Reading ", filename)
    with open(filename, 'rb') as rp:
        for p in tqdm.tqdm(iter_paragraphs(rp), desc="Converting to trecweb"):
            # Write to file
            writer(p, fp, meta_dict=meta_dict)
            total += 1
    print("Total paras written = ", total)
    print("Closing File")

    rp.close()
    fp.close()