'''
Created on Jul 28, 2015

@author: Ernst Oberortner
'''

import pycurl

if __name__ == '__main__':
    
    curl = pycurl.Curl()
    files = curl.post('https://sdm-dev.jgi-psf.org:8034/api/metadata/query',data={'file_type':'fastq.gz','metadata.library_name':'HYCU'})
    
    print files
    
    pass