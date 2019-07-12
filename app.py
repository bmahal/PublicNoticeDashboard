from flask import Flask
from flask import render_template
from pymongo import MongoClient
import json
from bson import json_util
from bson.json_util import dumps

app = Flask(__name__)


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
DATA_STATE_COLLECTION = 'projects'
PARALLEL_DATA_STATE_COLLECTION = 'variables_data'
TOPIC_COLLECTION='topics'
DBS_NAME = 'noticesFinal'
DATA_FIELDS={'state':True,'id':True,'county':True,'newspaper':True,'date':True,'notice_id':True,'category':True,'year':True,'month':True,'day':True,'weekday':True,'month_year':True,'_id':False}
PARALLEL_FIELDS={'state':True,'population_2017':True,'Births_2017':True,'Deaths_2017':True,'notices_count':True,'unemployment':True,'pov':True,'uneducated':True,'Auctions and Bids':True,'Business and Corporates':True,'Foreclosures':True,'Property Notice':True,'Tax Notice':True,'_id':False}
TOPIC_FIELDS={'Document_No':True,'Dominant_Topic':True,'Topic_Perc_Contrib':True,'Keywords':True,'Text':True,'_id':False}
connection = MongoClient(MONGODB_HOST, MONGODB_PORT)
collection = connection[DBS_NAME][DATA_STATE_COLLECTION]
parallelCollection=connection[DBS_NAME][PARALLEL_DATA_STATE_COLLECTION]
topicCollection=connection[DBS_NAME][TOPIC_COLLECTION]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/noticesFinal/projects")
def noticesYear():
    noticeprojects = collection.find(projection=DATA_FIELDS)
    json_projects = []
    for project in noticeprojects:
        json_projects.append(project)
    ##print(json_projects)
    json_projects = json.dumps(json_projects, default=json_util.default)
    connection.close()
    return json_projects

@app.route("/noticesFinal/parallel")
def parallel():
    parallelprojects = parallelCollection.find(projection=PARALLEL_FIELDS)
    json_projects2 = []
    for project in parallelprojects:
        json_projects2.append(project)
    ##print(json_projects2)
    json_projects2 = json.dumps(json_projects2, default=json_util.default)
    connection.close()
    return json_projects2

@app.route("/noticesFinal/topics")
def topics():
    topicprojects = topicCollection.find(projection=TOPIC_FIELDS)
    json_projects3 = []
    for project in topicprojects:
        json_projects3.append(project)
    ##print(json_projects2)
    json_projects3 = json.dumps(json_projects3, default=json_util.default)
    connection.close()
    return json_projects3



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
