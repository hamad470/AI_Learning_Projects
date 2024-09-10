# Initialization 


from flask import Flask , template_rendered , jsonify ,request
app = Flask(__name__)




# Router contain address and request type 


# How many types of request can be possible 
# GET 
# POST
# PUT this api use for putting data on existing data 
# mean it use for update 
# DELETE Request is use for deleting data 


@app.route('/names',methods = ['GET'])
def names():
    
    
    data = {'username':"AKhlaq",'password':"12345"}

    return jsonify(data)


@app.route('/data/data=<data>')
def template_render(data):

    print(data)
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 5000)