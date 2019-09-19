from markupsafe import Markup
from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask import request
from jinja2 import Template
import pymysql
import os
import json

con = pymysql.connect("localhost", "root", "", "sap")
app = Flask(__name__, template_folder="mytemplate")
cf_port = os.getenv("PORT")

cur = con.cursor()
cur.execute("SELECT * FROM zstockprod")
data2 = cur.fetchall()

@app.route('/')
def display():
    cur = con.cursor()
    cur.execute("SELECT * FROM zstockprod")
    data2 = cur.fetchall()
    return render_template("template2.html", data2=data2)

@app.route('/addform')
def addform():

    return render_template("template3.html")

@app.route('/processjson2', methods = ['POST'])
def processjson2():
    data3 = request.get_data('ID')
    data3 = data3.decode("utf-8")
    data3 = str(data3)
    data3 = data3.strip('ID=')
    json_data = []
    stx = data3.split("%2C")
    for lyt in stx:
        cur.execute("SELECT productid, name, category, available, unitprice, datechecked FROM zstockprod WHERE ID=(%s)",(lyt))
        row_headers=[x[0] for x in cur.description]
        con.commit()
        data4 = cur.fetchall()
        cur.execute("DELETE FROM zstockprod WHERE ID=%s", (lyt))
        con.commit()        
        for row in data4:
            json_data.append(dict(zip(row_headers,row)))
    print(json_data)    
    return render_template("template1.html", data = Markup(json.dumps(json_data)))

@app.route('/processjson', methods = ['POST'])
def processjson():
    if request.method == 'POST':
        productid = request.form["productid"]
        name = request.form["name"]
        category = request.form["category"]
        available = request.form["available"]
        unitprice = request.form["unitprice"]
        datechecked = request.form["datechecked"] 
        cursor = con.cursor()
        sql = "INSERT INTO zstockprod(productid,name,category,available,unitprice,datechecked) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (productid,name,category,available,unitprice,datechecked)
        cursor.execute(sql, val)
        con.commit()
        results = cursor.fetchall()

        return redirect(url_for('display'))
    
    return render_template("template3.html")
    return jsonify({'result' : 'Success!', 'productid' : productid, 'name' : name, 'category' : category, 'available' : available, 'unitprice' : unitprice, 'datechecked' : datechecked})

#if __name__ == '__main__':
#  app.run(host='0.0.0.0',debug=True)
if __name__ == '__main__':
   if cf_port is None:
       app.run(host='0.0.0.0', port=5000)
   else:
       app.run(host='0.0.0.0', port=int(cf_port))    
