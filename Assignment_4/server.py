from flask import Flask, request
import base64
import re

# linear algebra
import numpy as np 

# data processing
import pandas as pd 

# Algorithms
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB

# Saving Model
import pickle

app = Flask(__name__)

@app.route('/getResult', methods=['POST'])
def getResult():

    '''' Unwrapping the string data from server and converting it into pandas dataframe '''
    hug_pickled_str = request.data
    test_df = pickle.loads(base64.b64decode(hug_pickled_str))
    print("Test Dataset received from server: ")
    print(test_df)

    ''' Preprocessing data '''
    train_df = pd.read_csv("train.csv")

    data = [train_df, test_df]
    for dataset in data:
        dataset['relatives'] = dataset['SibSp'] + dataset['Parch']
        dataset.loc[dataset['relatives'] > 0, 'not_alone'] = 0
        dataset.loc[dataset['relatives'] == 0, 'not_alone'] = 1
        dataset['not_alone'] = dataset['not_alone'].astype(int)
    
    train_df = train_df.drop(['PassengerId'], axis=1)

    deck = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "U": 8}


    data = [train_df, test_df]
    for dataset in data:
        dataset['Cabin'] = dataset['Cabin'].fillna("U0")
        dataset['Deck'] = dataset['Cabin'].map(
            lambda x: re.compile("([a-zA-Z]+)").search(x).group())
        dataset['Deck'] = dataset['Deck'].map(deck)
        dataset['Deck'] = dataset['Deck'].fillna(0)
        dataset['Deck'] = dataset['Deck'].astype(
            int)  # we can now drop the cabin feature
    train_df = train_df.drop(['Cabin'], axis=1)
    test_df = test_df.drop(['Cabin'], axis=1)

    data = [train_df, test_df]
    for dataset in data:
        mean = train_df["Age"].mean()
        std = test_df["Age"].std()
        is_null = dataset["Age"].isnull().sum()
        # compute random numbers between the mean, std and is_null
        rand_age = np.random.randint(mean - std, mean + std, size=is_null)
        # fill NaN values in Age column with random values generated
        age_slice = dataset["Age"].copy()
        age_slice[np.isnan(age_slice)] = rand_age
        dataset["Age"] = age_slice
        dataset["Age"] = train_df["Age"].astype(int)

    common_value = 'S'
    data = [train_df, test_df]

    for dataset in data:
        dataset['Embarked'] = dataset['Embarked'].fillna(common_value)

    data = [train_df, test_df]
    for dataset in data:
        dataset['Fare'] = dataset['Fare'].fillna(0)
        dataset['Fare'] = dataset['Fare'].astype(int)

    data = [train_df, test_df]
    titles = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}

    for dataset in data:
        # extract titles
        dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
        # replace titles with a more common title or as Rare
        dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr',
                                                    'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
        dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
        dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
        dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')
        # convert titles into numbers
        dataset['Title'] = dataset['Title'].map(titles)
        # filling NaN with 0, to get safe
        dataset['Title'] = dataset['Title'].fillna(0)

    train_df = train_df.drop(['Name'], axis=1)
    test_df = test_df.drop(['Name'], axis=1)

    genders = {"male": 0, "female": 1}
    data = [train_df, test_df]
    for dataset in data:
        dataset['Sex'] = dataset['Sex'].map(genders)

    train_df = train_df.drop(['Ticket'], axis=1)
    test_df = test_df.drop(['Ticket'], axis=1)

    ports = {"S": 0, "C": 1, "Q": 2}
    data = [train_df, test_df]
    for dataset in data:
        dataset['Embarked'] = dataset['Embarked'].map(ports)

    data = [train_df, test_df]
    for dataset in data:
        dataset['Age'] = dataset['Age'].astype(int)
        dataset.loc[dataset['Age'] <= 11, 'Age'] = 0
        dataset.loc[(dataset['Age'] > 11) & (dataset['Age'] <= 18), 'Age'] = 1
        dataset.loc[(dataset['Age'] > 18) & (dataset['Age'] <= 22), 'Age'] = 2
        dataset.loc[(dataset['Age'] > 22) & (dataset['Age'] <= 27), 'Age'] = 3
        dataset.loc[(dataset['Age'] > 27) & (dataset['Age'] <= 33), 'Age'] = 4
        dataset.loc[(dataset['Age'] > 33) & (dataset['Age'] <= 40), 'Age'] = 5
        dataset.loc[(dataset['Age'] > 40) & (dataset['Age'] <= 66), 'Age'] = 6
        dataset.loc[dataset['Age'] > 66, 'Age'] = 6

    data = [train_df, test_df]
    for dataset in data:
        dataset.loc[dataset['Fare'] <= 7.91, 'Fare'] = 0
        dataset.loc[(dataset['Fare'] > 7.91) & (
            dataset['Fare'] <= 14.454), 'Fare'] = 1
        dataset.loc[(dataset['Fare'] > 14.454) & (
            dataset['Fare'] <= 31), 'Fare'] = 2
        dataset.loc[(dataset['Fare'] > 31) & (dataset['Fare'] <= 99), 'Fare'] = 3
        dataset.loc[(dataset['Fare'] > 99) & (dataset['Fare'] <= 250), 'Fare'] = 4
        dataset.loc[dataset['Fare'] > 250, 'Fare'] = 5
        dataset['Fare'] = dataset['Fare'].astype(int)

    data = [train_df, test_df]
    for dataset in data:
        dataset['Age_Class'] = dataset['Age'] * dataset['Pclass']

    for dataset in data:
        dataset['Fare_Per_Person'] = dataset['Fare']/(dataset['relatives']+1)
        dataset['Fare_Per_Person'] = dataset['Fare_Per_Person'].astype(int)
    
    X_test = test_df.drop("PassengerId", axis=1).copy()

    print("Test Dataset after cleaning ready to fit to model: ")
    print(X_test)

    ''' Loading the saved decision tree model '''
    modelfile = open('model.pkl', 'rb')
    decision_tree_model = pickle.load(modelfile)

    ''' Predicting survival with the decison tree model '''
    Y_pred = decision_tree_model.predict(X_test)

    # print(type(Y_pred))
    # print(Y_pred)

    ''' Converting numpy nd-array to list '''
    survival_list = Y_pred.tolist()
    print("Model calculated survival result of passengers: ")
    print(survival_list)

    ''' Reurning data to the server '''
    return str(survival_list)
    # return "Hello!"


if __name__ == '__main__':
    app.run(port=8000, debug=True)
