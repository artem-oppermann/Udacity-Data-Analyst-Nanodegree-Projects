# -*- coding: utf-8 -*-
"""
Created on Tue May 30 18:32:08 2017

@author: Admin
"""
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif
import math
from sklearn import grid_search
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier


"""Remove the outliers in the dataset.

    Keyword arguments:
    data_dict -- the dataset
    outlier_list --list with outliers
    """
def remove_outliers(data_dict, outlier_list):
    
    for x in outlier_list:
        data_dict.pop(x)
        
    return data_dict
    
    
    
"""Create the new feature "total_wealth"

    Keyword arguments:
    data_dict -- the dataset
    wealth_values --list with features that belongs to total wealth
    """
def create_total_wealth(data_dict, wealth_values):
    
    for name in data_dict:
        
        features_dict=data_dict[name]
        total_wealth=0
    
        for feature in wealth_values:
            
            if not features_dict[feature]=="NaN":
                total_wealth=total_wealth+features_dict[feature]
                features_dict["total_wealth"]=total_wealth
            else:
                features_dict["total_wealth"]=0
                             
    return data_dict



"""Creating the new features "email_from_poi_ratio" and 
    feature email_to_poi_ratio.
    
    Keyword arguments:
    data_dict -- the dataset
    """
def poi_emails_ratio(data_dict):
    
    for name, features_dict in data_dict.items():
    
        if not math.isnan(float(features_dict["from_poi_to_this_person"])):
            features_dict["email_from_poi_ratio"]=features_dict["from_poi_to_this_person"]/features_dict["from_messages"]
        else:
            features_dict["email_from_poi_ratio"]=0
        
        if not math.isnan(float(features_dict["from_this_person_to_poi"])):
           features_dict["email_to_poi_ratio"]=features_dict["from_this_person_to_poi"]/features_dict["to_messages"]
        else:
           features_dict["email_to_poi_ratio"]=0
    
    return data_dict



"""Returns a dictionary where the key is a feature and values how many 
    NaN belong to one feature
    
    Keyword arguments:
    my_dataset -- the dataset
    """
def get_nan(my_dataset):
    
    nans={}

    """Identify a feature in the dataset which has a NaN value and initialize the dictionary"""
    for name in my_dataset:

        features_dict=my_dataset[name]
    
        for key, value in features_dict.items():
        
            if not key=="email_address":
               if math.isnan(float(value)):
                nans[key]=0

    """Count the number of NaN's for each feature"""
    for name in my_dataset:
    
        features_dict=my_dataset[name]
    
        for key, value in features_dict.items():
        
            if not key=="email_address":
                if math.isnan(float(value)):
                    nans[key]+=1
    return nans



"""Get the scores for the features according to SelectKBest
    
    Keyword arguments:
    features -- features
    labels -- labels
    features_list -- a list of strings with feature names
    """
def get_k_best_features(features, labels, features_list):

    k_best=SelectKBest(f_classif, k="all")
    k_best.fit(features,labels)
    features_list.remove('poi')
    k_best_features=zip(features_list,k_best.scores_)
    k_best_features=sorted(k_best_features, key=lambda x: x[1], reverse=True)
    
    return k_best_features



"""Get the best input parameters for a classifier
    
    Keyword arguments:
    clf -- classifier
    parameters -- dictionary of possible parameters
    features -- features
    labels -- labels
    """
def get_best_parameters(clf, parameters,features, labels):
    
    grid = grid_search.GridSearchCV(clf, parameters)
    grid.fit(features, labels)
    
    return grid.best_params_



"""Get the Pipeline
    
    Keyword arguments:
    classifier -- classifier
    features -- features
    labels -- labels
    pca -- PCA()
    scaler -- StandardScaler()
    k_best -- SelectKBest()
    """
def get_pipeline(classifier, features, labels, pca, scaler, k_best):
   
    estimators =[]

    if not isinstance(scaler, type(None)):
        estimators+=[("Scaler",scaler)]
    if not isinstance(k_best, type(None)):
        estimators+=[("k_best",k_best)]
    if not isinstance(pca, type(None)):
        estimators+=[("PCA", pca)]
        
    estimators +=[('clf', classifier)]
    pipe = Pipeline(estimators)
    
    return pipe



"""Returning tuned Logistic Regression classifier
    
    Keyword arguments:
    classifier -- classifier
    parameters -- best input parameters according to GridSearchCV
    features -- features
    labels -- labels
    pca -- PCA()
    scaler -- StandardScaler()
    k_best -- SelectKBest()
    """
def get_tuned_LogisticRegression(classifier, parameters, features, labels, pca, scaler, k_best):
    
    bestParameter=get_best_parameters(classifier, parameters,features, labels)
    
    logReg=LogisticRegression(**bestParameter)
    
    return get_pipeline(logReg, features, labels, pca=pca, scaler=scaler, k_best=k_best)
    
    
    
"""Returning tuned AdaBoost classifier
    
    Keyword arguments:
    classifier -- classifier
    parameters -- best input parameters according to GridSearchCV
    features -- features
    labels -- labels
    pca -- PCA()
    scaler -- StandardScaler()
    k_best -- SelectKBest()
    """
def get_tuned_AdaBoost(classifier, parameters, features, labels, pca, scaler, k_best):
    
    bestParameter=get_best_parameters(classifier, parameters,features, labels)
    AdaBoost=AdaBoostClassifier(**bestParameter)

    return get_pipeline(AdaBoost, features, labels, pca=pca, scaler=scaler, k_best=k_best)
     


"""Returning tuned DecisionTree classifier
    
    Keyword arguments:
    classifier -- classifier
    parameters -- best input parameters according to GridSearchCV
    features -- features
    labels -- labels
    pca -- PCA()
    scaler -- StandardScaler()
    k_best -- SelectKBest()
    """
def get_tuned_DecisionTree(classifier, parameters, features, labels, pca, scaler, k_best):
    
    bestParameter=get_best_parameters(classifier, parameters,features, labels)
    DecisionTree=DecisionTreeClassifier(**bestParameter)

    return get_pipeline(DecisionTree, features, labels, pca=pca, scaler=scaler,k_best=k_best)
    
    

"""Returning tuned RandomForest classifier
    
    Keyword arguments:
    classifier -- classifier
    parameters -- best input parameters according to GridSearchCV
    features -- features
    labels -- labels
    pca -- PCA()
    scaler -- StandardScaler()
    k_best -- SelectKBest()
    """
def get_tuned_RandomForest(classifier, parameters, features, labels, pca, scaler, k_best):
    
    bestParameter=get_best_parameters(classifier, parameters,features, labels)
    RandomForest=RandomForestClassifier(**bestParameter)

    return get_pipeline(RandomForest, features, labels, pca=pca, scaler=scaler, k_best=k_best)
    
    
    
"""Returning tuned GaussianNB classifier
    
    Keyword arguments:
    classifier -- classifier
    parameters -- best input parameters according to GridSearchCV
    features -- features
    labels -- labels
    pca -- PCA()
    scaler -- StandardScaler()
    k_best -- SelectKBest()
    """
def get_tuned_GaussianNB(classifier, features, labels, pca, scaler, k_best):
    
    return get_pipeline(classifier, features, labels, pca=pca, scaler=scaler, k_best=k_best)
    
    
    
    
    
    
    

