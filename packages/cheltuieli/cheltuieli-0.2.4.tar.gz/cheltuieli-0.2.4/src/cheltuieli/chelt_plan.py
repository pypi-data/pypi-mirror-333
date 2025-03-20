import csv
import os.path
import traceback

import numpy
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import *
import sys
import json
import shutil
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import zipfile
from mysqlquerys import connect
from mysqlquerys import mysql_rm

np.set_printoptions(linewidth=250)
__version__ = 'V5'

tables_dict = {'users': 'id',
               'banca': 'id_users',
               'chelt_plan': 'id_users',
               'knowntrans': 'id_users',
               'income': 'id_users',
               # 'real_expenses': 'id_users',
               'deubnk': 'id_users',
               'n26': 'id_users',
               'sskm': 'id_users',
               'plan_vs_real': 'id_users',
               'imported_csv': 'id_users'
               }
sskm_tabHeadDict = {'Auftragskonto': 'Auftragskonto',
                    'Buchungstag': 'Buchungstag',
                    'Valutadatum': 'Valutadatum',
                    'Buchungstext': 'Buchungstext',
                    'Verwendungszweck': 'Verwendungszweck',
                    'Glaeubiger ID': 'Glaeubiger',
                    'Mandatsreferenz': 'Mandatsreferenz',
                    'Kundenreferenz (End-to-End)': 'Kundenreferenz',
                    'Sammlerreferenz': 'Sammlerreferenz',
                    'Lastschrift Ursprungsbetrag': 'Lastschrift',
                    'Auslagenersatz Ruecklastschrift': 'Auslagenersatz',
                    'Beguenstigter/Zahlungspflichtiger': 'Beguenstigter',
                    'Kontonummer/IBAN': 'IBAN',
                    'BIC (SWIFT-Code)': 'BIC',
                    'Betrag': 'Betrag',
                    'Waehrung': 'Waehrung',
                    'Info': 'Info'}
n26_tabHeadDict = {'Booking Date': 'Buchungstag',
                   'Value Date': 'ValueDate',
                   'Partner Name': 'PartnerName',
                   'Partner Iban': 'IBAN',
                   'Type': 'Type',
                   'Payment Reference': 'PaymentReference',
                   'Account Name': 'AccountName',
                   'Amount (EUR)': 'Amount',
                   'Original Amount': 'OriginalAmount',
                   'Original Currency': 'OriginalCurrency',
                   'Exchange Rate': 'ExchangeRate'
                   }
db_tabHeadDict = {'Booking date': 'Buchungstag',
                  'Value date': 'Valuedate',
                  'Transaction Type': 'TransactionType',
                  'Beneficiary / Originator': 'BeneficiaryOriginator',
                  'Payment Details': 'Verwendungszweck',
                  'IBAN': 'IBAN',
                  'BIC': 'BIC',
                  'Customer Reference': 'CustomerReference',
                  'Mandate Reference': 'Mandatsreferenz',
                  'Creditor ID': 'CreditorID',
                  'Compensation amount': 'Compensationamount',
                  'Original Amount': 'OriginalAmount',
                  'Ultimate creditor': 'Ultimatecreditor',
                  'Ultimate debtor': 'Ultimatedebtor',
                  'Number of transactions': 'Numberoftransactions',
                  'Number of cheques': 'Numberofcheques',
                  'Debit': 'Debit',
                  'Credit': 'Credit',
                  'Currency': 'Currency'
                  }

plan_vs_real_tabHeadDict = {'sskm': {'Buchungstag': 'Buchungstag',
                                     'Betrag': 'Betrag',
                                     'PaymentReference': 'Verwendungszweck',
                                     'PartnerName': 'Beguenstigter'},
                            'n26': {'Buchungstag': 'Buchungstag',
                                    'Betrag': 'Amount',
                                    'PaymentReference': 'PaymentReference',
                                    'PartnerName': 'PartnerName'},
                            'deubnk': {'Buchungstag': 'Buchungstag',
                                       'Betrag': 'Debit',
                                       'PaymentReference': 'Verwendungszweck',
                                       'PartnerName': 'BeneficiaryOriginator'},
                            }

bank_tabHeadDict = {'Stadtsparkasse München': sskm_tabHeadDict,
                    'N26': n26_tabHeadDict,
                    'DeutscheBank': db_tabHeadDict,
                    }

bank_sql_table = {'Stadtsparkasse München': 'sskm',
                  'N26': 'n26',
                  'DeutscheBank': 'deubnk',
                  }


def calculate_last_day_of_month(mnth, year):
    if mnth < 12:
        # lastDayOfMonth = datetime(datetime.now().year, mnth + 1, 1) - timedelta(days=1)
        lastDayOfMonth = datetime(year, mnth + 1, 1) - timedelta(days=1)
        lastDayOfMonth = lastDayOfMonth.day
    elif mnth == 12:
        lastDayOfMonth = 31
    return lastDayOfMonth


def default_interval():
    # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
    print('Caller : ', sys._getframe().f_back.f_code.co_name)
    startDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    if datetime.now().month != 12:
        mnth = datetime.now().month + 1
        lastDayOfMonth = datetime(datetime.now().year, mnth, 1) - timedelta(days=1)
    else:
        lastDayOfMonth = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

    return startDate, lastDayOfMonth


def get_monthly_interval(month: str, year):
    # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
    mnth = datetime.strptime(month, "%B").month
    startDate = datetime(year, mnth, 1)

    if mnth != 12:
        lastDayOfMonth = datetime(year, mnth + 1, 1) - timedelta(days=1)
    else:
        lastDayOfMonth = datetime(year + 1, 1, 1) - timedelta(days=1)

    return startDate.date(), lastDayOfMonth.date()


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
            self.checkup_list()
            self.users_table = mysql_rm.Table(self.credentials, 'users')
        except:
            print('Could not connect to Tables')
            raise RuntimeError('Could not connect to Tables')

    # def checkup_list_old(self):
    #     pth_template_users = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'users_template.sql')
    #     pth_banca_template = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'banca_template.sql')
    #     pth_income_template = os.path.join(os.path.dirname(__file__), 'static', 'sql', 'income_template.sql')
    #     if self.users_table.tableName not in self.db.allAvailableTablesInDatabase:
    #         self.db.createTableFromFile(pth_template_users, 'users')
    #         self.users_table = mysql_rm.Table(self.credentials, 'users')
    #         # raise NotImplementedError('Table users missing')
    #     if self.banca_table.tableName not in self.db.allAvailableTablesInDatabase:
    #         self.db.createTableFromFile(pth_banca_template, 'banca')
    #         self.banca_table = mysql_rm.Table(self.credentials, 'banca')
    #         # raise NotImplementedError('Table all_cars missing')
    #     if self.income_table.tableName not in self.db.allAvailableTablesInDatabase:
    #         self.db.createTableFromFile(pth_income_template, 'income')
    #         self.income_table = mysql_rm.Table(self.credentials, 'income')
    #         # raise NotImplementedError('Table all_cars missing')
    #     same = self.users_table.compare_sql_file_to_sql_table(pth_template_users)
    #     if same is not True:
    #         print(same)
    #     same = self.banca_table.compare_sql_file_to_sql_table(pth_banca_template)
    #     if same is not True:
    #         print(same)
    #     same = self.income_table.compare_sql_file_to_sql_table(pth_income_template)
    #     if same is not True:
    #         print(same)

    def checkup_list(self):
        for table in tables_dict.keys():
            # print(table)
            pth_table_template = os.path.join(os.path.dirname(__file__), 'static', 'sql',
                                              '{}_template.sql'.format(table))
            if table not in self.db.allAvailableTablesInDatabase:
                print('Table {} not in database...creating it'.format(table))
                self.db.createTableFromFile(pth_table_template, table)
            else:
                # exec("sqltable = mysql_rm.Table(self.credentials, '{}')".format(table))
                varName = 'table_{}'.format(table)
                loc = locals()
                exec("{} = mysql_rm.Table(self.credentials, '{}')".format(varName, table), globals(), loc)
                varName = loc[varName]

                same = varName.compare_sql_file_to_sql_table(pth_table_template)
                # if same is not True:
                #     print(same)

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

    # @property
    # def masini(self):
    #     # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    #     masini = {}
    #     matches = ('user_id', self.id)
    #     cars_rows = self.all_cars_table.returnRowsWhere(matches)
    #     if cars_rows:
    #         for row in cars_rows:
    #             indx_brand = self.all_cars_table.columnsNames.index('brand')
    #             indx_model = self.all_cars_table.columnsNames.index('model')
    #             table_name = '{}_{}'.format(row[indx_brand], row[indx_model])
    #             app_masina = Masina(self.credentials, table_name=table_name.lower())
    #             masini[table_name] = app_masina
    #     return masini

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

    def export_profile(self, output_dir=None, export_files=True):
        tim = datetime.strftime(datetime.now(), '%Y_%m_%d__%H_%M_%S')
        output_dir_name = '{}_{:09d}'.format(tim, self.id)
        if not output_dir:
            dir = os.path.dirname(__file__)
            output_dir = os.path.join(dir, r'static\backup_profile', '{:09d}'.format(self.id), output_dir_name)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
        print('starting backup')
        print('tables_dict', tables_dict)
        print('output_dir', output_dir)
        print('self.id', self.id)

        self.db.backup_profile_with_files(tables_dict, user_id=self.id, output_dir=output_dir,
                                          export_files=export_files)
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
        if not os.path.exists(src_dir):
            raise RuntimeError('Missing Folder {}'.format(src_dir))

        sql_files = [x for x in os.listdir(src_dir) if x.endswith('.sql')]
        sql_file = os.path.join(src_dir, sql_files[0])
        # print(sql_file)
        # return
        self.db.run_sql_file(sql_file)
        if import_files:
            attachments = [x for x in os.listdir(src_dir) if
                           (x.endswith('.jpg') or x.endswith('.pdf') or x.endswith('.csv') or x.endswith('.CSV'))]
            tab = []
            for file_name in attachments:
                try:
                    # print(file_name)
                    user_id, table_name, table_id, orig_name = file_name.split('+')
                    # print(user_id, table_name, table_id, orig_name)
                except:
                    print('could not import {}, name not ok'.format(file_name))
                tup = (user_id, table_name, table_id, orig_name, file_name)
                tab.append(tup)
            tab = np.atleast_2d(tab)
            all_sql_tables = list(np.unique(tab[:, 1]))
            for table_name in all_sql_tables:
                # print('table_name', table_name)
                sql_table = mysql_rm.Table(self.credentials, table_name)
                table = tab[tab[:, 1] == table_name]
                for row in table:
                    user_id, table_name, table_id, orig_name, fl_name = row
                    # print('&', user_id, table_name, table_id, orig_name, fl_name)
                    fil = os.path.join(src_dir, fl_name)
                    sql_table.changeCellContent('file', fil, 'id', table_id)
                    sql_table.changeCellContent('file_name', str(orig_name), 'id', table_id)
        if os.path.exists(src_dir):
            shutil.rmtree(src_dir)

    def erase_traces(self):
        for i in self.db.checkProcess():
            print(i)
        self.db.drop_table_list(list(tables_dict.keys()))


