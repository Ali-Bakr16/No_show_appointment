#!/usr/bin/env python
# coding: utf-8

# # Database_No_show_appointments 

# ## Introduction
# 

# ### Import all the packages I will need.

# In[1]:


# Import packages that will used 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ### Load data csv file and print first five rows 
#  Discaver information about the data to analysis it

# In[2]:


# Load our data and print the first 5 rows
df = pd.read_csv('database_new.csv')
df.head()


# In[3]:


# Print the shape of our dataframe
df.shape


# In[4]:


# Print all information about datafram (dtype , non null count)
df.info()


# ### Note
# there is no null value in this database.

# In[5]:


# Round data to 3 number after dismil point becouse results were so big
df.describe().round(3)


# # Data Wrangling;

# 
# ### What will i do
# 1- convert all database columns to lower                
# 2- convert patientid from float to int              
# 3- convert scheduleday and appointmentday from object to datetime

# In[6]:


# Convert all columns to lowercase 
df.rename(columns= lambda x : x.strip().lower().replace('-','_'),inplace = True)


# In[7]:


# Modify some columns name to be easy to read
df.rename(columns = {'patientid':'patient_id', 'appointmentid' : 'appointment_id','scheduledday':'scheduled_day','appointmentday':'appointment_day'},inplace = True)


# In[8]:


# Convert scheduled_day and appointment_day to datetime 
df['scheduled_day'] = pd.to_datetime(df['scheduled_day'])
df['appointment_day'] = pd.to_datetime(df['appointment_day'])


# In[9]:


df.head(20)


# In[10]:


# Function to print describation statistics for specific column 
def MyFunc(dataframe,colname):
    print(dataframe[colname].describe())
MyFunc(df,'age')


# In[11]:


df.duplicated().sum()


# ## Note 
# There is no duplicate values 

# # Questions

# Q : What is the most age patients suffer from diabetes ?    
# Q : the average of patient that suffer from diabetes?        
# Q : What is the most gender that have diabetes?     
# Q : What is the most age people drink alcohol?        
# Q : What is the most gender suffer from diabetes?
# Q : What is the most hospital resive patients?      
# Q : What is the gender that drinke alcohol very much?        
# Q : Number of patients that scholarship? Did all registered patients attend the examination?           
# Q : Is there a relationship between diabetes and alcoholism ?        
# Q : What factors are important for us to know in order to predict if a patient will show up for their scheduled appointment?   
# 

# # EXPLORATORY DATA ANALYSIS

# In[12]:


df[df['diabetes'] == 1]['age'].hist()
plt.xlabel('Age')
plt.ylabel('The number of diabetics')
plt.title('The relationship between age and incidence of diabetes');


# I plot this chart to know the most age that suffer from diabetes.            
# I found that most age is 60 to 70 year old.

# ### the average of patient that suffer from diabetes

# In[13]:


df.groupby('diabetes')['age'].mean()


# In[14]:


df.groupby('diabetes')['age'].mean().plot(kind = 'bar' )
plt.title('Age average for patient that have diabetes and not');


# ### What is the most gender that have diabetes?

# In[15]:


gen_diab = df[df['diabetes'] == 1]
gen_diab.groupby('diabetes')['gender'].value_counts()


# In[16]:


x = gen_diab.groupby('diabetes')['gender'].value_counts().tolist()
plt.bar(x = ['F','M'], height= x )
plt.xlabel('Gender')
plt.ylabel('count')
plt.title('Count genders that have diabetes');


# Bar chart showed that females suffer from diabetes more than males

# Q : What is the most age people drink alcohol?

# In[17]:


df[df['alcoholism'] == 1]['age'].hist()
plt.title('Relation between age and dring alcohol')
plt.xlabel('Age')
plt.ylabel('Count of alcoholism');


# I plot this chart to show the most age that drink alcohol.                 
# I found that most age is 45:51 years old.

# In[18]:


df[df['hipertension'] == 1]['age'].hist()
plt.title('Relation between hipertension and age')
plt.xlabel('Age')
plt.ylabel('count');


# In[19]:


# print the smallest age
df[df['age']<15]['age'].value_counts()


# In[20]:


# Drop row that contian negative age
df.drop(df.index[df['age'] <= 0].tolist(),inplace = True)


# Q : What is the most gender suffer from diabetes?

# In[21]:


# print count of diabetes group by gender to now most gender suffer from diabetes
df.groupby('gender')['diabetes'].count()


# Q : What is the most hospital resive patients?

