'''
Created on Jul 28, 2015

@author: Ernst Oberortner
'''

import requests, json

from Bio import SeqIO

class SDMInvoker(object):
    '''
    The SDMInvoker class provides (mainly static) methods to 
    invoke the API of JGI's Data Management Platform (SDM)
    
    URL: https://sdm2.jgi-psf.org
    '''

    SDM_API_URL = 'https://sdm2.jgi-psf.org/api/illumina'
    SDM_DEV_API_URL = 'https://sdm-dev.jgi-psf.org:8034'
    
    SUPPORTED_FUNCTIONS = {'library':'library', 'seq unit' : 'sdmsequnit'}
    
    JSON_KEYS = {'seq unit id':"sdm_seq_unit_id", 'children':'children', 'library name':'library_name'}
    
    @staticmethod
    def loadLibraryData(libraryName):
        
        LIBRARY_INFO_URL = '{}/{}/{}'.format(SDMInvoker.SDM_API_URL, SDMInvoker.SUPPORTED_FUNCTIONS['library'], libraryName)
        
        ## send the request to the URL above
        libInfoReq = requests.get(LIBRARY_INFO_URL)
        if libInfoReq.status_code == 200:
            
            libraryInfo = json.loads(libInfoReq.content)
            
            ## 
            seqUnitID = libraryInfo[0][SDMInvoker.JSON_KEYS.get('seq unit id')]
            
            ## load the IDs of the child libraries
            SEQ_UNIT_URL = '{}/{}/{}'.format(SDMInvoker.SDM_API_URL, SDMInvoker.SUPPORTED_FUNCTIONS['seq unit'], seqUnitID)
            seqUnitResp = requests.get(SEQ_UNIT_URL)
            if seqUnitResp.status_code == 200:
                
                seqUnit = json.loads(seqUnitResp.content)
                
                for children in seqUnit[SDMInvoker.JSON_KEYS.get("children")]:
                   
                    print children
                    subLibraryName = children[SDMInvoker.JSON_KEYS.get('library name')]
                    subLibraryID = children[SDMInvoker.JSON_KEYS.get('seq unit id')]
                    SUB_SEQ_UNIT_URL = '{}/{}/{}'.format(SDMInvoker.SDM_API_URL, SDMInvoker.SUPPORTED_FUNCTIONS['seq unit'], subLibraryID)

                    subSeqUnitResp = requests.get(SUB_SEQ_UNIT_URL)
                    if subSeqUnitResp.status_code == 200:
                        print '*** {} ***'.format(subLibraryName)
                        subSeqUnit = json.loads(subSeqUnitResp.content)
                        
                        for fastqFileInfo in subSeqUnit['files']:
                            if fastqFileInfo['file_type'] == 'FASTQ':
                                print '{}/{}'.format(fastqFileInfo['fs_location'], fastqFileInfo['file_name'])
                                #fastqFilename = '{}/{}'.format(fastqFile['fs_location'], fastqFile['file_name'])
                                #handle = open(fastqFilename, "rU")
                                #for record in SeqIO.parse(handle, "fastq-illumina") :
                                #    print record.id
                                
                                print '{}/api/metadata/query'.format(SDMInvoker.SDM_DEV_API_URL)
                                
                                #queryData = {'file_type':'fastq.gz','metadata.library_name':'{}'.format(subLibraryName)}
                                queryData = {'file_type':'fastq.gz','metadata.library_name':'AAONP'}
                                fastqFileResp = requests.post('{}/api/metadata/query'.format(SDMInvoker.SDM_API_URL), queryData)
                                
                                if fastqFileResp.status_code == 200:
                                    print json.loads(fastqFileResp.content)
                                
                                else:
                                    print 'Something went wrong! wrong URL perhaps?'
                                    print fastqFileResp.content

                    
                
                
#             if "library_info" in libraryInfo:
#                 if "pooled_list" in libraryInfo["library_info"]:
#                     return libraryInfo["library_info"]["pooled_list"]
        
        return None
        
        
        
# /global/seqfs/sdm/prod/illumina/staging/miseq09/150505_M02100_0157_000000000-AEFR7/9050.1.118433.TAAGGCG-CTCTCTA.fastq.gz        
# /global/seqfs/sdm/prod/illumina/staging/miseq09/150505_M02100_0157_000000000-AEFR7/9050.1.118433.TAAGGCG-CTCTCTA.fastq.gz            
        
        
        