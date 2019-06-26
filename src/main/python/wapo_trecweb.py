# Version 1.0
import json
import sys
import os
import codecs

def write_to_file(fp, data, i):

    """
    Converts all the available paragraphs into the trecweb format
    and writes it to a file. Ids to each paragraphs are assigned
    in a sequential order.

    Args:
        fp: file pointer for writing the trecweb docs
        data: json parsed line containing all the paragraphs
        i: (optional) index of parsed data
   
    """
 
    main_idx = 'WAPO_' + str(data['id'])
    main_url = data['article_url']

    paras = data['contents']
    counter = 0

    # writes paragraphs in the trecweb format
    for idx, each in enumerate(paras):
        if each == None:
            continue
        elif 'subtype' in each:
            if each['subtype'] == 'paragraph':
                body =  each['content']
                if body != '':
                    counter += 1
                    paraidx = main_idx + '-' + str(counter)
                    content = u'<DOC>\n'
                    content += u'<DOCNO>'
                    content += str(paraidx)
                    content += u'</DOCNO>\n'
                    content += u'<DOCHDR>\n'
                    content += main_url
                    content += u'\n</DOCHDR>\n'
                    content += u'<HTML>\n'
                    content += u'<BODY>\n'
                    content += body
                    content += '\n'
                    content += u'</BODY>\n'
                    content += '</HTML>\n'
                    content += '</DOC>\n'
                    fp.write(content)

def parse(file_path, dumper):

    """
    Iterates over each file in the WAPO dataset.
    Each file is opened, its contents are read,
    and the paragraphs are dumped in the trecweb
    format.
    """

    if not os.path.exists(dumper):
        os.mkdir(dumper)

    # iterates over each file in the directory
    for file in os.listdir(file_path):
        dumper_file = os.path.join(dumper, file + '.xml')
        fp = codecs.open(dumper_file, 'w', 'utf-8')
        file = os.path.join(file_path, file)
        print("Opening " + file)
        lines = open(file, 'r').readlines()
        print("Read " + file)
        for i, data in enumerate(lines):
            data1 = data.strip()
            data1 = json.loads(data1)
            write_to_file(fp, data1, i)
        fp.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python wapo_trecweb.py DATAPATH DUMP_PATH")
        print("Example: python wapo_trecweb.py ../wapo_path ../wapo_dump_dir")
        exit(0)
    dumper = sys.argv[2] 
    data_path = sys.argv[1]
    parse(data_path, dumper)
