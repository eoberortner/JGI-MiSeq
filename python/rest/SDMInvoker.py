'''
Created on Jul 28, 2015

@author: Ernst Oberortner
'''

import requests, json

class SDMInvoker(object):
    '''
    The SDMInvoker class provides (mainly static) methods to 
    invoke the API of JGI's Data Management Platform (SDM)
    
    URL: https://sdm2.jgi-psf.org
    '''

    SDM_API_URL = 'https://sdm2.jgi-psf.org/api/illumina'
    
    SUPPORTED_FUNCTIONS = {'library':'library'}
    
    @staticmethod
    def loadLibraryData(libraryName):
        
        REQUEST_URL = '{}/{}/{}'.format(SDMInvoker.SDM_API_URL, SDMInvoker.SUPPORTED_FUNCTIONS['library'], libraryName)
        
        ## send the request to the URL above
        r = requests.get(REQUEST_URL)
        if r.status_code == 200:
            
            print r.content
            
            libraryInfo = json.loads(r.content)
            
            print libraryInfo
            
#             if "library_info" in libraryInfo:
#                 if "pooled_list" in libraryInfo["library_info"]:
#                     return libraryInfo["library_info"]["pooled_list"]
        
        return None
        
        
        
        
        
        
        
        