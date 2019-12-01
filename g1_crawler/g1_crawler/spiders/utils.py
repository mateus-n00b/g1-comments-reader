def body_to_json(body):
        # Convert body response to json
        body = body.split('({')[1].split('})')[0]
        body = eval("{"+body.replace('false', 'False')
        .replace('true','True')
        .replace('null',"False")+"}")

        return body
def save_in(file_name, data):
    file_out = open(file_name,"wb")
    file_out.write(data)
    file_out.close()