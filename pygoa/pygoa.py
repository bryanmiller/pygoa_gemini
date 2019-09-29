# Python library for communicating with the Gemini Observatory Archive (GOA) using requests
# Bryan Miller
# Created 2019-sep-17

from __future__ import print_function
import requests
import os

home = os.environ['HOME']


def get_goa_authority(keydir=home):
    """
    Read the GOA authentication cookie stored in a a hidden file so that it is not embedded in code

    Parameters
        keydir:    Directory for authentication file, defaults to the home directory

    Return
        arch_session:   web cookie
    """
    
    keyfile = keydir + '/.goa_auth'
    
    try:
        with open(keyfile) as f:
            arch_session = f.read()
    except Exception as exc:
        print('get_goa_authority: error reading {}'.format(keyfile))
        raise exc

    return arch_session


def goa_json(user_request, option='jsonfilelist', verbose=False):
    """
    Query one of the GOA json APIs

    Parameters
        user_request:   Search request URL string, it should not contain 'jsonfilelist' or 'jsonsummary'
        option:         Valid options are jsonfilelist and jsonsummary

    Return
        request_json:   JSON query result as a list of dictionaries
    """

    options = ['jsonfilelist', 'jsonsummary']
    if option not in options:
        print('goa_json: option must be one of {}'.format(options))
        raise ValueError('Option must be one of {}'.format(options))
        
    response = requests.get(
        'https://archive.gemini.edu/' + option + '/' + user_request,
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        print('goa_json: request failed: {}'.format(response.text))
        raise exc
    else:
        request_json = response.json()

    if verbose:
        print(response.url)
    # print(response.text)

    return request_json


def goa_calmgr(user_request, verbose=False):
    """
    Query the GOA galmgr API

    Parameters
        user_request:   Search request URL string, it should not contain 'calmgr'
\
    Return
        request_xml:    Query result in XML format
    """

    response = requests.get(
        'https://archive.gemini.edu/calmgr/' + user_request,
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        print('goa_calmgr: request failed: {}'.format(response.text))
        raise exc
    else:
        request_xml = response.content

    if verbose:
        print(response.url)
    # print(response.text)

    return request_xml


def goa_file(user_request, filedir='./', tarfile='', option='file', cookie='', verbose=False):
    """
    Query the GOA to download a FITS file, TAR files, or preview PNG.

    Parameters
        user_request:   Search request URL string, it should not contain 'file', 'preview', or 'download'
        filedir:        Directory for the resulting file
        tarfile:        Name of the tar file if the option is 'download'
        option:         Valid options are file, preview, and download
        cookie:         Unique browser cookie for authentication, only needed to download proprietary data

    Return
        filename:       The name of the file that was written
    """

    options = ['file', 'preview', 'download']
    if option not in options:
        print('goa:file: option must be one of {}'.format(options))
        raise ValueError('Option must be one of {}'.format(options))

    l_user_request = user_request

    if option == 'download':
        if tarfile.strip() != '':
            filename = tarfile
        else:
            filename = 'gemini_data.tar'
    else:
        l_user_request = l_user_request.strip('.bz2')
        filename = l_user_request

    if option == 'preview':
        filename = filename + '.jpeg'

    response = requests.get(
        'https://archive.gemini.edu/' + option + '/' + l_user_request,
        headers={'Cookie': 'gemini_archive_session={}'.format(cookie)},
        stream=True
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        print('goa_file: request failed: {}'.format(response.text))
        raise exc
    else:
        with open(filedir + filename, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=128):
                fd.write(chunk)

    if verbose:
        print(response.url)

    return filename
