#!/usr/bin/python3

import base64
import http.client
import json
import optparse
import os
import os.path
import urllib.parse

HOST = "api.faxage.com"


def send_fax(document, username, company, password, recip_fax, recip_name='', sender_name='', sender_phone=''):
    with open(document, 'rb') as raw_file:
        fax_data = raw_file.read()
    fax_data_b64 = base64.b64encode(fax_data)

    document_name = os.path.basename(document)

    parameters = {
        # API call and authentication:
        'host':                 HOST,
        'username':             username,
        'company':              company,
        'password':             password,
        'operation':            'sendfax',
        # fax information:
        'faxfilenames[]':       document_name,
        'faxfiledata[]':        fax_data_b64,
        # 'faxfiledata[]':        fax_data,
        # recipient information:
        'faxno':                recip_fax,
        'recipname':            recip_name,
        # sender information:
        'tagname':              sender_name,
        'tagnumber':            sender_phone,
    }

    payload_length = 0
    payload = []
    for key, value in parameters.items():
        item = '%s=%s' % (key, urllib.parse.quote(value))
        payload.append(item)
        payload_length += len(item)
    # account for & between items.
    payload_length += len(payload) - 1

    conn = http.client.HTTPSConnection(HOST)
    conn.putrequest("POST", '/httpsfax.php')

    conn.connect()
    conn.putheader('Content-Type', 'application/x-www-form-urlencoded')
    conn.putheader('Content-Length', payload_length)
    conn.endheaders()
    conn.send(bytes('&'.join(payload), 'utf-8'))
    resp = conn.getresponse()

    print('Response...')
    print(resp.read())


if __name__ == '__main__':
    parser = optparse.OptionParser(prog="example", description="Send a fax via FAXAGE using python.")
    parser.add_option("-a", "--document", help="The document to fax.")
    # note: user the prefix of your email, e.g., myemail@gmail.com, use "myemail" as username
    parser.add_option("-u", "--username", help="The FAXAGE API username.", default="")
    # You'll probably to need to get your "company ID from faxage support (usually a 5 digit #)
    parser.add_option("-c", "--company", help="The FAXAGE API company.", default="")
    parser.add_option("-p", "--password", help="The FAXAGE API password.", default="")
    parser.add_option("-r", "--recipient", help="The fax number to send the document to.")
    parser.add_option("-d", "--debug", action="store_true", help="Break into debugger before the interesting bits.")

    (options, args) = parser.parse_args()

    if not options.document:
        parser.error('You must supply a document to fax using the --document argument.')
    if not options.username or not options.company or not options.password:
        parser.error('You must supply a username, company and password to access the FAXAGE API.')
    if not options.recipient:
        parser.error('You must supply a fax number using the --recipient argument.')

    if options.debug:
        import pdb
        pdb.set_trace()

    send_fax(options.document, options.username, options.company, options.password, options.recipient)
