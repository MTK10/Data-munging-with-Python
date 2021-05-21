#!/usr/bin/env python
# coding: utf-8

# ## Profitable Apps Project
# 
# 
# 
# 
# 
# **Project Description**
# 
# Aim of Project is to find mobile apps which are profitable  for app store and google play markets. As Data analyst, I want to enable developers via data driven decisions with respect to kind of apps they build. 

# In[1]:


#Opening Apple and Google Datasets using Absolute Paths
from csv import reader
opened_applefile = open('E:\Educational\Python\Datasets\AppleStore.csv', encoding='utf8')
read_apple = reader(opened_applefile)
data_apple = list(read_apple)
apple_rows = data_apple[1:] #Slicing out the header from the dataset
apple_header = data_apple[0]#only Headers of the dataset

opened_googlefile = open('E:\Educational\Python\Datasets\googleplaystore.csv', encoding='utf8')
read_google = reader(opened_googlefile)
data_google = list(read_google)
google_rows = data_google[1:]
google_header = data_google[0]

#calling datasets for check
print(apple_rows[0:2],'\n')
print(google_rows[0:2])


# ## Creating a function to call data sets

# In[2]:


def explore_data(dataset,start,end,rows_cols = True):
    for r in dataset[start:end]:
        print(r,'\n')
    if rows_cols:
        print('Number of rows :', len(dataset))
        print('Number of columns:',len(dataset[0]))


# In[3]:


print(google_header,'\n')
explore_data(google_rows,0,2) #rows_cols condition True by default no need to place an argument for it in function


# ## Removing Duplicates & Non English/Free Apps
# **Data Cleaning**
# 
# Reading Kaggle discussion forumn, it was shown that data set is missing a column value. How to determine which row has that missing value in the dataset?

# In[4]:


for rows in google_rows:
    Col_len = len(google_header)
    row_len = len(rows)
    if Col_len != row_len:
        print(rows,'\n')
        print('Row with missing column is', google_rows.index(rows))


# ## Deleting wrong Data
# 
# We will compare the row 10472 with headers to understand origin of the data error. Then delete the row. Two steps ofcourse are mutually exclusive.

# In[5]:


print(google_header,'\n')
print(google_rows[1],'\n')
print(google_rows[10472])


# As we can see the row 10472 is missing the Category Column, this leads to eroneous alignment for other data points for example Ratings for app in this row is 19. However, Google playstore ratings are only upto 5.

# In[6]:


print(len(google_rows))
del google_rows[10472]
print(len(google_rows))


# ## Removing Duplicates
# 
# **PART 1**
# 
# **Creating two Seperate lists for Duplicates & Unique values**
# 
# Logic: if an element in dataset exists in unique apps already then it is a duplicate. Hence we should add it to duplicate list via append method. 

# In[7]:


duplicate_apps = []
unique_apps = []

