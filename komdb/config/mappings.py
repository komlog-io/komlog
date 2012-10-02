'''
Created on 02/10/2012

@author: jcazor
'''

MAPPING_MODULES = ['states','types']

MAPPING_OBJECTS = {'TYPE:AGENT':'AgentType','TYPE:USER':'UserType',
                   'TYPE:DATASOURCE':'DatasourceType', 'TYPE:SAMPLE':'SampleType',
                   'STATE:USER':'UserState','STATE:AGENT':'AgentState',
                   'STATE:DATASOURCE':'DatasourceState','STATE:SAMPLE':'SampleState',
                   'STATE:DATAPOINT':'DatapointState'}

MAPPING_CONSTANTS = {'TYPE':0,'FIELD':1,'SUBTYPE':2,'ELEMENT':3}

MAPPING_PARAMS = {'AgentType':'VALUE:DESCRIPTION',
                  'UserType':'VALUE:DESCRIPTION',
                  'DatasourceType':'VALUE:DESCRIPTION',
                  'SampleType':'VALUE:DESCRIPTION',
                  'UserState':'VALUE:DESCRIPTION',
                  'AgentState':'VALUE:DESCRIPTION',
                  'DatasourceState':'VALUE:DESCRIPTION',
                  'SampleState':'VALUE:DESCRIPTION',
                  'DatapointState':'VALUE:DESCRIPTION'}



def map_messages_to_objects(constants):
    """
    This function receives an array of tuples, each one representing
    a constant with its value. It returns an array of object types and 
    the necessary parameters to create those objects.
    """
    count_type=0
    count_subtype=0
    count_element=0
    
    map_type={}
    map_subtype={}
    map_element={}
    
    
    """ In this block, we create a MAP regarding the constants received"""
    for constant in constants:
        if constant[0][0:2]=='__':
            continue
        splitted_constant = constant[0].split('_')
        objtype = splitted_constant[MAPPING_CONSTANTS['TYPE']]
        objsubtype = splitted_constant[MAPPING_CONSTANTS['SUBTYPE']]
        element = splitted_constant[MAPPING_CONSTANTS['ELEMENT']]
        if not map_type.has_key(objtype):
            map_type[objtype]=count_type
            count_type+=1
        if not map_subtype.has_key(objsubtype):
            map_subtype[objsubtype]=count_subtype
            count_subtype+=1
        if not map_element.has_key(element):
            map_element[element]=count_element
            count_element+=1
            
    """ In this block we join the values received of each constant"""
    constant_index = {}
    
    for constant in constants:
        if constant[0][0:2]=='__':
            continue
        splitted_constant = constant[0].split('_')
        value = constant[1]
        objtype = splitted_constant[MAPPING_CONSTANTS['TYPE']]
        objsubtype = splitted_constant[MAPPING_CONSTANTS['SUBTYPE']]
        element = splitted_constant[MAPPING_CONSTANTS['ELEMENT']]
        index = str(map_type[objtype])+':'+str(map_subtype[objsubtype])+':'+str(map_element[element])
        objectType = MAPPING_OBJECTS[str(objtype)+':'+str(objsubtype)]
        if constant_index.has_key(index):
            value = constant_index[index].replace(splitted_constant[MAPPING_CONSTANTS['FIELD']], str(constant[1]))
        else:
            value = str(MAPPING_PARAMS[objectType]).replace(splitted_constant[MAPPING_CONSTANTS['FIELD']], str(constant[1]))      
        constant_index[index]=value
    
    
    """ In this block we generate the entry containing the params and objectype"""
    entry_list = []
            
    for index, value in constant_index.iteritems():
        splitted_index = index.split(':')
        objtype =  [k for k,v in map_type.iteritems() if v==int(splitted_index[0])][0]
        objsubtype = [k for k,v in map_subtype.iteritems() if v==int(splitted_index[1])][0]
        entry = [MAPPING_OBJECTS[str(objtype)+':'+str(objsubtype)]]
        for argument in value.split(':'):
            entry.append(argument)
        entry_list.append(entry)

    return entry_list  