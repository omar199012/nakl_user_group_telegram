from sqlitedict import SqliteDict
import subprocess
import random
import validators

def is_urls(U):
    if validators.url(U):
        return True
    else:
        return False

class sql():
    def __init__(self, param):
        self.param = param

def save(key, value, cache_file="sql/cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            mydict[key] = value # Using dict[key] to store
            mydict.commit() # Need to commit() to actually flush the data
    except Exception as ex:
        pass
def load(key, cache_file="sql/cache.sqlite3"):
    try:
        with SqliteDict(cache_file) as mydict:
            value = mydict[key] # No need to use commit(), since we are only loading data!
        return value
    except Exception as ex:
        pass

def put(var, value, cache_file="sql/cache.sqlite3"):
    sqlite = sql(value)
    save(var, sqlite, cache_file=cache_file)

def get(var, cache_file="sql/cache.sqlite3"):
    try:
        obj2 = load(var, cache_file)
        return obj2.param
    except:
        return 0

def send_shell(*arg):
    command = subprocess.Popen(arg)

def file_put(filename,data):
    f = open(filename, "w")
    f.write(data)
    f.close()

def file_append(filename,data):
    f = open(filename, "a")
    f.write(data)
    f.close()
  

def read(filename):
    f = open(filename, "r")
    return f.read()

def randtext(num):
    arr = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    randtext = ''
    for i in range(num):
        randtext += str(arr[random.randint(0, len(arr) - 1)])
    return randtext
    
def send_command(cmd1, cmd2='not', cmd3='not', cmd4='not', cmd5='not', cmd6='not', cmd7='not'):
    command = 'python3 '+ cmd1 + ' ' + cmd2 + ' ' + cmd3 + ' ' + cmd4 + ' ' + cmd5 + ' ' + cmd6 + ' ' + cmd7
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]

def is_int(num):
    try:
        int(num)
        return True
    except:
        return False


def is_tele(U):
    try:
        sp = U.split('/')
        if sp[-1][0] == '+':
            return ['PV', U]
        
        if sp[-1][0] in ['1','2','3','4','5','6', '7','8','9','0']:
            return False
        else:
            return ['PU', '@'+sp[-1]]
    except:
        return False
    
