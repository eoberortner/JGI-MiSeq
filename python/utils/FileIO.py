'''
Created on Aug 17, 2015

@author: eoberortner
'''

class FileIO(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
     
    @staticmethod
    def writeSublibraries(subLibraries):
        
        ## open file
        f = open('sub.libraries.info', 'w')
        
        i = 0
        for subLibrary in subLibraries:
            f.write('{}'.format(subLibrary))
            
            i = i + 1
            
            if i < len(subLibraries):
                f.write('\n')
            
        
        f.close() 