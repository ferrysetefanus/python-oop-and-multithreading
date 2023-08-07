#import abc library untuk mendefinisikan abstract class dan abstract method
from abc import ABC, abstractmethod
#import library gspread untuk ekspor transaction_history ke spreadsheet dan oauth2client untuk autentikasi menggunakan service account
import gspread
from google.oauth2.service_account import Credentials
#import pandas untuk ekspor file excel ke local
import pandas as pd

#membuat abstract base class (ABC)
class SavingsAccount(ABC):
    #mendefinisikan atribut yang akan digunakan
    def __init__(self, account_number, account_holder, balance, interest_rate, password):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
        self.interest_rate = interest_rate
        self.password = password

    #membuat fungsi untuk menambahkan saldo berdasarkan jumlah deposit dan merekam histori transaksi 
    def deposit(self, amount):
        self.balance += amount
        transaction = {
            "Transaction": "Jumlah Penarikan",
            "Amount": f"-{amount}",
            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Account_Number": self.account_number,
            "Account_Name": self.account_holder,
            "Balance": self.balance,
            "Student": "Ferry Setefanus" 
        }
        self.transaction_history.append(transaction)

    #membuat fungsi untuk mengurangi saldo berdasarkan penarikan dan merekam histori transaksi
    def withdraw(self, amount):
        #melakukan pengecekan agar saldo rekening tidak minus setelah dikurangi penarikan
        if amount <= self.balance: 
            self.balance -= amount
            transaction = {
            "Transaction": "Jumlah Deposit",
            "Amount": f"+{amount}",
            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Account_Number": self.account_number,
            "Account_Name": self.account_holder,
            "Balance": self.balance,
            "Student": "Ferry Setefanus"  
        }
            self.transaction_history.append(transaction)
        else:
            print("Penarikan tidak bisa dilakukan karena saldo kurang!")

    #membuat fungsi abstrak agar dapat diturunkan ke class ConventionalSavings dan ShariaSavings dengan perhitungan bunga tersendiri
    @abstractmethod 
    def calculate_interest(self):
        pass

    #membuat fungsi untuk menampilkan informasi akun (account_number, account_holder, balance)
    def display_account_info(self):
        print(f"Nomor Akun: {self.account_number}")
        print(f"Nama Pemilik Akun : {self.account_holder}")
        print(f"Jumlah Saldo : {self.balance}")

#membuat class ConventionalSavings yang merupakan turunan dari SavingsAccount
class ConventionalSavings(SavingsAccount):
    def __init__(self, account_number, account_holder, balance, interest_rate, min_balance, password):
        #memanggil konstruktor dari class SavingsAccount dengan tambahan atribut min_balance
        super().__init__(account_number, account_holder, balance, interest_rate, password)
        self.min_balance = min_balance
        self.transaction_history = [] 

    #override fungsi calculate_interest untuk menghitung bunga bank conventional (saldo * suku bunga)
    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        return interest

#membuat class ShariaSavings yang juga turunan dari class SavingsAccount
class ShariaSavings(SavingsAccount):
    def __init__(self, account_number, account_holder, balance, interest_rate, password):
        #memanggil konstruktor dari class SavingsAccount dengan nilai default interest_rate = 0
        super().__init__(account_number, account_holder, balance, interest_rate, password)
        self.transaction_history = [] 

    #override fungsi calculate_interest untuk menghitung bunga bank syariah (suku bunga 0%)
    def calculate_interest(self):
        return 0
        