for apps in google_rows:
    name = apps[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
duplicate_apps[0:10] #some examples of duplicate apps


# ## PART 2
# **Removing Duplicates on a Criterion**
# 
# As you can see each row with respective duplicate name is copied across the database. Quickly eye balling the Slack app duplicates in dataset we can observe that higher the number of reviews more recent the data should be. Hence rather than removing duplicates randomly, we will only keep entries of duplicates with highest number of reviews whilst remove others.

# In[8]:


reviews_max = {}

for e in google_rows:
    name = e[0]
    n_reviews = float(e[3])
    
    if name in reviews_max and reviews_max[name]< n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
#Important to use ELIF here and not ELSE - using else will also take exception of n_reviews.
#We only want to pivot on names


# In[9]:


print('Expected Length',len(reviews_max),'\n')
print(len(duplicate_apps),'\n')
print('Actual Length',len(google_rows)-len(duplicate_apps))


# 
# Now, let's use the reviews_max dictionary to remove the duplicates. For the duplicate cases, we'll only keep the entries with the highest number of reviews. In the code cell below:
# 
# * We start by initializing two empty lists, android_clean and already_added.
# * We loop through the android data set, and for every iteration:
#     * We isolate the name of the app and the number of reviews.
#     * We add the current row (app) to the android_clean list, and the app name     (name) to the already_added list if:
# 
#         - The number of reviews of the current app matches the number of reviews of that app as described in the reviews_max dictionary; and
# 
#         - The name of the app is not already in the already_added list. We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for reviews_max[name] == n_reviews, we'll still end up with duplicate entries for some apps.

# In[10]:


google_clean = []
already_added = []

for rows in google_rows:
    name = rows[0]
    n_reviews = float(rows[3])
    
    if reviews_max[name]== n_reviews and name not in already_added:
        google_clean.append(rows)
        already_added.append(name)


# Exploring the clean data set, it should give us same dataset length and width as created above in the dictionary. 

# In[11]:


explore_data(google_clean,0,4)


# In[ ]:





# **As expected - we have 9659 rows.**

# # Removing Non English Apps
# 
# **Part One**
# 
# Exploring the data set we can see there are many apps which are not in english language hence we will end targeting the wrong audience. Below we will sort the data and segregate english apps from non english.
# 
# **Use the Built-in Ord() function to leverage ASCII character standard**
# 
# * All english alphabets have ASCII numerical value between 0 and 127

# In[12]:


def is_english(string):
    for element in string:
        if ord(element) > 127:
            return False
        
    return True
            

        
    


# In[13]:


print(is_english('Instagram '))
print(is_english('a视剧热播'))

print(is_english('Instachat 😜'))
print(is_english('Docs To Go™ Free Office Suite'))
print(ord("剧"))


# However as you can see, the function is not perfect. Some apps use emojis or symbols in their names. Due to which the existing function check will drop them in selection. One way to limit data loss is by setting a criteria. For example. The apps which have atleast 3 characters outside ASCII range, will be deemed **Non English** . 
# 
# # Part Two

# In[14]:


def is_english(string):
    non_ascii = 0
    
    for e in string:
        if ord(e)>127:
            non_ascii += 1
    
    if non_ascii >3:
        return False
    else:
        return True
    


# In[15]:


print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# Although Function is still not but this limits the data loss quite a bit.
# 
# # Seperating English & Non English into Seperate Lists Via Defined Function

# In[16]:


google_english = []
apple_english = []

for rows in google_clean:
    name = rows[0]
    
    if is_english(name):
        google_english.append(rows)
        

for rows in apple_rows:
    name = rows[1]
    
    if is_english(name):
        apple_english.append(rows)
        
explore_data(google_english,0,2)
print('\n')
explore_data(apple_english,0,2)


# # Isolating the Free Apps
# 
# 

# In[17]:


google_free = []
apple_free = []

for rows in google_english:
    price = rows[7]
    
    if price == '0':
        google_free.append(rows)
        

for rows in apple_english:
    price = rows[4]
    
    if price == '0.0':
        apple_free.append(rows)

print(len(google_free), "android free apps")
print(len(apple_free), "ios free apps")


# # Finding Common Genres in IOS & Andorid App Stores
# 
# Pursuing a strategy we need to find an app which is most likely to be used by most number of people on both IOS & Google play stores. 
# 
# To do so , we will create few functions which will be applicable to both ios and andorid datasets.
# 
# * Function to display Genres by Absolute frequency
# 
# * Function to display Genres by percentage proportion of all

# In[18]:


#Creating function to genreate absolute frequency table with ascending/desending order flexibility
def abs_frequency(dataset,index,descend = True):
    table = {}
    total = 0
    #altnernate to total counter : sum(list(table.values())) -> this will sum the total occurences in dictionary and be same thing as total counter
    for rows in dataset:
        genre = rows[index]
        total += 1
        if genre in table:
            table[genre] += 1
        else:
            table[genre] = 1
    if descend:
        return sorted(table.items(),key=lambda x:x[1],reverse = True) #to ensure table rolls out in descending order
    else:
        return sorted(table.items(),key=lambda x:x[1],reverse = False) # Ascending order

            


#Creating function to display genres in percentage, ascending/descending flexibility

def display_table(dataset, index, descend = True):
    table = {}
    total = 0
    
    for rows in dataset:
        genre = rows[index]
        total += 1
        if genre in table:
            table[genre] += 1
        else:
            table[genre] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key]/total)*100
        table_percentages[key] = percentage
        
    if descend:
        return sorted(table_percentages.items(),key=lambda x:x[1],reverse=True)
    else:
        return sorted(table_percentages.items(),key=lambda x:x[1],reverse=False)
    
