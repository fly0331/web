from flask import Flask
from flask import render_template
import pymysql

app = Flask(__name__)



@app.route('/')
def index():
    conn = pymysql.connect(host='localhost', user='root', password='ap565639', port=3306,
                           db='student')
    cur = conn.cursor()
    sql = "SELECT * FROM student.student_table;"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('fuck.html',u=u)
    


if __name__ == '__main__':
    app.debug = True
    app.run(port=8003)