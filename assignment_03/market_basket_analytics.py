
# coding: utf-8

# In[1]:

import pandas as pd
import requests
import numpy
import csv
from operator import itemgetter
import itertools


# In[2]:

#The train link
link = 'http://kevincrook.com/utd/market_basket_training.txt'
#Putting the train file in the directory
data = requests.get(link)
train_file = "market_basket_training.txt"
#Reading the train file
train = open(train_file,"wb")
train.write(data.content)
train.close()


# In[3]:

#The test link
link = 'http://kevincrook.com/utd/market_basket_test.txt'
#Putting the test file in the directory
data = requests.get(link)
test_file = "market_basket_test.txt"
#Reading the testfile
test = open(test_file,"wb")
test.write(data.content)
test.close()


# In[4]:

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
    #Split into set based on delimiter
    rand = row["sets"].split("|")
    return set(rand)

#Function to find all subset with size-1
def subsets(Set,n):
    return list(itertools.combinations(Set, n))


#Find the recommended product
def appended_list(a, b):
    final_list = []
    the_list = a
    new_set = b
    for ele in the_list:
        temp_set = set(ele)
        ctr = 0
        temp = []
        for index,row in mod_df_train.iterrows():
            comp = row[1]
            #Finding wors that match the conditions
            if temp_set < comp and len(comp) == len(temp_set)+1:
                ctr += 1
        temp.append(temp_set)
        temp.append(ctr)
        final_list.append(temp)
    #Sort the list
    final_list = sorted(final_list, key=lambda x: x[1],reverse=True)
    final_reccom = final_list[0][0]
    final_ctr = final_list[0][1]
    #Return the test set back to make smaller size subsets
    if final_ctr ==0:
        return new_set,final_ctr
    else:
        return final_reccom,final_ctr

#Finding subsets
def all_combination(new, length):
    #Calculating subset size
    length -= 1
    subs = subsets(new,length)
    new_set, new_length = appended_list(subs, new)
    #Function to exaluate subsets
    if new_length == 0:
        return all_combination(new_set, length)
    else:
        return new_set

#The recommendation
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
        #Sort the list
        final_list = sorted(final_list, key=lambda x: x[1],reverse=True)
        #Final recommendation
        final_reccom = final_list[0][0]
        return final_reccom
    elif len(final_list) == 0:
        leng = len(temp_set)
        new = all_combination(temp_set, leng)
        #The recommendation fucntion
        return the_reccom(new)


# In[5]:

#Assigning column header for simplicity
train_column = ["cart_num","prod_1","prod_2","prod_3","prod_4"]
test_column = ["cart_num","prod_1","prod_2","prod_3"]
#Reading the file
df_train = pd.read_csv(train_file, dtype="str",index_col="cart_num", names=train_column)
df_test = pd.read_csv(test_file, dtype="str",index_col="cart_num", names=test_column)
#Filling NA values
new_df_train = pd.DataFrame(df_train.fillna(0))
new_df_test = pd.DataFrame(df_test.fillna(0))
#Create new column - sets
new_df_train["sets"] = new_df_train.apply(lambda row: update_df(row),axis=1)
new_df_test["sets"] = new_df_test.apply (lambda row: update_df(row),axis=1)
#Create new column - count
new_df_train["count"] = 0
mod_df_train = pd.DataFrame(new_df_train.groupby(["sets"])["count"].count()).reset_index()
#Create new column - calues
mod_df_train["values"] = mod_df_train.apply(lambda row: create_set(row),axis=1)
#Drop the column - sets
mod_df_train.drop('sets', axis=1, inplace=True)
#Create new column - recomm
new_df_test["recomm"] = new_df_test.apply(lambda row: the_reccom(set(row[3].split("|"))),axis=1)
new_df_test_temp = pd.read_csv(test_file, dtype="str", names = test_column)
new_df_test_temp.index += 1
#Join two columns to create dataframe
new_df_test_temp = pd.concat([new_df_test_temp["cart_num"], new_df_test["recomm"]], axis=1)
#Write final recommendation to file
new_df_test_temp.to_csv("market_basket_recommendations.txt",header = False, index = False, encoding =  'utf-8')


# In[ ]:



