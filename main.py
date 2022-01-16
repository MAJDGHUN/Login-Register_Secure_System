import names
from random import randint
from cryptography.fernet import Fernet
import MySQLdb
import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_mysqldb import MySQL
import base64
import MySQLdb.cursors
import re
import sqlite3
from flask import jsonify
import json
from bs4 import BeautifulSoup
import requests
from flask_ipban import IpBan
from datetime import datetime
import ssl

from flask import abort, render_template
from flask_login import current_user, login_required
from flask import Flask, render_template, request, redirect, url_for, session, abort
import time


app = Flask(__name__)



key = Fernet.generate_key()
#strkey = str(key)



with open("C:\pythonlogin\muftah2.key", "r") as f:

    key=f.readline()


print(key)


with open("C:\pythonlogin\sdsd.key") as f:
    lst = f.readlines()
    line1 = str(lst[0])[0:-1]
    line2 = str(lst[1])[0:-1]
    line3 = str(lst[2])[0:-1]
    line4 = str(lst[3])[0:-1]
    line5 = str(lst[4])[0:-1]
    line6 = str(lst[4])[0:-1]


fernet=Fernet( key)

sss="**********************"

#encrypted = fernet.encrypt(bytes(sss, 'utf-8'))

#dd=fernet.decrypt(bytes(sss,'utf-8'))



HOST =fernet.encrypt(line1.encode())
DATABASE=fernet.encrypt(line2.encode())
USER=fernet.encrypt(line3.encode())

PASSWORD=fernet.encrypt(line4.encode())
DATABASE2=fernet.encrypt(line5.encode())
Seck=fernet.encrypt(line6.encode())
#decpass= fernet.decrypt(PASSWORD).decode()
#print(decpass)
DEC_HOST =fernet.decrypt(HOST).decode()
DEC_DATABASE=fernet.decrypt(DATABASE).decode()
DEC_USER=fernet.decrypt(USER).decode()
DEC_PASSWORD=fernet.decrypt(PASSWORD).decode()
DEC_DATABASE2=fernet.decrypt(DATABASE2).decode()
DEC_Seck=fernet.decrypt(Seck).decode()

##print(DEC_PASSWORD)
###################

##################
app.secret_key = str(DEC_Seck)
# Enter your database connection details below
app.config['MYSQL_HOST'] = str(DEC_HOST)
app.config['MYSQL_USER'] = str(DEC_USER)
app.config['MYSQL_PASSWORD'] = str(DEC_PASSWORD)
app.config['MYSQL_DB'] = str(DEC_DATABASE)

print(str(DEC_PASSWORD))
mysql = MySQL(app)



#####################################
######################################

conn = sqlite3.connect(str(DEC_DATABASE2))
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS Tab_friends (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        friends text NOT NULL
                                    ); """

conn.execute(sql_create_projects_table)

conn.close()



# Enter your database connection details below




# http://localhost:5000/pythonlogin/
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():

    msg = ''

    # if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        
    #     ss= jsonify({'ip': request.environ['REMOTE_ADDR']}), 200
    #     print(request.environ['REMOTE_ADDR'])
    listt=[]


  
    if request.environ.get('HTTP_X_FORWARDED_FOR') is not None:
        
        ss= jsonify({'ip': request.environ['HTTP_X_FORWARDED_FOR']}), 200
        print(request.environ['HTTP_X_FORWARDED_FOR'])
        ipp=request.environ['HTTP_X_FORWARDED_FOR']
        
        
        URL = ("https://myip.ms/info/whois/"+str(ipp))
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        print(ss)

        for d in soup.findAll('div', attrs={'id':'fixed_width_page'}):
            
            you = d.find('tbody')
                

            sss=you.findAll('a')
                
            for s in sss:
                listt.append(s.text)

                
            if len(listt)>=13 and listt[13] =="Belgium":
                print("you are Authorized")
            

            else:
                    
                return render_template('unauthorized.html')
                

        else:
            pass
            

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      
        username = request.form['username']
        password = request.form['password']
        
      
        
        #DEC_password =fernet.decrypt(ENC_password).decode()
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT password FROM accounts WHERE username = %s', (username,))
        accountpass = cursor.fetchall()
        accountpass2 = str(accountpass)
        
        listt= []
        
        i=14

        sizeofList = len(accountpass2)
        while i < sizeofList:
            
            if accountpass2[i] == "'" or accountpass2[i] =="(" or accountpass2[i] =="{" or accountpass2[i] ==")" or accountpass2[i] =="}" or accountpass2[i] ==":" or accountpass2[i] ==",":
                pass

            else:
                listt.append(accountpass2[i])
            i += 1

        listToStr = ''.join(map(str, listt))
  
        print(listToStr) 
        #encrypted = fernet.encrypt(bytes(sss, 'utf-8'))
        try:
            passdec=fernet.decrypt((listToStr.encode())).decode()
            ENC_password=fernet.encrypt(bytes(password.encode()))
        
        
            password2=ENC_password

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
        

        except:
            passdec = "========================"



  
        

        


        if (passdec)==(password):
           
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            ##last login
            timestamp= datetime.now()
            print(timestamp)


            try:
                cursor.execute('INSERT INTO user_action VALUES (%s, %s, %s)', (session['id'],"Login",timestamp))
                mysql.connection.commit()
                cursor.close()
            except:
       


                cursor.execute("""UPDATE user_action SET  id= %s, action= %s,timestamp= %s WHERE id= %s""", (session['id'], "Login", timestamp,session['id']))
        
                mysql.connection.commit()
                cursor.close()
                


            
  
            
            
            # Redirect to home page

            return redirect(url_for('home'))
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Your username can only contain alphanumeric characters!'
            
        elif len(str(password)) < 8 or "|" in str(password) or "=" in str(password) or "-" in str(password) or "'" in str(password):
            msg = 'Invalid password input'
            
      

        else:
        
            msg = 'Incorrect username/password!'
        
        ####
       
    

    return render_template('index.html', msg=msg)


@app.route('/pythonlogin/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')
    

   
        
     
        


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    
    msg = ''
   
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'hobby' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        hobby = request.form['hobby']
        
        ENC_password=fernet.encrypt(bytes(password.encode()))
        
        
        password2=ENC_password
        

        

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
      
        
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only letter and numbers!'
        elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$", password):
            msg = 'Password must contain at least one upper character, one lower character, one digit and one special character. You can only use !, # and $. Minimum length of 8.'
            
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s)', (username, password2, email,hobby))
            mysql.connection.commit()
            cursor.close()
            msg = 'You have successfully registered!'

            timestamp= datetime.now()

          
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select id FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            new_id= account.get('id')
         
         
            print("///////////")
            print(new_id)
           
            print("///////////")
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO user_action VALUES (%s, %s, %s)', (new_id,"Register",timestamp))
            mysql.connection.commit()
            cursor.close()
            

    elif request.method == 'POST':
        msg = 'Please fill out the form!'




    return render_template('register.html', msg=msg)

@app.route('/pythonlogin/home')
def home():
  
    if 'loggedin' in session:
       
        return render_template('home.html', username=session['username'])

    return redirect(url_for('login'))



 





@app.route('/pythonlogin/update', methods=['GET', 'POST'])
def update():
    
    msg = ''
    if 'loggedin' in session:
   
      
   
        if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'hobby' in request.form:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            hobby = request.form['hobby']

            # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            
            cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
            account = cursor.fetchone()
            
            
            #  validation checks
            if not account:
                msg = 'Account is not exists!'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address!'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers!'
            elif not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$", password):
                msg = 'Password must contain at least one upper character, one lower character, one digit and one special character. You can only use !, # and $. Minimum length of 8.'
                
            elif not username or not password or not email:
                msg = 'Please fill out the form!'
            else:
                ENC_password=fernet.encrypt(bytes(password.encode()))

                password2=ENC_password
               
                cursor.execute("""UPDATE accounts SET  username= %s, password= %s,email= %s,hobby= %s WHERE id= %s""", (username, password2, email,hobby, session['id']))
                mysql.connection.commit()
                cursor.close()
                
                msg = 'You have successfully Updated!'
                timestamp= datetime.now()
                try:
                    cursor.execute('INSERT INTO user_action VALUES (%s, %s, %s)', (session['id'],"Update",timestamp))
                    mysql.connection.commit()
                    

                except:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

                    cursor.execute("""UPDATE user_action SET  action= %s,timestamp= %s WHERE id= %s""", ("Update", timestamp,session['id']))
            
                    mysql.connection.commit()
                    cursor.close()


                return render_template('update.html', msg=msg)
        return render_template('update.html', msg=msg)
            
        



    return redirect(url_for('login'))




@app.route('/pythonlogin/delete', methods=['GET', 'POST'])
def delete():
  
    msg = ''
    if 'loggedin' in session:
   
        
   
        if request.method == 'POST' :
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
            account =cursor.execute('DELETE FROM accounts WHERE id = %s ', (session['id'],))
            mysql.connection.commit()
            cursor.close()

            timestamp= datetime.now()
         


            try:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO user_action VALUES (%s, %s, %s)', (session['id'],"Delete",timestamp))
                mysql.connection.commit()
                cursor.close()
            except:
       

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("""UPDATE user_action SET  id= %s, action= %s,timestamp= %s WHERE id= %s""", (session['id'], "Delete", timestamp,session['id']))
        
                mysql.connection.commit()
                cursor.close()
                

            
            msg = 'Your account has been deleted successfully!'
            time.sleep(5)
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)

   
            return render_template('delete.html', msg=msg)

  
          
        return render_template('delete.html', msg=msg)
        

        

   

   
    return redirect(url_for('login'))

@app.route('/pythonlogin/logout')
def logout():
 

   cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
   account =cursor.execute('DELETE FROM accounts WHERE id = %s ', (session['id'],))
   mysql.connection.commit()
   cursor.close()

   timestamp= datetime.now()
         


   try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO user_action VALUES (%s, %s, %s)', (session['id'],"Logout",timestamp))
        mysql.connection.commit()
        cursor.close()
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('login'))
   except:
       

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""UPDATE user_action SET  id= %s, action= %s,timestamp= %s WHERE id= %s""", (session['id'], "Logout", timestamp,session['id']))
        
        mysql.connection.commit()
        cursor.close()
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('login'))
                




