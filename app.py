from flask import Flask,render_template,url_for,request,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
import sqlite3

app = Flask(__name__)
app.secret_key='somekey'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///casestudy.db'
db= SQLAlchemy(app)
SQLALCHEMY_TRACK_MODIFICATIONS = False

class userstore(db.Model):
    uname=db.Column(db.String,primary_key=True)
    password=db.Column(db.String)
class patients(db.Model):
    __tablename__="patients"
    ssnid=db.Column(db.String(9),unique=True)
    patient_id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String)
    age=db.Column(db.Integer)
    date_of_admission=db.Column(db.DateTime,default=datetime.utcnow)
    bed=db.Column(db.String)
    address=db.Column(db.String)
    city=db.Column(db.String)
    state=db.Column(db.String)
    status=db.Column(db.String,default='Active')
class medicine_records(db.Model):
    record_id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.String)
    medicine_id=db.Column(db.String)
    medicine_name=db.Column(db.String)
    quantity=db.Column(db.Integer)
    total=db.Column(db.Integer)
class medicine(db.Model):
    medicine_idno=db.Column(db.Integer,primary_key=True)
    medicine_id=db.Column(db.String,unique=True)
    medicine_name=db.Column(db.String)
    price=db.Column(db.Integer)
class test_records(db.Model):
    record_id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.String)
    test_id=db.Column(db.String)
    test_name=db.Column(db.String)
    total=db.Column(db.Integer)
class test(db.Model):
    test_idno=db.Column(db.Integer,primary_key=True)
    test_id=db.Column(db.String)
    test_name=db.Column(db.String)
    price=db.Column(db.Integer)

db.create_all()

@app.route('/',methods=['GET','POST'])
def index():
    if request.method== 'POST':
            username=request.form.get('username')
            password=request.form.get('password')
            conn=sqlite3.connect('casestudy.db')
            c=conn.cursor()
            command='SELECT * FROM userstore;'
            c.execute(command)
            r=c.fetchall()
            for i in r:
                session['username']=username
                if (i[0]==username) and (i[1]==password):
                    return render_template('user.html')
            return render_template('login.html',message1='invalid password')        
    else:
        return render_template('login.html')
    return render_template('login.html')

@app.route('/log_out',methods=['GET','POST'])
def log_out():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = request.form.get('username')
        newpassword= request.form.get('newpassword')
        confirmpassword=request.form.get('confirmpassword')
        admin = userstore(uname=user, password=confirmpassword)
        db.session.add(admin)
        db.session.commit()
        time.sleep(3)
        return render_template("user.html")
    else:   
        return render_template('register.html')

@app.route('/patient_register',methods=['GET','POST'])
def patient_register():
    if 'username' in session:
        if request.method=='POST':
            ssnid1=request.form.get('ssnid')
            patientname=request.form.get('name')
            age1=request.form.get('age')
            address1=request.form.get('address')
            bed1=request.form.get('bed')
            city1=request.form.get('city')
            state1=request.form.get('state')
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = """SELECT * from patients"""
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall()
            for o in dat:
                if o[0]==ssnid1:
                    flash('SSN id already found in database')
                    time.sleep(3)
                    return render_template('patient_register.html',message1="SSN id already exists. Please reenter.")
            the_data=patients(ssnid=ssnid1,name=patientname,age=age1,address=address1,bed=bed1,city=city1,state=state1)
            db.session.add(the_data)
            db.session.commit()
            return render_template('user.html')
        else:        
            return render_template('patient_register.html')
    else:
        return redirect(url_for('index'))

@app.route('/patient_status',methods=['GET','POST'])
def patient_status():
    if 'username' in session:
        s=sqlite3.connect('casestudy.db')
        c=s.cursor()
        execute_query="SELECT * FROM patients"
        c.execute(execute_query)
        r=c.fetchall()
        return render_template('patient_status.html',data=r)

