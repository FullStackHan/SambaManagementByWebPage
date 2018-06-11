import os
from flask import Flask, render_template, request, redirect, json
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/checkLogin', methods=['POST'])
def checkLogin():
    username = request.form.get('username')
    password = request.form.get('password')
    print(username + "      "+ password)
    if(username == 'root' and password == "123456"):
        return 'true'
    else:
        return 'false'

@app.route('/showSamba')
def showSamba():
    return render_template('showSamba.html')

@app.route('/getData')
def getData():
    showResult = os.popen('bash {}/sambashell/detail'.format(basedir)).read()
    print(showResult)
    return showResult

@app.route('/edit', methods=['POST'])
def edit():
    old_share_name = request.form.get("old_share_name").replace('[', '').replace(']', '').strip()
    share_name = request.form.get("share_name").replace('[', '').replace(']', '').strip()
    share_directory = request.form.get("share_directory")
    chuliPath = "\\/".join(share_directory.split("/"))
    create_owner = request.form.get('create_owner')
    create_group = request.form.get('create_group')
    create_mask = request.form.get('create_mask')
    hosts_allow = request.form.get('hostallow')
    if(request.form.get('available') == None):
        available = "no"
    else:
        available = "yes"
    if(request.form.get('browserable') == None):
        browserable = "no"
    else:
        browserable = "yes"
    print(old_share_name,share_name,share_directory,create_owner,create_group,create_mask,available,browserable,hosts_allow)
    getPathResult = os.popen('bash {}/sambashell/dirExist {}'.format(basedir,share_directory)).read().strip()
    print(getPathResult)
    if getPathResult == "0" :
        return "1"
    getOwnResult = os.popen('bash {}/sambashell/ownExist {}'.format(basedir,create_owner)).read().strip()
    if getOwnResult == "0":
        return "2"
    getGroupResult = os.popen('bash {}/sambashell/groupExist {}'.format(basedir,create_group)).read().strip()
    if getGroupResult == "0":
        return "3"
    if old_share_name != share_name:
        getShareNameResult = os.popen('bash {}/sambashell/confExist {}'.format(basedir,share_name)).read().strip()
        
        if getShareNameResult == "1":
            print(getShareNameResult)
            #edit user has exist
            return "4"
        else:
            #edit 
            #print("this is Result:",Result)
            print('"\\\['+old_share_name+'\\\]"','"['+share_name+']"')
            ResultPath = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"path"','"path = '+chuliPath+'"')).read()
            ResultOwn = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"force user"','"force user = '+create_owner+'"')).read()
            ResultGroup = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"force group"','"force group = '+create_group+'"')).read()
            ResultMask = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"create mask"','"create mask = '+create_mask+'"')).read()
            ResultAvailable = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"available"','"available = '+available+'"')).read()
            ResultBrowseable = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"browseable"','"browseable = '+browserable+'"')).read()
            ResultHostAllow = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"hosts allow"','"hosts allow = '+hosts_allow+'"')).read()
            ResultName = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"\\['+old_share_name+'\\]"','"['+share_name+']"')).read().strip()
            startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
            print("startResult: ",startResult)
            return "0"
    else:
        #edit 
        #print('"\\['+old_share_name+'\\]"','"\\['+share_name+'\\]"')
        ResultPath = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"path"','"path = '+chuliPath+'"')).read()
        ResultOwn = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"force user"','"force user = '+create_owner+'"')).read()
        ResultGroup = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"force group"','"force group = '+create_group+'"')).read()
        ResultMask = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"create mask"','"create mask = '+create_mask+'"')).read()
        ResultAvailable = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"available"','"available = '+available+'"')).read()
        ResultBrowseable = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"browseable"','"browseable = '+browserable+'"')).read()
        ResultHostAllow = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,old_share_name,'"hosts allow"','"hosts allow = '+hosts_allow+'"')).read()
        startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
        print("startResult: ",startResult)
        return "0"

