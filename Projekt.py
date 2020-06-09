#!/usr/bin/env python
# coding: utf-8

# # Programming project
# 
# ### Making a personalized selection of media content
# 
# The program allows a user to filter media by various criteria, then creates a file listing content that fits their wishes.
# The database used is pulled from the internet site IMDb and is publically available at this address: https://datasets.imdbws.com In order for this program to work on your computer, you must download the 'title.basics' and 'title.ratings' files.

# In[1]:


import pandas as pd
import numpy as np

#Uvoz podatkov
data_dat = "data.tsv"

#definiram podatkovni okvir
data_df = pd.read_csv(data_dat, sep='\t', na_values='\\N')

#odstranim ponovitve
data_df.drop_duplicates(subset ="tconst", keep = 'first', inplace = True)


# In[2]:


#Uvoz dodatnih podatkov
ratings_dat = "data_1.tsv"
ratings_df = pd.read_csv(ratings_dat, sep='\t')
ratings_df.drop_duplicates(subset ="tconst", keep = 'first', inplace = True)


# In[3]:


#Združitev podatkov v en podatkovni okvir
data_full = pd.merge(data_df, ratings_df, how='right', on='tconst', sort=False)


# In[4]:


#odstranim nepotrebne kategorije
data_short = data_full[["primaryTitle", "titleType", "isAdult", "startYear",
                        "runtimeMinutes", "genres", "averageRating", "numVotes"]].copy()


# In[5]:


#preimenujem kategorije v bolj pregledne
data_short.rename(columns={'primaryTitle':'Title', 'titleType':'TitleType', 'isAdult':'AdultContent',
                           'startYear':'ReleaseYear', 'runtimeMinutes':'Runtime',
                           'genres':'Genres', 'averageRating':'Rating', 'numVotes':'NumberOfVotes'}, inplace=True)


# In[6]:


print('Hi! What would you like to watch?')


# In[7]:


#poizvedba po vrsti medija

while True:
    yn1 = input("Do you wish to filter by type of media? (Answer with yes or no)\n")
    
    if yn1 == 'yes':
        titletype = input("What type of media are you interested in?\nAvailable categories are:\nshort, movie, tvMovie, tvSeries, tvEpisode, tvShort, tvMiniSeries, tvSpecial, video, videogame\nPlease type in case sensitive. You may choose multiple categories, separated by spaces.\n")
        
        titletype = titletype.split() #razdeli vnos večih kategorij na posamezne predmete
        data_type = data_short[data_short.TitleType.isin(titletype)] #poišče vrstice, ki vsebujejo katero od naštetih kategorij
        break
        
    elif yn1 == 'no':
        data_type = data_short
        break
        
    else:
        print("Please input a valid answer.")
        continue


# In[8]:


#poizvedba po vsebini za odrasle

while True:
    try:
        adultcontent = int(input("Do you wish to filter by adult content? Enter the number corresponding to your answer.\n1 - I don't care\n2 - No adult content\n3 - Only adult content\n"))
        
    except:
        print("Please input a valid answer.")
        continue
        
    if adultcontent == 1:
        data_adult = data_type
        break
        
    elif adultcontent == 2:
        adultcontent = 0
        data_adult = data_type[data_type['AdultContent'] == 0]
        break
        
    elif adultcontent == 3:
        adultcontent = 1
        data_adult = data_type[data_type['AdultContent'] == 1]
        break
        
    else:
        print("Please input a valid answer.")
        continue


# In[9]:


#poizvedba po letnici izida

while True:
    yn2 = input("Do you wish to filter by release year? Answer with yes or no.\n")
    
    if yn2 == 'yes':
        try:
            year1 = int(input("Find films after: (enter year)\n"))
            year2 = int(input("Find films before: (enter year)\n"))
            data_year = pd.merge(data_type[data_type['ReleaseYear'] >= year1], data_type[data_type['ReleaseYear'] <= year2])
            break
            
        except:
            print("Please input a valid answer.")
            continue
            
    elif yn2 == 'no':
        data_year = data_adult
        break
        
    else:
        print("Please input a valid answer.")
        continue


# In[10]:


#stolpec Runtime je imel dve vrstici z napačno vnešenimi elementi, zato ju odstranim
data_year = data_year[data_short.Runtime != 'Talk-Show']
data_year = data_year[data_short.Runtime != 'Reality-TV']

