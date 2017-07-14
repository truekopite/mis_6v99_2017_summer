
# coding: utf-8

# In[1]:

import requests
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass
import pandas as pd


# In[2]:

#The link
link = 'https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip'
data = requests.get(link)


# In[3]:

new_dir = "staging_test" 
os.mkdir(new_dir) #Making a directory named 'staging_test'


# In[4]:

#Writing the ZIP file
medical_file =os.path.join(new_dir,"medicare_hospital_compare.zip")
medical = open(medical_file,"wb")
medical.write(data.content)
medical.close()


# In[5]:

#Extracting from ZIP file
med = zipfile.ZipFile(medical_file,'r')
med.extractall(new_dir)
med.close()


# In[6]:

#Create table
#a = a+b
#for column_name

#Insert into table
#sql_str = """insert into my_table(column_1,column_2,column_3) values(?,?,?)"""
#sql_tuple = ('a','b','c')
#c1.execute(sql_str,sql_tuple)
#conn.commit()


# In[7]:

#check if files exist
#print file names
conn = sqlite3.connect('medicare_hospital_compare.db')
c1 = conn.cursor()
main_dir = os.path.join(new_dir, "*.csv")
for file_name in glob.glob(main_dir):
    if os.path.basename(file_name) != 'FY2015_Percent_Change_in_Medicare_Payments.csv':
        os.chdir(new_dir)
        name = os.path.basename(file_name)
        #print(name)
        fn = os.path.join(new_dir,name)
        in_fp = open(name,"rt",encoding='cp1252')
        input_data = in_fp.read()
        in_fp.close()
        new_name = name + "_fix"
        #ofn = os.path.join(new_dir,new_name)
        #print(new_name)
        out_fp = open(new_name,"wt",encoding='utf-8')
        for c in input_data:
            if c != '\0':
                out_fp.write(c)       
        out_fp.close()
        df = pd.read_csv(new_name, dtype=str)
        #print(df.columns)
        new_name = new_name.lower()
        new_name = new_name.replace(".csv_fix", "")
        new_name = new_name.replace(" ", "_")
        new_name = new_name.replace("-", "_")
        new_name = new_name.replace("%", "pct")
        new_name = new_name.replace("/", "_")
        if (new_name[0].isalpha() != 1):
            new_name = "t_" +new_name
     #  sql_str = """ create table if not exists """+ new_name
        #for col_name in df.columns:
        #print(df.columns)
        df.rename(columns = lambda x: x.lower(), inplace = True)
        df.rename(columns = lambda x: x.replace(' ', '_'), inplace = True)
        df.rename(columns = lambda x: x.replace('-', '_'), inplace = True)
        df.rename(columns = lambda x: x.replace('%', 'pct'), inplace = True)
        df.rename(columns = lambda x: x.replace('/', '_'), inplace = True)
            #col_name = col_name.lower()
            #col_name = col_name.replace(" ", "_")
            #col_name = col_name.replace("-", "_")
            #col_name = col_name.replace("%", "pct")
            #col_name = col_name.replace("/", "_")
        df.rename(columns = lambda x: "c_" + x if x[0].isalpha() != 1 else x, inplace = True)
       #    c.execute("""alter table """+ new_name+""" add column """+ col_name + """ text""")
        #print(df)
        df.to_sql(new_name, conn, if_exists='replace', index = False)
     #  col = df.columns
      # print(col)
        #sql_str = """ create table if not exists """+ new_name+ """("""+col+""" text)"""
      #c1.execute(sql_str)
        os.chdir("../")
                #file.str.encode('utf-8')
        #print(file_name)
        #print("    basename:",os.path.basename(file_name))
        #print("    split extension:",os.path.splitext(file_name))
        #print("    dir name:",os.path.dirname(file_name))
        #print("    abs path:",os.path.abspath(file_name))
    else:
        continue
conn.commit()


# In[8]:

#name = os.path.basename(file_name).lower()
#name


# In[9]:

#name.replace(" ", "_")
#pandas.DataFrame.from_csv
#type(df.columns)
#for i in col:
#    print (i)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[10]:

#sql_str = """drop table if exists my_table"""


# In[11]:

#c1.execute(sql_str)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



