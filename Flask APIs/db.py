import pymysql
from decimal import Decimal
from flask import jsonify
def query(querystr,return_json=True):
    connection = pymysql.connect(host='skillup-team-07.cxgok3weok8n.ap-south-1.rds.amazonaws.com',user='admin',password='coscskillup',db='webapp',cursorclass=pymysql.cursors.DictCursor)
    connection.begin()
    mycursor=connection.cursor()
    mycursor.execute(querystr)
    print(querystr)
    #print(mycursor.fetchall())
    result = encode(mycursor.fetchall())
    print(result)
    connection.commit()
    mycursor.close()
    connection.close()
    if return_json :
        print(jsonify(result))
        return jsonify(result)
    else:
        return result
def encode(data):
    print(data)
    for row in data:
        for key,value in row.items():
            if isinstance(value,Decimal):
                row[key]=str(value)
    print(data)
    return data