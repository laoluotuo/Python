import hashlib
db = {}

def register(name, password):
    sha512 = hashlib.sha512()
    sha512.update((password + name +'12345').encode('utf-8'))
    db[name] = sha512.hexdigest()
    print(db[name])

def login(name, password):
    sha512 = hashlib.sha512()
    sha512.update((password + name +'12345').encode('utf-8'))
    if name in db.keys():
        if db[name] == sha512.hexdigest():
            print('Loggedin')
        else:print('Password Wrong')
    else:
        print('No name')

register('luo', 'yongjin')
print(db)
print(db['luo'])
# login('l','sfasf')
# login('luo', 'asofhiosdhf')
login('luo', 'yongjin')