import web, datetime, sqlite3

db = web.database(dbn='sqlite', db='blog')

def get_posts():
    return db.select('entries', order='id DESC')

def get_post(id):
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text, link, link_name):
    db.insert('entries', title=title, content=text, posted_on=datetime.datetime.utcnow(), link=link, link_name=link_name)

def del_post(id):
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text, link, link_name):
    db.update('entries', where="id=$id", vars=locals(),
        title=title, content=text, link=link, link_name=link_name)
