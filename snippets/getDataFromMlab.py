from pymongo import MongoClient
import pandas as pd
import time
import json
import numpy
from geopy.distance import great_circle,vincenty
MONGODB_URI = "mongodb://co-work-booked:12345@ds261128.mlab.com:61128/co-work-book"
client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client.get_database("co-work-book")
booked_records = db.coworkbooked
cowork_records = db.coworking
def getLong_Latitude():
    records = cowork_records.find()
    return records
def getAllRecode():
    records = booked_records.find()
    return records
def getCoWoringRecommended(dataRecomment,dataCoWork):
    listDataRecommendation= []
    for i in dataRecomment:
        for n in range(len(dataCoWork)):
            if dataCoWork[n]['coworking_id'] == i:
                listDataRecommendation.append(dataCoWork[n])
                break
    # print(listDataRecommendation)
    return listDataRecommendation
def getRECORD(user_id):
    records = booked_records.find_one({"User_ID":user_id})
    return records

def pushRECORD(record):
    booked_records.insert_one(record)

def updateRecord(record, updates):
    booked_records.update_one({'_id': record['_id']},{
                              '$set': updates
                              }, upsert=False)
def suggestionAlgorithm(self):
    dataCoWork = getLong_Latitude()
    listCoWork = []
    listCoWorkID = []
    for i in dataCoWork:
        listCoWork.append(i)
        listCoWorkID.append(i['coworking_id'])
    listCoWorkID.sort()
    distance = []
    for i in range(len(listCoWork)):
        distance.append(great_circle((listCoWork[0]['latitude'],listCoWork[0]['longitude']), (self['latitude'],self['longtitude'])).meters)
    dfDistance = pd.DataFrame(distance,columns=['distance'])
    dataUserBooked = getAllRecode()
    listCoWorkBooked = []
    for i in dataUserBooked:
        listCoWorkBooked.append(i)
    dfCoWorkBooked1 = pd.DataFrame(listCoWorkBooked).sort_values(by=['coworking_id'])
    dfCoWorkBooked = dfCoWorkBooked1.drop(columns=['_id']).reset_index(drop=True)
    listAverageRating = []
    listCountRiting   = []
    baseData = dfCoWorkBooked['coworking_id'][0]
    rating   = 0
    countRating = 0
    for i in range(len(dfCoWorkBooked)):
        if dfCoWorkBooked['coworking_id'][i] == baseData and dfCoWorkBooked['rating'][i]>0:
            countRating = countRating+1
            rating = dfCoWorkBooked['rating'][i] + rating
            if i == len(dfCoWorkBooked)-1 :
                listAverageRating.append(rating/countRating)
                listCountRiting.append(countRating)
        elif dfCoWorkBooked['coworking_id'][i] > baseData and dfCoWorkBooked['rating'][i]>0:
            listAverageRating.append(rating/countRating)
            listCountRiting.append(countRating)
            rating = 0
            countRating = 0
            baseData = dfCoWorkBooked['coworking_id'][i]
            countRating = countRating+1
            rating = dfCoWorkBooked['rating'][i] + rating
    dfDistance['coworking_id'] = listCoWorkID
    dfDistance['count_rating']  = listCountRiting
    dfDistance['average_rating']= listAverageRating
    C = dfDistance['average_rating'].mean()
    m = dfDistance['count_rating'].quantile(0.50)
    q_movies = dfDistance.copy().loc[dfDistance['count_rating'] >= m]
    q_movies.shape
    def weighted_rating(x, m=m, C=C):
        v = x['count_rating']
        R = x['average_rating']
        return (v/(v+m) * R) + (m/(m+v) * C) 
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

    q_movies = q_movies.sort_values('score', ascending=False).head(10).reset_index(drop=True)
    # Recommendation = q_movies.to_json(orient='records')
    return q_movies['coworking_id'],listCoWork

class getUserLocation():
    # AIzaSyAKC4z8tXSQajMdu0wV1RP3fUAxQr3LRbs  
    def getCoworkingForRecommendation(self) :
        dataForRecomment,dataCoWork = suggestionAlgorithm(self)
        dataRecomment = getCoWoringRecommended(dataForRecomment,dataCoWork)
        dfResultRecomment = pd.DataFrame(dataRecomment)
        dfResultRecomment = dfResultRecomment.drop(columns=['_id'])
        resultForRecomment = dfResultRecomment.to_json(orient='records')
        print(resultForRecomment)
        return resultForRecomment


