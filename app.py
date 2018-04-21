from flask import Flask, render_template, json, request, redirect, session, flash
from flaskext.mysql import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import closing
from flask import jsonify




mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '******'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)





@app.route('/')
def main():
    return render_template('index.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')




@app.route('/signin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')







@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@app.route('/validateLogin', methods=['POST'])
def validateLogin():

    global _username

    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']


        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()
        print(_username)


        if check_password_hash(str(data[0][3]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')



    except Exception as e:
        return render_template('error.html', error=str(e))



@app.route('/signUp', methods=['GET', 'POST'])
def signUp():

    try:

        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']


        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            with closing(mysql.connect()) as conn:
                with closing(conn.cursor()) as cursor:
                    _hashed_password = generate_password_hash(_password)
                    cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
                    data = cursor.fetchall()


                conn.commit()

                return jsonify({'message': 'User created successfully !'})


    except Exception as e:
        return json.dumps({'error': str(e)})






@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')




@app.route('/addWish',methods=['POST'])
def addWish():

    _title = request.form['inputTitle']
    _description = request.form['inputDescription']
    _categories = request.form['selected']
    _user = session.get('user')



    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor.callproc('sp_addWish', (_title, _description,_user,_categories))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                print(_user)
                return redirect('/userHome')


            else:
                return render_template('error.html', error='An error occurred!')









@app.route('/getWish',methods=['POST', 'GET' ])
def getWish():
    _user = session.get('user')
    _categories = request.form['selected']

    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor = mysql.connect().cursor()
            if _categories == 'Wszystkie':

                result = cursor.execute('select * from tbl_wish where wish_user_id= "%s" ', _user)

            else:

                result = cursor.execute('select * from tbl_wish where wish_user_id= "%s" and kategoria = %s',
                                        (_user, _categories))
            data = cursor.fetchall()
            print(_categories)


            return render_template('getwish.html', data=data)





@app.route('/edit_wish/<string:id>/', methods=['GET', 'POST'])

def edit_wish(id):
    _user = session.get('user')

    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
            data = cursor.execute('select * from tbl_wish where wish_user_id= "%s" and wish_id = %s', (_user,id))
            data = cursor.fetchall()


            if request.method == 'POST':
                _title = request.form['inputTitle']
                _description = request.form['inputDescription']
                _user = session.get('user')


                with closing(mysql.connect()) as conn:
                    with closing(conn.cursor()) as cursor:
                        cursor.execute('update tbl_wish set wish_title=%s, wish_description=%s where wish_id=%s', (_title,_description,id))
                        data = cursor.fetchall()




                    conn.commit()

                    return redirect('wyszukiwarka')


    return render_template('editwish.html', data=data)


@app.route('/usuniete_zadanie/<string:id>', methods=['POST'])


def usuniete_zadanie(id):
    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
             cursor.execute("delete from tbl_wish where wish_id=%s", [id])
             data = cursor.fetchall()


        conn.commit()


        return redirect('wyszukiwarka')


@app.route('/wykonane_zadanie/<string:id>', methods=['POST'])


def wykonane_zadanie(id):
    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
             cursor.execute("insert into complete_wish (wish_id, wish_title, wish_description, wish_user_id, wish_date, kategoria) select wish_id, wish_title, wish_description, wish_user_id, wish_date, kategoria from tbl_wish where wish_id=%s", [id])
             cursor.execute("delete from tbl_wish where wish_id=%s", [id])
             data = cursor.fetchall()


        conn.commit()


        return redirect('wyszukiwarka')


@app.route('/listofCompleteWish',methods=['POST', 'GET' ])
def listofCompleteWish():
    _user = session.get('user')
    _categories2 = request.form['selected2']





    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor = mysql.connect().cursor()
            if _categories2 == 'Wszystkie':

                result = cursor.execute('select * from complete_wish where wish_user_id= "%s" ', _user)

            else:

                result = cursor.execute('select * from complete_wish where wish_user_id= "%s" and kategoria = %s',
                                        (_user, _categories2))
            data = cursor.fetchall()


            return render_template('listofCompleteWish.html', data=data)




@app.route('/wyszukiwarka',methods=['POST', 'GET' ])
def search():

    _user = session.get('user')

    return render_template('wyszukiwarka.html')



@app.route('/searchcompletetask',methods=['POST', 'GET' ])
def completetask():

    _user = session.get('user')

    return render_template('searchcompletetask.html')








@app.route('/addhabits',methods=['get', 'post' ])
def addhabits():




    if request.method == 'POST':
        _title3 = request.form['inputTitle3']
        _description3 = request.form['inputDescription3']
        _categories3 = request.form['selected']
        print(_categories3)
        _user3 = session.get('user')


        with closing(mysql.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "insert into tbl_habits (habits_title, habits_description, habits_user_id, habits_often) VALUES(%s, %s, %s, %s)",
                    (_title3, _description3, _user3, _categories3))

                data = cursor.fetchall()

                conn.commit()

        return redirect('/userHome')

    return render_template('addhabits.html')



@app.route('/gethabits',methods=['POST', 'GET' ])
def gethabits():
    _user = session.get('user')


    with closing(mysql.connect()) as conn:
        with closing(conn.cursor()) as cursor:
            cursor = mysql.connect().cursor()
            cursor.execute('select * from tbl_habits where habits_user_id= "%s" ', _user)

            data2 = cursor.fetchall()


            return render_template('gethabits.html', data2=data2)





@app.route('/kalendarz/<string:id>',methods=['get', 'post' ])
def test(id):





    if request.method == 'POST':
        _user = session.get('user')
        _date = request.form['data']

        with closing(mysql.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("insert into data_habits(habits_id,habits_user_id,data_wykonania) values (%s,%s,%s) ",
                               (id, _user, _date))
                data = cursor.fetchall()
                conn.commit()

        return redirect('/userHome')


    return render_template('kalendarz.html')


@app.route('/wybordaty/<string:id>',methods=['get', 'post' ])
def wybordaty(id):


    if request.method == 'POST':
        _user = session.get('user')
        _date1 = request.form['data']
        _date2 = request.form['data2']

        with closing(mysql.connect()) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("select data_wykonania from data_habits where habits_user_id=%s and data_wykonania between %s and %s",
                               (id, _date1, _date2))

                data = cursor.fetchall()
                conn.commit()

        return render_template('statystyki.html', data=data)

    return render_template('wybordaty.html')



if __name__ == "__main__":
    app.run(debug=True)