@app.route('/update_patient',methods=['GET','POST'])
def update_patient():
    if 'username' in session:
        if request.method=='POST':
            whichbutton=request.form.get('submit')
            if whichbutton == 'submit':
                idno=request.form.get('idno')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                try:
                    execute_statement="SELECT * FROM patients where ssnid="+"'"+idno+"'"
                    m=cursor.execute(execute_statement)
                    data=cursor.fetchall()
                    name=data[0][2]
                    age=data[0][3]
                    bed=data[0][5]
                    address=data[0][6]
                    city=data[0][7]
                    state=data[0][8]
                    status=data[0][9]
                    sqliteconnection.close()
                    return render_template('update_patient.html',hidden1=idno,bed1=bed,message1=idno,name1=name,age1=age,address1=address,city1=city,state1=state,status1=status)
                except:
                    return render_template('update_patient.html',message1="SSN id not found")
            if whichbutton =="update":
                idno=request.form.get('hidden')
                name2=request.form.get('name')
                age2=str(request.form.get('age'))
                bed2=request.form.get('bed')
                address=request.form.get('address')
                city2=request.form.get('city')
                state2=request.form.get('state')
                status2=request.form.get('status')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                execute_statement="UPDATE patients SET age="+age2+",name="+"'"+name2+"'"+",bed="+"'"+bed2+"'"+",address="+"'"+address+"'"+",city="+"'"+city2+"'"+",state="+"'"+state2+"'"+",status="+"'"+status2+"'"+" WHERE ssnid="+"'"+idno+"';"
                cursor.execute(execute_statement)
                sqliteconnection.commit()
                return render_template('user.html',message1='Successfully updated')
                
            return render_template('update_patient.html',message1='Please reenter SSNID. Entered SSNID does not exist.')
        else:
            return render_template('update_patient.html')
    else:
        return redirect(url_for('index'))

@app.route('/delete_patient_record',methods=['GET','POST'])
def delete_patient_record():
    if 'username' in session:
        if request.method=='POST':
            whichbutton=request.form.get('submit')
            if whichbutton == 'submit':
                idno=request.form.get('idno')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                try:
                    execute_statement="SELECT * FROM patients where ssnid="+"'"+idno+"'"
                    m=cursor.execute(execute_statement)
                    data=cursor.fetchall()
                    name=data[0][2]
                    age=data[0][3]
                    bed=data[0][5]
                    address=data[0][6]
                    city=data[0][7]
                    state=data[0][8]
                    status=data[0][9]
                    sqliteconnection.close()
                    return render_template('delete_patient_record.html',hidden1=idno,bed1=bed,message1=idno,name1=name,age1=age,address1=address,city1=city,state1=state,status1=status)
                except:
                    return render_template('delete_patient_record.html',message1="SSN id not found")
            if whichbutton =="delete":
                idno=request.form.get('hidden')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                execute_statement="DELETE from patients WHERE ssnid="+"'"+idno+"';"
                cursor.execute(execute_statement)
                sqliteconnection.commit()
                return render_template('user.html',message1='Successfully deleted patient record')
                
            return render_template('delete_patient_record.html',message1='Please reenter SSNID. Entered SSNID does not exist.')
        else:
            return render_template('delete_patient_record.html')
    else:
        return redirect(url_for('index'))

@app.route('/patient_search',methods=['GET','POST'])
def patient_search():
    if 'username' in session:
        if request.method=='POST':
            whichbutton=request.form.get('submit')
            if whichbutton == 'submit':
                idno=request.form.get('idno')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                try:
                    execute_statement="SELECT * FROM patients where ssnid="+"'"+idno+"'"
                    m=cursor.execute(execute_statement)
                    data=cursor.fetchall()
                    name=data[0][2]
                    age=data[0][3]
                    checked_in=data[0][4]
                    checked_in=checked_in[0:10]
                    bed=data[0][5]
                    address=data[0][6]
                    city=data[0][7]
                    state=data[0][8]
                    status=data[0][9]
                    sqliteconnection.close()
                    return render_template('patient_search.html',hidden1=idno,bed1=bed,message1=idno,name1=name,checked_in1=checked_in,age1=age,address1=address,city1=city,state1=state,status1=status)
                except:
                    return render_template('patient_search.html',message1="SSN id not found")
        else:
            return render_template('patient_search.html')
    else:
        return redirect(url_for('index'))

@app.route('/add_medicine',methods=['GET','POST'])
def add_medicine():
    if 'username' in session:
        if request.method=='POST':
            medid1=request.form.get('medid')
            name=request.form.get('name')
            rate=request.form.get('rate')
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = """SELECT * from medicine"""
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall()
            for o in dat:
                if o[1]==medid1 or o[2]==name:
                    flash('Medicine already found in database')
                    return render_template('add_medicine.html',message1="Medicine already exists.Please check medicine table.")
            the_data=medicine(medicine_id=medid1,price=rate,medicine_name=name)
            db.session.add(the_data)
            db.session.commit()
            return render_template('add_medicine.html',message1="Medicine Successfully added.")
        else:        
            return render_template('add_medicine.html')
    else:
        return redirect(url_for('index'))

