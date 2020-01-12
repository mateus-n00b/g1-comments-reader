import os
import datetime

def body_to_json(body):
        # Convert body response to json
        body = body.split('({')[1].split('})')[0]
        body = eval("{"+body.replace('false', 'False')
        .replace('true','True')
        .replace('null',"False")+"}")

        return body
def save_in(filename, data):
    date = datetime.datetime.now()
    path = "comments_{0}-{1}-{2}".format(date.day, date.month, date.year)
    try: 
        os.mkdir(path)
    except:
        pass
    file_out = open(path+"/"+filename,"w")
    file_out.write(str(data))
    file_out.close()