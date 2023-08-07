# python-oop-and-multithreading

# Judul Proyek

[Deskripsi singkat proyek]

## Daftar Isi

- [Deskripsi](#deskripsi)
- [Instalasi](#instalasi)
- [Cara Menggunakan](#cara-menggunakan)
- [Contoh Penggunaan](#contoh-penggunaan)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Deskripsi

Assigment python day 2 dari dibimbing.id, case 1 : menggunakan paradigma OOP python untuk membangun sebuah sistem pencatatan transaksi keuangan sederhana, case 2 : pemanfaatan multi threading untuk mengoptimalkan proses reading files untuk mencari kata tertentu pada pdf file yang sudah didownload.

## Cara Menggunakan

case 1 :
- mendaftarkan sebuah akun agar bisa melakukan transaksi menggunakan function register_account()
- lakukan login berdasarkan nomor akun dan password yang sudah didaftarkan
- jalankan transaksi menggunakan function deposit(), withdraw(), display_account_info(), calculate_interest().

## Contoh Penggunaan

```python
conv_account = ConventionalSavings("C4501", "Benjamin Pavard", 40210, 0.05, 1000, "12345")
sharia_account = ShariaSavings("S9901", "Dayot Upamecano", 78121, 0.0, "12345")
bank.register_account(conv_account)
bank.register_account(sharia_account)


logged_in_account_conv = bank.login("C4501", "12345")
logged_in_account_sharia = bank.login("S9901", "12345")

logged_in_accounts = []

if logged_in_account_conv:
    logged_in_account_conv.deposit(11532)
    logged_in_account_conv.withdraw(9181)
    logged_in_account_conv.display_account_info()
    interest = logged_in_account_conv.calculate_interest()
    print(f"Jumlah bunga diperoleh: {interest}")

    logged_in_accounts.append(logged_in_account_conv)

if logged_in_account_sharia:
    logged_in_account_sharia.deposit(19223)
    logged_in_account_sharia.withdraw(24778)
    logged_in_account_sharia.display_account_info()
    interest = logged_in_account_sharia.calculate_interest()
    print(f"Jumlah bunga diperoleh: {interest}")

    logged_in_accounts.append(logged_in_account_sharia)
```


