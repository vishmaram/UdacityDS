# this file is used to do set operation

def get_unique_set(data,dataField):
    s = set()
    for row in data:
        s.add(row[dataField])
    return s

# Get keys from orgset that are not in destSet
def get_key_set_not_in(orgSet,destSet):
    s = set()
    for key in orgSet:
        if key not in destSet:
            s.add(key)
    return s

# creates a list of data that hasdatafield in dataFieldSEt
def filter_data_with_keys(data,dataField,dataFieldSet):
    l = list()
    for row in data:
        if row[dataField] in dataFieldSet:
            l.append(row)
    return l

# creates a list of data that does not have datafield in dataFieldSEt
def filter_data_without_keys(data,dataField,dataFieldSet):
    l = list()
    for row in data:
        if row[dataField] not in dataFieldSet:
            l.append(row)
    return l
