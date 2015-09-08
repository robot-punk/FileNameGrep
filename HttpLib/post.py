# coding utf-8
'''
Created on 2015/09/07

@author: takashi okumura
'''
import sys
import os
import urllib
import urllib2
from lxml import etree

URL = 'http://example.com/'
POST_PARAMS = {'im_user': 'aoyagi', 'im_password': 'aoyagi'}
REQ_HEADER_PARAMS = {'Content-Type': 'application/x-www-form-urlencoded'}


def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    # read config xml
    read_conf('conf.xml')

    url = URL
    post_params = POST_PARAMS
    req_header_params = REQ_HEADER_PARAMS

    body = post(url, post_params, req_header_params)
    
    # write file
    write_file('response.html', body)


def read_conf(conf_path):
    conf = etree.parse(conf_path)
    URL = conf.find('url').text
    POST_PARAMS = conf.find('post-params').text
    REQ_HEADER_PARAMS = conf.find('req_header_params').text

def write_file(path, value):
    file = open(path, 'w')
    file.write(value)
    file.close()

def post(url, post_params, req_header_params):
    params = urllib.urlencode(post_params)

    req = urllib2.Request(url)
    for key, value in req_header_params.iteritems():
        req.add_header(key, value)

    req.add_data(params)

    res = urllib2.urlopen(req)
    body = res.read()
    return body


if __name__ == '__main__':
    sys.exit(main())
