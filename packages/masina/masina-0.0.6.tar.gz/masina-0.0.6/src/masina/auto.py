import numpy as np
from mysqlquerys import connect
from mysqlquerys import mysql_rm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import traceback
import sys, os
import zipfile
import shutil


# ini_file = '/home/radum/rmasina/static/wdb.ini'
# ini_file = r"D:\Python\MySQL\masina.ini"
# conf = connect.Config(ini_file)
# create_auto_table = '/home/radum/rmasina/static/sql/auto_template.sql'

class Users(UserMixin):
    def __init__(self, user_name, ini_file):
        self.user_name = user_name
        if isinstance(ini_file, dict):
            credentials = ini_file
        else:
            self.conf = connect.Config(ini_file)
            credentials = self.conf.credentials
        try:
            self.credentials = credentials
            self.db = mysql_rm.DataBase(credentials)
        except:
            print('Could not connect to database')
            raise RuntimeError
        try:
            self.users_table = mysql_rm.Table(credentials, 'users')
            self.all_cars_table = mysql_rm.Table(credentials, 'all_cars')
            self.checkup_list()
        except:
            print('Could not connect to Tables')
            raise RuntimeError

    def checkup_list(self):
        pth_template_users = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'users_template.sql')
        pth_template_all_cars = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'all_cars_template.sql')
        if self.users_table.tableName not in self.db.allAvailableTablesInDatabase:
            self.db.createTableFromFile(pth_template_users, 'users')
            self.users_table = mysql_rm.Table(self.credentials, 'users')
            # raise NotImplementedError('Table users missing')
        if self.all_cars_table.tableName not in self.db.allAvailableTablesInDatabase:
            self.db.createTableFromFile(pth_template_all_cars, 'all_cars')
            self.all_cars_table = mysql_rm.Table(self.credentials, 'all_cars')
            # raise NotImplementedError('Table all_cars missing')
        same = self.users_table.compare_sql_file_to_sql_table(pth_template_users)
        if same is not True:
            print(same)
        same = self.all_cars_table.compare_sql_file_to_sql_table(pth_template_all_cars)
        if same is not True:
            print(same)

    @property
    def all_users(self):
        all_users = self.users_table.returnColumn('username')
        return all_users

    @property
    def id(self):
        matches = ('username', self.user_name)
        # print('matches', matches)
        user_id = self.users_table.returnCellsWhere('id', matches)[0]
        # print('user_id', user_id)
        return user_id

    @property
    def valid_user(self):
        all_users = self.users_table.returnColumn('username')
        if self.user_name in all_users:
            return True
        else:
            return False

    @property
    def admin(self):
        if self.valid_user:
            matches = ('id', self.id)
            user_type = self.users_table.returnCellsWhere('user_type', matches)[0]
            if user_type == 'admin':
                return True
            else:
                return False

    @property
    def masini(self):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        masini = {}
        matches = ('user_id', self.id)
        cars_rows = self.all_cars_table.returnRowsWhere(matches)
        if cars_rows:
            for row in cars_rows:
                indx_brand = self.all_cars_table.columnsNames.index('brand')
                indx_model = self.all_cars_table.columnsNames.index('model')
                table_name = '{}_{}'.format(row[indx_brand], row[indx_model])
                app_masina = Masina(self.credentials, table_name=table_name.lower())
                masini[table_name] = app_masina
        return masini

    @property
    def hashed_password(self):
        matches = ('username', self.user_name)
        hashed_password = self.users_table.returnCellsWhere('password', matches)[0]
        return hashed_password

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def add_car(self, brand, model, car_type):
        brand = brand.lower()
        model = model.lower()
        car_type = car_type.lower()
        cols = ('user_id', 'brand', 'model', 'cartype')
        vals = (self.id, brand, model, car_type)
        matches = [('user_id', self.id), ('brand', brand), ('model', model), ('cartype', car_type)]
        existing_row = self.all_cars_table.returnRowsWhere(matches)
        # print('existing_row', existing_row)
        if existing_row:
            print('car already existing at id {}'.format(existing_row[0][0]))
            return
        else:
            self.all_cars_table.addNewRow(cols, vals)
            new_auto_table = '{}_{}'.format(brand, model)
            new_auto_table = new_auto_table.lower()
            if new_auto_table in self.db.allAvailableTablesInDatabase:
                print('table {} existing in database'.format(new_auto_table))
            else:
                pth_auto_template = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'auto_template.sql')
                self.db.createTableFromFile(pth_auto_template, new_auto_table)

    def get_id_all_cars(self, table_name):
        brand, model = table_name.split('_')
        matches = [('user_id', self.id),
                   ('brand', brand),
                   ('model', model),
                   ]
        print(matches)
        id_all_cars = self.all_cars_table.returnCellsWhere('id', matches)[0]
        return id_all_cars

    # def export_full_profile(self, output_file=None):
    #     tables_dict = {'users': 'id',
    #                    'all_cars': 'user_id'
    #                    }
    #     for car in self.masini.keys():
    #         tables_dict[car.lower()] = 'id_users'
    #     if not output_file:
    #         tim = datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S')
    #         output_file = '{}_{}.sql'.format(tim, self.user_name)
    #         dir = os.path.dirname(__file__)
    #         output_file = os.path.join(dir, r'static\backup_profile', output_file)
    #     self.db.backup_profile_with_id(tables_dict, output_file, user_id=self.id)
    #     return output_file
    #
    # def export_profile_without_files(self, output_file=None):
    #     tables_dict = {'users': 'id',
    #                    'all_cars': 'user_id'
    #                    }
    #     for car in self.masini.keys():
    #         tables_dict[car.lower()] = 'id_users'
    #     if not output_file:
    #         tim = datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S')
    #         output_file = '{}_{}.sql'.format(tim, self.user_name)
    #         dir = os.path.dirname(__file__)
    #         output_file = os.path.join(dir, r'static\backup_profile', output_file)
    #     self.db.backup_profile_with_id(tables_dict, output_file, user_id=self.id)
    #     return output_file
    #

    @property
    def tables_dict(self):
        tables_dict = {'users': 'id',
                       'all_cars': 'user_id'
                       }
        for car in self.masini.keys():
            tables_dict[car.lower()] = 'id_users'
        return tables_dict

    def export_profile(self, output_dir=None, export_files=True):
        # tables_dict = {'users': 'id',
        #                'all_cars': 'user_id'
        #                }
        # for car in self.masini.keys():
        #     tables_dict[car.lower()] = 'id_users'

        tim = datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S')
        output_dir_name = '{}_{:09d}'.format(tim, self.id)
        if not output_dir:
            dir = os.path.dirname(__file__)
            output_dir = os.path.join(dir, r'static\backup_profile', '{:09d}'.format(self.id), output_dir_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        print('starting backup')
        print('tables_dict', self.tables_dict)
        print('output_dir', output_dir)
        print('self.id', self.id)
        # return
        # self.db.backup_profile_with_files(tables_dict, output_dir, user_id=self.id)
        self.db.backup_profile_with_files(self.tables_dict, user_id=self.id, output_dir=output_dir, export_files=export_files)
        output_zip = os.path.join(os.path.dirname(output_dir), '{}.zip'.format(output_dir_name))
        zip_file = self.zip_profile_files(output_dir, output_zip)
        if os.path.exists(zip_file):
            shutil.rmtree(output_dir)
        print('finished backup')
        return output_dir

    def zip_profile_files(self, src_dir, output_file):
        relroot = os.path.abspath(os.path.join(src_dir, os.pardir))
        with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zip:
            for root, dirs, files in os.walk(src_dir):
                # add directory (needed for empty dirs)
                zip.write(root, os.path.relpath(root, relroot))
                for file in files:
                    filename = os.path.join(root, file)
                    if os.path.isfile(filename):  # regular files only
                        arcname = os.path.join(os.path.relpath(root, relroot), file)
                        zip.write(filename, arcname)
        return output_file

    def unzip_profile_files(self, src_file, output_dir):
        with zipfile.ZipFile(src_file, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        return output_dir

    def import_profile_with_files(self, zip_file, import_files=True):
        output_dir, file = os.path.split(zip_file)
        src_dir = self.unzip_profile_files(zip_file, output_dir)
        src_dir = os.path.join(src_dir, file[:-4])
        print(src_dir)
        if not os.path.exists(src_dir):
            raise RuntimeError('Missing Folder {}'.format(src_dir))
        sql_files = [x for x in os.listdir(src_dir) if x.endswith('.sql')]
        sql_file = os.path.join(src_dir, sql_files[0])
        print(sql_file)
        # return
        self.db.run_sql_file(sql_file)
        if import_files:
            attachments = [x for x in os.listdir(src_dir) if (x.endswith('.jpg') or x.endswith('.pdf'))]
            tab = []
            for file_name in attachments:
                try:
                    user_id, table_name, table_id, orig_name = file_name.split('+')
                except:
                    print('could not import {}, name not ok'.format(file_name))
                    #todo aici am ramas , nu exporta numele cum trebuie la fisiere
                tup = (user_id, table_name, table_id, orig_name, file_name)
                tab.append(tup)
            tab = np.atleast_2d(tab)
            all_sql_tables = list(np.unique(tab[:, 1]))
            for table_name in all_sql_tables:
                sql_table = mysql_rm.Table(self.credentials, table_name)
                table = tab[tab[:, 1] == table_name]
                for row in table:
                    user_id, table_name, table_id, orig_name, fl_name = row
                    fil = os.path.join(src_dir, fl_name)
                    sql_table.changeCellContent('file', fil, 'id', table_id)
                    sql_table.changeCellContent('file_name', orig_name, 'id', table_id)
        if os.path.exists(src_dir):
            shutil.rmtree(src_dir)

    def erase_traces(self):
        for i in self.db.checkProcess():
            print(i)
        self.db.drop_table_list(list(self.tables_dict.keys()))


class Masina:
    def __init__(self, ini_file, table_name='hyundai_ioniq'):
        '''
        :param ini_file:type=QFileDialog.getOpenFileName name=filename file_type=(*.ini;*.txt)
        '''
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        if isinstance(ini_file, dict):
            credentials = ini_file
        else:
            self.conf = connect.Config(ini_file)
            credentials = self.conf.credentials
        self.checkup_list(credentials)

        self.alimentari = mysql_rm.Table(credentials, table_name)
        self.types_of_costs = ["electric", "benzina", "intretinere", "asigurare", 'impozit', 'TüV', 'carwash']
        # try:
        #     self.dataBase = self.sql_rm.DataBase(self.conf.credentials)
        # except Exception as err:
        #     print(traceback.format_exc())

    # @property
    # def sql_rm(self):
    #     # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
    #     if self.conf.db_type == 'mysql':
    #         sql_rm = mysql_rm
    #     return sql_rm

    def checkup_list(self, credentials):
        if not isinstance(credentials, dict):
            raise RuntimeError('Credentials not dict')
        db = mysql_rm.DataBase(credentials)
        if not db.is_connected:
            raise RuntimeError('Could not connect to database')
        print('Connected to database:', db.is_connected)
        if 'users' not in db.allAvailableTablesInDatabase:
            print('Table "users" not in database...creating')
            pth_template_users = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'users_template.sql')
            if not os.path.exists(pth_template_users):
                raise RuntimeError('Could not find {}'.format(pth_template_users))
            db.createTableFromFile(pth_template_users, 'users')
        # else:
        #     users_table = mysql_rm.Table(credentials, 'users')
        #     print()

    @property
    def no_of_records(self):
        return self.alimentari.noOfRows

    @property
    def default_interval(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        startDate = datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day)
        endDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        return startDate, endDate

    @property
    def total_money(self):
        col = self.alimentari.returnColumn('brutto')
        return round(sum(col), 2)

    @property
    def tot_benzina(self):
        matches = [('type', 'benzina')]
        col = self.alimentari.returnCellsWhere('brutto', matches)
        return round(sum(col), 2)

    @property
    def tot_electric(self):
        matches = [('type', 'electric')]
        col = self.alimentari.returnCellsWhere('brutto', matches)
        return round(sum(col), 2)

    @property
    def monthly(self):
        try:
            return round((self.monthly_benzina + self.monthly_electric), 2)
        except:
            return None

    @property
    def monthly_benzina(self):
        try:
            matches = [('type', 'benzina')]
            money = self.alimentari.returnCellsWhere('brutto', matches)
            all_dates = self.alimentari.returnColumn('data')
            start_date = min(all_dates)
            finish_date = max(all_dates)
            total_money = round(sum(money), 2)
            days = (finish_date - start_date).days
            average_day_per_month = 365 / 12
            monthly = (average_day_per_month * total_money) / days
            return round(monthly, 2)
        except:
            return None

    @property
    def monthly_electric(self):
        matches = [('type', 'electric')]
        money = self.alimentari.returnCellsWhere('brutto', matches)
        all_dates = self.alimentari.returnColumn('data')
        start_date = min(all_dates)
        finish_date = max(all_dates)
        total_money = round(sum(money), 2)
        days = (finish_date - start_date).days
        average_day_per_month = 365 / 12
        try:
            monthly = (average_day_per_month * total_money) / days
            return round(monthly, 2)
        except:
            return None

    @property
    def db_start_date(self):
        all_dates = self.alimentari.returnColumn('data')
        # print('**all_dates', all_dates, type(all_dates))
        if all_dates:
            start_date = min(all_dates)
        else:
            start_date = None
        return start_date

    @property
    def db_last_record_date(self):
        try:
            all_dates = self.alimentari.returnColumn('data')
            finish_date = max(all_dates)
            return finish_date
        except:
            return None

    @property
    def electric_providers(self):
        matches = [('type', 'electric')]
        col = self.alimentari.returnCellsWhere('eProvider', matches)
        return list(set(col))

    @property
    def table_alimentari(self):
        arr = [('', 'Alimentari[€]', 'Benzina[€]', 'Electric[€]')]
        if self.no_of_records > 0:
            total_alim = self.tot_benzina + self.tot_electric
            arr.append(('Monthly', self.monthly, self.monthly_benzina, self.monthly_electric))
            arr.append(('Total', total_alim, self.tot_benzina, self.tot_electric))
        else:
            arr.append(('Monthly', None, None, None))
            arr.append(('Total', None, None, None))

        arr = np.atleast_2d(arr)
        return arr

    @property
    def table_totals(self):
        if not self.db_start_date:
            return None
        types = ['benzina', 'electric', 'asigurare', 'impozit', 'TüV', 'intretinere']
        table = []
        for year in reversed(range(self.db_start_date.year, self.db_last_record_date.year + 1)):
            # print(year)
            dd = {}
            dd['year'] = year
            startTime = datetime(year, 1, 1)
            endTime = datetime(year, 12, 31)
            rows = self.alimentari.returnRowsOfYear('data', startTime, 'data', endTime)
            arr = np.atleast_2d(rows)
            tot = 0
            for t in types:
                indx = np.where(arr[:, self.alimentari.columnsNames.index('type')] == t)
                # if t == 'asigurare':
                #     print(indx)
                col = arr[indx, self.alimentari.columnsNames.index('brutto')]
                value = sum(col[0])
                value = round(value, 2)
                dd[t] = value
                tot += value
            dd['total/row'] = round(tot, 2)
            table.append(dd)
        table_head = tuple(dd.keys())
        arr = [table_head]
        for tab in table:
            row = []
            for k, v in tab.items():
                row.append(v)
            arr.append(tuple(row))
        arr = np.atleast_2d(arr)
        row_totals = ['totals']
        total_total = 0
        for col in range(1, arr.shape[1]):
            # print(arr[0, col], round(sum(arr[1:, col].astype(float)), 2))
            val = round(sum(arr[1:, col].astype(float)), 2)
            row_totals.append(val)
            total_total += val
        row_tot = np.array(row_totals)
        new_arr = np.insert(arr, 1, row_tot, axis=0)
        return new_arr

    @property
    def last_records(self):
        table_head = self.alimentari.columnsNames
        if 'file' in table_head:
            table_head.remove('file')
        last_records = [table_head]
        for typ in self.types_of_costs:
            matches = [('type', typ)]
            table = self.alimentari.filterRows(matches, order_by=('data', 'DESC'))
            if typ == 'electric':
                already_listed = []
                for row in table:
                    provider = row[table_head.index('comment')]
                    if provider not in already_listed:
                        last_records.append(row)
                        already_listed.append(provider)
                continue
            if table:
                last_records.append(table[0])

        last_records = np.atleast_2d(last_records)
        del_cols = ['id_users', 'id_all_cars', 'amount', 'refuel', 'other', 'recharges', 'ppu', 'km']
        # for c in del_cols:
        #     last_records = np.delete(last_records, table_head.index(c), 1)
        return last_records

    def get_monthly_interval(self, month: str, year):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        mnth = datetime.strptime(month, "%B").month
        startDate = datetime(year, mnth, 1)

        if mnth != 12:
            lastDayOfMonth = datetime(year, mnth + 1, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(year + 1, 1, 1) - timedelta(days=1)

        return startDate, lastDayOfMonth

    def get_all_alimentari(self):
        cols = []
        for k, v in self.alimentari.columnsDetProperties.items():
            if v[0] == 'longblob':
                continue
            cols.append(k)
        alimentari = self.alimentari.returnColumns(cols)
        # alimentari = self.alimentari.returnAllRecordsFromTable()
        alimentari = np.atleast_2d(alimentari)
        alimentari = np.insert(alimentari, 0, cols, axis=0)
        return alimentari

    def get_alimentari_for_interval_type(self, selectedStartDate, selectedEndDate, alim_type):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        matches = [('data', (selectedStartDate, selectedEndDate))]
        if alim_type:
            matches.append(('type', alim_type))
        # print(matches)
        table = self.alimentari.filterRows(matches, order_by=('data', 'DESC'))

        if table:
            table_head = []
            for col_name, prop in self.alimentari.columnsDetProperties.items():
                # print(col_name, prop)
                if prop[0] == 'longblob':
                    continue
                table_head.append(col_name)
            arr = np.atleast_2d(table)
            arr = np.insert(arr, 0, np.array(table_head), axis=0)
        else:
            arr = np.atleast_2d(np.array(self.alimentari.columnsNames))
        return arr

    def upload_file(self, file_name, id):
        self.alimentari.changeCellContent('file', file_name, 'id', id)
        pth, file_name = os.path.split(file_name)
        self.alimentari.changeCellContent('file_name', file_name, 'id', id)

    def insert_new_alim(self, current_user_id, id_all_cars, data, alim_type, brutto, amount, refuel, other, recharges,
                        km, comment, file, provider):
        '''
        :param data:type=dateTime name=date
        :param alim_type:type=comboBox name=alim_type items=[electric,benzina,TüV,intretinere]
        :param brutto:type=text name=brutto
        :param amount:type=text name=amount
        :param refuel:type=text name=refuel
        :param other:type=text name=other
        :param recharges:type=text name=recharges
        :param km:type=text name=km
        :param comment:type=text name=comment
        :param file:type=QFileDialog.getOpenFileName name=file
        '''
        if file:
            _, file_name = os.path.split(file)
            cols = ['id_users', 'id_all_cars', 'data', 'type', 'brutto', 'amount', 'refuel', 'other', 'recharges',
                    'ppu', 'km', 'comment', 'file', 'file_name', 'eProvider']
        else:
            cols = ['id_users', 'id_all_cars', 'data', 'type', 'brutto', 'amount', 'refuel', 'other', 'recharges',
                    'ppu', 'km', 'comment', 'eProvider']
        try:
            if isinstance(brutto, str) and ',' in brutto:
                brutto = brutto.replace(',', '.')
            brutto = float(brutto)
        except:
            brutto = None
        try:
            if isinstance(amount, str) and ',' in amount:
                amount = amount.replace(',', '.')
            elif amount == '':
                amount = 1
            amount = float(amount)
        except:
            amount = None
        try:
            if isinstance(refuel, str) and ',' in refuel:
                refuel = refuel.replace(',', '.')
            refuel = float(refuel)
        except:
            refuel = None
        try:
            if isinstance(other, str) and ',' in other:
                other = other.replace(',', '.')
            other = float(other)
        except:
            other = None
        try:
            if isinstance(recharges, str) and ',' in recharges:
                recharges = recharges.replace(',', '.')
            recharges = float(recharges)
        except:
            recharges = None
        try:
            km = int(km)
        except:
            km = None

        ppu = round(float(brutto) / float(amount), 3)
        if file:
            vals = [current_user_id, id_all_cars, data, alim_type, brutto, amount, refuel, other, recharges, ppu, km,
                    comment, file, file_name, provider]
        else:
            vals = [current_user_id, id_all_cars, data, alim_type, brutto, amount, refuel, other, recharges, ppu, km,
                    comment, provider]

        self.alimentari.addNewRow(cols, tuple(vals))

    def create_sql_table(self, table_name):
        masina_sql = r'static\sql\auto.sql'
        mysql_rm.DataBase(self.conf.credentials).createTableFromFile(masina_sql, table_name)
