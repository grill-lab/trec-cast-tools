def convert_to_trecweb(passage_id, doc_title, doc_body, doc_url):
    
    '''
    Takes a document with passage spilts and converts it to trecweb format
    '''
    content = '<DOC>\n'
    content += '<DOCNO>'
    content += passage_id
    content += '</DOCNO>\n'
    content += '<DOCHDR>\n'
    # content += '\n'
    content += '</DOCHDR>\n'
    content += '<HTML>\n'
    content += '<TITLE>'
    content += doc_title
    content += '</TITLE>\n'
    content += '<URL>'
    content += doc_url
    content += '</URL>\n'
    content += '<BODY>\n'
    content += doc_body
    # content += '\n'
    content += '</BODY>\n'
    content += '</HTML>\n'
    content += '</DOC>\n'
    content += '\n'
    
    return content


def add_passage_ids(passages):

    passage_number = 0
    passage_splits = ''

    for passage in passages:
        passage_splits += '<passage id={}>\n'.format(passage["id"])
        passage_splits += passage["body"] + '\n'
        passage_splits += '</passage>\n'
        passage_number += 1

    
    return passage_splits