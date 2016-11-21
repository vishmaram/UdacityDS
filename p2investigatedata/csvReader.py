import unicodecsv

# this creates list of dictionary
def read_csv(filePath):
    with open(filePath,'rb') as f:
        reader = unicodecsv.DictReader(f)
        return list(reader)