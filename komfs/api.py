root_path = '/komlog/samples/'

def create_sample(sid, data):
    filename = root_path+str(sid)
    try:
        file_handler = open(filename,'w')
        lenght = file_handler.write(data)
        file_handler.close()
    except:
        return False
    else:
        return True
