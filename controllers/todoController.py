from flask import jsonify
from configs.db import MyDB
mycursor = MyDB.cursor()

class TodoController:
    @staticmethod
    def index():
        mycursor.execute("SELECT * FROM todos")
        myresult = mycursor.fetchall()
        rs = []
        for x in myresult:
            rs.append(
                {'id': x[0], 'title': x[1], 'des': x[2], 'completed': "false" if x[3] == 0 else 'true'})
        return jsonify({
            "status": 200,
            "data": rs
        })
        
