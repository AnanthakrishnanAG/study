#!/usr/bin/env python
# coding: utf-8

# # #App Data Analysis
# This is a small analysis project on various apps on android and ios inorder to find out trends among app users based on 2017 and 2018 data.Here i try to do an analysis on free apps and its popularity 

# In[1]:


from csv import reader
#opening applestore data
df_apple_store=open('AppleStore.csv',encoding="utf8")
df_apple_read=reader(df_apple_store)
df_list_apple=list(df_apple_read)
df_header_apple=df_list_apple[0]
df_data_apple=df_list_apple[1:]
#opening google playstore data
df_googleplaystore=open('googleplaystore.csv',encoding="utf8")
df_google_read=reader(df_googleplaystore)
df_list_google=list(df_google_read)
df_header_google=df_list_google[0]
df_data_google=df_list_google[1:]


# exporting data

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') 

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# In[3]:


explore_data(df_data_google,0,6,True)


# # DATA CLENSING

# In[4]:


#it is findout that there is a missing data at index number 10472
#for the sake of accurate analysis that data is removed
del df_data_google[10472]


# # Finding duplicate rows
# Duplicated rows will reduce the  accuracy of our analysis.So we have to keep only one row for each app details.
# 

# In[5]:


unique_data=[]
duplicate_data=[]
for row in df_list_apple:
    name=row[0]
    if name in unique_data:
        duplicate_data.append(name)
    else:
        unique_data.append(name)
print(unique_data)
print(duplicate_data)#we get an empty list as result which means 
#there is no duplicate data


# In[6]:


unique_data=[]
duplicate_data=[]
for row in df_list_google:
    name=row[0]
    if name in unique_data:
        duplicate_data.append(name)
    else:
        unique_data.append(name)

print(duplicate_data)#we get 1181 duplicate 
                          #data on googleplaystore dataset
print(len(duplicate_data))


# In[7]:


df_header_google


# # Criterion for removing duplicate data
# we get 1181 number of duplicate entries in googleplaystore data set.instead of removing randomly duplicate entries im going to keep most recently updated data and remove rest of the data 

# Here by analysing the Reviews column we can understand the duplicated apps have different reviews value.It is because the data is collected in different time and the highest value of review shows the latast data.So for the recent data here i pick most reviewed data of duplicated apps and ignore rest of the data

# In[8]:


reviews_max={}#creating a dictonary for storing highest review values for app keyword
for row in df_data_google:
    app_name=row[0]
    n_reviews=float(row[3])
    if app_name in reviews_max and reviews_max[app_name]<n_reviews:
        reviews_max[app_name]=n_reviews
    if app_name not in reviews_max:
        reviews_max[app_name]=n_reviews
        


# In[9]:


print(len(reviews_max))


# In[10]:


print((reviews_max))


# # removing duplicated rows

# In[11]:


android_clean = []
already_added = []

for app in df_data_google:
    app_name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[app_name] == n_reviews) and (app_name not in already_added):
        android_clean.append(app)
        already_added.append(app_name)


# In[12]:


print(android_clean)


# In[13]:


print(already_added)


# # Removing non english app names from list

# In[14]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3: #ASCII value of english charactors are below 127.if more than 3 non english charactors are detected 
        return False #remove that app from analysis
    else:
        return True

print(is_english('Docs To Go™ Free Office Suite'))#only have one non-english charactor.so it takes into account
print(is_english('Instachat 😜'))#only have one non-english charactor.so it takes into account


# In[15]:


android_english = []
ios_english = []

for app in android_clean:#iterate through anaroid apps for finding english app names only 
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in df_data_apple:#iterate through ios apps for finding english app names only 
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# # Analysing  on free apps 

# In[16]:


android_final = []
ios_final = []

for app in android_english:#iterate through android apps for finding free apps only
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:#iterate through ios apps for finding free apps only
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# # Most common app by genre

# For this im creating a frequency table by genre.Below there is a function which takes dataset and index number for creating the frequency table.Here i use python dictonary data type as frequency table.

# In[25]:


df_header_google


# In[29]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1 #counting total number of data
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100 #finding percentage
        table_percentages[key] = percentage  #adding percentage value to key in new dictonary
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)#creating tuple data type from dictonary data type
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)#sorting in ascending order
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# # for Andriod

# In[30]:


display_table(android_final,-4)


# From this result we can conclude that in android apps most apps are under genre of tools(8%).and second position is for entertainment.The above list is sorted in acending order so we can see very least apps are for Adventure and educational apps.

# # For IOS

# In[19]:




display_table(ios_final, -5)


# in case of ios apps the genres are few compare with android.However more than half percentage of apps are for entertainment(58%).other genres are just below 10%.We can see a huge gap between percentages

# Anyway from both app genre analysis we can see entertainment is always shows a good amount of quantity among both ios and android apps.

# # Most popular app by genre in ios

# Here we going to check popularity of apps by counting number of installs by users.It will show us which genre is more popular among users 

# In[20]:


df_header_apple


# from header of ios dataset we can use the total number of user rating(rating_count_tot) as total number of users and find out most popular app in ios.note that this is an assumption and not going to give auctual values of total number of installs of that particular app.

# In[32]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings #adding number of user reviews together 
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# from this result we can see more number of user reviews on Navigation genre.From this we can assume that Navigation genre is more popular among users in ios.Medical genre is very less popular among ios genres

# Lets analyse close on navigation

# In[36]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5])


# On navigation genre we can see most rated app is Waze - GPS Navigation, Maps & Real-time Traffic. and second position is for google map

# # Most popular app by genre in android
# 

# In[22]:


df_header_google


# Here installs is directly given.so we can find frequency table directly from our used defined function which we created in In[44] to find percentage of each install numbers.However the number is not accurate because it just dont give us auctual number of installs just give eg (10000+) rough figures.Anyway we going to take it as 10000(there is no way).To get a error free code we should replace '+' sign and ',' by just '' and convert the value to float for add up . After that we can easily addup the number of installs based on catagory on android apps. 

# In[23]:


display_table(android_final, 5)


# Number of installs based on catagory

# In[24]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# By analysing communication apps are mostly installed on android app (38456119).

# Lets analyse closely on communication apps which are top installed

# In[38]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts are most popular apps in communication genre

# In[ ]:




