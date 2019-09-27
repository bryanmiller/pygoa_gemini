#!/usr/bin/env python

# Examples of using pygoa to use the Gemini Observatory Archive APIs
# Bryan Miller

import pygoa.pygoa as pygoa
import os
import xml.etree.cElementTree as ElementTree

home = os.environ['HOME']


if __name__ == "__main__":

    # First we work though some of the examples from
    # https://archive.gemini.edu/help/api.html
    # using pygoa for the requests boilerplate.

    # jsonfilesummary
    # Returns a JSON representation of a full set of information on the files that match the query.
    # This is equivalent to the interactive search form.
    # Including /canonical is recommended in order to retrieve information on the latest versions of the files.
    query = '/canonical/OBJECT/GMOS-N/20101231'
    try:
        results = pygoa.goa_json(query, option='jsonsummary')
    except (ValueError, Exception):
        pass
    else:
        total_data_size = 0
        print("{:20} {:22} {:10} {:8} {}".format("Filename", "Data Label", "ObsClass", "QA state", "Object Name"))
        for r in results:
            total_data_size += r['data_size']
            print("{:20} {:22} {:10} {:8} {}".format(r['name'], r['data_label'],
                                                     r['observation_class'], r['qa_state'], r['object']))
        print("Total data size: {:d}".format(total_data_size))

    # jsonfilelist
    # Returns a JSON representation of a brief set of information of the files that match the query.
    # Including /canonical is recommended in order to retrieve information on the latest versions of the files.

    # Name of file to download later, for the example this will be the first file in the jsonfilelist results.
    filedown = ''

    query = '/canonical/GN-2010B-Q-22/GMOS-N/20101231'
    try:
        results = pygoa.goa_json(query, option='jsonfilelist')
    except (ValueError, Exception):
        pass
    else:
        for r in results:
            print("Filename: {:s}".format(r['filename']))
            print("-- file size: {:d}, data size: {:d}".format(r['file_size'], r['data_size']))
            if filedown == '':
                filedown = r['filename']

    # Here are examples of additional useful features.

    # calmgr
    # Returns an XML representation of the the science files that match a query plus the associated
    # Different calibration types can be specified,
    # e.g. bias, processed_bias, flat, processed_flat, photometric_standard
    # calibrations of each.
    try:
        xml = pygoa.goa_calmgr(query + '/photometric_standard')
    except (ValueError, Exception):
        pass
    else:
        results = ElementTree.fromstring(xml)
        # Need to add a URL tag to the field names, see
        # https://docs.python.org/2/library/xml.etree.elementtree.html#parsing-xml-with-namespaces
        url = results.tag[0:results.tag.find('}')+1]
        # print(url, url[1:-1])
        for dataset in results.findall(url+'dataset'):
            print(dataset.find(url+'datalabel').text, dataset.find(url+'filename').text, dataset.find(url+'md5').text)
            for cal in dataset.findall(url+'calibration'):
                print(cal.find(url+'caltype').text, cal.find(url+'datalabel').text, cal.find(url+'filename').text,
                      cal.find(url+'url').text, cal.find(url+'md5').text)
            print('')

        # Alternative
        # ns = {'url': url[1:-1]}
        # for dataset in results.findall('url:dataset', ns):
        #     print(dataset.find('url:datalabel', ns).text)

    # Get authentication cookie for downloading proprietary data (optional)
    # The instructions at https://archive.gemini.edu/help/api.html are out of date
    # 0) Login to https://archive.gemini.edu
    # Safari
    #   1) Go to Preferences - Advanced and turn on "Show Develop menu in menu bar"
    #   2) Click "Show Web Inspector" in the Develop menu
    #   3) Select Cookies in the Storage tab. The cookie you need is called gemini_archive_session.
    #
    # Firefox
    #   1) Select Tools->Web Developer->Storage Inspector
    #   2) Click on "Cookies" and select "https://archive.gemini.edu"
    #      The cookie you need is called gemini_archive_session.
    #
    # Chrome
    #   1) Select View->Developer->Developer Tools
    #   2) Click on "Cookies" and select "https://archive.gemini.edu"
    #      The cookie you need is called gemini_archive_session.
    #
    # Copy the value of the cookie and store it in a hidden file called <path>/.goa_auth.
    # By default get_goa_authority assumes that this is in the home directory, but the path (keydir)
    # can be specified.
    goa_auth = ''
    try:
        goa_auth = pygoa.get_goa_authority(keydir=home)
    except (ValueError, Exception):
        # exit()
        # This should exit if it fails, but for this example all the data is public, no authentication required
        pass

    # Download a jpeg preview of a particular file.
    try:
        file = pygoa.goa_file(filedown, filedir=home + '/Downloads/', option='preview',
                              cookie=goa_auth)
    except (ValueError, Exception):
        pass
    else:
        print(file + ' downloaded.')

    # Download a single FITS file. It will be uncompressed.
    try:
        file = pygoa.goa_file(filedown, filedir=home + '/Downloads/', option='file',
                              cookie=goa_auth)
    except (ValueError, Exception):
        pass
    else:
        print(file + ' downloaded.')

    # Download a TAR file of all files that match the query
    try:
        file = pygoa.goa_file(query, filedir=home + '/Downloads/', tarfile='gnQ22_20101231.tar',
                              option='download', cookie=goa_auth, verbose=False)
    except (ValueError, Exception):
        pass
    else:
        print(file + ' downloaded.')

    # Download a TAR file of all the associated calibration files for the query
    # As specified, this is a 3.36 GB download
    # try:
    #     file = pygoa.goa_file('/associated_calibrations/' + query,
    #                           filedir=home + '/Downloads/', tarfile='gnQ22_std_20101231.tar',
    #                           option='download', cookie=goa_auth)
    # except (ValueError, Exception):
    #     pass
    # else:
    #     print(file + ' downloaded.')
