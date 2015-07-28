'''
Created on Jul 23, 2015

@author: eoberortner
'''

import requests, json
import StringIO

if __name__ == '__main__':
    
#    library_name = 'ANZUA'
    library_name = 'ANZPH'
    r = requests.get('https://rqc.jgi-psf.org/api/library/info/{}'.format(library_name))
    
    
    #sublibraries = []
    if r.status_code == 200:
        library_info = json.loads(r.content)
        
        sublibraries = json.load(library_info["library_info"]["pooled_list"])
        
        #for subLibrary in library_info["library_info"]["pooled_list"]:
        #    sublibraries.append(subLibrary["library_name"])
            
        #print library_info["library_info"]
    
        print sublibraries    
    pass