@app.route('/editAvailable', methods=['POST'])
def editeditAvailable():
    share_name = request.form.get("share_name").replace('[', '').replace(']', '').strip()
    if(request.form.get('available') == "yes"):
        available = "yes"
    else:
        available = "no"
    print(share_name,available)
    ResultAvailable = os.popen('bash {}/sambashell/edit {} {} {}'.format(basedir,share_name,'"available"','"available = '+available+'"')).read()
    if(ResultAvailable == ""):
        startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
        print("startResult: ",startResult)
        return "true"
    else:
        startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
        print("startResult: ",startResult)
        return "false"

@app.route('/deleteUser', methods=['POST'])
def delete():
    old_share_name = request.form.get("old_share_name").replace('[', '').replace(']', '')
    print(old_share_name)
    Resultdelete = os.popen('bash {}/sambashell/delete {}'.format(basedir,old_share_name)).read()
    if(Resultdelete == ""):
        startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
        print("startResult: ",startResult)
        return "true"
    else:
        startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
        print("startResult: ",startResult)
        return "false"

@app.route('/addFilePage')
def addFile():
    return render_template('create.html')

@app.route('/getUserAndIp', methods=['POST'])
def getUserAndIp():
    ResultUser = os.popen('bash {}/sambashell/allUser'.format(basedir)).read().strip()
    #print(ResultUser)
    ResultGroup = os.popen('bash {}/sambashell/allGroup'.format(basedir)).read().strip()
    #print(ResultGroup)
    ResultIp = os.popen('bash {}/sambashell/ip'.format(basedir)).read().strip()
    #print(ResultIp)
    resultAll = '{"user": '+ResultUser+',"group":'+ResultGroup+',"ip":'+ResultIp+'}'
    print(resultAll)
    return resultAll



@app.route('/createFile', methods=["POST"])
def createFile():
    shareName = request.form.get("share_name")
    share_dir = request.form.get("share_directory")
    iscreate_dir = request.form.get("create_directory")
    owner = request.form.get("userList")
    ipList = request.form.get("ipList")
    createMask = request.form.get("create_permissions")
    createGroup = request.form.get("groupList")
    if(request.form.get("isava") == "on"):
        isAvailable = "yes"
    else:
        isAvailable = "no"
    if(request.form.get("isbro") == "on"):
        isbrowseable = "yes"
    else:
        isbrowseable = "no"
    print(shareName,'\"Shared Folder\"','"'+'"'+share_dir+'"'+'"',"yes","yes",'"'+owner+'"','"'+createMask+'"',"0777",'"'+createGroup+'"','"'+isAvailable+'"','"'+isbrowseable+'"','"'+ipList+'"')

    getShareNameResult = os.popen('bash {}/sambashell/confExist {}'.format(basedir,shareName)).read().strip()
    if getShareNameResult == "1":
        print("sharename",getShareNameResult)
        #edit sharename has exist
        return "0"
    if(request.form.get("create_directory") == "on"):
        getPathResult = os.popen('bash {}/sambashell/dirExist {}'.format(basedir,share_dir)).read().strip()
        print("getPathResult",getPathResult)
        if getPathResult == "0":
            os.popen('bash {}/sambashell/createDir.sh {} {} {} {}'.format(basedir,share_dir,createMask,owner,createGroup)).read().strip()
    Resultcreate = os.popen('bash {}/sambashell/new {} {} {} {} {} {} {} {} {} {} {} {}'.format(basedir,shareName,'\"Shared Folder\"','"'+'"'+share_dir+'"'+'"',"yes","yes",'"'+owner+'"','"'+createMask+'"',"0777",'"'+createGroup+'"','"'+isAvailable+'"','"'+isbrowseable+'"','"'+ipList+'"')).read()
    if(Resultcreate == ""):
        startResult = os.popen('bash {}/sambashell/startsmb.sh'.format(basedir)).read()
        print("startResult: ",startResult)
        return "1"
    else:
        return "3"

if __name__ == '__main__':
    app.run()
