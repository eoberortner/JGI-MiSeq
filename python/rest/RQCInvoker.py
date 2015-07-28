'''
Created on Jul 28, 2015

@author: Ernst Oberortner
'''

import requests, json

class RQCInvoker(object):
    '''
    The RQCInvoker class provides (mainly static) methods to 
    invoke the API of JGI's RQC
    '''

    RQC_API_URL = 'https://rqc.jgi-psf.org/api'
    
    SUPPORTED_FUNCTIONS = {'library':'library/info'}
    
    @staticmethod
    def loadLibrary(libraryName):
        
        REQUEST_URL = '{}/{}/{}'.format(RQCInvoker.RQC_API_URL, RQCInvoker.SUPPORTED_FUNCTIONS['library'], libraryName)
        
        ## send the request to the URL above
        r = requests.get(REQUEST_URL)
        if r.status_code == 200:
            
            libraryInfo = json.loads(r.content)
            if "library_info" in libraryInfo:
                if "pooled_list" in libraryInfo["library_info"]:
                    return libraryInfo["library_info"]["pooled_list"]
        
        return None
        
        
        
        
        
        
        
        