class Income:
    def __init__(self, ini_file):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        self.ini_file = ini_file
        pth2src = os.path.dirname(__file__)
        # self.taxes_file = r"static\taxes.csv"
        self.taxes_file = os.path.join(pth2src, 'static', 'taxes.csv')
        self.tax_array, self.tax_header = self.conv_csv_to_np(skipHeader=1)
        self.conf = connect.Config(self.ini_file)
        self.income_table = mysql_rm.Table(self.conf.credentials, 'income')
        self.selectedStartDate = None
        self.selectedEndDate = None
        self.conto = None
        self.tableHead = None
        self.income = None

    def apply_taxes_to_salary(self):
        for inc in self.incomes_for_time_interval:
            if inc.is_salary:
                # print('####', inc.id, inc.name, inc.payments_for_interval)
                inc.basic_brutto_35h_salary = inc.value
                other_incomes_with_salary = self.find_other_incomes_with_salary_tax()
                brutto = inc.basic_brutto_35h_salary
                # print('******inc.basic_brutto_35h_salary', inc.basic_brutto_35h_salary)
                for i in other_incomes_with_salary:
                    if i.value:
                        brutto += i.value
                    else:
                        brutto += inc.basic_brutto_35h_salary * float(i.proc)
                inc.monthly_35h_brutto_salary = brutto
                # print('******inc.monthly_35h_brutto_salary', inc.monthly_35h_brutto_salary)
                taxes = ['lohnsteuer', 'rentenvers', 'arbeitslosvers', 'krankenvers', 'privatvers']
                for tax in taxes:
                    res = round(self.calculate_tax(inc, tax), 2)
                    exec('inc.{} = {}'.format(tax, res))
                inc.brutto = round(inc.brutto_monthly_salary, 2)

        for inc in self.incomes_for_time_interval:
            if inc.tax == 'bonus':
                for payday in inc.payments_for_interval:
                    income_with_same_payday = self.find_salary_with_same_payday(payday)
                    if not income_with_same_payday:
                        print(inc.id, inc.name, payday)
                    inc.steuerklasse = income_with_same_payday.steuerklasse
                    if not inc.value:
                        inc.value = float(inc.proc) * income_with_same_payday.brutto_monthly_salary
                    inc.brutto = round(float(inc.value), 2)

                    taxes = ['lohnsteuer', 'rentenvers', 'arbeitslosvers']
                    for tax in taxes:
                        res = self.calculate_tax(inc, tax)
                        exec('inc.{} = {}'.format(tax, res))
            elif not inc.tax:
                inc.brutto = round(float(inc.value), 2)

    def find_salary_with_same_payday(self, payday):
        for inc in self.incomes_for_time_interval:
            if inc.is_salary:
                if payday in inc.payments_for_interval:
                    return inc

    def calculate_tax(self, income, steuer):
        indx_row = np.where((self.tax_array[:, self.tax_header.index('tax')] == income.tax) &
                            (self.tax_array[:, self.tax_header.index('steuerklasse')].astype(
                                int) == income.steuerklasse))

        lohnteuer_proc = self.tax_array[indx_row, self.tax_header.index(steuer)]
        lohnteuer_proc = float(lohnteuer_proc[0, 0]) / 100

        if income.is_salary:
            lohnteuer = float(income.brutto_monthly_salary) * lohnteuer_proc
        else:
            lohnteuer = float(income.value) * lohnteuer_proc
        return round(lohnteuer, 2)

    def convert_to_tabel(self):
        table = [('table', 'name', 'brutto', 'taxes', 'netto', 'myconto', 'payDay', 'freq')]
        for income in self.incomes_for_time_interval:
            for datum in income.payments_for_interval:
                if not income.brutto and not income.gesetzliche_abzuge and not income.netto:
                    continue
                tup = (
                    income.table, income.name, income.brutto, income.gesetzliche_abzuge, income.netto, income.myconto,
                    datum.date(), income.freq)
                table.append(tup)
        table = np.atleast_2d(table)
        return table

    def convert_to_salary_tabel(self):
        table = [('table', 'name', 'brutto', 'lohnsteuer', 'rentenvers', 'arbeitslosvers', 'gesetzliche_abzuge',
                  'netto', 'krankenvers', 'privatvers', 'abzuge', 'uberweisung', 'myconto', 'payDay', 'freq')]
        brutto = 0
        taxes = 0
        netto = 0
        abzuge = 0
        uberweisung = 0
        for income in self.incomes_for_time_interval:
            if not income.in_salary:
                print('++++++not in salary', income.name)
                continue
            for datum in income.payments_for_interval:
                if not income.brutto and not income.gesetzliche_abzuge and not income.netto:
                    continue
                tup = (income.table,
                       income.name,
                       income.brutto,
                       income.lohnsteuer,
                       income.rentenvers,
                       income.arbeitslosvers,
                       income.gesetzliche_abzuge,
                       income.netto,
                       income.krankenvers,
                       income.privatvers,
                       income.abzuge,
                       income.uberweisung,
                       income.myconto,
                       datum.date(),
                       income.freq)
                table.append(tup)
                try:
                    brutto += income.brutto
                    if income.gesetzliche_abzuge:
                        taxes += income.gesetzliche_abzuge
                    if income.abzuge:
                        abzuge += income.abzuge
                    netto += float(income.netto)
                    uberweisung += float(income.uberweisung)
                except:
                    print(income.name, income.brutto, income.netto)
        table = np.atleast_2d(table)
        return table, brutto, round(taxes, 2), netto, abzuge, uberweisung

    def convert_to_total_income_tabel(self):
        table = [('table', 'name', 'brutto', 'lohnsteuer', 'rentenvers', 'arbeitslosvers', 'gesetzliche_abzuge',
                  'netto', 'krankenvers', 'privatvers', 'abzuge', 'uberweisung', 'myconto', 'payDay', 'freq',
                  'in_salary')]
        salary_brutto = 0
        salary_gesetzliche_abzuge = 0
        salary_netto = 0
        salary_abzuge = 0
        salary_uberweisung = 0
        brutto = 0
        taxes = 0
        netto = 0
        abzuge = 0
        uberweisung = 0
        for income in self.incomes_for_time_interval:
            for datum in income.payments_for_interval:
                if not income.brutto and not income.gesetzliche_abzuge and not income.netto:
                    continue
                tup = (income.table,
                       income.name,
                       income.brutto,
                       income.lohnsteuer,
                       income.rentenvers,
                       income.arbeitslosvers,
                       income.gesetzliche_abzuge,
                       income.netto,
                       income.krankenvers,
                       income.privatvers,
                       income.abzuge,
                       income.uberweisung,
                       income.myconto,
                       datum.date(),
                       income.freq,
                       income.in_salary,
                       )
                table.append(tup)
                try:
                    if income.in_salary:
                        salary_brutto += income.brutto
                        if income.gesetzliche_abzuge:
                            salary_gesetzliche_abzuge += income.gesetzliche_abzuge
                        salary_netto += float(income.netto)
                        if income.abzuge:
                            salary_abzuge += income.abzuge
                        salary_uberweisung += float(income.uberweisung)
                    brutto += income.brutto
                    if income.gesetzliche_abzuge:
                        taxes += income.gesetzliche_abzuge
                    if income.abzuge:
                        abzuge += income.abzuge
                    netto += float(income.netto)
                    uberweisung += float(income.uberweisung)
                except:
                    print(income.name, income.brutto, income.netto)
        table = np.atleast_2d(table)
        result = (table, brutto, round(taxes, 2), netto, abzuge, uberweisung, salary_brutto, salary_gesetzliche_abzuge,
                  salary_netto, salary_abzuge, salary_uberweisung)
        return result

    def conv_csv_to_np(self, delimiter=';', skipHeader=None):
        array = []
        header = []
        with open(self.taxes_file, 'r') as file:
            reader = csv.reader(file, delimiter=delimiter)
            for i, row in enumerate(reader):
                if skipHeader:
                    if i < skipHeader:
                        header.append(row)
                        continue
                array.append(row)
            array = np.atleast_2d(array)
        if skipHeader == 1:
            header = header[0]

        return array, header

    def get_all_income_rows(self):
        vals = self.income_table.returnAllRecordsFromTable()
        all_incomes = []
        for row in vals:
            row = list(row)
            income = Cheltuiala(row, self.income_table.columnsNames)
            income.set_table(self.income_table.tableName)
            all_incomes.append(income)
        return all_incomes

    def filter_income_for_interval(self, all_income_rows):
        incomes_interval = []
        for inc in all_income_rows:
            payments_in_interval = None
            if self.myconto == 'all':
                payments_in_interval = inc.calculate_payments_in_interval(self.selectedStartDate, self.selectedEndDate)
            elif self.myconto == inc.myconto:
                payments_in_interval = inc.calculate_payments_in_interval(self.selectedStartDate, self.selectedEndDate)
            if payments_in_interval:
                inc.payments_for_interval = payments_in_interval
                incomes_interval.append(inc)
        return incomes_interval

    def find_other_incomes_with_salary_tax(self):
        other_incomes_with_salary = []
        for i in self.incomes_for_time_interval:
            if i.tax == 'salary' and i.name != 'Salariu':
                other_incomes_with_salary.append(i)
        return other_incomes_with_salary

    def prepareTablePlan(self, conto, selectedStartDate, selectedEndDate):
        self.selectedStartDate = selectedStartDate
        self.selectedEndDate = selectedEndDate
        self.myconto = conto

        all_income_rows = self.get_all_income_rows()
        self.incomes_for_time_interval = self.filter_income_for_interval(all_income_rows)
        self.apply_taxes_to_salary()
        # table = self.convert_to_tabel()
        result = self.convert_to_total_income_tabel()
        table, self.brutto, self.taxes, self.netto, self.abzuge, self.uberweisung, self.salary_brutto, \
        self.salary_gesetzliche_abzuge, self.salary_netto, self.salary_abzuge, self.salary_uberweisung = result

        self.tableHead, self.income = list(table[0]), table[1:]

    def get_salary_income(self, month):
        self.selectedStartDate, self.selectedEndDate = get_monthly_interval(month)
        self.myconto = 'EC'

        all_income_rows = self.get_all_income_rows()
        self.incomes_for_time_interval = self.filter_income_for_interval(all_income_rows)
        self.apply_taxes_to_salary()
        table, brutto, taxes, netto, abzuge, uberweisung = self.convert_to_salary_tabel()
        return table, brutto, taxes, netto, abzuge, uberweisung

    def get_total_monthly_income(self, month):
        self.selectedStartDate, self.selectedEndDate = get_monthly_interval(month)
        self.myconto = 'all'

        all_income_rows = self.get_all_income_rows()
        self.incomes_for_time_interval = self.filter_income_for_interval(all_income_rows)
        self.apply_taxes_to_salary()
        table, brutto, taxes, netto, abzuge, uberweisung = self.convert_to_total_income_tabel()
        return table, brutto, taxes, netto, abzuge, uberweisung

    def convert_to_display_table(self, tableHead, table, displayTableHead):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        newTableData = np.empty([table.shape[0], len(displayTableHead)], dtype=object)
        for i, col in enumerate(displayTableHead):
            indxCol = tableHead.index(col)
            newTableData[:, i] = table[:, indxCol]

        return displayTableHead, newTableData

    @property
    def monthly_income(self):
        monthly_income = 0
        for row in self.income:
            if row[self.tableHead.index('freq')] == 1:
                monthly_income += float(row[self.tableHead.index('netto')])
        return round(monthly_income, 2)

    @property
    def irregular_income(self):
        irregular_income = 0
        for row in self.income:
            if row[self.tableHead.index('freq')] > 1:
                irregular_income += float(row[self.tableHead.index('netto')])
        return round(irregular_income, 2)


class Cheltuiala:
    def __init__(self, row, tableHead):
        # print('#####', tableHead)
        self.tableHead = tableHead
        self.read_row(row)
        self.lohnsteuer = None
        self.rentenvers = None
        self.arbeitslosvers = None
        self.krankenvers = None
        self.privatvers = None
        self.brutto = None

    def read_row(self, row):
        for col in self.tableHead:
            exec('self.{} = row[self.tableHead.index("{}")]'.format(col, col))

        if self.pay_day is None:
            self.pay_day = calculate_last_day_of_month(self.valid_from.month, self.valid_from.year)

        if self.auto_ext is None or self.auto_ext == 0:
            self.auto_ext = False
        else:
            self.auto_ext = True

    def set_table(self, table_name):
        self.table = table_name

    @property
    def first_payment(self):
        try:
            first_payment = datetime(self.valid_from.year, self.valid_from.month, self.pay_day)
        except:
            # print(self.id, self.table, self.name)
            # print(self.valid_from.year, self.valid_from.month, self.pay_day)
            # first_payment = calculate_last_day_of_month(selectedStartDate.month)
            first_payment = datetime(self.valid_from.year, self.valid_from.month,
                                     calculate_last_day_of_month(self.valid_from.month, self.valid_from.year))
        return first_payment

    @property
    def is_salary(self):
        if self.name == 'Salariu' and self.freq == 1 and self.value:
            is_salary = True
        else:
            is_salary = False
        return is_salary

    @property
    def basic_brutto_35h_salary(self):
        return self.val

    @basic_brutto_35h_salary.setter
    def basic_brutto_35h_salary(self, income):
        self.val = float(income)

    @property
    def monthly_35h_brutto_salary(self):
        return self.val

    @monthly_35h_brutto_salary.setter
    def monthly_35h_brutto_salary(self, income):
        self.val = float(income)

    @property
    def hourly_salary(self):
        hourly_salary = self.monthly_35h_brutto_salary / 4 / 35
        return hourly_salary

    @property
    def brutto_monthly_salary(self):
        val = self.hourly_salary * self.hours * 4
        return val

    @property
    def gesetzliche_abzuge(self):
        try:
            gesetzliche_abzuge = round(self.lohnsteuer + self.rentenvers + self.arbeitslosvers, 2)
        except:
            return None
        return gesetzliche_abzuge

    @property
    def abzuge(self):
        try:
            abzuge = round(self.krankenvers + self.privatvers, 2)
        except:
            return None
        return abzuge

    @property
    def netto(self):
        if self.gesetzliche_abzuge and self.brutto:
            netto = round(self.brutto - self.gesetzliche_abzuge, 2)
        else:
            netto = self.brutto
        return netto

    @property
    def uberweisung(self):
        if self.netto and self.is_salary:
            uberweisung = round(float(self.netto) - self.abzuge, 2)
        else:
            uberweisung = self.netto
        return uberweisung

    def list_of_payments_valid_from_till_selected_end_date(self, selectedEndDate):
        list_of_payments_till_selected_end_date = []
        if self.valid_from <= self.first_payment.date() <= selectedEndDate:
            list_of_payments_till_selected_end_date.append(self.first_payment)

        next_payment = self.first_payment + relativedelta(months=self.freq)
        if next_payment.day != self.pay_day:
            try:
                next_payment = datetime(next_payment.year, next_payment.month, self.pay_day)
            except:
                next_payment = datetime(next_payment.year, next_payment.month,
                                        calculate_last_day_of_month(next_payment.month, next_payment.year))
        if self.valid_from <= next_payment.date() <= selectedEndDate:
            list_of_payments_till_selected_end_date.append(next_payment)

        while next_payment.date() <= selectedEndDate:
            next_payment = next_payment + relativedelta(months=self.freq)
            if next_payment.day != self.pay_day:
                try:
                    next_payment = datetime(next_payment.year, next_payment.month, self.pay_day)
                except:
                    # print('#####', next_payment.year, next_payment.month,
                    #                         calculate_last_day_of_month(next_payment.month, next_payment.year))
                    next_payment = datetime(next_payment.year, next_payment.month,
                                            calculate_last_day_of_month(next_payment.month, next_payment.year))
            if self.valid_from <= next_payment.date() <= selectedEndDate:
                list_of_payments_till_selected_end_date.append(next_payment)
        return list_of_payments_till_selected_end_date

    def cut_all_before_selectedStartDate(self, lista, selectedStartDate):
        new_list = []
        for date in lista:
            if date.date() >= selectedStartDate:
                new_list.append(date)
        return new_list

    def cut_all_after_valid_to(self, lista):
        new_list = []
        for date in lista:
            if date.date() <= self.valid_to:
                new_list.append(date)
        return new_list

    def calculate_payments_in_interval(self, selectedStartDate, selectedEndDate):
        list_of_payments_valid_from_till_selected_end_date = self.list_of_payments_valid_from_till_selected_end_date(
            selectedEndDate)
        # print(20*'*')
        # for i in list_of_payments_valid_from_till_selected_end_date:
        #     print(i)
        # print(20*'*')

        list_of_payments_selected_start_date_till_selected_end_date = self.cut_all_before_selectedStartDate(
            list_of_payments_valid_from_till_selected_end_date, selectedStartDate)
        # print(20*'*')
        # for i in list_of_payments_selected_start_date_till_selected_end_date:
        #     print(i)
        # print(20*'*')

        if self.valid_to and self.valid_to < selectedEndDate and not self.auto_ext:
            list_of_payments_selected_start_date_till_selected_end_date = self.cut_all_after_valid_to(
                list_of_payments_selected_start_date_till_selected_end_date)
            # print(20*'*')
            # for i in list_of_payments_selected_start_date_till_selected_end_date:
            #     print(i)
            # print(20*'*')

        return list_of_payments_selected_start_date_till_selected_end_date

    @property
    def first_payment_date(self):
        first_payment_date = datetime(self.valid_from.year, self.valid_from.month, self.pay_day)
        return first_payment_date

    @property
    def payments_for_interval(self):
        return self.pfi

    @payments_for_interval.setter
    def payments_for_interval(self, payments_days):
        self.pfi = payments_days


