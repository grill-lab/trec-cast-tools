from typing import List


def reform_document_body(passages: List) -> str:
    """
    Reforms the document body to include passage splits
    """

    passage_splits = ''

    for passage in passages:
        passage_splits += f'<PASSAGE id={passage["id"]}>\n'
        passage_splits += passage["body"] + '\n'
        passage_splits += '</PASSAGE>\n'

    return passage_splits


def create_trecweb_entry(idx: str, url: str, title: str, contents: str) -> str:
    """
    Creates a trecweb entry for a document
    """

    content = '<DOC>\n'
    content += '<DOCNO>'
    content += idx
    content += '</DOCNO>\n'
    content += '<DOCHDR>\n'
    content += '</DOCHDR>\n'
    content += '<HTML>\n'
    content += '<TITLE>'
    content += title
    content += '</TITLE>\n'
    content += '<URL>'
    content += url
    content += '</URL>\n'
    content += '<BODY>\n'
    content += contents
    content += '</BODY>\n'
    content += '</HTML>\n'
    content += '</DOC>\n'
    content += '\n'

    return content


def write_to_trecweb(file_path: str, document_batch):

    with open(file_path, 'w') as trecweb_file:
        for document in document_batch:
            contents = document["contents"]
            contents = reform_document_body(contents)
            trecweb_entry = create_trecweb_entry(
                document["id"], document["url"], document["title"], contents)
            trecweb_file.write(trecweb_entry)