#membuat class bank
class Bank:
    #membuat fungsi konstruktor untuk menampung akun yang sudah diregister
    def __init__(self):
        self.accounts = {}

    #membuat fungsi untuk menambahkan akun berdasarkan key (account_number) 
    def register_account(self, account):
        # Memeriksa apakah account_number sudah ada sebelumnya
        if account.account_number in self.accounts:
            print(f"Akun dengan nomor akun: {account.account_number} sudah ada!")
        else:
            # Jika nomor akun belum ada, tambahkan akun ke dalam dictionary accounts = {}
            self.accounts[account.account_number] = account
            print(f"Akun dengan nomor akun:{account.account_number} berhasil diregister!")

    #membuat fungsi untuk login berdasarkan account_number dan password 
    def login(self, account_number, password):
        # cek apakah account_number sudah diregister
        if account_number in self.accounts:
            # ambil account_number dari dictionary account = {}
            account = self.accounts[account_number]
            # melakukan cek apakah password yang diinput sama dengan yang di dictionary account = {}
            if account.password == password:
                return account
            else:
                print("Password salah!")
                return None
        else:
            print("Akun tidak ditemukan!")
            return None

    # membuat fungsi untuk ekspor history_transaksi ke file excel lokal    
    def export_transaction_history(self, account_list, spreadsheet_id, local_file_path):
        all_transactions = []
        sharia_transactions = []
        conventional_transactions = []

        #memasukkan semua transaksi ke all_transactions
        for account in account_list:
            if account.transaction_history:
                all_transactions.extend(account.transaction_history)
                #memisahkan antara transaksi akun sharia dan akun conventional
                if isinstance(account, ShariaSavings):
                    sharia_transactions.extend(account.transaction_history)
                elif isinstance(account, ConventionalSavings):
                    conventional_transactions.extend(account.transaction_history)

        if all_transactions:
            # menambahkan default value (none) kepada key yang tidak memiliki value
            for transaction in all_transactions:
                keys_to_add = set(["Date", "Account_Number", "Account_Name", "Balance", "Student"]) - set(transaction.keys())
                for key in keys_to_add:
                    transaction[key] = None

            # mengkonversi setiap transaksi yang ditampung di lists menjadi pandas dataframe
            df_all = pd.DataFrame(all_transactions, columns=["Date", "Account_Number", "Account_Name", "Balance", "Student"])
            df_sharia = pd.DataFrame(sharia_transactions, columns=["Date", "Account_Number", "Account_Name", "Balance", "Student"])
            df_conventional = pd.DataFrame(conventional_transactions, columns=["Date", "Account_Number", "Account_Name", "Balance", "Student"])

            # melakukan autentikasi dengan service account key dan library gspread
            scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
            credentials = Credentials.from_service_account_file('D:\DS\dibimbing\project python oop\day 2 python\OOP_assignment\google secret.json', scopes=scope)
            gc = gspread.authorize(credentials)

            try:
                # membaca google spreadsheet berdasarkan id (1ojN5IITl16HRFvXFrKuEJQOzpjr5L-vu2dZQ_lKTVJg)
                sh = gc.open_by_key(spreadsheet_id)

                # mendefinisikan sheet yang akan dieskpor berdasarkan jenis transaksinya
                worksheet_all = sh.get_worksheet(0)  
                worksheet_sharia = sh.get_worksheet(1)  
                worksheet_conventional = sh.get_worksheet(2)  

                # melakukan append setiap row dataframe pandas berdasarkan worksheetnya
                worksheet_all.append_rows(df_all.values.tolist())
                worksheet_sharia.append_rows(df_sharia.values.tolist())
                worksheet_conventional.append_rows(df_conventional.values.tolist())

                # ekspor file excel ke lokal
                df_all.to_excel(local_file_path, index=False)

                print(f"All transaction history appended to respective sheets in Google Spreadsheet: {spreadsheet_id}.")
                print(f"All transaction history also saved to local file: {local_file_path}.")
            except gspread.exceptions.SpreadsheetNotFound:
                print(f"Spreadsheet with ID '{spreadsheet_id}' not found.")
        else:
            print("No transaction history to export.")

# membuat instance dari class bank
bank = Bank()


conv_account = ConventionalSavings("C4501", "Benjamin Pavard", 40210, 0.05, 1000, "12345")
sharia_account = ShariaSavings("S9901", "Dayot Upamecano", 78121, 0.0, "12345")
bank.register_account(conv_account)
bank.register_account(sharia_account)


logged_in_account_conv = bank.login("C4501", "12345")
logged_in_account_sharia = bank.login("S9901", "12345")

logged_in_accounts = []

# Contoh deposit dan penarikan untuk akun konvensional
if logged_in_account_conv:
    logged_in_account_conv.deposit(11532)
    logged_in_account_conv.withdraw(9181)
    logged_in_account_conv.display_account_info()
    interest = logged_in_account_conv.calculate_interest()
    print(f"Jumlah bunga diperoleh: {interest}")

    logged_in_accounts.append(logged_in_account_conv)

# Contoh deposit dan penarikan untuk akun syariah
if logged_in_account_sharia:
    logged_in_account_sharia.deposit(19223)
    logged_in_account_sharia.withdraw(24778)
    logged_in_account_sharia.display_account_info()
    interest = logged_in_account_sharia.calculate_interest()
    print(f"Jumlah bunga diperoleh: {interest}")

    logged_in_accounts.append(logged_in_account_sharia)

# Ekspor seluruh data transaksi yang telah berhasil login ke lokal dan google spreadsheet
bank.export_transaction_history(logged_in_accounts, "1ojN5IITl16HRFvXFrKuEJQOzpjr5L-vu2dZQ_lKTVJg", "D:\DS\dibimbing\project python oop\day 2 python\OOP_assignment\history_transaction.xlsx")