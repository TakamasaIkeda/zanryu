#!/usr/bin/env python
#-*- coding:utf-8 -*-
import mechanize
import json
import re
from urlparse import urlparse, parse_qs
import sys
INFO_JSON = "./info.json"
KS = "70001"
YC = "2016_27060"

br = mechanize.Browser() 
br.set_handle_robots(False) 

##username, password, session_name, other properties to fill the zanryu_form
def getprops_from_json(): 
    f = open(INFO_JSON, 'rb') 
    json_data = json.load(f)
    return json_data

##LOGIN to sfc-sfs login form
def login(username, passwd): 
    br.select_form(nr=0) 
    br["u_login"] = username
    br["u_pass"] = passwd
    res = br.submit() 

def getURLParams(url):
    params = parse_qs(urlparse(url).query, True)
    return params 

def check_access(url):
    if br.response().geturl() == url:
        print("OK: %s" % url)
    else: 
        print("ERROR: %s" % url) 

def getRoomNumber(room): 
    room_number = ''
    if room == 'k':
        room_number = '1'
    elif room == 'e':
        room_number = '2'
    elif room == 'i':
        room_number = '3'
    elif room == 'o':
        room_number = '4'
    elif room == 'l':
        room_number = '5'
    elif room == 'd':
        room_number = '6'
    elif room == 't':
        room_number = '7'
    elif room == 'z':
        room_number = '8'
    elif room == 'n':
        room_number = '9'
    elif room == 'w':
        room_number = '10'
    else:
        room_number = '11'
    return room_number
        
def submit_form(prop): 
    br.select_form(name='formRoom') 
    br['stay_phone'] = prop['phone'].encode('euc-jp') 
    br['stay_p_phone'] = prop['phone_emergency'].encode('euc-jp') 
    br['stay_time'] = prop['zanryu_time'].encode('euc-jp')
    br['selectRoom'] = [getRoomNumber(prop['building'])] 
    br['selectFloor'] = ["s2"] #多分selectRoomによって動的に変化するから、うまく指名できてない。
    br['stay_room_other'] = prop['room_number']
    br['stay_reason'] = prop['reason'].encode('euc-jp') 

    br.submit() 


#Necessary properties to login and go to a zanryu form
def zanryu(): 
    #get username && passwd from json
    prop = getprops_from_json() 
    username = prop["username"]
    passwd = prop["passwd"]

    #Processes till submit a zanryu form
    home_url = "https://vu.sfc.keio.ac.jp/sfc-sfs/"
    try:
        html = br.open(home_url) #login page 
    except:
        print('ERROR: COULD NOT ACCESS TO %s' % home_url) 
    check_access(home_url) 
    
    login(username, passwd) #submit uname&passwd 
    top_url = br.response().geturl()  
    params = getURLParams(top_url) 
    
    #open a page of your session
    session_url = "https://vu.sfc.keio.ac.jp/sfc-sfs/sfs_class/student/s_class_top.cgi?lang=ja&ks=" + KS + "&yc=" + YC +"&id=" + str(params['id']).strip('[\'\']') 
    br.open(session_url) 
    check_access(session_url)

    #got to zanryu form page
    br.select_form(nr=0) 
    br.submit() 

    #fill out zanryu form
    submit_form(prop) 

if __name__ == "__main__":
    zanryu() 