@app.route('/issue_medicine',methods=['GET','POST'])
def issue_medicine():
    if 'username' in session:
        if request.method=='POST':
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = "SELECT medicine_name from medicine;"
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall() 
            sqliteconnection.close()
            patid1=request.form.get('patid')
            name=request.form.get('name')
            quantity1=int(request.form.get('quantity'))
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = "SELECT * from medicine WHERE medicine_name="+"'"+name+"';"
            cursor.execute(sqlite_select_query)
            dat1=cursor.fetchall()
            price1=dat1[0][3]
            med_id1=dat1[0][1]
            sqliteconnection.close()
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            try:
                sqlite_select_query = "SELECT ssnid from patients where ssnid="+"'"+patid1+"';"
                cursor.execute(sqlite_select_query)
                total1=price1*quantity1
                bat=cursor.fetchall()
                the_id=bat[0][0]
            except:
                return render_template('issue_medicine.html',data=dat,message1="SSN id not found in patients database.")
            for i in bat:
                if i[0]==patid1:
                    the_data=medicine_records(medicine_name=name,medicine_id=med_id1,quantity=quantity1,patient_id=patid1,total=total1)
                    db.session.add(the_data)
                    db.session.commit()
            if the_id=="":
                return render_template('issue_medicine.html',data=dat,message1="SSN id not found in patients database.")
            return render_template('issue_medicine.html',data=dat,message1="Medicine Successfully issued.")
        else:
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = "SELECT medicine_name from medicine;"
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall() 
            sqliteconnection.close()
            return render_template('issue_medicine.html',data=dat)
    else:
        return redirect(url_for('index'))

@app.route('/edit_medicine',methods=['GET','POST'])
def edit_medicine():
    if 'username' in session:
        if request.method=='POST':
            whichbutton=request.form.get('submit')
            if whichbutton == 'submit':
                idno=request.form.get('idno')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                try:
                    execute_statement="SELECT * FROM medicine where medicine_id="+"'"+idno+"'"
                    m=cursor.execute(execute_statement)
                    data=cursor.fetchall()
                    name=data[0][2]
                    price=data[0][3]
                    sqliteconnection.close()
                    return render_template('edit_medicine.html',hidden1=idno,message1=idno,name1=name,price1=price)
                except:
                    return render_template('edit_medicine.html',message1="medicine id not found")
            if whichbutton =="update":
                idno=request.form.get('hidden')
                name2=request.form.get('name')
                price2=str(request.form.get('price'))
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                execute_statement="UPDATE medicine SET price="+price2+",medicine_name="+"'"+name2+"'"+" WHERE medicine_id="+"'"+idno+"';"
                cursor.execute(execute_statement)
                sqliteconnection.commit()
                return render_template('edit_medicine.html',message1='Successfully updated')
            if whichbutton =="delete":
                idno=request.form.get('hidden')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                execute_statement="DELETE from medicine WHERE medicine_id="+"'"+idno+"';"
                cursor.execute(execute_statement)
                sqliteconnection.commit()
                return render_template('user.html',message1='Successfully deleted medicine record')    
            return render_template('edit_medicine.html',message1='Please reenter medicine id. Entered id does not exist.')
        else:
            return render_template('edit_medicine.html')
    else:
        return redirect(url_for('index'))

@app.route('/view_medicine',methods=['GET','POST'])
def view_medicine():
    if 'username' in session:
        s=sqlite3.connect('casestudy.db')
        c=s.cursor()
        execute_query="SELECT * FROM medicine"
        c.execute(execute_query)
        r=c.fetchall()
        return render_template('view_medicine.html',data=r)
    else:
        return redirect(url_for('index'))

@app.route('/view_tests',methods=['GET','POST'])
def view_tests():
    if 'username' in session:
        s=sqlite3.connect('casestudy.db')
        c=s.cursor()
        execute_query="SELECT * FROM test;"
        c.execute(execute_query)
        r=c.fetchall()
        return render_template('view_tests.html',data=r)
    else:
        return redirect(url_for('index'))

