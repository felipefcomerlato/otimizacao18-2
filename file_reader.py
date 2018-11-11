import os

#-------------------------------------------------------
# READ
def input_path():
    file_name = raw_input("Enter name of instance file: ")
    load("input_files/"+file_name)

def load(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file_object:
            try:
                getInfos(file_object)
                return True
            except:
                print("Fail while opening file. Try again!\n")
                input_path()
    else:
        print("Name file not exist. Try again!\n")
        input_path()

def getInfos(f):
    content = [x.strip() for x in f.readlines()]
    for line in content:
        print(line)



# END READ
#-----------------------------------------------------

input_path()