@app.route('/pythonlogin/add', methods=['GET', 'POST'])

def add():
    
    msg = ''
    if 'loggedin' in session:

        if request.method == 'POST' and 'friend' in request.form:
           
            friend = request.form['friend']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            account =cursor.execute('SELECT * FROM accounts WHERE username = %s ', (friend,))
            cursor.close()
            
            print(account)
        


            conn = sqlite3.connect(str(DEC_DATABASE2))
            account2 = conn.execute('SELECT * FROM Tab_friends WHERE username = ?', (friend,))
            
            print(str(account2))

          
            if account :
                
                conn = sqlite3.connect(str(DEC_DATABASE2))
                account2 = conn.execute('INSERT INTO Tab_friends VALUES (NULL, ?, ?)', (session['username'], friend))
                conn.commit()
                conn.close()
                
                msg = 'You have successfully added your friend!'
                timestamp= datetime.now()
                try:
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO user_action VALUES (%s, %s, %s)', (session['id'],"Add",timestamp))
                    mysql.connection.commit()
                    cursor.close()
                except:
        

                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute("""UPDATE user_action SET  id= %s, action= %s,timestamp= %s WHERE id= %s""", (session['id'], "Add", timestamp,session['id']))
            
                    mysql.connection.commit()
                    cursor.close()
                



            else:
                msg = 'Friend not found!'
                
                

                
        return render_template('add.html', msg=msg)
            
        



    return redirect(url_for('login'))



@app.route('/pythonlogin/profile')
def profile():

    if 'loggedin' in session:
        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        cursor.close()
       
        return render_template('profile.html', account=account)
  
    return redirect(url_for('login'))






key="C:\\pythonlogin\privkey.pem"
cert="C:\\pythonlogin\certificate.crt"
#ssl_context=context.load_cert_chain(cert,key)
#ssl_context='adhoc'
if __name__ == '__main__':
    app.run(host='localhost',debug=True,port=5000,ssl_context='adhoc')
    #app.run(host='localhost',debug=True,port=5000,ssl_context='adhoc')
