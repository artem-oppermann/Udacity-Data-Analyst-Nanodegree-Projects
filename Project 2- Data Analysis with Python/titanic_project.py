import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
titanic=pd.read_csv("titanic-data.csv")
titanic.head()

# Create new dataset without unwanted columns
titanic=titanic.drop(['Name','Ticket','Cabin','Embarked','SibSp'], axis=1)
titanic.head()

# Identify if duplicates in the data do exists
titanic_duplicates = titanic.duplicated()
print('Number of duplicates: {}'.format(titanic_duplicates.sum()))

# Calculating the number of missing values
titanic.isnull().sum()

# Determine the number of males and females with missing age in the dataset
missing_age_male = titanic[pd.isnull(titanic['Age'])]['Sex'] == 'male'
missing_age_female = titanic[pd.isnull(titanic['Age'])]['Sex'] == 'female'

print('Number of male passengers with missing age: {}'.format(missing_age_male.sum()))
print('Number of female passengers with missing age: {}'.format(missing_age_female.sum()))


#%%
ages=titanic["Age"].dropna()
plt.figure(figsize=(7,7))
plt.hist(ages, bins=80, color='#377eb8',edgecolor = "Black")
plt.xlabel("Age/Years")
plt.ylabel('Count')
plt.title('Distribution of the passenger ages.')

#%%
gender=titanic['Sex']

counts = Counter(gender)
common = counts.most_common()
gender = [item[0] for item in common]
count = [item[1] for item in common]

plt.bar(np.arange(2), count, tick_label=gender, width=0.4, color='#377eb8',edgecolor = "Black")
plt.ylabel('Count')
plt.title('Number of female and male passengers')
plt.show()

#%%

survival=titanic['Survived']
counts=Counter(survival)
common = counts.most_common()
label=["Dead", "Survived"]
count=[item[1] for item in common]
plt.bar(np.arange(2), count, tick_label=label, width=0.4, color='#377eb8',edgecolor = "Black")
plt.ylabel('Count')
plt.title('Number of survived and dead passengers.')
plt.show()
#%%


#############Did the gender determine the chances of survival?###################



# Group thy PassengerId by Gender und Survival
g=titanic.groupby(["Survived","Sex"])["PassengerId"]

# Count how many passengers died or survived dependent on the gender
survived_men=g.get_group((1,"male")).count()
survived_women=g.get_group((1,"female")).count()
dead_men=g.get_group((0,"male")).count()
dead_women=g.get_group((0,"female")).count()

# Group the PassengerId by gender and count the Id's dependent on the gender to find out the total number of women and men
g=titanic.groupby("Sex")["PassengerId"]
men_sum=float(g.get_group(("male")).count())
women_sum=float(g.get_group(("female")).count())

#Normalization of dead and survived passengers depentend on the gender
p2=survived=[survived_men/men_sum, survived_women/women_sum] 
p1=dead=[dead_men/men_sum, dead_women/women_sum]

# Plot the survival by gender ration 
plt.figure(figsize=(7,7))
N=2
ind = np.arange(N)               
width = 0.35                      
bar1 = plt.bar(ind, survived, width,color='#377eb8', edgecolor = "Black")
bar2 = plt.bar(ind+width, dead, width,color='#e41a1c', edgecolor = "Black")
plt.ylabel('Ratio of passengers')
plt.title('Survival by Gender')
plt.xticks(ind+width/2, ['Men', "Female"])
plt.legend((bar2, bar1), ('Dead', 'Survived'))
plt.figure(num=None, figsize=(1, 1), dpi=80, facecolor='w', edgecolor='k')
plt.show()

#%%


#################Did the social-economic status determine the chances of survival?########

################################ Survival regarding the fare ##########################
# Create a dataframe of all fares
fares_df=titanic[["Fare", "Survived"]]
fares=titanic["Fare"]

# Create 20 fare ranges from 0 $ - 300 $ and count how many fares from fares_df belong to each range
num_bins=20
bar_width=300/float(num_bins)
fare_ranges_all=[]
for i in np.arange(0,num_bins,1):
    fare_ranges_all.append(len([x for x in fares if i*bar_width <= x < (i+1)*bar_width]))

# Create a dataframe with fares of passengers who survived
survived_fares=fares_df.ix[(fares_df["Survived"]==1)]["Fare"]

# Determine how many fares of passengers who survived belong in each of the 20 ranges 
fare_ranges_survived=[]
for i in np.arange(0,num_bins,1):
    fare_ranges_survived.append(len([x for x in survived_fares if i*bar_width <= x < (i+1)*bar_width]))

# Handle the case in which a fare range does not contain any counts (to avoid devide by null error during normalization)
for n,i in enumerate(fare_ranges_all):
    if i==0:
      fare_ranges_all[n]=1
 
 
################################ Survival regarding the class ##########################
 
# Get the Groupby object 
g=titanic.groupby(["Survived","Pclass"])

# Count the passengers from each class who not have survived
dead_class_1=g.get_group((0,1))["PassengerId"].count()
dead_class_2=g.get_group((0,2))["PassengerId"].count()
dead_class_3=g.get_group((0,3))["PassengerId"].count()

# Count the passengers from each class who  have survived
survived_class_1=g.get_group((1,1))["PassengerId"].count()
survived_class_2=g.get_group((1,2))["PassengerId"].count()
survived_class_3=g.get_group((1,3))["PassengerId"].count()

# Get the Groupby object
g=titanic.groupby(["Pclass"])
# Count the passengers in each class
passengers_class1=float(g.get_group((1))["PassengerId"].count())
passengers_class2=float(g.get_group((2))["PassengerId"].count())
passengers_class3=float(g.get_group((3))["PassengerId"].count())


# Plot the fare-survival relation

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 5))  
fare_ranges_all=np.array(fare_ranges_all).astype(float)

#Normalize the number of fares in each range
normed_survived_fares=np.array(fare_ranges_survived)/fare_ranges_all
axes[0].bar(np.arange(0, 300,bar_width)+bar_width/2.0,normed_survived_fares,width=bar_width, align="center", edgecolor = "Black")
axes[0].set_title("Survival by Fare")
axes[0].set_xlabel("Fare price / $")
axes[0].set_ylabel("Ratio of passengers")


# Plot the class-survival relation
y1, y2, y3=dead_class_1/passengers_class1, dead_class_2/passengers_class2, dead_class_3/passengers_class3
z1, z2, z3=survived_class_1/passengers_class1, survived_class_2/passengers_class2, survived_class_3/passengers_class3
dead=[y1, y2, y3]
survived=[z1, z2, z3]
width=0.25
ind = np.arange(3) 
bar1 = axes[1].bar(ind, survived, width,color='#377eb8', edgecolor = "Black")
bar2 = axes[1].bar(ind+width, dead, width,color='#e41a1c', edgecolor = "Black")
axes[1].legend((bar2, bar1), ('Dead', 'Survived'))
axes[1].set_title("Survival by Class")
axes[1].set_xlabel("Class")
axes[1].set_ylabel("Ratio of passengers")
axes[1].set_xticks(ind+width/2)
axes[1].set_xticklabels(["1", "2", "3"])
plt.show()

#%%



################Did age, regardless of gender, determine your chances of survival?###########


# Count the PassengerId grouped by the age and save it as dataframe
df=pd.DataFrame({'count' : titanic.groupby("Age")["PassengerId"].count()}).reset_index()

# Make a dictionary out of df, where age is the key and count is the value
passengers_by_age = dict(zip(df["Age"], df["count"]))

# Count the PassengerId that is grouped by survival and gernder and save it in a dataframe
df=pd.DataFrame({'count' : titanic.groupby( ["Survived","Age"])["PassengerId"].count()}).reset_index()
# New dataframe where all passengers survived
df2 = df.ix[(df['Survived'] == 1)]

# Make a dictionary where keys are the passenger age group and the values the normalized count of passengers in this age group
age_survived_norm={}
for index, row in df2.iterrows():
        age_survived_norm.update(({row["Age"]:row["count"]/float(passengers_by_age[row["Age"]])}))
    
# Plot the results
plt.figure(figsize=(13,7))
plt.bar(list(age_survived_norm.keys()), list(age_survived_norm.values()), align='center', color="#377eb8")
plt.xlabel('Age / years')
plt.ylabel('Ratio of survived passengers')
plt.title('Survival of passengers by age')
plt.show()


#%%


###########Did the age considering the gender determine the chances of survival?###########

# Count the PassengerId grouped by age and gender and save ad dataframe
df=pd.DataFrame({'count' : titanic.groupby(["Age", "Sex"])["PassengerId"].count()}).reset_index()

# Take from df values which belong to men and save as new dataframe
df_male=df.ix[(df['Sex']=='male')]
# Take from df values which belong to women and save as new dataframe
df_women=df.ix[(df['Sex']=='female')]

# Create dictionary with age of men as the key and the count of men in this age group as value
male_by_age=dict(zip(df_male["Age"], df_male["count"]))
# Create dictionary with age of women as the key and the count of women in this age group as value
female_by_age=dict(zip(df_women["Age"], df_women["count"]))

#Count the PassengerId grouped by survival, age and gender and save as dataframe
df=pd.DataFrame({'count' : titanic.groupby( ["Survived","Age", "Sex"])["PassengerId"].count()}).reset_index()

#Create two dictionaries in which the keys are the age of men/women and the normalized count of men/women in this age group as value
male_by_age_survived={}
female_by_age_survived={}
for index, row in df.iterrows():
    if row["Survived"]==1:
        if row["Sex"]=="male":
            male_by_age_survived.update(({row["Age"]:row["count"]/float(male_by_age[row["Age"]])}))
        else:
             female_by_age_survived.update(({row["Age"]:row["count"]/float(female_by_age[row["Age"]])}))
                
# Plot the results
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))
axes[0].bar(list(male_by_age_survived.keys()), list(male_by_age_survived.values()), align='center')
axes[0].set_xlabel('Age / years')
axes[0].set_ylabel('Ration of survived men')
axes[0].set_title('Survival of male passengers by age')

axes[1].bar(list(female_by_age_survived.keys()), list(female_by_age_survived.values()), align='center')
axes[1].set_xlabel('Age / years')
axes[1].set_ylabel('Ration of survived women')
axes[1].set_title('Survival of female passengers by age')
plt.show()

#%%


###############Did the number of children aboard per passenger determine the chances of survival?########


# How many passengers do have how many children? Create new dataframe and transform it's columns to a dictionary
parch_count=pd.DataFrame({'count' : titanic.groupby("Parch")["PassengerId"].count()}).reset_index()
parch_count=dict(zip(parch_count["Parch"],parch_count["count"]))

# Same dataframe as above but also grouped by survival
df=pd.DataFrame({'count' : titanic.groupby(["Survived","Parch"])["PassengerId"].count()}).reset_index()

# Calculate the survival ratio per children aboard
surival_ratio={}
for index, row in df.iterrows():
    if not row["Survived"]:
        surival_ratio[row["Parch"]]=1-(row["count"]/float(parch_count[row["Parch"]]))
          
    
plt.figure(figsize=(10,6))      
plt.bar(list(surival_ratio.keys()),list(surival_ratio.values()),color='#377eb8', edgecolor = "Black")
plt.title("Survival ratio per children aboard")
plt.xlabel("Number of children per passenger")
plt.ylabel("Ratio of survival")
plt.show()