@app.route('/add_test',methods=['GET','POST'])
def add_test():
    if 'username' in session:
        if request.method=='POST':
            testid1=request.form.get('testid')
            name=request.form.get('name')
            rate=request.form.get('rate')
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = """SELECT * from test"""
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall()
            for o in dat:
                if o[1]==testid1 or o[2]==name:
                    flash('test already found in database')
                    return render_template('add_test.html',message1="test already exists.Please check test table.")
            the_data=test(test_id=testid1,price=rate,test_name=name)
            db.session.add(the_data)
            db.session.commit()
            return render_template('add_test.html',message1="Test Successfully added.")
        else:        
            return render_template('add_test.html')
    else:
        return redirect(url_for('index'))

@app.route('/issue_test',methods=['GET','POST'])
def issue_test():
    if 'username' in session:
        if request.method=='POST':
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = "SELECT test_name from test;"
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall() 
            sqliteconnection.close()
            patid1=request.form.get('patid')
            name=request.form.get('name')
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = "SELECT * from test WHERE test_name="+"'"+name+"';"
            cursor.execute(sqlite_select_query)
            dat1=cursor.fetchall()
            price1=dat1[0][3]
            test_id1=dat1[0][1]
            sqliteconnection.close()
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            try:
                sqlite_select_query = "SELECT ssnid from patients where ssnid="+"'"+patid1+"';"
                cursor.execute(sqlite_select_query)
                total1=price1
                bat=cursor.fetchall()
                the_id=bat[0][0]
            except:
                return render_template('issue_test.html',data=dat,message1="SSN id not found in patients database.")
            for i in bat:
                if i[0]==patid1:
                    the_data=test_records(test_name=name,test_id=test_id1,patient_id=patid1,total=total1)
                    db.session.add(the_data)
                    db.session.commit()
            if the_id=="":
                return render_template('issue_test.html',data=dat,message1="SSN id not found in patients database.")
            return render_template('issue_test.html',data=dat,message1="Test Successfully issued.")
            
        else:
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            sqlite_select_query = "SELECT test_name from test;"
            cursor.execute(sqlite_select_query)
            dat=cursor.fetchall() 
            sqliteconnection.close()
            return render_template('issue_test.html',data=dat)
    else:
        return redirect(url_for('index'))

@app.route('/edit_test',methods=['GET','POST'])
def edit_test():
    if 'username' in session:
        if request.method=='POST':
            whichbutton=request.form.get('submit')
            if whichbutton == 'submit':
                idno=request.form.get('idno')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                try:
                    execute_statement="SELECT * FROM test where test_id="+"'"+idno+"'"
                    m=cursor.execute(execute_statement)
                    data=cursor.fetchall()
                    name=data[0][2]
                    price=data[0][3]
                    sqliteconnection.close()
                    return render_template('edit_test.html',hidden1=idno,message1=idno,name1=name,price1=price)
                except:
                    return render_template('edit_test.html',message1="test id not found")
            if whichbutton =="update":
                idno=request.form.get('hidden')
                name2=request.form.get('name')
                price2=str(request.form.get('price'))
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                execute_statement="UPDATE test SET price="+price2+",test_name="+"'"+name2+"'"+" WHERE test_id="+"'"+idno+"';"
                cursor.execute(execute_statement)
                sqliteconnection.commit()
                return render_template('edit_test.html',message1='Successfully updated')
            if whichbutton =="delete":
                idno=request.form.get('hidden')
                sqliteconnection=sqlite3.connect('casestudy.db')
                cursor=sqliteconnection.cursor()
                execute_statement="DELETE from test WHERE test_id="+"'"+idno+"';"
                cursor.execute(execute_statement)
                sqliteconnection.commit()
                return render_template('user.html',message1='Successfully deleted test record')    
            return render_template('edit_test.html',message1='Please reenter test id. Entered id does not exist.')
        else:
            return render_template('edit_test.html')
    else:
        return redirect(url_for('index'))