class CheltuieliPlanificate:
    def __init__(self, ini_file):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        self.ini_file = ini_file
        self.conf = connect.Config(self.ini_file)
        self.tableHead = ['id', 'category', 'name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to',
                          'auto_ext']
        # self.myAccountsTable = self.sql_rm.Table(self.conf.credentials, 'banca')
        self.one_time_transactions_Table = self.sql_rm.Table(self.conf.credentials, 'one_time_transactions')
        # self.myContos = self.myAccountsTable.returnColumn('name')
        self.chelt_plan = self.sql_rm.Table(self.conf.credentials, 'chelt_plan')
        try:
            self.dataBase = self.sql_rm.DataBase(self.conf.credentials)
        except Exception as err:
            print(traceback.format_exc())

    def default_interval(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        # print('Caller : ', sys._getframe().f_back.f_code.co_name)
        startDate = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
        if datetime.now().month != 12:
            mnth = datetime.now().month + 1
            lastDayOfMonth = datetime(datetime.now().year, mnth, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

        return startDate, lastDayOfMonth

    @property
    def sql_rm(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        if self.conf.db_type == 'mysql':
            sql_rm = mysql_rm
        return sql_rm

    def tot_no_of_irregular_expenses(self):
        indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] != 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        return monthly.shape[0]

    def tot_val_of_irregular_expenses(self):
        indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] != 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        if None in monthly:
            monthly = monthly[monthly != np.array(None)]
        totalMonthly = round(sum(monthly.astype(float)), 2)
        return totalMonthly

    def tot_no_of_monthly_expenses(self):
        indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] == 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        return monthly.shape[0]

    def tot_val_of_monthly_expenses(self):
        indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] == 1)[0]
        monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
        if None in monthly:
            monthly = monthly[monthly != np.array(None)]
        totalMonthly = round(sum(monthly.astype(float)), 2)
        return totalMonthly

    def tot_no_of_expenses(self):
        allValues = self.expenses[:, self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        return len(allValues)

    def tot_val_of_expenses(self):
        allValues = self.expenses[:, self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = round(sum(allValues.astype(float)), 2)
        return totalVal

    def tot_no_of_income(self):
        allValues = self.income[:, self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        return len(allValues)

    def tot_val_of_income(self):
        allValues = self.income[:, self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = round(sum(allValues.astype(float)), 2)
        return totalVal

    def tot_no_of_expenses_income(self):
        allExpenses = self.expenses[:, self.tableHead.index('value')]
        allIncome = self.income[:, self.tableHead.index('value')]
        tot = len(allExpenses) + len(allIncome)
        return tot

    def tot_val_of_expenses_income(self):
        allValues = self.income[:, self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalIncome = round(sum(allValues.astype(float)), 2)
        allValues = self.expenses[:, self.tableHead.index('value')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalExpenses = round(sum(allValues.astype(float)), 2)
        return round(totalIncome + totalExpenses, 2)

    def get_all_sql_vals(self):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name,
        #                                                           sys._getframe().f_back.f_code.co_name))
        new_table_head = []
        all_chelt = []
        for table in self.dataBase.allAvailableTablesInDatabase:
            if table == 'income':
                continue
            active_table = self.sql_rm.Table(self.conf.credentials, table)
            active_table_head = active_table.columnsNames
            if 'table' in self.tableHead:
                self.tableHead.remove('table')
            if 'payDay' in self.tableHead:
                self.tableHead.remove('payDay')
            check = all(item in active_table_head for item in self.tableHead)
            if check:
                print(table)
                # print(active_table_head)
                # for jj in active_table_head:
                #     if jj not in new_table_head:
                #         new_table_head.append(jj)
                # vals = active_table.returnColumns(self.tableHead)
                vals = active_table.returnAllRecordsFromTable()
                for row in vals:
                    row = list(row)
                    # print('*', row)
                    chelt = Cheltuiala(row, active_table.columnsNames)
                    chelt.set_table(table)
                    all_chelt.append(chelt)

                    # if table == 'chelt_plan':
                    #     continue
                    # cols = ['category']
                    # valori = [table]
                    # for colo in self.tableHead[1:]:
                    #     # print(colo)
                    #     cols.append(colo)
                    #     valori.append(row[active_table_head.index(colo)])
                    # print(cols)
                    # print(valori)
                    # self.chelt_plan.addNewRow(cols, valori)
        return all_chelt

    def filter_dates(self, all_chelt, selectedStartDate, selectedEndDate):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        remaining = []
        for chelt in all_chelt:
            # print('++', chelt.category, chelt.name, chelt.id, chelt.pay_day)
            payments_in_interval = chelt.calculate_payments_in_interval(selectedStartDate, selectedEndDate)
            # print(payments_in_interval)
            # if chelt.name == 'Steuererklärung_2022':
            #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, payments_in_interval)
            if isinstance(payments_in_interval, list):
                chelt.payments_for_interval = payments_in_interval
                # print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.payments_for_interval)
                if chelt.payments_for_interval:
                    remaining.append(chelt)
        return remaining

    # def filter_conto_old(self, chelt_list, conto):
    #     # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    #     remaining = []
    #     for ch in chelt_list:
    #         if conto == 'all' and ch.category != 'intercontotrans':
    #             remaining.append(ch)
    #         elif ch.myconto == conto:
    #             remaining.append(ch)
    #     return remaining

    def filter_conto(self, chelt_list, conto, hideintercontotrans):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        # print('ÖÖÖÖÖÖÖÖintercontotrans', intercontotrans)
        remaining = []
        for ch in chelt_list:
            if hideintercontotrans and ch.category == 'intercontotrans':
                continue
            if conto != 'all' and ch.myconto != conto:
                continue
            remaining.append(ch)
        return remaining

    def split_expenses_income(self, chelt):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        arr_expenses = []
        arr_income = []
        for ch in chelt:
            if ch.value == 0:
                continue
            for payment_day in ch.payments_for_interval:
                # if ch.value and ch.value > 0:
                #     incomeTable = self.sql_rm.Table(self.conf.credentials, ch.table)
                #     full_row = list(incomeTable.returnRowsWhere(('id', ch.id))[0])
                #     venit_instance = Income(full_row, incomeTable.columnsNames)
                #     ch.value = venit_instance.calculate_income()

                variables = vars(ch)
                row = [ch.table]
                for col in self.tableHead:
                    val = variables[col]
                    row.append(val)
                # print('######', payment_day, type(payment_day))
                row.append(payment_day.date())
                if ch.value and ch.value > 0:
                    arr_income.append(row)
                else:
                    arr_expenses.append(row)
        arr_expenses = np.atleast_2d(arr_expenses)
        arr_income = np.atleast_2d(arr_income)
        self.tableHead.insert(0, 'table')
        self.tableHead.append('payDay')
        return arr_expenses, arr_income

    def prepareTablePlan(self, conto, selectedStartDate, selectedEndDate, intercontotrans):
        # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
        print(selectedStartDate, selectedEndDate)
        all_chelt = self.get_all_sql_vals()
        # for i in all_chelt:
        #     print(i.freq)
        # all_chelt = self.get_one_time_transactions(all_chelt)

        chelt_in_time_interval = self.filter_dates(all_chelt, selectedStartDate, selectedEndDate)
        # for chelt in chelt_in_time_interval:
        #     print(chelt.category, chelt.name, chelt.id, chelt.pay_day, chelt.myconto, chelt.payments_for_interval)

        chelt_after_contofilter = self.filter_conto(chelt_in_time_interval, conto, intercontotrans)
        # for chelt in chelt_after_contofilter:
        #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.conto, chelt.payments_for_interval)

        self.expenses, self.income = self.split_expenses_income(chelt_after_contofilter)
        if self.expenses.shape == (1, 0):
            expenses = np.empty((0, len(self.tableHead)))
        if self.income.shape == (1, 0):
            income = np.empty((0, len(self.tableHead)))

    def convert_to_display_table(self, tableHead, table, displayTableHead):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        newTableData = np.empty([table.shape[0], len(displayTableHead)], dtype=object)
        for i, col in enumerate(displayTableHead):
            indxCol = tableHead.index(col)
            newTableData[:, i] = table[:, indxCol]

        return displayTableHead, newTableData

    def add_one_time_transactions(self, name, value, myconto, pay_day):
        cols = ('name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to', 'auto_ext')
        payday = pay_day.day
        valid_from = pay_day
        valid_to = pay_day
        vals = (name, value, myconto, 999, payday, valid_from, valid_to, 0)
        self.one_time_transactions_Table.addNewRow(cols, vals)


class CheltPlusIncome:
    def __init__(self, ini_file, conto, dataFrom, dataBis):
        self.income = Income(ini_file)
        self.income.prepareTablePlan(conto, dataFrom, dataBis)

        self.chelt = CheltuieliPlanificate(ini_file)
        self.chelt.prepareTablePlan(conto, dataFrom, dataBis)

    @property
    def summary_table(self):
        total_dif = round(self.income.netto + self.chelt.tot_val_of_expenses(), 2)
        monthly_dif = round(self.income.monthly_income + self.chelt.tot_val_of_monthly_expenses(), 2)
        irregular_dif = round(self.income.irregular_income + self.chelt.tot_val_of_irregular_expenses())
        arr = [('', 'Income', 'Expenses', 'Diff'),
               ('Total', self.income.netto, self.chelt.tot_val_of_expenses(), total_dif),
               ('Monthly', self.income.monthly_income, self.chelt.tot_val_of_monthly_expenses(), monthly_dif),
               ('Irregular', self.income.irregular_income, self.chelt.tot_val_of_irregular_expenses(), irregular_dif),
               ]
        arr = np.atleast_2d(arr)
        return arr


class CheltuieliReale:
    def __init__(self, ini_file):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        self.ini_file = ini_file
        self.conf = connect.Config(self.ini_file)
        self.myAccountsTable = self.sql_rm.Table(self.conf.credentials, 'banca')
        self.imported_csv = self.sql_rm.Table(self.conf.credentials, 'imported_csv')
        self.chelt_plan = self.sql_rm.Table(self.conf.credentials, 'chelt_plan')
        # self.expensesTableReal = self.sql_rm.Table(self.conf.credentials, 'real_expenses')
        self.expensesTableReal = self.sql_rm.Table(self.conf.credentials, 'plan_vs_real')
        self.sskm = self.sql_rm.Table(self.conf.credentials, 'sskm')
        self.deubnk = self.sql_rm.Table(self.conf.credentials, 'deubnk')
        self.n26 = self.sql_rm.Table(self.conf.credentials, 'n26')
        self.myContos = self.myAccountsTable.returnColumn('name')
        self.realExpenses = None
        self.realIncome = None

        try:
            self.dataBase = self.sql_rm.DataBase(self.conf.credentials)
        except Exception as err:
            print(traceback.format_exc())

    @property
    def sql_rm(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        if self.conf.db_type == 'mysql':
            sql_rm = mysql_rm
        return sql_rm

    def default_interval(self):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        print('Caller : ', sys._getframe().f_back.f_code.co_name)
        startDate = datetime(datetime.now().year - 1, datetime.now().month, datetime.now().day)
        if datetime.now().month != 12:
            mnth = datetime.now().month + 1
            lastDayOfMonth = datetime(datetime.now().year, mnth, 1) - timedelta(days=1)
        else:
            lastDayOfMonth = datetime(datetime.now().year + 1, 1, 1) - timedelta(days=1)

        return startDate, lastDayOfMonth

    def get_buchungstag_interval(self, currentConto):
        if currentConto != 'all':
            matches = ('banca', currentConto)
            # print(currentConto)
            start_col = self.imported_csv.returnCellsWhere('start', matches)
            end_col = self.imported_csv.returnCellsWhere('end', matches)
            # print(start_col)
        else:
            start_col = self.imported_csv.returnColumn('start')
            end_col = self.imported_csv.returnColumn('end')

        # print(100*'allbuchungstag')
        # print(allbuchungstag)
        if start_col and end_col:
            return min(start_col), max(end_col)
        else:
            return None, None

    # def get_buchungstag_interval_old(self, currentConto):
    #     if currentConto != 'all':
    #         col = 'IBAN'
    #         matches = ('name', currentConto)
    #         iban = self.myAccountsTable.returnCellsWhere(col, matches)[0]
    #         # print('ÖÖ', iban)
    #         matches = ('myconto', currentConto)
    #         allbuchungstag = self.expensesTableReal.returnCellsWhere('Buchungstag', matches)
    #     else:
    #         allbuchungstag = self.expensesTableReal.returnColumn('Buchungstag')
    #     # print(100*'allbuchungstag')
    #     # print(allbuchungstag)
    #     if allbuchungstag:
    #         return min(allbuchungstag), max(allbuchungstag)
    #     else:
    #         return None, None
    #
    # def csv_table_head_ok(self, row):
    #     tableHead = [c.strip('"') for c in row]
    #     tabHeadDict = {'Auftragskonto': 'Auftragskonto',
    #                    'Buchungstag': 'Buchungstag',
    #                    'Valutadatum': 'Valutadatum',
    #                    'Buchungstext': 'Buchungstext',
    #                    'Verwendungszweck': 'Verwendungszweck',
    #                    'Glaeubiger ID': 'Glaeubiger',
    #                    'Mandatsreferenz': 'Mandatsreferenz',
    #                    'Kundenreferenz (End-to-End)': 'Kundenreferenz',
    #                    'Sammlerreferenz': 'Sammlerreferenz',
    #                    'Lastschrift Ursprungsbetrag': 'Lastschrift',
    #                    'Auslagenersatz Ruecklastschrift': 'Auslagenersatz',
    #                    'Beguenstigter/Zahlungspflichtiger': 'Beguenstigter',
    #                    'Kontonummer/IBAN': 'IBAN',
    #                    'BIC (SWIFT-Code)': 'BIC',
    #                    'Betrag': 'Betrag',
    #                    'Waehrung': 'Waehrung',
    #                    'Info': 'Info'}
    #
    #     cols = list(tabHeadDict.values())
    #     cols.append('path2inp')
    #     for col in tableHead:
    #         if col not in tabHeadDict.keys():
    #             message = 'column {} new in csv table'.format(col)
    #             # QMessageBox.warning(self, 'Inconsistent Data', message, QMessageBox.Ok)
    #             raise RuntimeError(message)
    #             # return ()
    #         elif tabHeadDict[col] not in self.expensesTableReal.columnsNames:
    #             message = 'column {} missing in SQL table'.format(tabHeadDict[col])
    #             # QMessageBox.warning(self, 'Inconsistent Data', message, QMessageBox.Ok)
    #             # return ()
    #             raise RuntimeError(message)
    #     return True
    #
    # def copy_csv_to_profile(self, src):
    #     try:
    #         pth_2_profile = r'static\backup_profile\radu'
    #         destination = os.path.join(os.path.dirname(__file__), pth_2_profile)
    #         # print('ÖÖ', destination, os.path.exists(destination))
    #         shutil.copy(src, destination)
    #         message = 'successfully copied {} \n\tto {}'.format(src, destination)
    #         print(message)
    #     except Exception:
    #         message = traceback.format_exc()
    #     return message

    def add_row_to_imported_csv(self, inpFile, banca, start, end, total_rows, imported_rows):
        cols = ['file_name', 'banca', 'start', 'end', 'file', 'total_rows', 'imported_rows']
        path, file_name = os.path.split(inpFile)
        vals = [file_name, banca, start, end, inpFile, total_rows, imported_rows]
        self.imported_csv.addNewRow(cols, tuple(vals))

    # def importCSV(self, currentConto, inpFile):
    #     print(sys._getframe().f_code.co_name)
    #     # self.copy_csv_to_profile(inpFile)
    #     col = 'banca'
    #     matches = ('name', currentConto)
    #     banca = self.myAccountsTable.returnCellsWhere(col, matches)[0]
    #     print('banca', banca)
    #     total_transactions = 0
    #     inserted_transactions = 0
    #     not_inserted_transactions = 0
    #     start = None
    #     end = None
    #     if banca == 'Stadtsparkasse München':
    #         with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #             linereader = csv.reader(csvfile, delimiter=';', quotechar='|')
    #             for i, row in enumerate(linereader):
    #                 if i == 0:  # and self.csv_table_head_ok(row)
    #                     tableHead = [c.strip('"') for c in row]
    #                     tabHeadDict = {'Auftragskonto': 'Auftragskonto',
    #                                    'Buchungstag': 'Buchungstag',
    #                                    'Valutadatum': 'Valutadatum',
    #                                    'Buchungstext': 'Buchungstext',
    #                                    'Verwendungszweck': 'Verwendungszweck',
    #                                    'Glaeubiger ID': 'Glaeubiger',
    #                                    'Mandatsreferenz': 'Mandatsreferenz',
    #                                    'Kundenreferenz (End-to-End)': 'Kundenreferenz',
    #                                    'Sammlerreferenz': 'Sammlerreferenz',
    #                                    'Lastschrift Ursprungsbetrag': 'Lastschrift',
    #                                    'Auslagenersatz Ruecklastschrift': 'Auslagenersatz',
    #                                    'Beguenstigter/Zahlungspflichtiger': 'Beguenstigter',
    #                                    'Kontonummer/IBAN': 'IBAN',
    #                                    'BIC (SWIFT-Code)': 'BIC',
    #                                    'Betrag': 'Betrag',
    #                                    'Waehrung': 'Waehrung',
    #                                    'Info': 'Info'}
    #
    #                     auftragskontoIndx = tableHead.index('Auftragskonto')
    #                     betragIndx = tableHead.index('Betrag')
    #                     buchungstagIndx = tableHead.index('Buchungstag')
    #                     valutadatumIndx = tableHead.index('Valutadatum')
    #                     verwendungszweckIndx = tableHead.index('Verwendungszweck')
    #                     ibanIndx = tableHead.index('Kontonummer/IBAN')
    #                     cols = list(tabHeadDict.values())
    #                     cols.append('path2inp')
    #                     cols.append('row_no')
    #                     cols.append('myconto')
    #                     for col in tableHead:
    #                         if col not in tabHeadDict.keys():
    #                             message = 'column {} new in csv table'.format(col)
    #                             # QMessageBox.warning(self, 'Inconsistent Data', message, QMessageBox.Ok)
    #                             raise RuntimeError(message)
    #                             # return ()
    #                         elif tabHeadDict[col] not in self.expensesTableReal.columnsNames:
    #                             message = 'column {} missing in SQL table'.format(tabHeadDict[col])
    #                             # QMessageBox.warning(self, 'Inconsistent Data', message, QMessageBox.Ok)
    #                             # return ()
    #                             raise RuntimeError(message)
    #                     # print('OOOOOOOOOOOOOk',)# todo
    #                     continue
    #                 total_transactions += 1
    #                 row = [c.strip('"') for c in row]
    #                 # print('row', row)
    #                 # modify value to float
    #                 val = row[betragIndx]
    #                 val = float(val.replace(",", "."))
    #                 row[betragIndx] = val
    #                 # modify date format
    #                 if row[buchungstagIndx] == "" or row[valutadatumIndx] == "":
    #                     continue
    #                 buchungstag = self.expensesTableReal.convertDatumFormat4SQL(row[buchungstagIndx])
    #                 # print('ÖÖ, buchungstag, buchungstagIndx', buchungstag, buchungstagIndx)
    #                 row[buchungstagIndx] = buchungstag
    #                 if not start:
    #                     start = buchungstag
    #                 else:
    #                     start = min(buchungstag, start)
    #                 if not end:
    #                     end = buchungstag
    #                 else:
    #                     end = max(buchungstag, end)
    #
    #                 valutadatum = self.expensesTableReal.convertDatumFormat4SQL(row[valutadatumIndx])
    #                 row[valutadatumIndx] = valutadatum
    #
    #                 # check if already in table
    #                 verwendungszweck = row[verwendungszweckIndx]
    #                 iban = row[ibanIndx]
    #                 auftragskonto = row[auftragskontoIndx]
    #
    #                 matches = [('Buchungstag', str(buchungstag)),
    #                            ('Auftragskonto', str(auftragskonto)),
    #                            ('Valutadatum', str(valutadatum)),
    #                            ('Betrag', val),
    #                            ('IBAN', iban),
    #                            ('Verwendungszweck', verwendungszweck)]
    #
    #                 res = self.expensesTableReal.returnCellsWhere('id', matches)
    #                 if res:
    #                     # print('**row', i+1, row)
    #                     message = 'row\n{}\nalready existing at row id {}...skip'.format(row, str(res))
    #                     # print(('Auftragskonto', str(auftragskonto),
    #                     #        ('Buchungstag', str(buchungstag)),
    #                     #       ('Valutadatum', str(valutadatum)),
    #                     #       ('Betrag', val),
    #                     #       ('IBAN', iban),
    #                     #       ('Verwendungszweck', verwendungszweck)))
    #                     # QMessageBox.warning(self, 'Inconsistent Data', message, QMessageBox.Ok)
    #                     not_inserted_transactions += 1
    #                     print(message)
    #                     print(400 * '*')
    #                     continue
    #
    #                     # raise RuntimeError(message)
    #                 else:
    #                     row.append(inpFile)
    #                     row.append(i + 1)
    #
    #                     row.append(currentConto)
    #                     self.expensesTableReal.addNewRow(cols, row)
    #                     inserted_transactions += 1
    #     if banca == 'DeutscheBank':
    #         col = 'IBAN'
    #         matches = ('name', currentConto)
    #         IBAN = self.myAccountsTable.returnCellsWhere(col, matches)[0]
    #         with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #             linereader = csv.reader(csvfile, delimiter=';', quotechar='|')
    #             for i, row in enumerate(linereader):
    #                 if i < 4:
    #                     continue
    #                 elif i == 4:
    #                     tableHead = [c.strip('"') for c in row]
    #                     print(tableHead)
    #                     tabHeadDict = {'Booking date': 'Buchungstag',
    #                                    'Value date': 'Valutadatum',
    #                                    'Transaction Type': 'Buchungstext',
    #                                    'Beneficiary / Originator': 'Beguenstigter',
    #                                    'Payment Details': 'Verwendungszweck',
    #                                    'IBAN': 'IBAN',
    #                                    'BIC': 'BIC',
    #                                    'Customer Reference': 'Kundenreferenz',
    #                                    'Mandate Reference': 'Mandatsreferenz',
    #                                    'Creditor ID': 'Glaeubiger',
    #                                    # 'Compensation amount': 'Sammlerreferenz',
    #                                    'Original Amount': 'Sammlerreferenz',
    #                                    'Ultimate creditor': 'Lastschrift',
    #                                    'Number of transactions': 'Auslagenersatz',
    #                                    # 'Number of cheques': 'Auslagenersatz',
    #                                    # 'Debit': 'Betrag',
    #                                    # 'Credit': 'Betrag',
    #                                    'Currency': 'Waehrung'
    #                                    }
    #                     continue
    #                 elif row[0] == 'Account balance':
    #                     continue
    #                 total_transactions += 1
    #                 row = [c.strip('"') for c in row]
    #                 cols = ['Auftragskonto', 'path2inp', 'row_no']
    #                 vals = [IBAN, inpFile, i + 1]
    #                 for ir, v in enumerate(row):
    #                     origColName = tableHead[ir]
    #                     if (origColName == 'Debit' and v != '') or (origColName == 'Credit' and v != ''):
    #                         # print(origColName, 'Betrag', v)
    #                         cols.append('Betrag')
    #                         vals.append(float(v.replace(",", "")))
    #                     if origColName in list(tabHeadDict.keys()):
    #                         # print(origColName, tabHeadDict[origColName], v)
    #                         cols.append(tabHeadDict[origColName])
    #                         if (tabHeadDict[origColName] == 'Buchungstag') or (
    #                                 tabHeadDict[origColName] == 'Valutadatum'):
    #                             v = self.expensesTableReal.convertDatumFormat4SQL(v)
    #                         vals.append(v)
    #                 cols.append('myconto')
    #                 vals.append(currentConto)
    #                 # check if already in table
    #                 buchungstag = vals[cols.index('Buchungstag')]
    #                 if not start:
    #                     start = buchungstag
    #                 else:
    #                     start = min(buchungstag, start)
    #                 if not end:
    #                     end = buchungstag
    #                 else:
    #                     end = max(buchungstag, end)
    #
    #                 valutadatum = vals[cols.index('Valutadatum')]
    #                 iban = vals[cols.index('IBAN')]
    #                 verwendungszweck = vals[cols.index('Verwendungszweck')]
    #                 val = vals[cols.index('Betrag')]
    #                 matches = [('Buchungstag', str(buchungstag)),
    #                            ('Valutadatum', str(valutadatum)),
    #                            ('Betrag', val),
    #                            ('IBAN', iban),
    #                            ('Verwendungszweck', verwendungszweck)]
    #                 res = self.expensesTableReal.returnCellsWhere('id', matches)
    #                 if res:
    #                     message = 'row\n{}\nalready existing...skip'.format(row)
    #                     print(('Buchungstag', str(buchungstag)),
    #                           ('Valutadatum', str(valutadatum)),
    #                           ('Betrag', val),
    #                           ('Verwendungszweck', verwendungszweck))
    #                     # QMessageBox.warning(self, 'Inconsistent Data', message, QMessageBox.Ok)
    #                     # continue
    #                     # raise RuntimeError(message)
    #                     not_inserted_transactions += 1
    #                     print(message)
    #                     continue
    #                 else:
    #                     self.expensesTableReal.addNewRow(cols, vals)
    #                     inserted_transactions += 1
    #     if banca == 'N26':
    #         # print(200*'Ö')
    #         col = 'IBAN'
    #         matches = ('name', currentConto)
    #         IBAN = self.myAccountsTable.returnCellsWhere(col, matches)[0]
    #         # print('ÄÄÄÄIBAN', IBAN)
    #         with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #             linereader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #             for i, row in enumerate(linereader):
    #                 # print('LLLL_row', row)
    #                 if i == 0:
    #                     tableHead = [c.strip('"') for c in row]
    #                     print(tableHead)
    #                     if 'Partner Name' in tableHead:
    #                         tabHeadDict = {'Booking Date': 'Buchungstag',
    #                                        'Partner Name': 'Beguenstigter',
    #                                        'Partner Iban': 'IBAN',
    #                                        'Type': 'Buchungstext',
    #                                        'Payment Reference': 'Verwendungszweck',
    #                                        'Account Name': 'Info',
    #                                        'Amount (EUR)': 'Betrag',
    #                                        'Original Amount': 'Mandatsreferenz',
    #                                        'Original Currency': 'Waehrung',
    #                                        'Exchange Rate': 'Lastschrift'
    #                                        }
    #                     else:
    #                         tabHeadDict = {'Date': 'Buchungstag',
    #                                        'Payee': 'Beguenstigter',
    #                                        'Account number': 'IBAN',
    #                                        'Transaction type': 'Buchungstext',
    #                                        'Payment reference': 'Verwendungszweck',
    #                                        'Amount (EUR)': 'Betrag',
    #                                        'Amount (Foreign Currency)': 'Mandatsreferenz',
    #                                        'Type Foreign Currency': 'Waehrung',
    #                                        'Exchange Rate': 'Lastschrift'
    #                                        }
    #
    #                     continue
    #                 # print(row, type(row))
    #                 # continue
    #                 # row = [c.strip('"') for c in row]
    #                 total_transactions += 1
    #                 cols = ['Auftragskonto', 'path2inp', 'row_no']
    #                 vals = [IBAN, inpFile, i + 1]
    #                 buchungstag = None
    #                 betrag = None
    #                 beguenstigter = None
    #                 verwendungszweck = None
    #                 for ir, v in enumerate(row):
    #                     origColName = tableHead[ir]
    #                     # print('kk', v, tableHead[ir], origColName, origColName in list(tabHeadDict.keys()))
    #                     if origColName in list(tabHeadDict.keys()):
    #                         cols.append(tabHeadDict[origColName])
    #                         if tabHeadDict[origColName] == 'Buchungstag':
    #                             v = self.expensesTableReal.convertDatumFormat4SQL(v)
    #                             buchungstag = v
    #                             if not start:
    #                                 start = v
    #                             else:
    #                                 start = min(v, start)
    #                             if not end:
    #                                 end = v
    #                             else:
    #                                 end = max(v, end)
    #                         if tabHeadDict[origColName] == 'Betrag':
    #                             v = float(v)
    #                             betrag = v
    #                         if tabHeadDict[origColName] == 'Beguenstigter':
    #                             v = str(v)
    #                             beguenstigter = v
    #                         if tabHeadDict[origColName] == 'Verwendungszweck':
    #                             v = str(v)
    #                             verwendungszweck = v
    #                         vals.append(v)
    #
    #                 cols.append('myconto')
    #                 vals.append(currentConto)
    #                 print(cols)
    #                 print(vals)
    #                 if vals[cols.index('Buchungstag')].year < 2022:
    #                     continue
    #                 matches = [('Buchungstag', str(buchungstag)),
    #                            # ('Auftragskonto', str(auftragskonto)),
    #                            ('Beguenstigter', str(beguenstigter)),
    #                            ('Betrag', betrag),
    #                            # ('IBAN', IBAN),
    #                            ('Verwendungszweck', verwendungszweck)]
    #
    #                 print('matches', matches)
    #                 res = self.expensesTableReal.returnCellsWhere('id', matches)
    #                 if res:
    #                     # print('**row', i+1, row)
    #                     message = 'row\n{}\nalready existing at row id {}...skip'.format(row, str(res))
    #                     not_inserted_transactions += 1
    #                     print(message)
    #                     print(400 * '*')
    #                     continue
    #                 else:
    #                     self.expensesTableReal.addNewRow(cols, vals)
    #                     inserted_transactions += 1
    #                 # return
    #     print('total_transactions', total_transactions)
    #     print('inserted_transactions', inserted_transactions)
    #     print('not_inserted_transactions', not_inserted_transactions)
    #     # print(start, start)
    #     self.add_row_to_imported_csv(inpFile, currentConto, start, end, total_transactions, inserted_transactions)
    #
    # def check_csv_table_head_old(self, inpFile, bank):
    #     if bank == 'DeutscheBank':
    #         delimiter = ';'
    #     elif bank == 'Stadtsparkasse München':
    #         delimiter = ';'
    #     elif bank == 'N26':
    #         delimiter = ','
    #
    #     with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #         linereader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
    #         for i, row in enumerate(linereader):
    #             if i == 0 and bank != 'DeutscheBank':
    #                 # print('####', row)
    #                 csv_table_head = row
    #                 tabHeadDict = bank_tabHeadDict[bank]
    #                 # print('AAAAAAAAAA', tabHeadDict)
    #                 known_table_head = (list(tabHeadDict.keys()))
    #                 all_csv_cols_in_known_table_head = all(item in known_table_head for item in csv_table_head)
    #                 # print('all_csv_cols_in_known_table_head', all_csv_cols_in_known_table_head)
    #                 all_known_table_head_cols_in_csv = all(item in csv_table_head for item in known_table_head)
    #                 # print('all_known_table_head_cols_in_csv', all_known_table_head_cols_in_csv)
    #                 if all_csv_cols_in_known_table_head and all_known_table_head_cols_in_csv:
    #                     return list(tabHeadDict.values())
    #                 else:
    #                     return False
    #             elif i == 4 and bank == 'DeutscheBank':
    #                 print('####', row)
    #                 csv_table_head = row
    #                 tabHeadDict = bank_tabHeadDict[bank]
    #                 known_table_head = (list(tabHeadDict.keys()))
    #                 print('AAAAAAAAAAknown_table_head', known_table_head)
    #                 all_csv_cols_in_known_table_head = all(item in known_table_head for item in csv_table_head)
    #                 print('all_csv_cols_in_known_table_head', all_csv_cols_in_known_table_head)
    #                 all_known_table_head_cols_in_csv = all(item in csv_table_head for item in known_table_head)
    #                 print('all_known_table_head_cols_in_csv', all_known_table_head_cols_in_csv)
    #                 if all_csv_cols_in_known_table_head and all_known_table_head_cols_in_csv:
    #                     return list(tabHeadDict.values())
    #                 else:
    #                     return False

    def check_csv_table_head(self, inpFile, bank):
        sql_table_head = None
        csv_tabel_cheltuieli = []
        if bank == 'DeutscheBank':
            delimiter = ';'
        elif bank == 'Stadtsparkasse München':
            delimiter = ';'
        elif bank == 'N26':
            delimiter = ','

        with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
            linereader = csv.reader(csvfile, delimiter=delimiter, quotechar='"')
            for i, row in enumerate(linereader):
                if i == 0 and bank != 'DeutscheBank':
                    # print('####', row)
                    csv_table_head = row
                    tabHeadDict = bank_tabHeadDict[bank]
                    # print('AAAAAAAAAA', tabHeadDict)
                    known_table_head = (list(tabHeadDict.keys()))
                    all_csv_cols_in_known_table_head = all(item in known_table_head for item in csv_table_head)
                    # print('all_csv_cols_in_known_table_head', all_csv_cols_in_known_table_head)
                    all_known_table_head_cols_in_csv = all(item in csv_table_head for item in known_table_head)
                    # print('all_known_table_head_cols_in_csv', all_known_table_head_cols_in_csv)
                    if all_csv_cols_in_known_table_head and all_known_table_head_cols_in_csv:
                        sql_table_head = list(tabHeadDict.values())
                elif i > 0 and bank != 'DeutscheBank':
                    csv_tabel_cheltuieli.append(row)
                elif i < 4 and bank == 'DeutscheBank':
                    continue
                elif i == 4 and bank == 'DeutscheBank':
                    csv_table_head = row
                    tabHeadDict = bank_tabHeadDict[bank]
                    known_table_head = (list(tabHeadDict.keys()))
                    all_csv_cols_in_known_table_head = all(item in known_table_head for item in csv_table_head)
                    # print('all_csv_cols_in_known_table_head', all_csv_cols_in_known_table_head)
                    all_known_table_head_cols_in_csv = all(item in csv_table_head for item in known_table_head)
                    # print('all_known_table_head_cols_in_csv', all_known_table_head_cols_in_csv)
                    if all_csv_cols_in_known_table_head and all_known_table_head_cols_in_csv:
                        sql_table_head = list(tabHeadDict.values())
                elif i > 4 and bank == 'DeutscheBank' and len(row) > 10:
                    csv_tabel_cheltuieli.append(row)

        return sql_table_head, csv_tabel_cheltuieli

    # def import_sskm_CSV(self, currentConto, inpFile):
    #     print(sys._getframe().f_code.co_name)
    #     matches = ('name', currentConto)
    #     banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
    #     matches = ('name', currentConto)
    #     auftragskonto_iban = self.myAccountsTable.returnCellsWhere('IBAN', matches)[0]
    #     sskm_table = self.sql_rm.Table(self.conf.credentials, 'sskm')
    #     total_transactions = 0
    #     inserted_transactions = 0
    #     not_inserted_transactions = 0
    #     start = None
    #     end = None
    #     if banca == 'Stadtsparkasse München':
    #         table_head = self.check_csv_table_head(inpFile, ';')
    #         table_head.append('id_users')
    #         table_head.append('myconto')
    #         table_head.append('path2inp')
    #         table_head.append('row_no')
    #         if table_head:
    #             auftragskontoIndx = table_head.index('Auftragskonto')
    #             betragIndx = table_head.index('Betrag')
    #             buchungstagIndx = table_head.index('Buchungstag')
    #             valutadatumIndx = table_head.index('Valutadatum')
    #             verwendungszweckIndx = table_head.index('Verwendungszweck')
    #             ibanIndx = table_head.index('IBAN')
    #             # return
    #             with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #                 linereader = csv.reader(csvfile, delimiter=';', quotechar='"')
    #                 for i, row in enumerate(linereader):
    #                     if i == 0:
    #                         continue
    #                     row.append(1)
    #                     row.append(currentConto)
    #                     row.append(inpFile)
    #                     row.append(i)
    #                     # modify value to float
    #                     val = row[betragIndx]
    #                     val = float(val.replace(",", "."))
    #                     row[betragIndx] = val
    #                     # modify date format
    #                     if row[buchungstagIndx] == "" or row[valutadatumIndx] == "":
    #                         continue
    #                     buchungstag = self.expensesTableReal.convertDatumFormat4SQL(row[buchungstagIndx])
    #                     row[buchungstagIndx] = buchungstag
    #
    #                     # check if already in table
    #                     verwendungszweck = row[verwendungszweckIndx]
    #                     iban = row[ibanIndx]
    #                     auftragskonto = row[auftragskontoIndx]
    #                     if auftragskonto != auftragskonto_iban:
    #                         raise RuntimeError(
    #                             'IBAN in csv {} diffrent then the one in the bank {} for myconto'.format(auftragskonto,
    #                                                                                                      iban,
    #                                                                                                      currentConto))
    #
    #                     if not start:
    #                         start = buchungstag
    #                     else:
    #                         start = min(buchungstag, start)
    #                     if not end:
    #                         end = buchungstag
    #                     else:
    #                         end = max(buchungstag, end)
    #
    #                     matches = [('Buchungstag', str(buchungstag)),
    #                                ('Auftragskonto', str(auftragskonto)),
    #                                # ('Valutadatum', str(valutadatum)),
    #                                ('Betrag', val),
    #                                ('IBAN', iban),
    #                                ('Verwendungszweck', verwendungszweck)]
    #                     res = sskm_table.returnCellsWhere('id', matches)
    #                     if res:
    #                         message = 'row\n{}\nalready existing at row id {}...skip'.format(row, str(res))
    #                         not_inserted_transactions += 1
    #                         print(message)
    #                         continue
    #                     else:
    #                         sskm_table.addNewRow(table_head, row)
    #                         inserted_transactions += 1
    #         print('total_transactions', total_transactions)
    #         print('inserted_transactions', inserted_transactions)
    #         print('not_inserted_transactions', not_inserted_transactions)
    #         # print(start, start)
    #         self.add_row_to_imported_csv(inpFile, currentConto, start, end, total_transactions, inserted_transactions)
    #         return
    #
    # def import_n26_CSV(self, currentConto, inpFile):
    #     print(sys._getframe().f_code.co_name)
    #     matches = ('name', currentConto)
    #     banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
    #     # print(banca)
    #     matches = ('name', currentConto)
    #     auftragskonto_iban = self.myAccountsTable.returnCellsWhere('IBAN', matches)[0]
    #     n26_table = self.sql_rm.Table(self.conf.credentials, 'n26')
    #     total_transactions = 0
    #     inserted_transactions = 0
    #     not_inserted_transactions = 0
    #     start = None
    #     end = None
    #     if banca == 'N26':
    #         table_head = self.check_csv_table_head(inpFile, ',', banca)
    #         if table_head:
    #             table_head.append('id_users')
    #             table_head.append('myconto')
    #             table_head.append('path2inp')
    #             table_head.append('row_no')
    #             # print('ÖÖÖÖÖMMMM', table_head)
    #             # return
    #             # auftragskontoIndx = table_head.index('Auftragskonto')
    #             betragIndx = table_head.index('Amount')
    #             buchungstagIndx = table_head.index('Buchungstag')
    #             valutadatumIndx = table_head.index('ValueDate')
    #             verwendungszweckIndx = table_head.index('PaymentReference')
    #             ibanIndx = table_head.index('IBAN')
    #             # return
    #             with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #                 linereader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #                 for i, row in enumerate(linereader):
    #                     if i == 0:
    #                         continue
    #                     row.append(1)
    #                     row.append(currentConto)
    #                     row.append(inpFile)
    #                     row.append(i)
    #                     # modify value to float
    #                     val = row[betragIndx]
    #                     val = float(val)
    #                     row[betragIndx] = val
    #                     # modify date format
    #                     if row[buchungstagIndx] == "" or row[valutadatumIndx] == "":
    #                         continue
    #                     buchungstag = self.expensesTableReal.convertDatumFormat4SQL(row[buchungstagIndx])
    #                     row[buchungstagIndx] = buchungstag
    #
    #                     # check if already in table
    #                     verwendungszweck = row[verwendungszweckIndx]
    #                     iban = row[ibanIndx]
    #                     if not start:
    #                         start = buchungstag
    #                     else:
    #                         start = min(buchungstag, start)
    #                     if not end:
    #                         end = buchungstag
    #                     else:
    #                         end = max(buchungstag, end)
    #
    #                     matches = [('Buchungstag', str(buchungstag)),
    #                                # ('Auftragskonto', str(auftragskonto)),
    #                                # ('Valutadatum', str(valutadatum)),
    #                                ('Amount', val),
    #                                ('IBAN', iban),
    #                                ('PaymentReference', verwendungszweck)]
    #                     res = n26_table.returnCellsWhere('id', matches)
    #                     if res:
    #                         message = 'row\n{}\nalready existing at row id {}...skip'.format(row, str(res))
    #                         not_inserted_transactions += 1
    #                         print(message)
    #                         continue
    #                     else:
    #                         n26_table.addNewRow(table_head, row)
    #                         inserted_transactions += 1
    #         print('total_transactions', total_transactions)
    #         print('inserted_transactions', inserted_transactions)
    #         print('not_inserted_transactions', not_inserted_transactions)
    #         # print(start, start)
    #         self.add_row_to_imported_csv(inpFile, currentConto, start, end, total_transactions, inserted_transactions)
    #
    # def import_DB_CSV(self, currentConto, inpFile):
    #     print(sys._getframe().f_code.co_name)
    #     matches = ('name', currentConto)
    #     banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
    #     # print(banca)
    #     matches = ('name', currentConto)
    #     auftragskonto_iban = self.myAccountsTable.returnCellsWhere('IBAN', matches)[0]
    #     deubnk_table = self.sql_rm.Table(self.conf.credentials, 'deubnk')
    #     total_transactions = 0
    #     inserted_transactions = 0
    #     not_inserted_transactions = 0
    #     start = None
    #     end = None
    #     if banca == 'DeutscheBank':
    #         table_head = self.check_csv_table_head(inpFile, ';', banca)
    #         if table_head:
    #             table_head.append('id_users')
    #             table_head.append('myconto')
    #             table_head.append('path2inp')
    #             table_head.append('row_no')
    #             # print('ÖÖÖÖÖMMMM', table_head)
    #             # return
    #             # auftragskontoIndx = table_head.index('Auftragskonto')
    #             debitIndx = table_head.index('Debit')
    #             creditIndx = table_head.index('Credit')
    #             buchungstagIndx = table_head.index('Buchungstag')
    #             valutadatumIndx = table_head.index('Valuedate')
    #             verwendungszweckIndx = table_head.index('Verwendungszweck')
    #             ibanIndx = table_head.index('IBAN')
    #             # return
    #             with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
    #                 linereader = csv.reader(csvfile, delimiter=';', quotechar='"')
    #                 for i, row in enumerate(linereader):
    #                     if i < 5 or len(row) < 10:
    #                         continue
    #                     # print('**', row)
    #                     row.append(1)
    #                     row.append(currentConto)
    #                     row.append(inpFile)
    #                     row.append(i)
    #                     # modify value to float
    #                     valdebit = row[debitIndx]
    #                     if valdebit != '':
    #                         if ',' in valdebit:
    #                             valdebit = valdebit.replace(",", "")
    #                         valdebit = float(valdebit)
    #                     else:
    #                         valdebit = 0
    #                     row[debitIndx] = valdebit
    #                     # modify value to float
    #                     valcredit = row[creditIndx]
    #                     if valcredit != '':
    #                         if ',' in valcredit:
    #                             valcredit = valcredit.replace(",", "")
    #                         valcredit = float(valcredit)
    #                     else:
    #                         valcredit = 0
    #                     row[creditIndx] = valcredit
    #                     # modify date format
    #                     if row[buchungstagIndx] == "" or row[valutadatumIndx] == "":
    #                         continue
    #                     buchungstag = self.expensesTableReal.convertDatumFormat4SQL(row[buchungstagIndx])
    #                     row[buchungstagIndx] = buchungstag
    #
    #                     valueDate = self.expensesTableReal.convertDatumFormat4SQL(row[valutadatumIndx])
    #                     row[valutadatumIndx] = valueDate
    #
    #                     # check if already in table
    #                     verwendungszweck = row[verwendungszweckIndx]
    #                     iban = row[ibanIndx]
    #                     if not start:
    #                         start = buchungstag
    #                     else:
    #                         start = min(buchungstag, start)
    #                     if not end:
    #                         end = buchungstag
    #                     else:
    #                         end = max(buchungstag, end)
    #
    #                     matches = [('Buchungstag', str(buchungstag)),
    #                                # ('Auftragskonto', str(auftragskonto)),
    #                                # ('Valutadatum', str(valutadatum)),
    #                                ('Debit', valdebit),
    #                                ('Credit', valcredit),
    #                                ('IBAN', iban),
    #                                ('Verwendungszweck', verwendungszweck)]
    #                     res = deubnk_table.returnCellsWhere('id', matches)
    #                     if res:
    #                         message = 'row\n{}\nalready existing at row id {}...skip'.format(row, str(res))
    #                         not_inserted_transactions += 1
    #                         print(message)
    #                         continue
    #                     else:
    #                         deubnk_table.addNewRow(table_head, row)
    #                         inserted_transactions += 1
    #         print('total_transactions', total_transactions)
    #         print('inserted_transactions', inserted_transactions)
    #         print('not_inserted_transactions', not_inserted_transactions)
    #         # print(start, start)
    #         self.add_row_to_imported_csv(inpFile, currentConto, start, end, total_transactions, inserted_transactions)

    def import_CSV_new(self, currentConto, inpFile):
        print(sys._getframe().f_code.co_name)
        matches = ('name', currentConto)
        banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
        # print(banca)
        table_head, csv_tabel_cheltuieli = self.check_csv_table_head(inpFile, banca)
        file_name = os.path.split(inpFile)[1]
        if banca == 'DeutscheBank':
            bnk_table = self.sql_rm.Table(self.conf.credentials, 'deubnk')
            betragIndx = table_head.index('Debit')
            creditIndx = table_head.index('Credit')
            buchungstagIndx = table_head.index('Buchungstag')
            valutadatumIndx = table_head.index('Valuedate')
            verwendungszweckIndx = table_head.index('Verwendungszweck')
            ibanIndx = table_head.index('IBAN')
        elif banca == 'Stadtsparkasse München':
            bnk_table = self.sql_rm.Table(self.conf.credentials, 'sskm')
            betragIndx = table_head.index('Betrag')
            buchungstagIndx = table_head.index('Buchungstag')
            valutadatumIndx = table_head.index('Valutadatum')
            verwendungszweckIndx = table_head.index('Verwendungszweck')
            ibanIndx = table_head.index('IBAN')
        elif banca == 'N26':
            bnk_table = self.sql_rm.Table(self.conf.credentials, 'n26')
            betragIndx = table_head.index('Amount')
            buchungstagIndx = table_head.index('Buchungstag')
            valutadatumIndx = table_head.index('ValueDate')
            verwendungszweckIndx = table_head.index('PaymentReference')
            ibanIndx = table_head.index('IBAN')

        total_transactions = 0
        inserted_transactions = 0
        not_inserted_transactions = 0
        start = None
        end = None

        if table_head:
            print('#####table_head', table_head)
            table_head.append('id_users')
            table_head.append('myconto')
            table_head.append('path2inp')
            table_head.append('row_no')
            # with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
            #     linereader = csv.reader(csvfile, delimiter=';', quotechar='"')
            #     for i, row in enumerate(linereader):
            #         if i < 5 or len(row) < 10:
            #             continue
            #         # print('**', row)
            #         row.append(1)
            #         row.append(currentConto)
            #         row.append(inpFile)
            #         row.append(i)
            #         # modify value to float
            #         val = row[betragIndx]
            #         if val != '':
            #             if ',' in val:
            #                 val = val.replace(",", "")
            #             val = float(val)
            #         else:
            #             val = 0
            #         row[betragIndx] = val
            #         if banca == 'DeutscheBank':
            #             # modify value to float
            #             valcredit = row[creditIndx]
            #             if valcredit != '':
            #                 if ',' in valcredit:
            #                     valcredit = valcredit.replace(",", "")
            #                 valcredit = float(valcredit)
            #             else:
            #                 valcredit = 0
            #             row[creditIndx] = valcredit
            #         # modify date format
            #         if row[buchungstagIndx] == "" or row[valutadatumIndx] == "":
            #             continue
            #         buchungstag = self.expensesTableReal.convertDatumFormat4SQL(row[buchungstagIndx])
            #         row[buchungstagIndx] = buchungstag
            #
            #         valueDate = self.expensesTableReal.convertDatumFormat4SQL(row[valutadatumIndx])
            #         row[valutadatumIndx] = valueDate
            #
            #         # check if already in table
            #         verwendungszweck = row[verwendungszweckIndx]
            #         iban = row[ibanIndx]
            #         if not start:
            #             start = buchungstag
            #         else:
            #             start = min(buchungstag, start)
            #         if not end:
            #             end = buchungstag
            #         else:
            #             end = max(buchungstag, end)
            #
            #         if banca == 'DeutscheBank':
            #             matches = [('Buchungstag', str(buchungstag)),
            #                        ('Debit', val),
            #                        ('Credit', valcredit),
            #                        ('IBAN', iban),
            #                        ('Verwendungszweck', verwendungszweck)]
            #         elif banca == 'Stadtsparkasse München':
            #             matches = [('Buchungstag', str(buchungstag)),
            #                        ('Betrag', val),
            #                        ('IBAN', iban),
            #                        ('Verwendungszweck', verwendungszweck)]
            #         elif banca == 'N26':
            #             matches = [('Buchungstag', str(buchungstag)),
            #                        ('Amount', val),
            #                        ('IBAN', iban),
            #                        ('PaymentReference', verwendungszweck)]
            #
            #         res = bnk_table.returnCellsWhere('id', matches)
            #         if res:
            #             message = 'row\n{}\nalready existing at row id {}...skip'.format(row, str(res))
            #             not_inserted_transactions += 1
            #             print(message)
            #             continue
            #         else:
            #             bnk_table.addNewRow(table_head, row)
            #             inserted_transactions += 1
            # with open(inpFile, 'r', encoding='unicode_escape', newline='') as csvfile:
            #     linereader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for i, row in enumerate(csv_tabel_cheltuieli):
                print(row)
                total_transactions += 1
                row.append(1)
                row.append(currentConto)
                row.append(file_name)
                row.append(i)
                # modify value to float
                val = row[betragIndx]
                if val != '':
                    if ',' in val and '.' in val:
                        val = val.replace(",", "")
                    elif ',' in val:
                        val = val.replace(",", ".")
                    val = float(val)
                else:
                    val = 0
                row[betragIndx] = val
                if banca == 'DeutscheBank':
                    # modify value to float
                    valcredit = row[creditIndx]
                    if valcredit != '':
                        if ',' in valcredit:
                            valcredit = valcredit.replace(",", "")
                        valcredit = float(valcredit)
                    else:
                        valcredit = 0
                    row[creditIndx] = valcredit
                # modify date format
                if row[valutadatumIndx] == "":
                    row[valutadatumIndx] = None
                else:
                    valueDate = self.expensesTableReal.convertDatumFormat4SQL(row[valutadatumIndx])
                    row[valutadatumIndx] = valueDate

                buchungstag = self.expensesTableReal.convertDatumFormat4SQL(row[buchungstagIndx])
                row[buchungstagIndx] = buchungstag

                # check if already in table
                verwendungszweck = row[verwendungszweckIndx]
                iban = row[ibanIndx]
                if not start:
                    start = buchungstag
                else:
                    start = min(buchungstag, start)
                if not end:
                    end = buchungstag
                else:
                    end = max(buchungstag, end)

                if banca == 'DeutscheBank':
                    matches = [('Buchungstag', str(buchungstag)),
                               ('Debit', val),
                               ('Credit', valcredit),
                               ('IBAN', iban),
                               ('Verwendungszweck', verwendungszweck)]
                elif banca == 'Stadtsparkasse München':
                    matches = [('Buchungstag', str(buchungstag)),
                               ('Betrag', val),
                               ('IBAN', iban),
                               ('Verwendungszweck', verwendungszweck)]
                elif banca == 'N26':
                    matches = [('Buchungstag', str(buchungstag)),
                               ('Amount', val),
                               ('IBAN', iban),
                               ('PaymentReference', verwendungszweck)]

                found_ids = bnk_table.returnCellsWhere('id', matches)
                if found_ids:
                    other_file = False
                    for f_id in found_ids:
                        fl = bnk_table.returnCellsWhere('path2inp', ('id', f_id))[0]
                        # print('++', fl, file_name, fl != file_name)
                        if fl != file_name:
                            other_file = True
                    if other_file:
                        message = 'row {} already existing at row id {}...skip'.format(row, str(found_ids))
                        not_inserted_transactions += 1
                        print(message)
                        continue
                    else:
                        bnk_table.addNewRow(table_head, row)
                        inserted_transactions += 1
                else:
                    print('**table_head', table_head)
                    print('**row', row)
                    print(len(table_head), len(row))
                    bnk_table.addNewRow(table_head, row)
                    inserted_transactions += 1
            print('total_transactions', total_transactions)
            print('inserted_transactions', inserted_transactions)
            print('not_inserted_transactions', not_inserted_transactions)
            # print(start, start)
            self.add_row_to_imported_csv(inpFile, currentConto, start, end, total_transactions, inserted_transactions)

    def remove_intercontotrans(self, payments4Interval):
        new_payments4Interval = []
        category_col_indx = self.expensesTableReal.columnsNames.index('category')
        for row in payments4Interval:
            # print('ßß', row[category_col_indx])
            if row[category_col_indx] == 'intercontotrans':
                continue
            else:
                new_payments4Interval.append(row)
        return new_payments4Interval

    # def prepareTableReal_bkp(self, currentConto, selectedStartDate, selectedEndDate, hideIntercontotrans):
    #     print(sys._getframe().f_code.co_name)
    #     self.defaultFilter = True
    #     self.filterList = []
    #
    #     match1 = ('Buchungstag', (selectedStartDate, selectedEndDate))
    #     matches = [match1]
    #
    #     if currentConto != 'all':
    #         col = 'IBAN'
    #         IBAN = self.myAccountsTable.returnCellsWhere(col, ('name', currentConto))[0]
    #         match2 = ('AuftragsKonto', IBAN)
    #         matches.append(match2)
    #
    #     # print('*********', matches)
    #     payments4Interval = self.expensesTableReal.filterRows(matches)
    #     # print('*****', matches)
    #     # print('*****', type(payments4Interval))
    #     # for i in payments4Interval:
    #     #     print(i)
    #     # print()
    #     if hideIntercontotrans:
    #         payments4Interval = self.remove_intercontotrans(payments4Interval)
    #     # print(len(payments4Interval))
    #     # payments4Interval = self.apply_dates_interval_filter(res)
    #     payments, income = self.split_expenses_income(payments4Interval)
    #     realExpenses = np.atleast_2d(payments)
    #     realIncome = np.atleast_2d(income)
    #
    #     return realExpenses, realIncome

    # def prepareTableReal(self, currentConto, selectedStartDate, selectedEndDate, hideIntercontotrans):
    #     print(sys._getframe().f_code.co_name)
    #     self.defaultFilter = True
    #     self.filterList = []
    #
    #     match1 = ('Buchungstag', (selectedStartDate, selectedEndDate))
    #     matches = [match1]
    #
    #     if currentConto != 'all':
    #         # col = 'IBAN'
    #         # IBAN = self.myAccountsTable.returnCellsWhere(col, ('name', currentConto))[0]
    #         match2 = ('myconto', currentConto)
    #         matches.append(match2)
    #
    #     # print('*********', matches)
    #     payments4Interval = self.expensesTableReal.filterRows(matches)
    #     # print('*****', matches)
    #     # print('*****', type(payments4Interval))
    #     # for i in payments4Interval:
    #     #     print(i)
    #     # print()
    #     if hideIntercontotrans:
    #         payments4Interval = self.remove_intercontotrans(payments4Interval)
    #     # print(len(payments4Interval))
    #     # payments4Interval = self.apply_dates_interval_filter(res)
    #     payments, income = self.split_expenses_income(payments4Interval)
    #     realExpenses = np.atleast_2d(payments)
    #     realIncome = np.atleast_2d(income)
    #
    #     return realExpenses, realIncome

    def get_unplanned_chelt_from_bank_table(self, currentConto, selectedStartDate, selectedEndDate):
        chelt_not_in_plan_vs_real = []
        matches = [('Buchungstag', '>=', selectedStartDate),
                   ('Buchungstag', '<=', selectedEndDate),
                   ('id_plan_vs_real', 'IS', None)]

        table_list = []
        if currentConto != 'all':
            tup = ('myconto', '=', currentConto)
            # matches.append(tup)

            matches.append(tup)
            banca = self.myAccountsTable.returnCellsWhere('banca', ('name', currentConto))[0]
            sql_table_name = bank_sql_table[banca]
            table_list.append(sql_table_name)
        else:
            table_list = list(plan_vs_real_tabHeadDict.keys())

        for sql_table_name in table_list:
            table = mysql_rm.Table(self.conf.credentials, sql_table_name)
            table_head = table.columnsNames
            not_found_in_planned = table.returnRowsQuery(matches)
            tabHeadConversion = plan_vs_real_tabHeadDict[sql_table_name]
            for nf in not_found_in_planned:
                new_row = []
                for col in self.expensesTableReal.columnsNames:
                    if col in table_head:
                        new_row.append(nf[table_head.index(col)])
                    elif col in list(tabHeadConversion.keys()):
                        new_row.append(nf[table_head.index(tabHeadConversion[col])])
                    else:
                        new_row.append(None)
                chelt_not_in_plan_vs_real.append(tuple(new_row))
        return chelt_not_in_plan_vs_real

    def prepareTableReal_new(self, currentConto, selectedStartDate, selectedEndDate, hideIntercontotrans):
        print(sys._getframe().f_code.co_name)
        matches = [('Buchungstag', '>=', selectedStartDate),
                   ('Buchungstag', '<=', selectedEndDate)]

        if hideIntercontotrans:
            tup = ('category', '!=', 'intercontotrans')
            matches.append(tup)
        if currentConto != 'all':
            tup = ('myconto', '=', currentConto)
            matches.append(tup)
        payments4Interval = self.expensesTableReal.returnRowsQuery(matches)

        chelt_not_in_plan_vs_real = self.get_unplanned_chelt_from_bank_table(currentConto, selectedStartDate,
                                                                             selectedEndDate)
        for row in chelt_not_in_plan_vs_real:
            payments4Interval.append(row)

        payments, income = self.split_expenses_income(payments4Interval)
        self.realExpenses = np.atleast_2d(payments)
        self.realIncome = np.atleast_2d(income)

    def split_expenses_income(self, table):
        print(sys._getframe().f_code.co_name)
        indxValue = self.expensesTableReal.columnsNames.index('Betrag')
        payments = []
        income = []
        for row in table:
            if row[indxValue] > 0:
                income.append(row)
            if row[indxValue] <= 0:
                payments.append(row)
        payments = np.atleast_2d(payments)
        income = np.atleast_2d(income)

        return payments, income

    # def compare2plan(self):
    #     expensesTableReal = np.atleast_2d(self.expensesTableReal.returnAllRecordsFromTable())
    #     searchCols = ['name', 'value', 'identification']
    #     cols2write2expensesTableReal = ['name', 'value']
    #
    #     # loop over each table that includes the searchCols
    #     for table in self.dataBase.allAvailableTablesInDatabase:
    #         # self.dataBase.active_table = table
    #         active_table = mysql_rm.Table(self.conf.credentials, table)
    #         check = all(item in list(active_table.columnsProperties.keys()) for item in searchCols)
    #         if check:
    #             # loop over each row in table that includes the searchCols
    #             for row in active_table.returnAllRecordsFromTable():
    #                 print(row)
    #                 for sCol in searchCols:
    #                     v = row[active_table.columnsNames.index(sCol)]
    #                     # if there is a value in col 'identification' create the condition query
    #                     if sCol == 'identification' and v:
    #                         # print(100*'v')
    #                         # print(v)
    #                         v = v.replace("'", '"')
    #                         # print(v)
    #                         # print(100*'v')
    #                         conditions = json.loads(v)
    #                         # print('conditions', conditions)
    #                         print(100 * 'v')
    #                         # continue
    #                         cond = ''
    #                         for key, val in conditions.items():
    #                             print('key', key)
    #                             colNo = self.expensesTableReal.columnsNames.index(key)
    #                             if key == 'Verwendungszweck':
    #                                 colIndx = self.expensesTableReal.columnsNames.index('Verwendungszweck')
    #                                 # print('colIndx', colIndx)
    #                                 # print('expensesTableReal[:, colIndx]', expensesTableReal[:, colIndx])
    #                                 # print('val', val)
    #                                 # indVerwendungszweck = []
    #                                 # for x, item in enumerate(expensesTableReal[:, colIndx]):
    #                                 #     # print('ÄÄ', x, item)
    #                                 #     if val in item:
    #                                 #         indVerwendungszweck.append(x)
    #                                 # print('val', val)
    #                                 indVerwendungszweck = [x for x, item in enumerate(expensesTableReal[:, colIndx]) if
    #                                                        val in item]
    #                             elif key == 'Beguenstigter':
    #                                 colIndx = self.expensesTableReal.columnsNames.index('Beguenstigter')
    #                                 indBeguenstigter = [x for x, item in enumerate(expensesTableReal[:, colIndx]) if
    #                                                     val in item]
    #                                 print('BINGO', val)
    #                                 print('BINGO', indBeguenstigter)
    #                             else:
    #                                 cond += '(expensesTableReal[:, {}] == "{}") & '.format(colNo, val)
    #                         cond = cond[:-2]
    #                         # print(cond)
    #                         # print(50*'#')
    #                         # sys.exit()
    #
    #                         if cond != '':
    #                             print('cond', cond)
    #                             ind = np.where(eval(cond))
    #                             if 'Verwendungszweck' in conditions.keys():
    #                                 newInd = []
    #                                 for ii in ind[0]:
    #                                     if ii in indVerwendungszweck:
    #                                         newInd.append(ii)
    #                                 ind = newInd
    #                             if 'Beguenstigter' in conditions.keys():
    #                                 newInd = []
    #                                 for ii in ind[0]:
    #                                     if ii in indBeguenstigter:
    #                                         newInd.append(ii)
    #                                 ind = newInd
    #                         elif indVerwendungszweck:
    #                             ind = indVerwendungszweck
    #                         elif indBeguenstigter:
    #                             ind = indBeguenstigter
    #                         # interrogate expensesTableReal for rows that fulfill the condition
    #                         # and do a loop over each of them
    #                         print('***ind', ind)
    #                         for rowExp in expensesTableReal[ind]:
    #                             expensesTableRowId = rowExp[self.expensesTableReal.columnsNames.index('id')]
    #                             category = row[active_table.columnsNames.index('category')]
    #                             if table == 'knowntrans':
    #                                 name = row[active_table.columnsNames.index('name')]
    #                                 self.expensesTableReal.changeCellContent('category', table, 'id',
    #                                                                          expensesTableRowId)
    #                                 self.expensesTableReal.changeCellContent('name', name, 'id', expensesTableRowId)
    #                             else:
    #                                 self.expensesTableReal.changeCellContent('category', category, 'id',
    #                                                                          expensesTableRowId)
    #
    #                             for wCol in cols2write2expensesTableReal:
    #                                 val = row[active_table.columnsNames.index(wCol)]
    #                                 self.expensesTableReal.changeCellContent(wCol, val, 'id', expensesTableRowId)
    #                             # sys.exit()

    def get_identification_from_chelt_plan_table(self):
        identification_arr = []
        active_table = mysql_rm.Table(self.conf.credentials, 'chelt_plan')
        for row in active_table.returnAllRecordsFromTable():
            id = row[active_table.columnsNames.index('id')]
            identif = row[active_table.columnsNames.index('identification')]
            if identif:
                identif = identif.replace("'", '"')
                conditions = json.loads(identif)
                tup = (id, conditions, row)
                identification_arr.append(tup)
                # print(tup)
        table_head_chelt_plan = active_table.columnsNames
        return identification_arr, table_head_chelt_plan

    # def get_index_plan_real(self, conditions, expensesTableReal):
    #     cond = ''
    #     indVerwendungszweck = None
    #     indBeguenstigter = None
    #     ind = None
    #     for key, val in conditions.items():
    #         # print('key', key)
    #         colNo = self.expensesTableReal.columnsNames.index(key)
    #         if key == 'Verwendungszweck':
    #             colIndx = self.expensesTableReal.columnsNames.index('Verwendungszweck')
    #             indVerwendungszweck = [x for x, item in enumerate(expensesTableReal[:, colIndx]) if val in item]
    #         elif key == 'Beguenstigter':
    #             colIndx = self.expensesTableReal.columnsNames.index('Beguenstigter')
    #             indBeguenstigter = [x for x, item in enumerate(expensesTableReal[:, colIndx]) if val in item]
    #         else:
    #             cond += '(expensesTableReal[:, {}] == "{}") & '.format(colNo, val)
    #     cond = cond[:-2]
    #     # print('++', cond)
    #     if cond != '':
    #         # print('cond', cond)
    #         ind = np.where(eval(cond))
    #         if 'Verwendungszweck' in conditions.keys():
    #             newInd = []
    #             for ii in ind[0]:
    #                 if ii in indVerwendungszweck:
    #                     newInd.append(ii)
    #             ind = newInd
    #         if 'Beguenstigter' in conditions.keys():
    #             newInd = []
    #             for ii in ind[0]:
    #                 if ii in indBeguenstigter:
    #                     newInd.append(ii)
    #             ind = newInd
    #     elif indVerwendungszweck:
    #         ind = indVerwendungszweck
    #     elif indBeguenstigter:
    #         ind = indBeguenstigter
    #     return ind

    def get_index_plan_real_new(self, table_head, row, bank_table):
        identif = row[table_head.index('identification')]
        identif = identif.replace("'", '"')
        conditions = json.loads(identif)
        # print(conditions)
        matches = []
        for col, search_value in conditions.items():
            # print(col, search_value)
            if col == 'Verwendungszweck' or col == 'Beguenstigter':
                sign = 'LIKE'
            else:
                sign = '='
            tup = (col, sign, search_value)
            matches.append(tup)
        tup = ('Buchungstag', '>', row[table_head.index('valid_from')])
        matches.append(tup)
        if row[table_head.index('valid_to')]:
            tup = ('Buchungstag', '<', row[table_head.index('valid_to')])
            matches.append(tup)
        # print(matches)
        bank_table = mysql_rm.Table(self.conf.credentials, bank_table)
        found_rows = bank_table.returnRowsQuery(matches)
        return found_rows

    def write_cols_in_real_table_new(self, table_head, row, found_rows, bank_table):
        plan_vs_real_table = mysql_rm.Table(self.conf.credentials, 'plan_vs_real')
        sql_bank_table = mysql_rm.Table(self.conf.credentials, bank_table)
        id_ch_pl = row[table_head.index('id')]
        category = row[table_head.index('category')]
        myconto = row[table_head.index('myconto')]
        name = row[table_head.index('name')]
        plannedvalue = row[table_head.index('value')]
        pl_vs_re_thDict = plan_vs_real_tabHeadDict[bank_table]
        for found_row in found_rows:
            cols = ['id_users', 'id_ch_pl', 'category', 'myconto', 'name', 'plannedvalue', 'bank_table']
            vals = [1, id_ch_pl, category, myconto, name, plannedvalue, bank_table]
            # print(found_row)
            id_bank_table = found_row[0]
            cols.append('id_bank_table')
            vals.append(id_bank_table)
            for col_pl_vs_re, col_bnk_table in pl_vs_re_thDict.items():
                val = found_row[sql_bank_table.columnsNames.index(col_bnk_table)]
                # print(col_pl_vs_re, col_bnk_table, val)
                cols.append(col_pl_vs_re)
                vals.append(val)
            matches = [('bank_table', bank_table),
                       ('id_bank_table', id_bank_table),
                       ('id_ch_pl', id_ch_pl)]
            found_ids = plan_vs_real_table.returnCellsWhere('id', matches)
            if found_ids:
                # print('cols', cols)
                # print('vals', vals)
                print('already in table, skipping...', found_row)
            else:
                print('cols', len(cols), cols)
                print('vals', len(vals), vals)
                lastrowid = plan_vs_real_table.addNewRow(cols, vals)
                sql_bank_table.changeCellContent('id_plan_vs_real', lastrowid, 'id', id_bank_table)
        print('FINISH')

    # def write_cols_in_real_table(self, expensesTableReal, ind, active_table, row, cols2write2expensesTableReal):
    #     for rowExp in expensesTableReal[ind]:
    #         expensesTableRowId = rowExp[self.expensesTableReal.columnsNames.index('id')]
    #         category = row[active_table.columnsNames.index('category')]
    #         self.expensesTableReal.changeCellContent('category', category, 'id', expensesTableRowId)
    #         for wCol in cols2write2expensesTableReal:
    #             val = row[active_table.columnsNames.index(wCol)]
    #             self.expensesTableReal.changeCellContent(wCol, val, 'id', expensesTableRowId)

    def find_chelt_plan_rows_in_banks_tables_and_write_to_plan_vs_real_table(self):
        identification_arr, table_head_chelt_plan = self.get_identification_from_chelt_plan_table()
        for id, conditions, row in identification_arr:
            print(id, conditions, row)
            # continue
            currentConto = row[table_head_chelt_plan.index('myconto')]
            matches = ('name', currentConto)
            banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
            sql_bank_table_name = bank_sql_table[banca]
            # print(currentConto, banca, sql_bank_table_name)
            found_rows = self.get_index_plan_real_new(table_head_chelt_plan, row, sql_bank_table_name)
            if not found_rows:
                print('no rows found in bank table')
            self.write_cols_in_real_table_new(table_head_chelt_plan, row, found_rows, sql_bank_table_name)

    def get_rows_from_chelt_plan_that_misses_in_banks(self):
        not_found = []
        identification_arr, table_head_chelt_plan = self.get_identification_from_chelt_plan_table()
        for id, conditions, row in identification_arr:
            currentConto = row[table_head_chelt_plan.index('myconto')]
            matches = ('name', currentConto)
            banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
            sql_bank_table_name = bank_sql_table[banca]
            # print(currentConto, banca, sql_bank_table_name)
            found_rows = self.get_index_plan_real_new(table_head_chelt_plan, row, sql_bank_table_name)
            if not found_rows:
                print(id, conditions, row)
                not_found.append(row)
        return not_found

    def check_1_row_from_chelt_plan(self, row_id):
        chelt_plan_table = mysql_rm.Table(self.conf.credentials, 'chelt_plan')
        table_head_chelt_plan = chelt_plan_table.columnsNames
        match = ('id', row_id)
        row = chelt_plan_table.returnRowsWhere(match)[0]
        currentConto = row[table_head_chelt_plan.index('myconto')]
        matches = ('name', currentConto)
        banca = self.myAccountsTable.returnCellsWhere('banca', matches)[0]
        sql_bank_table_name = bank_sql_table[banca]
        found_rows = self.get_index_plan_real_new(table_head_chelt_plan, row, sql_bank_table_name)
        for rr in found_rows:
            print(rr)

    @property
    def real_table_dates(self):
        buchungs_min_max = {}
        all_contos = list(set(self.imported_csv.returnColumn('banca')))
        for con in all_contos:
            min, max = self.get_buchungstag_interval(con)
            buchungs_min_max[con] = [min, max]
        return buchungs_min_max

    @property
    def banks(self):
        all_banks = list(set(self.myAccountsTable.returnColumn('banca')))
        return all_banks

    @property
    def tot_no_of_expenses(self):
        # allValues = self.expenses[:, self.tableHead.index('value')]
        # if None in allValues:
        #     allValues = allValues[allValues != np.array(None)]
        return self.realExpenses.shape[0]

    @property
    def tot_val_of_expenses(self):
        allValues = self.realExpenses[:, self.table_head.index('Betrag')]
        if None in allValues:
            allValues = allValues[allValues != np.array(None)]
        totalVal = round(sum(allValues.astype(float)), 2)
        return totalVal

    @property
    def table_head(self):
        return self.expensesTableReal.columnsNames

    ##################################################################
    #
    # def tot_no_of_irregular_expenses(self):
    #     indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] != 1)[0]
    #     monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
    #     return monthly.shape[0]
    #
    # def tot_val_of_irregular_expenses(self):
    #     indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] != 1)[0]
    #     monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
    #     if None in monthly:
    #         monthly = monthly[monthly != np.array(None)]
    #     totalMonthly = round(sum(monthly.astype(float)), 2)
    #     return totalMonthly
    #
    # def tot_no_of_monthly_expenses(self):
    #     indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] == 1)[0]
    #     monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
    #     return monthly.shape[0]
    #
    # def tot_val_of_monthly_expenses(self):
    #     indxMonthly = np.where(self.expenses[:, self.tableHead.index('freq')] == 1)[0]
    #     monthly = self.expenses[indxMonthly, self.tableHead.index('value')]
    #     if None in monthly:
    #         monthly = monthly[monthly != np.array(None)]
    #     totalMonthly = round(sum(monthly.astype(float)), 2)
    #     return totalMonthly
    #
    # def tot_no_of_income(self):
    #     allValues = self.income[:, self.tableHead.index('value')]
    #     if None in allValues:
    #         allValues = allValues[allValues != np.array(None)]
    #     return len(allValues)
    #
    # def tot_val_of_income(self):
    #     allValues = self.income[:, self.tableHead.index('value')]
    #     if None in allValues:
    #         allValues = allValues[allValues != np.array(None)]
    #     totalVal = round(sum(allValues.astype(float)), 2)
    #     return totalVal
    #
    # def tot_no_of_expenses_income(self):
    #     allExpenses = self.expenses[:, self.tableHead.index('value')]
    #     allIncome = self.income[:, self.tableHead.index('value')]
    #     tot = len(allExpenses) + len(allIncome)
    #     return tot
    #
    # def tot_val_of_expenses_income(self):
    #     allValues = self.income[:, self.tableHead.index('value')]
    #     if None in allValues:
    #         allValues = allValues[allValues != np.array(None)]
    #     totalIncome = round(sum(allValues.astype(float)), 2)
    #     allValues = self.expenses[:, self.tableHead.index('value')]
    #     if None in allValues:
    #         allValues = allValues[allValues != np.array(None)]
    #     totalExpenses = round(sum(allValues.astype(float)), 2)
    #     return round(totalIncome + totalExpenses, 2)
    #
    # def get_all_sql_vals(self):
    #     # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    #     all_chelt = []
    #     for table in self.dataBase.allAvailableTablesInDatabase:
    #         if table == 'income':
    #             continue
    #         active_table = self.sql_rm.Table(self.conf.credentials, table)
    #         active_table_head = active_table.columnsNames
    #         if 'table' in self.tableHead:
    #             self.tableHead.remove('table')
    #         if 'payDay' in self.tableHead:
    #             self.tableHead.remove('payDay')
    #         check = all(item in active_table_head for item in self.tableHead)
    #         if check:
    #             # vals = active_table.returnColumns(self.tableHead)
    #             vals = active_table.returnAllRecordsFromTable()
    #             for row in vals:
    #                 row = list(row)
    #                 chelt = Cheltuiala(row, active_table.columnsNames)
    #                 chelt.set_table(table)
    #                 all_chelt.append(chelt)
    #     return all_chelt
    #
    # def filter_dates(self, all_chelt, selectedStartDate, selectedEndDate):
    #     # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    #     remaining = []
    #     for chelt in all_chelt:
    #         # print(chelt.table, chelt.name, chelt.id, chelt.pay_day)
    #         payments_in_interval = chelt.calculate_payments_in_interval(selectedStartDate, selectedEndDate)
    #         # print(payments_in_interval)
    #         # if chelt.name == 'Steuererklärung_2022':
    #         #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, payments_in_interval)
    #         if isinstance(payments_in_interval, list):
    #             chelt.payments_for_interval = payments_in_interval
    #             # print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.payments_for_interval)
    #             if chelt.payments_for_interval:
    #                 remaining.append(chelt)
    #     return remaining
    #
    # def filter_conto(self, chelt_list, conto):
    #     # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    #     remaining = []
    #     for ch in chelt_list:
    #         if conto == 'all' and ch.table != 'intercontotrans':
    #             remaining.append(ch)
    #         elif ch.myconto == conto:
    #             remaining.append(ch)
    #
    #     return remaining
    #
    # def prepareTablePlan(self, conto, selectedStartDate, selectedEndDate):
    #     # print('Module: {}, Class: {}, Def: {}, Caller: {}'.format(__name__, __class__, sys._getframe().f_code.co_name, sys._getframe().f_back.f_code.co_name))
    #     print(selectedStartDate, selectedEndDate)
    #     all_chelt = self.get_all_sql_vals()
    #     # for i in all_chelt:
    #     #     print(i.freq)
    #     # all_chelt = self.get_one_time_transactions(all_chelt)
    #
    #     chelt_in_time_interval = self.filter_dates(all_chelt, selectedStartDate, selectedEndDate)
    #     # for chelt in chelt_in_time_interval:
    #     #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.conto, chelt.payments_for_interval)
    #
    #     chelt_after_contofilter = self.filter_conto(chelt_in_time_interval, conto)
    #     # for chelt in chelt_after_contofilter:
    #     #     print(chelt.table, chelt.name, chelt.id, chelt.pay_day, chelt.conto, chelt.payments_for_interval)
    #
    #     self.expenses, self.income = self.split_expenses_income(chelt_after_contofilter)
    #     if self.expenses.shape == (1, 0):
    #         expenses = np.empty((0, len(self.tableHead)))
    #     if self.income.shape == (1, 0):
    #         income = np.empty((0, len(self.tableHead)))
    #
    # def convert_to_display_table(self, tableHead, table, displayTableHead):
    #     # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
    #     newTableData = np.empty([table.shape[0], len(displayTableHead)], dtype=object)
    #     for i, col in enumerate(displayTableHead):
    #         indxCol = tableHead.index(col)
    #         newTableData[:, i] = table[:, indxCol]
    #
    #     return displayTableHead, newTableData
    #
    # def add_one_time_transactions(self, name, value, myconto, pay_day):
    #     cols = ('name', 'value', 'myconto', 'freq', 'pay_day', 'valid_from', 'valid_to', 'auto_ext')
    #     payday = pay_day.day
    #     valid_from = pay_day
    #     valid_to = pay_day
    #     vals = (name, value, myconto, 999, payday, valid_from, valid_to, 0)
    #     self.one_time_transactions_Table.addNewRow(cols, vals)


class CheltPlanVSReal:
    def __init__(self, ini_file, currentConto, selectedStartDate, selectedEndDate, hideintercontotrans):
        # print('Module: {}, Class: {}, Def: {}'.format(__name__, __class__, sys._getframe().f_code.co_name))
        self.ini_file = ini_file
        self.currentConto = currentConto
        self.selectedStartDate = selectedStartDate
        self.selectedEndDate = selectedEndDate

        self.chelt_app = CheltuieliPlanificate(ini_file)
        self.chelt_app.prepareTablePlan(currentConto, selectedStartDate, selectedEndDate, hideintercontotrans)
        # print(50*'8')
        # print(self.chelt_app.tableHead)
        # print(50*'8')
        self.planned_table_head = self.chelt_app.tableHead
        self.app_reale = CheltuieliReale(ini_file)
        self.found_payments_from_planned = None
        self.not_found_payments_from_planned = None

    def find_planned_in_real_expenses_table(self, hideintercontotrans, puffer_days_to_plann=15, ):
        found_payments_from_planned_table_head = list(self.chelt_app.tableHead)
        found_payments_from_planned_table_head.append('real_payment_date')
        found_payments_from_planned_table_head.append('real_payment_value')
        found_payments_from_planned = [tuple(found_payments_from_planned_table_head)]
        not_found_payments_from_planned = [tuple(self.chelt_app.tableHead)]
        self.app_reale.prepareTableReal_new(self.currentConto,
                                            self.selectedStartDate - timedelta(
                                                days=puffer_days_to_plann),
                                            self.selectedEndDate + timedelta(
                                                days=puffer_days_to_plann),
                                            hideintercontotrans)
        # print(20*'realExpenses')
        # print(realExpenses)
        # print(20*'realExpenses')
        real_table_head = self.app_reale.expensesTableReal.columnsNames
        sum_realised = 0
        # sum_values_planned = 0
        self.used_real_expenses_indexes = []
        multiple_row = []
        rows_more_than_one_time = 0
        for row in self.chelt_app.expenses:
            # print('**', row)
            not_found = True
            row_id = row[self.planned_table_head.index('id')]
            category = row[self.planned_table_head.index('category')]
            name = row[self.planned_table_head.index('name')]
            payDay = row[self.planned_table_head.index('payDay')]
            value_planned = row[self.planned_table_head.index('value')]
            # print(category, name, payDay)
            from_date = payDay - timedelta(days=puffer_days_to_plann)
            up_to_date = payDay + timedelta(days=puffer_days_to_plann)
            index = np.where((category == self.app_reale.realExpenses[:, real_table_head.index('category')]) &
                             (name == self.app_reale.realExpenses[:, real_table_head.index('name')])
                             )
            # print('::', index, type(index))
            if self.app_reale.realExpenses[index].shape[0] > 0:
                for ind in index[0]:
                    r = self.app_reale.realExpenses[ind]
                    real_payment_date = r[real_table_head.index('Buchungstag')]
                    real_payment_value = r[real_table_head.index('Betrag')]
                    if from_date < real_payment_date < up_to_date:
                        not_found = False
                        found = list(row)
                        found.append(real_payment_date)
                        found.append(real_payment_value)
                        found_payments_from_planned.append(tuple(found))
                        sum_realised += real_payment_value
                        self.used_real_expenses_indexes.append(int(ind))
                        if row_id in list(set(multiple_row)):
                            rows_more_than_one_time += 1
                        else:
                            multiple_row.append(row_id)
                        # print('\t',found)
                    # print()
            # print(200*'#')
            if not_found:
                # print(row)
                not_found_payments_from_planned.append(tuple(row))
        # print(self.chelt_app.tableHead)
        # print(type())
        # print(100*'*')
        # for i in found_payments_from_planned:
        #     print(i)
        # print(self.app_reale.expensesTableReal.columnsNames)
        # print(self.chelt_app.expenses.shape)
        self.found_payments_from_planned = np.atleast_2d(found_payments_from_planned)
        self.not_found_payments_from_planned = np.atleast_2d(not_found_payments_from_planned)
        # return found_payments_from_planned, not_found_payments_from_planned

    def find_unplanned_real_expenses(self, puffer_days_to_plann=15):
        self.app_reale.prepareTableReal_new(self.currentConto,
                                            self.selectedStartDate - timedelta(
                                                days=puffer_days_to_plann),
                                            self.selectedEndDate + timedelta(
                                                days=puffer_days_to_plann),
                                            False)
        unplanned_real_expenses = [self.app_reale.expensesTableReal.columnsNames]
        # if realExpenses:
        if isinstance(self.app_reale.realExpenses, np.ndarray) and self.app_reale.realExpenses.shape[0] > 0:
            for ii, exp_row in enumerate(self.app_reale.realExpenses):
                # print(ii, type(ii), ii in used_real_expenses_indexes)
                if ii not in self.used_real_expenses_indexes:
                    # continue
                    buchungstag = exp_row[self.app_reale.expensesTableReal.columnsNames.index('Buchungstag')]
                    # print('buchungstag', buchungstag, self.selectedStartDate, self.selectedEndDate)
                    if self.selectedStartDate <= buchungstag <= self.selectedEndDate:
                        # print(type(exp_row), exp_row.shape)
                        # print('ßßßß', ii, exp_row)
                        unplanned_real_expenses.append(list(exp_row))
        unplanned_real_expenses = np.atleast_2d(unplanned_real_expenses)
        return unplanned_real_expenses

    def cheltPlanVsReal(self, puffer_days_to_plann=15):
        found_payments_from_planned_table_head = list(self.chelt_app.tableHead)
        found_payments_from_planned_table_head.append('real_payment_date')
        found_payments_from_planned_table_head.append('real_payment_value')
        found_payments_from_planned = [tuple(found_payments_from_planned_table_head)]
        not_found_payments_from_planned = [tuple(self.chelt_app.tableHead)]
        self.app_reale.prepareTableReal_new(self.currentConto,
                                            self.selectedStartDate - timedelta(
                                                days=puffer_days_to_plann),
                                            self.selectedEndDate + timedelta(
                                                days=puffer_days_to_plann),
                                            False)
        # print(20*'self.chelt_app.expenses')
        # print(self.chelt_app.expenses)
        # print(20*'self.chelt_app.expenses')
        real_table_head = self.app_reale.expensesTableReal.columnsNames
        sum_realised = 0
        # sum_values_planned = 0
        used_real_expenses_indexes = []
        multiple_row = []
        rows_more_than_one_time = 0
        if isinstance(self.chelt_app.expenses, np.ndarray) and self.chelt_app.expenses.shape[0] > 0:
            for row in self.chelt_app.expenses:
                # print('**', row)
                not_found = True
                row_id = row[self.planned_table_head.index('id')]
                category = row[self.planned_table_head.index('category')]
                name = row[self.planned_table_head.index('name')]
                payDay = row[self.planned_table_head.index('payDay')]
                value_planned = row[self.planned_table_head.index('value')]
                print(category, name, payDay)
                from_date = payDay - timedelta(days=puffer_days_to_plann)
                up_to_date = payDay + timedelta(days=puffer_days_to_plann)
                index = np.where((category == self.app_reale.realExpenses[:, real_table_head.index('category')]) &
                                 (name == self.app_reale.realExpenses[:, real_table_head.index('name')])  # &
                                 # (from_date < realExpenses[:, real_table_head.index('Buchungstag')]) &
                                 # (up_to_date > realExpenses[:, real_table_head.index('Buchungstag')])
                                 )
                # print('::', index, type(index))
                if self.app_reale.realExpenses[index].shape[0] > 0:
                    for ind in index[0]:
                        # print('\t', r, type(r))
                        # print('\t', from_date, up_to_date, r[real_table_head.index('Buchungstag')], from_date < r[real_table_head.index('Buchungstag')], up_to_date > r[real_table_head.index('Buchungstag')])
                        # print('\t', r[real_table_head.index('Buchungstag')])
                        r = self.app_reale.realExpenses[ind]
                        real_payment_date = r[real_table_head.index('Buchungstag')]
                        real_payment_value = r[real_table_head.index('Betrag')]
                        if from_date < real_payment_date < up_to_date:
                            not_found = False
                            found = list(row)
                            found.append(real_payment_date)
                            found.append(real_payment_value)
                            found_payments_from_planned.append(tuple(found))
                            # sum_values_planned += value_planned
                            sum_realised += real_payment_value
                            # print('PPPPPP', ind, type(ind), r)
                            used_real_expenses_indexes.append(int(ind))
                            if row_id in list(set(multiple_row)):
                                rows_more_than_one_time += 1
                                # print('multiple_row', multiple_row)
                                # print('AAAAAA', row_id, row)
                            else:
                                multiple_row.append(row_id)
                            # print('\t',found)
                        # print()
                # print(200*'#')
                if not_found:
                    # print(row)
                    not_found_payments_from_planned.append(tuple(row))
        # print(self.chelt_app.tableHead)
        # print(type())
        # print(100*'*')
        # for i in found_payments_from_planned:
        #     print(i)
        # print(self.app_reale.expensesTableReal.columnsNames)
        # print(self.chelt_app.expenses.shape)
        found_payments_from_planned = np.atleast_2d(found_payments_from_planned)
        not_found_payments_from_planned = np.atleast_2d(not_found_payments_from_planned)
        # print(found_payments_from_planned.shape)
        # print(not_found_payments_from_planned.shape)
        self.sum_realised_from_planned_found = sum_realised
        # self.sum_planned_from_planned_found = sum_values_planned
        # print(20*'realExpenses')
        # print(realExpenses)
        # print(20*'realExpenses')

        # print('used_real_expenses_indexes', used_real_expenses_indexes)
        unplanned_real_expenses = [self.app_reale.expensesTableReal.columnsNames]
        # if realExpenses:
        if isinstance(self.app_reale.realExpenses, np.ndarray) and self.app_reale.realExpenses.shape[0] > 0:
            for ii, exp_row in enumerate(self.app_reale.realExpenses):
                # print(ii, type(ii), ii in used_real_expenses_indexes)
                if ii not in used_real_expenses_indexes:
                    # continue
                    buchungstag = exp_row[self.app_reale.expensesTableReal.columnsNames.index('Buchungstag')]
                    # print('buchungstag', buchungstag, self.selectedStartDate, self.selectedEndDate)
                    if self.selectedStartDate <= buchungstag <= self.selectedEndDate:
                        # print(type(exp_row), exp_row.shape)
                        # print('ßßßß', ii, exp_row)
                        unplanned_real_expenses.append(list(exp_row))
        unplanned_real_expenses = np.atleast_2d(unplanned_real_expenses)
        print(type(unplanned_real_expenses), len(unplanned_real_expenses))
        self.no_of_unplanned_real_expenses = unplanned_real_expenses.shape[0] - 1
        self.sum_of_unplanned_real_expenses = sum(
            unplanned_real_expenses[1:, self.app_reale.expensesTableReal.columnsNames.index('Betrag')])
        return found_payments_from_planned, not_found_payments_from_planned, unplanned_real_expenses, rows_more_than_one_time

    @property
    def sum_planned(self):
        sum_planned = sum(self.chelt_app.expenses[:, self.planned_table_head.index('value')])
        return sum_planned

    @property
    def no_of_transactions_planned(self):
        return self.chelt_app.expenses.shape[0]

    @property
    def sum_realised_from_planned_found(self):
        return self._sum_realised

    @sum_realised_from_planned_found.setter
    def sum_realised_from_planned_found(self, real):
        self._sum_realised = real

    @property
    def no_of_unplanned_real_expenses(self):
        return self._no_planned

    @no_of_unplanned_real_expenses.setter
    def no_of_unplanned_real_expenses(self, plan):
        self._no_planned = plan

    @property
    def sum_of_unplanned_real_expenses(self):
        return self._sum_planned

    @sum_of_unplanned_real_expenses.setter
    def sum_of_unplanned_real_expenses(self, plan):
        self._sum_planned = plan

# todo table_head
# todo create a table 4 each bank and a summary table for all banks
# todo CheltPlanVSReal better structure
# todo CheltPlanVSReal summarys
# todo switch between table & tree
