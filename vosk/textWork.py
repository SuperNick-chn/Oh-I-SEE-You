import sqlite3

def sqlinit():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    sql_text_1 = '''CREATE TABLE targets(TEXT)'''
    cur.execute(sql_text_1)

def del(obj):
    



def add(obj):




def solve(text):
   conn = sqlite3.connect('test.db')
   cur = conn.cursor()
   f = open('textlog.txt', 'a')
   if '没' in text:
       f.write('none\n')
   else:
       f.write('okay\n')
   f.close()
   