#Important to define x:x[1] as it will always then apply sort on whatever value on index position at 1
#after sort is applied dictionary is changed to type list


# # Part three
# 
# We start examining the frequency table for genres in both data bases.

# In[19]:


display_table(apple_free,11)


# In[20]:


display_table(google_free,1)


# We can see that among Free English apps in IOS store almost 58 % are games and then entertainment apps are close to 8 %. Then followed by photography and social media apps. However 'fun' apps in IOS quite large does not imply they will have the most users as well. Demand might not be the same. 

# In[21]:


display_table(google_free,1)


# The landscape seems significantly different on Google Play: there are not that many apps designed for fun, and it seems that a good number of apps are designed for practical purposes (family, tools, business, lifestyle, productivity, etc.). However, if we investigate this further, we can see that the family category (which accounts for almost 19% of the apps) means mostly games for kids.

# # Most Popular Apps by Genre on App Store
# 
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play data set, we can find this information in the Installs column, but for the App Store data set this information is missing. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.

# In[22]:


genres_ios= abs_frequency(apple_free,-5) # this will return a LIST not a dictionary, hence genre has to be defined within the loop

for rows in genres_ios:
    genre = rows[0]
    total = 0
    len_genre = 0
    for app in apple_free:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_rating = total/len_genre
    print(genre,':',avg_rating)


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:

# In[23]:


for app in apple_free:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# 
# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.

# # Most Popular apps by Genre on Play store
# 
# For the Google Play market, we actually have data about the number of installs, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# In[24]:


display_table(google_free,5)


# One problem with this data is that is not precise. For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to get an idea which app genres attract the most users, and we don't need perfect precision with respect to the number of users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on.
# 
# To perform computations, however, we'll need to convert each install number to float — this means that we need to remove the commas and the plus characters, otherwise the conversion will fail and raise an error. We'll do this directly in the loop below, where we also compute the average number of installs for each genre (category).

# In[25]:


categories_android = abs_frequency(google_free,1)
install_dist = []

for e in categories_android:
    category = e[0]
    total = 0
    len_categ = 0
    for rows in google_free:
        category_app = rows[1]
        if category_app == category:
            n_installs = rows[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            n_installs = float(n_installs)
            total += n_installs
            len_categ += 1
    
    avg_installs = total/len_categ
    print(category,':',avg_installs)
            
#The nested loops follow block logic, you can re build a small case using example on page 12


    


# On average - communication genre has most installs as shownn by the distribution generated above. However upon analyzing the category closely we can observer how heavily skewed this category is. As it will be true for most other categories too.

# In[26]:


for apps in google_free:
    if apps [1] == 'COMMUNICATION' and (apps[5] == '1,000,000,000+' 
                                       or apps[5]== '500,000,000+'
                                       or apps[5]== '100,000,000+'):
        print(apps[0], ':',apps[5])


# Removing apps with installs above 100 M + will bring down the category avg install number down drastically. 

# In[27]:


under_100m = []

for app in google_free:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    n_installs = float(n_installs)
    if app[1] == 'COMMUNICATION' and n_installs<100000000:
        under_100m.append(n_installs)
        
sum(under_100m)/len(under_100m)


# **Exploring another Category**

# In[28]:


for app in google_free:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# 
# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[29]:


for app in google_free:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# 
# This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.

# # Conclusions
# 
# In this project, we analyzed data about the App Store and Google Play mobile apps with the goal of recommending an app profile that can be profitable for both markets.
# 
# We concluded that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets. The markets are already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.
# 
# 
# Similar process can be taken to analyze and slice through IOS based apps

# In[30]:


#example to revise nested loop confusion

some_string = ['First','Second']
some_int = [1,2,3,4]

for e in some_string:
    print(e)
    for z in some_int:
        print(z)
    x = sum(some_int)
    print(x)


# In[ ]:




