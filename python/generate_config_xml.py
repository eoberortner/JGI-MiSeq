'''
Created on Jul 23, 2015

@author: Ernst Oberortner
'''

CONFIG_XML_HEADER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<SBAnalysis>
<analysis name="{}" 
    reference="/global/scratch2/sd/synbio/sequencing/illumina/{}/ref/references.fasta" 
    location="/global/scratch2/sd/synbio/sequencing/illumina">
'''

CONFIG_XML_FOOTER = '''        
</analysis>

</SBAnalysis>'''


POOL_TAG = '''
    <pool name="{}" samples="{}">
        <job name="bwa_dir" protocol="bwa_dir"/>
    </pool>'''


if __name__ == '__main__':
    
    ## input:
    ## -- libraries.info
    ## -- references.fasta
    ##library_name = '072315_ANZPH'
    library_name = '072315_ANZUA'
    
    CONFIG_XML = CONFIG_XML_HEADER.format(library_name, library_name)
        
    with open('../data/libraries/{}/libraries.info'.format(library_name)) as libs:
        
        for line in libs:
            line_elements = line.split('\t')
            CONFIG_XML = CONFIG_XML + POOL_TAG.format(line_elements[0].strip(),line_elements[0].strip())
            
    CONFIG_XML = CONFIG_XML + CONFIG_XML_FOOTER
    
    print CONFIG_XML
    
    pass