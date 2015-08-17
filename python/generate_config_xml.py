'''
Created on Jul 23, 2015

@author: Ernst Oberortner
'''

CONFIG_XML_HEADER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<SBAnalysis>
<analysis name="{}" 
    reference="{}/{}/ref/references.fasta" 
    location="{}">
'''

CONFIG_XML_FOOTER = '''        
</analysis>

</SBAnalysis>'''


POOL_TAG = '''
    <pool name="{}" samples="{}">
        <job name="bwa_dir" protocol="bwa_dir"/>
    </pool>'''


def generateConfigXML(base_dir, library_name, list_of_sublibraries):
    
    ## HEADER information
    CONFIG_XML_CONTENT = CONFIG_XML_HEADER.format(library_name, base_dir, library_name, base_dir)

    for subLibrary in list_of_sublibraries:
        
        CONFIG_XML_CONTENT = CONFIG_XML_CONTENT + POOL_TAG.format(subLibrary, subLibrary)

    ## content of the config.xml file            
    CONFIG_XML_CONTENT = CONFIG_XML_CONTENT + CONFIG_XML_FOOTER
    
    ## write the content of the CONFIG_XML variable 
    ## to the config.xml file
    fConfigXML = open('{}/{}/config.xml'.format(base_dir, library_name), 'w')
    fConfigXML.write(CONFIG_XML_CONTENT)
    fConfigXML.flush()
    fConfigXML.close()


if __name__ == '__main__':
        
    ##
    ## NERSC USAGE
    ##
    
    ## input:
    ## -- libraries.info
    ## -- references.fasta
    base_dir = '/global/scratch2/sd/synbio/sequencing/illumina/'
    ##library_name = '081115_ANZUA'
    ##library_name = '072315_ANZUA'
    
    ##library_name = '080415_ANZPH'
    #library_name = '081215_ANZPH'
    library_name = '081515_AOSPB'
    
    CONFIG_XML_CONTENT = CONFIG_XML_HEADER.format(library_name, base_dir, library_name, base_dir)
        
    with open('../data/libraries/{}/libraries.info'.format(library_name)) as libs:
        for line in libs:
            line_elements = line.split('\t')
            
            library_dir = line_elements[0].strip() + '_' + line_elements[1].strip()
            CONFIG_XML_CONTENT = CONFIG_XML_CONTENT + POOL_TAG.format(library_dir, library_dir)
        
        libs.close()

    ## content of the config.xml file            
    CONFIG_XML_CONTENT = CONFIG_XML_CONTENT + CONFIG_XML_FOOTER
    
    ## write the content of the CONFIG_XML variable 
    ## to the config.xml file
    fConfigXML = open('{}/{}/config.xml'.format(base_dir, library_name), 'w')
    fConfigXML.write(CONFIG_XML_CONTENT)
    fConfigXML.flush()
    fConfigXML.close()
     
    pass