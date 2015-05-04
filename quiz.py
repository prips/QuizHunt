__author__ = 'pseth'

import json
from bottle import route, run, post, request, response, static_file
import fileinput, os
from time import gmtime, strftime
from random import randint

@route('/questions/')
def question_list():
    complete_list=""
    json_complete = []
    for line in open("data.txt"):
        parsed = json.loads(line)
        json_complete.append(parsed)
        print complete_list
    response.content_type = 'application/json'
    return json.dumps(json_complete, sort_keys=False)

@route('/teams/')
def team_list():
    complete_list=""
    json_complete = []
    for line in open("team.txt"):
        parsed = json.loads(line)
        json_complete.append(parsed)
        print complete_list
    response.content_type = 'application/json'
    return json.dumps(json_complete, sort_keys=True)

@route('/teams/<number>', method='GET')
def team_show( number="1" ):
    q = {"reason":"incorrect ID"}
    with open('team.txt') as f:
        for line in f:
            data=json.loads(line)
            if str(data['team_id'])==str(number):
                q = data
    f.close()
    response.content_type = 'application/json'
    return q

@route('/questions/<number>', method='GET')
def question_show( number="1" ):
    q = "default"
    with open('data.txt') as file:
        for line in file:
            data=json.loads(line)
            if data['id']==number:
                q = data
    return q

@post('/teams')
def team_create( data="test" ):
    flag = False
    team_id = randint(1000000000,9999999999)
    data = {}
    incoming = {}
    incoming = request.json
    if not incoming.has_key('name'):
        return "expected {\"name\":\"value\"}"
    else:
        data['name'] = request.json['name']
        data['team_id'] = team_id
        f = open("team.txt", 'r')
        for line in f:
            existing=json.loads(line)
            if existing['name']==request.json['name'] or existing['team_id']==team_id:
                flag = True
        f.close()
        fname = str(data['team_id'])+".txt"
        f = open(fname, 'w')
        f.close()
    if flag:
        return "Team not unique. Please try again"
    else:
        f = open("team.txt", 'a+')
        for line in f:
            existing=json.loads(line)
            if existing['name']==request.json['name']:
                return "team name not unique"
        json.dump(data, f)
        f.write("\n")
        f.close()
        response.content_type = 'application/json'
        return json.dumps(data, sort_keys=True)

@post('/questions/redeem')
def questions_redeem( data="test" ):
    flag = False
    data = {}
    incoming = {}
    incoming = request.json
    print incoming['question_id']
    print incoming['answer']
    print incoming['team_id']
    if not incoming.has_key('question_id') and incoming.has_key('answer') and incoming.has_key['team_id']:
        return "{'reason':'missing question_id/answer/team_id'}"
    else:
        data['answer'] = request.json['answer']
        data['team_id'] = request.json['team_id']
        data['question_id'] = request.json['question_id']
        data['timestamp'] = strftime("%Y-%m-%d %H:%M:%S")
        f = open("data.txt", 'r')
        for line in f:
            temp=json.loads(line)
            if temp['question_id']==data['question_id']:
                data['score']=temp['score']
                flag=False
                break
            else:
                flag=True
        f.close()
        if flag:
            response.content_type = 'application/json'
            return "{'reason':'Invalid question Id'}"
        try:
            if not os.path.isfile(data['team_id']+".txt"):
                response.content_type = 'application/json'
                return "{'reason':'Team not registered'}"
            f = open(str(data['team_id'])+".txt", 'r')
            print str(data['team_id'])+".txt"
            for line in f:
                temp=json.loads(line)
                print data['question_id']
                print temp['question_id']
                if str(data['question_id'])==str(temp['question_id']):
                    response.content_type = 'application/json'
                    return "{'reason':'Question already redeemed'}"
            f.close()
            f = open(str(data['team_id'])+".txt", 'a+')
            json.dump(data, f)
            f.write("\n")
            f.close()
        except Exception as e:
            print e

# @post('/questions')
# def question_create( data="test" ):
#     result = {"question_id":""}
#     incorrect = {"reason":"missing score/description/type"}
#     question_id = 0
#     flag = True
#     data = {}
#     incoming = {}
#     incoming = request.json
#     if not incoming.has_key('score') or incoming.has_key('description') or incoming.has_key('type'):
#         flag = False
#     else:
#         if incoming['type']=="bug":
#             print "Do validation here"
#         elif incoming['type']=="mcq":
#             print "Do validation here"
#         elif incoming['type']=="short":
#             print "Do validation here"
#         elif incoming['type']=="image":
#             print "Do validation here"
#         f = open("data.txt")
#         for line in f:
#             if line:
#                 existing = json.loads(line)
#                 question_id = int(existing['question_id'])
#         f.close()
#         data['description'] = request.json['description']
#         data['question_id'] = str(question_id + 1)
#         data['type']= request.json['type']
#         data['score']= request.json['score']
#         file = open("data.txt", 'a')
#         json.dump(data, file)
#         file.write("\n")
#         file.close()
#     response.content_type = 'application/json'
#     if flag:
#         result['question_id']=data['question_id']
#         return result
#     else:
#         return incorrect

@route('/questions/<number>', method='DELETE' )
def question_delete( number="test" ):
    with open('data.txt') as file:
        for line in fileinput.input("data.txt", inplace=True):
            data=json.loads(line)
            if data['question_id']!=number:
                print line,
    fileinput.close()
    return "Question deleted "

@route('/questions/<number>', method='PUT')
def question_save( number="test" ):
    return "UPDATE Question " + number

@route('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')

run(host='localhost', port=9090, debug=True)
