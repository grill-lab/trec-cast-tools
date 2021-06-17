def convert_to_trecweb(passage_id, doc_title, passage_text, doc_url):
    
    '''
    Takes a chunked passage from a document and converts it to trecweb format
    '''
    content = (u'<DOC>\n')
    content += (u'<DOCNO>')
    content += (passage_id)
    content += (u'</DOCNO>\n')
    content += (u'<DOCHDR>\n')
    content += (u'\n')
    content += (u'</DOCHDR>\n')
    content += (u'<HTML>\n')
    content += (u'<TITLE>')
    content += (doc_title)
    content += (u'</TITLE>\n')
    content += (u'<URL>')
    content += (doc_url)
    content += (u'</URL>\n')
    content += (u'<BODY>\n')
    content += (passage_text)
    content += (u'\n')
    content += (u'</BODY>\n')
    content += (u'</HTML>\n')
    content += (u'</DOC>\n')
    
    return content