@app.route('/view_issued_medicine',methods=['GET','POST'])
def view_issued_medicine():
    if 'username' in session:
        if request.method=='POST':
            idno=request.form.get('idno')
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            try:
                execute_statement="SELECT * FROM medicine_records where patient_id="+"'"+idno+"'"
                m=cursor.execute(execute_statement)
                dat1=cursor.fetchall()
                return render_template('view_issued_medicine.html',data=r)
            except:
                s=sqlite3.connect('casestudy.db')
                c=s.cursor()
                execute_query="SELECT * FROM medicine_records;"
                c.execute(execute_query)
                r=c.fetchall()
                return render_template('view_issued_medicine.html',data=r,message1="Patient SSN id not found in database.")

        else:
            s=sqlite3.connect('casestudy.db')
            c=s.cursor()
            execute_query="SELECT * FROM medicine_records;"
            c.execute(execute_query)
            r=c.fetchall()
            return render_template('view_issued_medicine.html',data=r)
    else:
        return redirect(url_for('index'))

@app.route('/view_issued_test',methods=['GET','POST'])
def view_issued_test():
    if 'username' in session:
        if request.method=='POST':
            idno=request.form.get('input')
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            try:
                execute_statement="SELECT * FROM test_records where patient_id="+"'"+idno+"'"
                m=cursor.execute(execute_statement)
                dat1=cursor.fetchall()
                return render_template('view_issued_test.html',data=dat1)
            except:
                s=sqlite3.connect('casestudy.db')
                c=s.cursor()
                execute_query="SELECT * FROM test_records;"
                c.execute(execute_query)
                r=c.fetchall()
                return render_template('view_issued_test.html',data=r,message1="Patient SSN id not found")
        else:
            s=sqlite3.connect('casestudy.db')
            c=s.cursor()
            execute_query="SELECT * FROM test_records;"
            c.execute(execute_query)
            r=c.fetchall()
            return render_template('view_issued_test.html',data=r)
    else:
        return redirect(url_for('index'))

@app.route('/final_billing',methods=['GET','POST'])
def final_billing():
    if 'username' in session:
        if request.method=='POST':
            idno=request.form.get('input')
            s=sqlite3.connect('casestudy.db')
            c=s.cursor()
            
            execute_query="SELECT * FROM patients where ssnid="+"'"+idno+"';"
            c.execute(execute_query)
            r=c.fetchall()
            s.close()
            for i in r:
                admit_date=i[4]
                bed=i[5]
            try:
                admit_date=admit_date[0:10]
                a_y=int(admit_date[0:4])
                a_m=int(admit_date[5:7])
                a_d=int(admit_date[8:10])
            except:
                return render_template('final_billing.html',message1="Patient ssn id does not exist.Please reenter and try again.")
            a_date=datetime(a_y,a_m,a_d)
            discharge=str(datetime.utcnow())[0:10]
            discharge_date=str(datetime.utcnow())
            d_y=int(discharge_date[0:4])
            d_m=int(discharge_date[5:7])
            d_d=int(discharge_date[8:10])
            d_date=datetime(d_y,d_m,d_d)

            day=(d_date-a_date).days
            if admit_date=="":
                return render_template('final_billing.html',message1="ssn id does not exist")
            if bed=="general ward":
                bed_rate=2000
            elif bed=="semi sharing":
                bed_rate=4000
            else:
                bed_rate=8000
            bed_total=bed_rate*day
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            query="SELECT * FROM medicine_records WHERE patient_id="+"'"+idno+"';"
            cursor.execute(query)
            dat=cursor.fetchall()
            sqliteconnection.close()
            sqliteconnection=sqlite3.connect('casestudy.db')
            cursor=sqliteconnection.cursor()
            query="SELECT * FROM test_records WHERE patient_id="+"'"+idno+"';"
            cursor.execute(query)
            dat1=cursor.fetchall()
            sqliteconnection.close()
            med_list=[]
            test_list=[]
            med_total=0
            test_total=0
            try:
                for i in dat:
                    med_list.append(i[5])
                med_total=sum(med_list)+med_total 
            except:
                pass
            try:
                for o in dat1:
                    test_list.append(o[4])
                test_total=sum(test_list)+test_total
            except:
                pass
            grandtotal=med_total+test_total+bed_total
            return render_template('final_billing.html',discharge1=discharge,data2=r,medtotal1=med_total,testtotal1=test_total,grandtotal1=grandtotal,data=dat,data1=dat1,bed_total1=bed_total)
        else:
            return render_template('final_billing.html')
    else:
        return redirect(url_for('index'))




if __name__=="__main__":
    app.run(debug=True)
