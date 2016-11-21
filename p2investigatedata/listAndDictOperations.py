from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


def get_data_grouped_by_field(data,datafield):
    data_by_account = defaultdict(list)
    for row in data:
        data_by_account[row[datafield]].append(row)
    return data_by_account

def get_sum_byField(data,dataField):
    val = 0.0
    for row in data:
        val += row[dataField]
    return val

# get row count with field value greater than zero
def get_rowcount_with_field_greater_than_zero(data,dataField):
    val = 0.0
    for row in data:
        if row[dataField] > 0:
            val +=1
    return val

def get_list_of_dataField(data,dataField):
    l = list()
    for row in data:
        l.append(row[dataField])
    return l

def describe_data(data, title=None, xlabel=None, bins=None):
    print "\n mean : ", np.mean(data)
    print " standard deviation :", np.std(data)
    print " Minimum : ", np.min(data)
    print " Max : ", np.max(data)
    if bins != None:
        plt.hist(data,bins)
    else: plt.hist(data)
    if title != None:
        plt.title(title)
    if xlabel != None:
        plt.xlabel(xlabel)