#nato ga pretvorim v številski tip, zato da lahko z njim računam
data_year["Runtime"] = pd.to_numeric(data_year["Runtime"])


# In[11]:


#poizvedba po dolžini

while True:
    yn3 = input("Do you wish to filter by runtime? Answer with yes or no.\n")
    
    if yn3 == 'yes':
        try:
            runtime1 = int(input("Find media longer than: (enter minutes)\n"))
            runtime2 = int(input("And shorter than: (enter minutes)\n"))
            data_runtime = pd.merge(data_year[data_year['Runtime'] >= runtime1], data_year[data_year['Runtime'] <= runtime2])
            break
            
        except:
            print("Please input a valid answer.")
            continue
            
    elif yn3 == 'no':
        data_runtime = data_year
        break
        
    else:
        print("Please input a valid answer.")
        continue


# In[12]:


#poizvedba po žanru

while True:
    yn4 = input("Do you wish to filter by genre? Answer with yes or no.\n")
    
    if yn4 == 'yes':
        genres = str(input("Available genres are:\n-Fantasy     -Adventure    -Animation   -Action       -Short\n-Thriller    -Horror       -Musical     -History      -Talk-Show\n-Documentary -Biography    -Western     -Adult        -Comedy\n-Drama       -Family       -Sci-Fi      -Romance      -Mystery\n-Music       -Crime        -War         -Sport        -Game-Show\n-News        -Reality-TV   -Film-Noir\n\nWrite down which genre or combination of genres you want to see, separated by spaces.\n"))
        
        genres = genres.split()
        if len(genres) == 1:
            data_genre = data_runtime[data_runtime.Genres.str.contains(genres[0], case=False, na=False)]
            
        elif len(genres) == 2:
            dgen1 = data_runtime[data_runtime.Genres.str.contains(genres[0], case=False, na=False)]
            dgen2 = data_runtime[data_runtime.Genres.str.contains(genres[1], case=False, na=False)]
            data_genre = pd.merge(dgen1, dgen2)
            
        elif len(genres) == 3:
            dgen1 = data_runtime[data_runtime.Genres.str.contains(genres[0], case=False, na=False)]
            dgen2 = data_runtime[data_runtime.Genres.str.contains(genres[1], case=False, na=False)]
            dgen3 = data_runtime[data_runtime.Genres.str.contains(genres[2], case=False, na=False)]
            data_genre = pd.merge(dgen1, dgen2)
            data_genre = pd.merge(data_genre, dgen3)
            
        else:
            print("You may not choose more than 3 categories or leave the field empty.")
            continue
        break
        
    elif yn4 == 'no':
        data_genre = data_runtime
        break
        
    else:
        print("Please input a valid answer.")
        continue


# In[13]:


#poizvedba po oceni

while True:
    yn3 = input("Do you wish to filter by rating? Answer with yes or no.\n")
    
    if yn3 == 'yes':
        print("Enter the range of ratings you wish to see. Ratings are formated like \"0.0\"")
        try:
            rating_low = float(input("Lower limit: "))
            rating_up = float(input("Upper limit: "))
            
        except:
            print("Please input a valid answer.")
            continue
            
        data_rating = pd.merge(data_genre[data_genre['Rating'] >= rating_low], data_genre[data_genre['Rating'] <= rating_up])
        break
        
    elif yn3 == 'no':
        data_rating = data_genre
        break
        
    else:
        print("Please input a valid answer.")
        continue


# In[14]:


#poizvedba po številu ocen

while True:
    yn3 = input("Do you wish to filter by number of votes?\nIf you are filtering by rating, it is recommended to choose a minimum number of votes.\nAnswer with yes or no.\n")
    
    if yn3 == 'yes':
        try:
            votes = int(input("Enter the minimum number of votes: "))
            
        except:
            print("Please input a valid answer.")
            continue
            
        data_final = data_rating[data_rating['NumberOfVotes'] >= votes]
        break
        
    elif yn3 == 'no':
        data_final = data_rating
        break
        
    else:
        print("Please input a valid answer.")
        continue


# Thank you for using my program. Your selection will be saved to a csv file named 'Search_results' in the folder you're using this program in.

# In[15]:


#zapis rezultatov v datoteko

data_final.to_csv('Search_results.csv')


# In[ ]:




