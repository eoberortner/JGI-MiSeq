'''
Created on Jul 23, 2015

@author: Ernst Oberortner
'''

import requests, json
import sys
from utils.FileIO import FileIO 

def usage():
    print "get_RQC_library_info library_name"
    sys.exit(1)
    
def processArguments(argv):
    if len(argv) != 2:
        usage()
    
    return argv[1]
    
if __name__ == '__main__':

    libraryName = processArguments(sys.argv)    
    #library_name = 'ANZUA'
    #library_name = 'ANZPH'
    #library_name = 'AAONP'
    
    ## retrieve the sub-libraries from the RQC API
    r = requests.get('https://rqc.jgi-psf.org/api/library/info/{}'.format(libraryName))
    
    #sublibraries = []
    if r.status_code == 200:
        library_info = json.loads(r.content)
        
        subLibraries = []
        s = ''
        for subLibrary in library_info["library_info"]["pooled_list"]:
            
            s = '{} {}'.format(s, subLibrary["library_name"])
            subLibraries.append(subLibrary["library_name"])
            
        #print library_info["library_info"]
        
        ## write the names of the sublibraries to a file 
        FileIO.writeSublibraries(subLibraries)
        
    pass