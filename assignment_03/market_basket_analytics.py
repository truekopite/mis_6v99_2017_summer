
# coding: utf-8

# In[ ]:

import pandas as pd
import requests
import numpy
import csv
from operator import itemgetter
import itertools


# In[ ]:

#The train link
link = 'http://kevincrook.com/utd/market_basket_training.txt'
#Putting the train file in the directory
data = requests.get(link)
train_file = "market_basket_training.txt"
#Reading the train file
train = open(train_file,"wb")
train.write(data.content)
train.close()


# In[ ]:

#The test link
link = 'http://kevincrook.com/utd/market_basket_test.txt'
#Putting the test file in the directory
data = requests.get(link)
test_file = "market_basket_test.txt"
#Reading the testfile
test = open(test_file,"wb")
test.write(data.content)
test.close()


# In[ ]:

#Function to tweak sets
def update_df(row):
    data_frame = [] 
    for ele in row:
        if not(ele  == 0):
            data_frame.append(str(ele))
    #Convert dataframe to set
    set_data_frame = set(data_frame)
    #Sort the dataframe
    sort_frame = sorted(set_data_frame, key=lambda item: int(item.split("P")[1]))
    #Joining the sets with | in between
    joined_frame = '|'.join(sort_frame)
    return joined_frame

#Function to convert string to set
def create_set(row):
    rand = row["sets"].split("|")
    return set(rand)

#Function to find all subset with size-1
def subsets(Set,n):
    return list(itertools.combinations(Set, n))


def appended_list(a):
    final_list = []
    the_list = a
    for ele in the_list:
        temp_set = set(ele)
        ctr = 0
        temp = []
        for index,row in mod_df_train.iterrows():
            comp = row[1]
            if temp_set < comp and len(comp) == len(temp_set)+1:
                ctr += 1
        temp.append(temp_set)
        temp.append(ctr)
        final_list.append(temp)
    final_list = sorted(final_list, key=lambda x: x[1],reverse=True)
    final_reccom = final_list[0][0]
    final_ctr = final_list[0][1]
    return final_reccom, final_ctr

def all_combination(new):
    length = len(new)
    subs = subsets(new,length-1)
    new_set, new_length = appended_list(subs)
    if new_length == 0:
        return all_combination(new_set)
    else:
        return new_set
    
def the_reccom(temp_set):
    final_list = []
    for index,row in mod_df_train.iterrows():
        comp = row[1]
        temp = []
        if temp_set < comp and len(comp) == len(temp_set)+1:
            diff = comp - temp_set
            temp.append(diff.pop())
            temp.append(row[0])
            final_list.append(temp)
    if len(final_list) != 0:
        final_list = sorted(final_list, key=lambda x: x[1],reverse=True)
        final_reccom = final_list[0][0]
        return final_reccom
    elif len(final_list) == 0:
        new = all_combination(temp_set)
        return the_reccom(new)


# In[ ]:

#Assigning column header for simplicity
train_column = ["cart_num","prod_1","prod_2","prod_3","prod_4"]
test_column = ["cart_num","prod_1","prod_2","prod_3"]
df_train = pd.read_csv(train_file, dtype="str",index_col="cart_num", names=train_column)
df_test = pd.read_csv(test_file, dtype="str",index_col="cart_num", names=test_column)
#Filling NA values
new_df_train = pd.DataFrame(df_train.fillna(0))
new_df_test = pd.DataFrame(df_test.fillna(0))
new_df_train["sets"] = new_df_train.apply(lambda row: update_df(row),axis=1)
new_df_test["sets"] = new_df_test.apply (lambda row: update_df(row),axis=1)
new_df_train["count"] = 0
mod_df_train = pd.DataFrame(new_df_train.groupby(["sets"])["count"].count()).reset_index()
mod_df_train["values"] = mod_df_train.apply(lambda row: create_set(row),axis=1)
mod_df_train.drop('sets', axis=1, inplace=True)
new_df_test["recomm"] = new_df_test.apply(lambda row: the_reccom(set(row[3].split("|"))),axis=1)
new_df_test_temp = pd.read_csv(test_file, dtype="str", names = test_column)
new_df_test_temp.index += 1
new_df_test_temp = pd.concat([new_df_test_temp["cart_num"], new_df_test["recomm"]], axis=1)
new_df_test_temp.to_csv("market_basket_recommendations.txt",header = False, index = False, encoding =  'utf-8')


# In[ ]:



