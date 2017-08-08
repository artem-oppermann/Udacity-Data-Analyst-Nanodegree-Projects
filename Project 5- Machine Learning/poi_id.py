#!/usr/bin/python

import sys
import pickle
import math
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data, test_classifier
from tool_functions import remove_outliers, create_total_wealth, \
                           poi_emails_ratio, \
                           get_k_best_features, get_best_parameters, \
                           get_tuned_LogisticRegression, \
                           get_tuned_AdaBoost, \
                           get_tuned_DecisionTree, \
                           get_tuned_RandomForest, \
                           get_tuned_GaussianNB, \
                           get_nan
                                    

from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest
from sklearn.preprocessing import StandardScaler

from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier



"""Task 1: Select what features you'll use."""
features_list = ["poi",
                 "loan_advances",
                 "from_this_person_to_poi",
                 "expenses",
                 "total_payments",
                 "other",
                 "from_messages",
                 "restricted_stock_deferred",
                 "salary",
                 "long_term_incentive",
                 "shared_receipt_with_poi",
                 "bonus",
                 "deferred_income",
                 "exercised_stock_options",
                 "from_poi_to_this_person",
                 "deferral_payments",
                 "to_messages",
                 "director_fees",
                 "total_stock_value",
                 "restricted_stock",
                 "total_wealth",
                 "email_from_poi_ratio",
                 "email_to_poi_ratio"
                 ] 


"""Load the dictionary containing the dataset."""
with open("final_project_dataset.pkl", "rb") as data_file:
    data_dict = pickle.load(data_file)




"""Task 2: Remove outliers."""
outlier_keys=["TOTAL", 
              "THE TRAVEL AGENCY IN THE PARK", 
              "LOCKHART EUGENE E"
              ]
data_dict=remove_outliers(data_dict,outlier_keys )

     

"""Task 3: Create new feature(s)."""
"""Definition of the new feature "total Wealth""" 
wealth_values=["salary",
               "bonus", 
               "exercised_stock_options",
               "total_stock_value"
               ]
"""Create the new feature total_wealth, total welath is the sum of "salary" """
""" "bonus", "exercised_stock_options" and "total_stock_value """
data_dict=create_total_wealth(data_dict, wealth_values)

""" Creating the new features "email_from_poi_ratio" and "feature email_to_poi_ratio".
"email_from_poi_ratio" :=number of emails the person received from poi/number of all received emails
"email_to_poi_ratio" :=number of emails the person sent toi poi/number of all sent emails """
data_dict=poi_emails_ratio(data_dict)

""" Store to my_dataset for easy export below. """
my_dataset = data_dict
    
""" Extract features and labels from dataset for local testing """
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)



""" Task 4: Try a varity of classifiers """ 

logReg=LogisticRegression()
svc=SVC()
AdaBoost=AdaBoostClassifier()
DecisionTree=DecisionTreeClassifier()
RandomForest=RandomForestClassifier()
gaussian=GaussianNB()

""" Gets the number of Nan's for each feature in the dataset """
get_nan(my_dataset)

""" Printing the scores of the features, this line must stay commented """
#get_k_best_features(features, labels, features_list)



""" Task 5: Tuning and testing the classifiers """

""" Input parameters for each algorithm from which the best parameter combination is determined """
""" Parameters for Logistic Regression """
logReg_parameters = {"C":[0.5,1,5,5.5,6],
                     "penalty":["l1",  "l2"],
                     "tol":[1e-2, 1e-3, 1e-4, 1e-5]
                     } 
""" Parameters for AdaBoostClassifier """
AdaBoost_parameters = {'n_estimators':[25,50,75], 
                       "learning_rate":[0.25, 0.5, 0.75, 1.0],
                       } 
""" Parameters for DecisionTreeClassifier """
DecisionTree_parameters = {"criterion":["gini","entropy"], 
                           "min_samples_split":[2,3,4],
                           "min_samples_leaf":[1,2,3]
                           } 
""" Parameters for RandomForestClassifier """
RandomForest_parameters = {"max_depth":[3,4,5,6,7], 
                           "criterion":["gini","entropy"],
                           "n_estimators":[20,25,30],
                           "random_state":[35,40,45]
                           } 

""" Tuning the Logistic Regression """
tuned_logReg=get_tuned_LogisticRegression(logReg,logReg_parameters, features,\
                                          labels, pca=PCA(n_components=12),\
                                          scaler=None, k_best=None)
""" Tuning AdaBoost Classifier """
tuned_AdaBoost=get_tuned_AdaBoost(AdaBoost, AdaBoost_parameters, features,\
                                  labels, pca=None, scaler=StandardScaler(),\
                                  k_best=None)
""" Tuning DecisionTreeClassifier """
tuned_DecisionTree=get_tuned_DecisionTree(DecisionTree, DecisionTree_parameters,\
                                          features, labels, pca=None, \
                                          scaler=StandardScaler(), \
                                          k_best=SelectKBest(k=4))
""" Tuning RandomForestClassifier """
tuned_RandomForest=get_tuned_RandomForest(RandomForest, RandomForest_parameters, \
                                          features, labels, pca=PCA(n_components=5),\
                                          scaler=None, \
                                          k_best=SelectKBest(k=10))
""" Tuning Gaussian Naive Bayes """ 
tuned_gaussian=get_tuned_GaussianNB(gaussian, features, labels, \
                                    pca=PCA(n_components=10), scaler=None, \
                                    k_best=SelectKBest(k=13))

""" Testing the algorithms to determine the one with the best performance """
test_classifier(tuned_logReg,my_dataset,features_list)
test_classifier(tuned_gaussian,my_dataset,features_list)
test_classifier(tuned_AdaBoost,my_dataset,features_list)
test_classifier(tuned_DecisionTree,my_dataset,features_list)
test_classifier(tuned_RandomForest,my_dataset,features_list)



""" Task 6: Dump your classifier, dataset, and features_list """
clf=tuned_gaussian
dump_classifier_and_data(clf, my_dataset, features_list)