# In[22]:


df[df['no_show'] == 'No']['neighbourhood'].value_counts()


# ### What is the gender that drinke alcohol very much? 

# In[23]:


count_alc = df[df['alcoholism'] == 1].groupby('gender')['alcoholism'].value_counts().tolist()
plt.pie(x = count_alc, labels= ['F','M'], autopct='%1.2f%%')
plt.title('Percentage of gender that drinks alcohol');


# Q: Number of patients that scholarship? Did all registered patients attend the examination?

# In[24]:


#create new dataframe that contian the scholarship patients
df_sch = df[df['scholarship'] == 1]
df_sch


# In[25]:


# print number of patient that go to hospital from scholarship patients
df_sch['no_show'].value_counts()


# Patients that scholarship and show up more than No show

# In[55]:


# plot chart that describe the percentage of patient that show up and scholarship
high = df_sch['no_show'].value_counts(normalize = True).mul(100)
label = ['No' , 'Yes']
plt.bar(x = label, height= high)
plt.title('Patients that attend the examination')
plt.xlabel('Patient attendance')
plt.ylabel('count of patients');


# I plot this chart to show number patient that attend to show.         
# The percentage of patients that scholarship and show up more than No show

# In[27]:


df_sch['gender'].value_counts()


# Females that scholarship more than Males.

# In[28]:


plt.pie(x = df_sch['gender'].value_counts(), labels=  ['F','M'] , autopct='%1.2f%%')
plt.title('Percentage of gender that Scholoarship');


# The percentage of Females that scholarship more than Males.

# In[29]:


# print number of patient that suffer from diabetes and has not scholarship
df[df['scholarship'] == 0]['diabetes'].value_counts()


# The patients that not scholarship and have diabetes more than patients have not diabetes.

# Q: Is there a relationship between diabetes and alcoholism ?

# In[30]:


# prnit the average of diabetes patients and drink alcohol
df[df['alcoholism'] == 1]['diabetes'].mean()


# The average of patients that are alcoholism and have diabetes not heigh.

# In[31]:


#print number of patients that drink alcohol and suffer from diabetes
df[df['alcoholism'] == 1]['diabetes'].value_counts()


# Patients that are alcoholism and not have diabetes more than patients have diabetes.          
# This tell us that alcoholism have not strong effect for diabetes.

# In[32]:


# This function use to print pie for any column in datafram
def pie_chart(dataframe, colname):
    '''This function take 2 arguments
         dataframe : dataframe name
         colname : column name that you want to bar diagram
         '''
   
    plt.pie(dataframe[colname].value_counts(), autopct='%1.2f%%', labels= dataframe[colname].value_counts().index)
    plt.title('The percentage of {} '.format(colname))
    
#call function to excute
pie_chart(df, 'gender')


# This pie chart show that percentage of females more than Males

# ## What factors are important for us to know in order to predict if a patient will show up for their scheduled appointment?

# In[33]:


# Create new column wait that contain the difference between appointment day and scheduled day and convert it to int
df['wait'] = df['appointment_day'].dt.date - df['scheduled_day'].dt.date
#convert datetime to string
df['wait'] = df['wait'].astype(str)
# extract int number from string
df['wait'] = df['wait'].str.extract('(\d+)')
# convert it to int
df['wait'] = df['wait'].astype(int)


# In[34]:


df


# In[35]:


df['sms_received'].value_counts()


# In[36]:


# create new dataset that contian wait column equal 0
adb = df[df['wait'] == 0]


# In[37]:


adb['sms_received'].value_counts()


# In[38]:


df['sms_received'].value_counts() - adb['sms_received'].value_counts()


# # Conclusion 
# 1- I used No show appointment database.         
# 2- I import the packages and load the database.                
# 3- I discaver the data , clean it and convert columns data type to correct data type to be easy to use.         
# 4- I started to plot diagrams to discover the relations between columns         
# 5- Many questions appear and i started to answer them                    
# 6- the important questions is What factors are important for us to know in order to predict if a patient will show up for their scheduled appointment?                  
# 7- I discaverd that the factor is sms_received (All patients that wait value equal 0 not receive sms).
# 8- I found that females have diabetes more than males.         
# 9- I found that Males drink alcohol more than Females.               
# 10- I found that drinking kohl is not always accompanied by diabetes.

# # Limitation 
# Females have diseases more than Males.                    
# Males alcoholism more than Females.                  
# All patients that not receive sms show up at same day of scheduled day.
