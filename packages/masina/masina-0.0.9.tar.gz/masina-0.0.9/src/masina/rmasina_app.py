from datetime import datetime
import traceback
import sys
import re
import os
import csv
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask import send_file, send_from_directory, Response
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from mysqlquerys import connect
from mysqlquerys import mysql_rm
from auto import Masina, Users


UPLOAD_FOLDER = r"D:\Python\test"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://newuser_radu:Paroladetest_1234@localhost/cheltuieli_desktop"
app.config['SECRET_KEY'] = "my super secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'

ini_file = r"D:\Python\MySQL\masina.ini"
# ini_file = '/home/radum/rmasina/static/wdb.ini'
report_file = '/home/radum/rmasina/report.csv'


conf = connect.Config(ini_file)



@login_manager.user_loader
def load_user(user_id):
    print(25*'Ä')
    print(sys._getframe().f_code.co_name, request.method)
    print('##**##user_id _{}_'.format(user_id), type(user_id))
    try:
        mat = int(user_id)
    except:
        mat = int(re.findall("\[(.+?)\]", user_id)[0])

    matches = ('id', mat)
    users_table = mysql_rm.Table(conf.credentials, 'users')
    name = users_table.returnCellsWhere('username', matches)[0]

    user = Users(name)
    # print('##user.user_access', user.admin)
    print(25 * 'Ä')
    return user


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        return render_template('index.html')
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        if request.method == "POST":
            username = request.form['username']
            user = Users(username)
            if not user.valid_user:
                print('User {} not in database'.format(username))
                return redirect(url_for("login"))
            if user.verify_password(request.form['password']):
                login_user(user)
                return redirect(url_for("index"))
        return render_template("login.html")
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        logout_user()
        return redirect(url_for('index'))
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        conf = connect.Config(ini_file)
        users_table = mysql_rm.Table(conf.credentials, 'users')
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            cols = ('username', 'password')
            hash = generate_password_hash(password)
            vals = (username, hash)
            users_table.addNewRow(cols, vals)
            user = Users(username)
            login_user(user)
            return redirect(url_for("index"))
        elif request.method == 'GET':
            print('****', request.method)

        return render_template('register.html')
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/car/<table_name>', methods=['GET', 'POST'])
def car(table_name):
    print('Module: {}, Def: {}, Caller: {}'.format(__name__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    try:
        print(sys._getframe().f_code.co_name, request.method)
        if request.method == 'POST':
            if 'export_detail_table_as_csv' in request.form:
                app_masina = Masina(conf.credentials, table_name=table_name.lower())
                dataFrom, dataBis = app_masina.default_interval
                alim_type = None
                alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
                exact_path = "report.csv"
                with open(exact_path, 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    for row in alimentari:
                        writer.writerow('rrrr')
                        writer.writerow(row)
                return send_file(exact_path, as_attachment=True)

        app_masina = Masina(conf.credentials, table_name=table_name.lower())
        session['current_table'] = table_name.lower()
        session['types_of_costs'] = app_masina.types_of_costs
        if app_masina.no_of_records == 0:
            # return "<h1>Please insert some data</h1>"
            session['current_table'] = table_name.lower()
            session['types_of_costs'] = app_masina.types_of_costs
            return redirect(url_for("addalim"))
        dataFrom, dataBis = app_masina.default_interval
        alim_type = None
        alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
        return render_template('masina.html',
                               userDetails=alimentari,
                               dataFrom=dataFrom.date(),
                               dataBis=dataBis.date(),
                               tabel_alimentari=app_masina.table_alimentari,
                               tabel_totals=app_masina.table_totals,
                               types_of_costs=app_masina.types_of_costs,
                               table_name = table_name,
                               last_records=app_masina.last_records
                               )
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/addalim', methods=['GET', 'POST'])
def addalim():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        electric_providers = ['MyHyundai', 'EnBW', 'SWM_Plus', 'SWM', 'eCharge']
        if request.method == 'POST':
            if "add_alim" in request.form:
                date = request.form['data']
                alim_type = request.form['type']
                brutto = request.form['brutto']
                amount = request.form['amount']
                refuel = request.form['refuel']
                other = request.form['other']
                recharges = request.form['recharges']
                km = request.form['km']
                comment = request.form['Comment']
                file = request.files['rfile']
                fl = None
                if file:
                    file.save(secure_filename(file.filename))
                    fl = file.filename
                id_all_cars = current_user.get_id_all_cars(session['current_table'].lower())
                app_masina = Masina(conf.credentials, table_name=session['current_table'].lower())
                app_masina.insert_new_alim(current_user.id, id_all_cars, data=date, alim_type=alim_type, brutto=brutto, amount=amount,
                refuel=refuel, other=other, recharges=recharges, km=km, comment=comment, file=fl)
                return redirect(url_for('car', table_name=session['current_table'].lower()))
        return render_template('addalim.html',
                               table_name=session['current_table'],
                               types_of_costs=session['types_of_costs'],
                               electric_providers = electric_providers
                               )
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/masina', methods=['GET', 'POST'])
def masina():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        credentials = conf.credentials
        app_masina = Masina(credentials, table_name='hyundai_ioniq')
        dataFrom, dataBis = app_masina.default_interval
        alim_type = None
        if request.method == 'POST':
            print('LLLLLrequest.form', request.form)
            if "filter" in request.form:
                month = request.form['month']
                year = int(request.form['year'])
                alim_type = request.form['type']
                if alim_type == 'all':
                    alim_type = None
                dataFrom = request.form['dataFrom']
                dataBis = request.form['dataBis']

                if month != 'interval':
                    dataFrom, dataBis = app_masina.get_monthly_interval(month, year)
                elif month == 'interval' and (dataFrom == '' or dataBis == ''):
                    dataFrom, dataBis = app_masina.default_interval
                else:
                    try:
                        dataFrom = datetime.strptime(dataFrom, "%Y-%m-%d")
                        dataBis = datetime.strptime(dataBis, "%Y-%m-%d")
                    except:
                        print(traceback.format_exc())
            elif "add_alim" in request.form:
                date = request.form['data']
                alim_type = request.form['type']
                brutto = request.form['brutto']
                amount = request.form['amount']
                km = request.form['km']
                comment = request.form['Comment']
                file = request.files['rfile']
                file.save(secure_filename(file.filename))
                fl = file.filename
                fl = app_masina.alimentari.convertToBinaryData(fl)

                ppu = round(float(brutto)/float(amount), 3)
                columns = ['data', 'type', 'brutto', 'amount', 'ppu', 'km', 'comment', 'file']
                values = [date, alim_type, brutto, amount, ppu, km, comment, fl]
                redirect(url_for('masina'))
                app_masina.insert_new_alim(columns, values)
            elif 'read_txt_file_content' in request.form:
                file = request.files['myfile']
                filename = secure_filename(file.filename)
                print('filename', filename)
                fl = os.path.join("D:\Python\MySQL", filename)
                file.save(fl)
                with open(fl) as f:
                    file_content = f.read()
                    print(file_content)
                return file_content
            elif 'save_file_locally' in request.form:
                file = request.files['myfile']
                # file = 'test.csv'

                print('file', file, type(file))
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                print('filename', filename, type(filename))
            elif 'upload_file_to_db' in request.form:
                file = request.files['myfile']
                # print('file', file, type(file))
                file.save(secure_filename(file.filename))
                fl = file.filename
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                #
                # print('filename', filename, type(filename))
                # fl = os.path.normpath(filename)
                fl = app_masina.alimentari.convertToBinaryData(fl)
                app_masina.alimentari.changeCellContent('file', fl, 'id', 2)
                # print('filename', filename)
                # fl = os.path.join("D:\Python\MySQL", filename)
                # file.save(fl)
                # with open(fl) as f:
                #     file_content = f.read()
                #     print(file_content)
                # return file_content
            # elif 'download_file' in request.form:
            #     print('AAAAAAAAAA')
            #     fl = app_masina.alimentari.returnCellsWhere('file', ('id', 651))
            #     exact_path = "report.csv"
            #
            #     with open(exact_path, 'wb') as file:
            #         file.write(fl[0])
            #     print('BBBBBBBBBBB')
            #     return send_file(exact_path, as_attachment=True)
            #     # return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            elif 'export_detail_table_as_csv' in request.form:
                alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
                exact_path = "report.csv"
                with open(exact_path, 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    for row in alimentari:
                        writer.writerow(row)
                return send_file(exact_path, as_attachment=True)
            else:
                print("AAAA")
        print('*****dataFrom', dataFrom)
        print('*****dataBis', dataBis)
        print('*****alim_type', alim_type)
        alimentari = app_masina.get_alimentari_for_interval_type(dataFrom, dataBis, alim_type)
        return render_template('masina.html',
                               userDetails=alimentari,
                               dataFrom=dataFrom.date(),
                               dataBis=dataBis.date(),
                               tabel_alimentari=app_masina.table_alimentari,
                               tabel_totals=app_masina.table_totals,
                               types_of_costs=app_masina.types_of_costs,
                               last_records=app_masina.last_records
                               )
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/addcar', methods=['GET', 'POST'])
def addcar():
    try:
        print(sys._getframe().f_code.co_name, request.method)
        if request.method == 'POST':
            brand = request.form['brand']
            model = request.form['model']
            car_type = request.form['car_type']
            current_user.add_car(brand, model, car_type)
            return redirect(url_for('index'))
        return render_template('addcar.html')
    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/addfile/<index>', methods=['GET', 'POST'])
def addfile(index):
    try:
        credentials = conf.credentials
        app_masina = Masina(credentials, table_name=session['current_table'].lower())
        if request.method == 'POST':
            file = request.files['myfile']
            name = file.filename
            app_masina.alimentari.changeCellContent('file_name', str('file_{}'.format(name)), 'id', index)
            #return "UPLOAD {} {} {} ++{}++".format(index, request.method, file.filename, )
            file.save(secure_filename(name))
            fl = file.filename
            fl = app_masina.alimentari.convertToBinaryData(fl)

            app_masina.upload_file(fl, index, name)
            return redirect(url_for('car', table_name=session['current_table'].lower()))
            #return "UPLOAD {} {} {}".format(index, request.method, secure_filename(file.filename))
        elif request.method == 'GET':
            file_content = app_masina.alimentari.returnCellsWhere('file', ('id', index))[0]
            exact_path = report_file
            with open(exact_path, 'wb') as file:
                file.write(file_content)
            return send_file(exact_path, as_attachment=True)

    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)


@app.route('/importtable', methods=['GET', 'POST'])
def importtable():
    try:
        if request.method == 'POST':
            credentials = conf.credentials
            app_masina = Masina(credentials, table_name=session['current_table'].lower())
            if 'import_table' in request.form:
                file = request.files['myfile']
                filename = secure_filename(file.filename)

                file.save(filename)
#                with open(filename) as f:
#                    file_content = f.readlines()
                file_content = []
                with open(filename, 'r') as file:
                    reader = csv.reader(file, delimiter=';')
                    for i, row in enumerate(reader):
                        print(i, row)
                        file_content.append(row)

                columns, rows = file_content[0], file_content[1:]
                for row in rows:
                    app_masina.alimentari.addNewRow(columns[1:-1], row[1:-1])

                #return file_content[0]
                return redirect(url_for('car', table_name=session['current_table'].lower()))
        elif request.method == 'GET':
            return render_template('importtable.html')

    except:
        myerr = 'definition {}\n{}'.format(sys._getframe().f_code.co_name, str(traceback.format_exc()))
        return render_template('err.html',
                               myerr=myerr)




if __name__ == "__main__":
    app.run(debug=True)
