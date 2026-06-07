from tkinter import *
from tkinter import messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup

from modelki import companies as companies_data
from modelki import parcels as parcels_data
from modelki import employees as employees_data

companies: list = []
parcels: list = []
employees: list = []


class CourierCompany:
    def __init__(self, nazwa: str, rok_zalozenia: int, liczba_pracownikow: int, lokalizacja: str):
        self.nazwa = nazwa
        self.rok_zalozenia = rok_zalozenia
        self.liczba_pracownikow = liczba_pracownikow
        self.lokalizacja = lokalizacja
        self.coordinates = CourierCompany.get_coordinates(self)

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.nazwa)

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


class Parcel:
    def __init__(self, numer_przesylki: str, nadawca: str, odbiorca: str, status: str, firma_kurierska: str,
                 lokalizacja: str):
        self.numer_przesylki = numer_przesylki
        self.nadawca = nadawca
        self.odbiorca = odbiorca
        self.status = status
        self.firma_kurierska = firma_kurierska
        self.lokalizacja = lokalizacja
        self.coordinates = Parcel.get_coordinates(self)

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.numer_przesylki)

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


class Employee:
    def __init__(self, imie: str, nazwisko: str, stanowisko: str, firma_kurierska: str, lokalizacja: str):
        self.imie = imie
        self.nazwisko = nazwisko
        self.stanowisko = stanowisko
        self.firma_kurierska = firma_kurierska
        self.lokalizacja = lokalizacja
        self.coordinates = Employee.get_coordinates(self)

        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1], text=self.imie)

    def get_coordinates(self) -> list:
        url = f"https://pl.wikipedia.org/wiki/{self.lokalizacja}"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response_html = BeautifulSoup(response.text, 'html.parser')
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        return [latitude, longitude]


def login():
    login_value = entry_login.get()
    password_value = entry_password.get()

    if login_value == "Artur" and password_value == "Bruderek":
        ramka_logowanie.grid_forget()

        ramka_firmy.grid(row=0, column=0, padx=10, pady=10, sticky=N)
        ramka_przesylki.grid(row=0, column=1, padx=10, pady=10, sticky=N)
        ramka_pracownicy.grid(row=0, column=2, padx=10, pady=10, sticky=N)
        ramka_wyniki.grid(row=1, column=0, columnspan=3, pady=10)
        ramka_mapa.grid(row=2, column=0, columnspan=3)
    else:
        messagebox.showerror("Błąd", "Niepoprawny login lub hasło")


# funkcje firm

def show_companies() -> None:
    listbox_firmy.delete(0, END)
    for idx, company in enumerate(companies):
        nazwa = company.nazwa
        listbox_firmy.insert(idx, nazwa)


def add_company():
    nazwa = entry_nazwa_firmy.get()
    rok_zalozenia = entry_rok_zalozenia.get()
    liczba_pracownikow = entry_liczba_pracownikow_firmy.get()
    lokalizacja = entry_lokalizacja_firmy.get()

    new_company = CourierCompany(nazwa=nazwa, rok_zalozenia=int(rok_zalozenia),
                                 liczba_pracownikow=int(liczba_pracownikow), lokalizacja=lokalizacja)
    companies.append(new_company)

    entry_nazwa_firmy.delete(0, END)
    entry_rok_zalozenia.delete(0, END)
    entry_liczba_pracownikow_firmy.delete(0, END)
    entry_lokalizacja_firmy.delete(0, END)

    entry_nazwa_firmy.focus()
    show_companies()


def remove_company() -> None:
    i = listbox_firmy.index(ACTIVE)
    companies[i].marker.delete()
    companies.pop(i)
    show_companies()


def show_company_details():
    i = listbox_firmy.index(ACTIVE)

    nazwa = companies[i].nazwa
    rok_zalozenia = companies[i].rok_zalozenia
    liczba_pracownikow = companies[i].liczba_pracownikow
    lokalizacja = companies[i].lokalizacja
    coordinates = companies[i].coordinates

    label_nazwa_firmy_wartosc.config(text=nazwa)
    label_rok_zalozenia_wartosc.config(text=rok_zalozenia)
    label_liczba_pracownikow_firmy_wartosc.config(text=liczba_pracownikow)
    label_lokalizacja_firmy_wartosc.config(text=lokalizacja)

    map_widget.set_position(coordinates[0], coordinates[1])
    map_widget.set_zoom(12)


def edit_company():
    i = listbox_firmy.index(ACTIVE)

    nazwa = companies[i].nazwa
    rok_zalozenia = companies[i].rok_zalozenia
    liczba_pracownikow = companies[i].liczba_pracownikow
    lokalizacja = companies[i].lokalizacja

    entry_nazwa_firmy.insert(0, nazwa)
    entry_rok_zalozenia.insert(0, rok_zalozenia)
    entry_liczba_pracownikow_firmy.insert(0, liczba_pracownikow)
    entry_lokalizacja_firmy.insert(0, lokalizacja)

    button_dodaj_firme.config(text="Zapisz zmiany", command=lambda: update_company(i))


def update_company(i):
    nazwa = entry_nazwa_firmy.get()
    rok_zalozenia = entry_rok_zalozenia.get()
    liczba_pracownikow = entry_liczba_pracownikow_firmy.get()
    lokalizacja = entry_lokalizacja_firmy.get()

    companies[i].nazwa = nazwa
    companies[i].rok_zalozenia = rok_zalozenia
    companies[i].liczba_pracownikow = liczba_pracownikow
    companies[i].lokalizacja = lokalizacja
    companies[i].coordinates = CourierCompany.get_coordinates(companies[i])
    companies[i].marker.delete()
    companies[i].marker = map_widget.set_marker(companies[i].coordinates[0], companies[i].coordinates[1], text=nazwa)

    button_dodaj_firme.config(text="Dodaj firmę", command=add_company)

    entry_nazwa_firmy.delete(0, END)
    entry_rok_zalozenia.delete(0, END)
    entry_liczba_pracownikow_firmy.delete(0, END)
    entry_lokalizacja_firmy.delete(0, END)

    entry_nazwa_firmy.focus()
    show_companies()


# funckja przesylek

def show_parcels() -> None:
    listbox_przesylki.delete(0, END)
    for idx, parcel in enumerate(parcels):
        numer_przesylki = parcel.numer_przesylki
        listbox_przesylki.insert(idx, numer_przesylki)


def add_parcel():
    numer_przesylki = entry_numer_przesylki.get()
    nadawca = entry_nadawca.get()
    odbiorca = entry_odbiorca.get()
    status = entry_status.get()
    firma_kurierska = entry_firma_przesylki.get()
    lokalizacja = entry_lokalizacja_przesylki.get()

    new_parcel = Parcel(numer_przesylki=numer_przesylki, nadawca=nadawca, odbiorca=odbiorca, status=status,
                        firma_kurierska=firma_kurierska, lokalizacja=lokalizacja)
    parcels.append(new_parcel)

    entry_numer_przesylki.delete(0, END)
    entry_nadawca.delete(0, END)
    entry_odbiorca.delete(0, END)
    entry_status.delete(0, END)
    entry_firma_przesylki.delete(0, END)
    entry_lokalizacja_przesylki.delete(0, END)

    entry_numer_przesylki.focus()
    show_parcels()


def remove_parcel() -> None:
    i = listbox_przesylki.index(ACTIVE)
    parcels[i].marker.delete()
    parcels.pop(i)
    show_parcels()


def show_parcel_details():
    i = listbox_przesylki.index(ACTIVE)

    numer_przesylki = parcels[i].numer_przesylki
    nadawca = parcels[i].nadawca
    odbiorca = parcels[i].odbiorca
    status = parcels[i].status
    firma_kurierska = parcels[i].firma_kurierska
    lokalizacja = parcels[i].lokalizacja
    coordinates = parcels[i].coordinates

    label_numer_przesylki_wartosc.config(text=numer_przesylki)
    label_nadawca_wartosc.config(text=nadawca)
    label_odbiorca_wartosc.config(text=odbiorca)
    label_status_wartosc.config(text=status)
    label_firma_przesylki_wartosc.config(text=firma_kurierska)
    label_lokalizacja_przesylki_wartosc.config(text=lokalizacja)

    map_widget.set_position(coordinates[0], coordinates[1])
    map_widget.set_zoom(12)


def edit_parcel():
    i = listbox_przesylki.index(ACTIVE)

    numer_przesylki = parcels[i].numer_przesylki
    nadawca = parcels[i].nadawca
    odbiorca = parcels[i].odbiorca
    status = parcels[i].status
    firma_kurierska = parcels[i].firma_kurierska
    lokalizacja = parcels[i].lokalizacja

    entry_numer_przesylki.insert(0, numer_przesylki)
    entry_nadawca.insert(0, nadawca)
    entry_odbiorca.insert(0, odbiorca)
    entry_status.insert(0, status)
    entry_firma_przesylki.insert(0, firma_kurierska)
    entry_lokalizacja_przesylki.insert(0, lokalizacja)

    button_dodaj_przesylke.config(text="Zapisz zmiany", command=lambda: update_parcel(i))


def update_parcel(i):
    numer_przesylki = entry_numer_przesylki.get()
    nadawca = entry_nadawca.get()
    odbiorca = entry_odbiorca.get()
    status = entry_status.get()
    firma_kurierska = entry_firma_przesylki.get()
    lokalizacja = entry_lokalizacja_przesylki.get()

    parcels[i].numer_przesylki = numer_przesylki
    parcels[i].nadawca = nadawca
    parcels[i].odbiorca = odbiorca
    parcels[i].status = status
    parcels[i].firma_kurierska = firma_kurierska
    parcels[i].lokalizacja = lokalizacja
    parcels[i].coordinates = Parcel.get_coordinates(parcels[i])
    parcels[i].marker.delete()
    parcels[i].marker = map_widget.set_marker(parcels[i].coordinates[0], parcels[i].coordinates[1],
                                              text=numer_przesylki)

    button_dodaj_przesylke.config(text="Dodaj przesyłkę", command=add_parcel)

    entry_numer_przesylki.delete(0, END)
    entry_nadawca.delete(0, END)
    entry_odbiorca.delete(0, END)
    entry_status.delete(0, END)
    entry_firma_przesylki.delete(0, END)
    entry_lokalizacja_przesylki.delete(0, END)

    entry_numer_przesylki.focus()
    show_parcels()


# funckje robotnikow

def show_employees() -> None:
    listbox_pracownicy.delete(0, END)
    for idx, employee in enumerate(employees):
        imie = employee.imie
        nazwisko = employee.nazwisko
        listbox_pracownicy.insert(idx, imie + " " + nazwisko)


def add_employee():
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    stanowisko = entry_stanowisko.get()
    firma_kurierska = entry_firma_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()

    new_employee = Employee(imie=imie, nazwisko=nazwisko, stanowisko=stanowisko, firma_kurierska=firma_kurierska,
                            lokalizacja=lokalizacja)
    employees.append(new_employee)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_stanowisko.delete(0, END)
    entry_firma_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)

    entry_imie.focus()
    show_employees()


def remove_employee() -> None:
    i = listbox_pracownicy.index(ACTIVE)
    employees[i].marker.delete()
    employees.pop(i)
    show_employees()


def show_employee_details():
    i = listbox_pracownicy.index(ACTIVE)

    imie = employees[i].imie
    nazwisko = employees[i].nazwisko
    stanowisko = employees[i].stanowisko
    firma_kurierska = employees[i].firma_kurierska
    lokalizacja = employees[i].lokalizacja
    coordinates = employees[i].coordinates

    label_imie_wartosc.config(text=imie)
    label_nazwisko_wartosc.config(text=nazwisko)
    label_stanowisko_wartosc.config(text=stanowisko)
    label_firma_pracownika_wartosc.config(text=firma_kurierska)
    label_lokalizacja_pracownika_wartosc.config(text=lokalizacja)

    map_widget.set_position(coordinates[0], coordinates[1])
    map_widget.set_zoom(12)


def edit_employee():
    i = listbox_pracownicy.index(ACTIVE)

    imie = employees[i].imie
    nazwisko = employees[i].nazwisko
    stanowisko = employees[i].stanowisko
    firma_kurierska = employees[i].firma_kurierska
    lokalizacja = employees[i].lokalizacja

    entry_imie.insert(0, imie)
    entry_nazwisko.insert(0, nazwisko)
    entry_stanowisko.insert(0, stanowisko)
    entry_firma_pracownika.insert(0, firma_kurierska)
    entry_lokalizacja_pracownika.insert(0, lokalizacja)

    button_dodaj_pracownika.config(text="Zapisz zmiany", command=lambda: update_employee(i))


def update_employee(i):
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    stanowisko = entry_stanowisko.get()
    firma_kurierska = entry_firma_pracownika.get()
    lokalizacja = entry_lokalizacja_pracownika.get()

    employees[i].imie = imie
    employees[i].nazwisko = nazwisko
    employees[i].stanowisko = stanowisko
    employees[i].firma_kurierska = firma_kurierska
    employees[i].lokalizacja = lokalizacja
    employees[i].coordinates = Employee.get_coordinates(employees[i])
    employees[i].marker.delete()
    employees[i].marker = map_widget.set_marker(employees[i].coordinates[0], employees[i].coordinates[1], text=imie)

    button_dodaj_pracownika.config(text="Dodaj pracownika", command=add_employee)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_stanowisko.delete(0, END)
    entry_firma_pracownika.delete(0, END)
    entry_lokalizacja_pracownika.delete(0, END)

    entry_imie.focus()
    show_employees()


# filtracja nowaa

def hide_all_markers():
    for company in companies:
        company.marker.delete()

    for parcel in parcels:
        parcel.marker.delete()

    for employee in employees:
        employee.marker.delete()


def show_all_markers():
    hide_all_markers()

    for company in companies:
        company.marker = map_widget.set_marker(
            company.coordinates[0],
            company.coordinates[1],
            text=company.nazwa
        )

    for parcel in parcels:
        parcel.marker = map_widget.set_marker(
            parcel.coordinates[0],
            parcel.coordinates[1],
            text=parcel.numer_przesylki
        )

    for employee in employees:
        employee.marker = map_widget.set_marker(
            employee.coordinates[0],
            employee.coordinates[1],
            text=employee.imie
        )


def show_only_company_markers():
    hide_all_markers()

    for company in companies:
        company.marker = map_widget.set_marker(
            company.coordinates[0],
            company.coordinates[1],
            text=company.nazwa
        )


# wyszukiwanie po firmie


def show_company_parcels():
    listbox_wyniki.delete(0, END)
    company_name = entry_wyszukaj_firme.get()

    hide_all_markers()

    for idx, parcel in enumerate(parcels):
        firma_kurierska = parcel.firma_kurierska

        if firma_kurierska == company_name:
            numer_przesylki = parcel.numer_przesylki
            status = parcel.status

            listbox_wyniki.insert(idx, numer_przesylki + " - " + status)

            parcel.marker = map_widget.set_marker(
                parcel.coordinates[0],
                parcel.coordinates[1],
                text=parcel.numer_przesylki
            )


def show_company_employees():
    listbox_wyniki.delete(0, END)
    company_name = entry_wyszukaj_firme.get()

    hide_all_markers()

    for idx, employee in enumerate(employees):
        firma_kurierska = employee.firma_kurierska

        if firma_kurierska == company_name:
            imie = employee.imie
            nazwisko = employee.nazwisko
            stanowisko = employee.stanowisko

            listbox_wyniki.insert(idx, imie + " " + nazwisko + " - " + stanowisko)

            employee.marker = map_widget.set_marker(
                employee.coordinates[0],
                employee.coordinates[1],
                text=employee.imie
            )


root = Tk()

root.title("Projekt firm kurierskich")
root.geometry("1300x900")

# FRAME
ramka_logowanie = Frame(root)
ramka_firmy = Frame(root)
ramka_przesylki = Frame(root)
ramka_pracownicy = Frame(root)
ramka_wyniki = Frame(root)
ramka_mapa = Frame(root)

# logowanie

ramka_logowanie.grid(row=0, column=0, padx=500, pady=250)

label_logowanie = Label(ramka_logowanie, text="Logowanie")
label_login = Label(ramka_logowanie, text="Login:")
label_password = Label(ramka_logowanie, text="Hasło:")

entry_login = Entry(ramka_logowanie)
entry_password = Entry(ramka_logowanie)

button_login = Button(ramka_logowanie, text="Zaloguj", command=login)

label_logowanie.grid(row=0, column=0, columnspan=2)
label_login.grid(row=1, column=0, sticky=W)
entry_login.grid(row=1, column=1)
label_password.grid(row=2, column=0, sticky=W)
entry_password.grid(row=2, column=1)
button_login.grid(row=3, column=0, columnspan=2)

# firmy


label_firmy = Label(ramka_firmy, text="Firmy kurierskie")
listbox_firmy = Listbox(ramka_firmy, width=30)

button_pokaz_firme = Button(ramka_firmy, text="Pokaż szczegóły", command=show_company_details)
button_usun_firme = Button(ramka_firmy, text="Usuń", command=remove_company)
button_edytuj_firme = Button(ramka_firmy, text="Edytuj", command=edit_company)

label_nazwa_firmy = Label(ramka_firmy, text="Nazwa:")
label_rok_zalozenia = Label(ramka_firmy, text="Rok założenia:")
label_liczba_pracownikow_firmy = Label(ramka_firmy, text="Liczba pracowników:")
label_lokalizacja_firmy = Label(ramka_firmy, text="Lokalizacja:")

entry_nazwa_firmy = Entry(ramka_firmy)
entry_rok_zalozenia = Entry(ramka_firmy)
entry_liczba_pracownikow_firmy = Entry(ramka_firmy)
entry_lokalizacja_firmy = Entry(ramka_firmy)

button_dodaj_firme = Button(ramka_firmy, text="Dodaj firmę", command=add_company)

label_szczegoly_firmy = Label(ramka_firmy, text="Szczegóły firmy")

label_nazwa_firmy_szczegoly = Label(ramka_firmy, text="Nazwa firmy")
label_nazwa_firmy_wartosc = Label(ramka_firmy, text="...")
label_rok_zalozenia_szczegoly = Label(ramka_firmy, text="Rok założenia")
label_rok_zalozenia_wartosc = Label(ramka_firmy, text="...")
label_liczba_pracownikow_firmy_szczegoly = Label(ramka_firmy, text="Liczba pracowników")
label_liczba_pracownikow_firmy_wartosc = Label(ramka_firmy, text="...")
label_lokalizacja_firmy_szczegoly = Label(ramka_firmy, text="Lokalizacja")
label_lokalizacja_firmy_wartosc = Label(ramka_firmy, text="...")

label_firmy.grid(row=0, column=0, columnspan=3)
listbox_firmy.grid(row=1, column=0, columnspan=3)
button_pokaz_firme.grid(row=2, column=0)
button_usun_firme.grid(row=2, column=1)
button_edytuj_firme.grid(row=2, column=2)

label_nazwa_firmy.grid(row=3, column=0, sticky=W)
entry_nazwa_firmy.grid(row=3, column=1)
label_rok_zalozenia.grid(row=4, column=0, sticky=W)
entry_rok_zalozenia.grid(row=4, column=1)
label_liczba_pracownikow_firmy.grid(row=5, column=0, sticky=W)
entry_liczba_pracownikow_firmy.grid(row=5, column=1)
label_lokalizacja_firmy.grid(row=6, column=0, sticky=W)
entry_lokalizacja_firmy.grid(row=6, column=1)
button_dodaj_firme.grid(row=7, column=0, columnspan=2)

label_nazwa_firmy_szczegoly.grid(row=9, column=0, sticky=W)
label_nazwa_firmy_wartosc.grid(row=9, column=1, sticky=W)
label_rok_zalozenia_szczegoly.grid(row=10, column=0, sticky=W)
label_rok_zalozenia_wartosc.grid(row=10, column=1, sticky=W)
label_liczba_pracownikow_firmy_szczegoly.grid(row=11, column=0, sticky=W)
label_liczba_pracownikow_firmy_wartosc.grid(row=11, column=1, sticky=W)
label_lokalizacja_firmy_szczegoly.grid(row=12, column=0, sticky=W)
label_lokalizacja_firmy_wartosc.grid(row=12, column=1, sticky=W)

# przesylki


label_przesylki = Label(ramka_przesylki, text="Przesyłki")
listbox_przesylki = Listbox(ramka_przesylki, width=30)

button_pokaz_przesylke = Button(ramka_przesylki, text="Pokaż szczegóły", command=show_parcel_details)
button_usun_przesylke = Button(ramka_przesylki, text="Usuń", command=remove_parcel)
button_edytuj_przesylke = Button(ramka_przesylki, text="Edytuj", command=edit_parcel)

label_numer_przesylki = Label(ramka_przesylki, text="Numer:")
label_nadawca = Label(ramka_przesylki, text="Nadawca:")
label_odbiorca = Label(ramka_przesylki, text="Odbiorca:")
label_status = Label(ramka_przesylki, text="Status:")
label_firma_przesylki = Label(ramka_przesylki, text="Firma:")
label_lokalizacja_przesylki = Label(ramka_przesylki, text="Lokalizacja:")

entry_numer_przesylki = Entry(ramka_przesylki)
entry_nadawca = Entry(ramka_przesylki)
entry_odbiorca = Entry(ramka_przesylki)
entry_status = Entry(ramka_przesylki)
entry_firma_przesylki = Entry(ramka_przesylki)
entry_lokalizacja_przesylki = Entry(ramka_przesylki)

button_dodaj_przesylke = Button(ramka_przesylki, text="Dodaj przesyłkę", command=add_parcel)

label_szczegoly_przesylki = Label(ramka_przesylki, text="Szczegóły przesyłki")

label_numer_przesylki_szczegoly = Label(ramka_przesylki, text="Numer:")
label_numer_przesylki_wartosc = Label(ramka_przesylki, text="...")
label_nadawca_szczegoly = Label(ramka_przesylki, text="Nadawca:")
label_nadawca_wartosc = Label(ramka_przesylki, text="...")
label_odbiorca_szczegoly = Label(ramka_przesylki, text="Odbiorca:")
label_odbiorca_wartosc = Label(ramka_przesylki, text="...")
label_status_szczegoly = Label(ramka_przesylki, text="Status:")
label_status_wartosc = Label(ramka_przesylki, text="...")
label_firma_przesylki_szczegoly = Label(ramka_przesylki, text="Firma:")
label_firma_przesylki_wartosc = Label(ramka_przesylki, text="...")
label_lokalizacja_przesylki_szczegoly = Label(ramka_przesylki, text="Lokalizacja:")
label_lokalizacja_przesylki_wartosc = Label(ramka_przesylki, text="...")

label_przesylki.grid(row=0, column=0, columnspan=3)
listbox_przesylki.grid(row=1, column=0, columnspan=3)
button_pokaz_przesylke.grid(row=2, column=0)
button_usun_przesylke.grid(row=2, column=1)
button_edytuj_przesylke.grid(row=2, column=2)

label_numer_przesylki.grid(row=3, column=0, sticky=W)
entry_numer_przesylki.grid(row=3, column=1)
label_nadawca.grid(row=4, column=0, sticky=W)
entry_nadawca.grid(row=4, column=1)
label_odbiorca.grid(row=5, column=0, sticky=W)
entry_odbiorca.grid(row=5, column=1)
label_status.grid(row=6, column=0, sticky=W)
entry_status.grid(row=6, column=1)
label_firma_przesylki.grid(row=7, column=0, sticky=W)
entry_firma_przesylki.grid(row=7, column=1)
label_lokalizacja_przesylki.grid(row=8, column=0, sticky=W)
entry_lokalizacja_przesylki.grid(row=8, column=1)
button_dodaj_przesylke.grid(row=9, column=0, columnspan=2)

label_szczegoly_przesylki.grid(row=10, column=0, sticky=W)
label_numer_przesylki_szczegoly.grid(row=11, column=0, sticky=W)
label_numer_przesylki_wartosc.grid(row=11, column=1, sticky=W)
label_nadawca_szczegoly.grid(row=12, column=0, sticky=W)
label_nadawca_wartosc.grid(row=12, column=1, sticky=W)
label_odbiorca_szczegoly.grid(row=13, column=0, sticky=W)
label_odbiorca_wartosc.grid(row=13, column=1, sticky=W)
label_status_szczegoly.grid(row=14, column=0, sticky=W)
label_status_wartosc.grid(row=14, column=1, sticky=W)
label_firma_przesylki_szczegoly.grid(row=15, column=0, sticky=W)
label_firma_przesylki_wartosc.grid(row=15, column=1, sticky=W)
label_lokalizacja_przesylki_szczegoly.grid(row=16, column=0, sticky=W)
label_lokalizacja_przesylki_wartosc.grid(row=16, column=1, sticky=W)

# pracownik


label_pracownicy = Label(ramka_pracownicy, text="Pracownicy")
listbox_pracownicy = Listbox(ramka_pracownicy, width=30)

button_pokaz_pracownika = Button(ramka_pracownicy, text="Pokaż szczegóły", command=show_employee_details)
button_usun_pracownika = Button(ramka_pracownicy, text="Usuń", command=remove_employee)
button_edytuj_pracownika = Button(ramka_pracownicy, text="Edytuj", command=edit_employee)

label_imie = Label(ramka_pracownicy, text="Imię:")
label_nazwisko = Label(ramka_pracownicy, text="Nazwisko:")
label_stanowisko = Label(ramka_pracownicy, text="Stanowisko:")
label_firma_pracownika = Label(ramka_pracownicy, text="Firma:")
label_lokalizacja_pracownika = Label(ramka_pracownicy, text="Lokalizacja:")

entry_imie = Entry(ramka_pracownicy)
entry_nazwisko = Entry(ramka_pracownicy)
entry_stanowisko = Entry(ramka_pracownicy)
entry_firma_pracownika = Entry(ramka_pracownicy)
entry_lokalizacja_pracownika = Entry(ramka_pracownicy)

button_dodaj_pracownika = Button(ramka_pracownicy, text="Dodaj pracownika", command=add_employee)

label_szczegoly_pracownika = Label(ramka_pracownicy, text="Szczegóły pracownika")
label_imie_szczegoly = Label(ramka_pracownicy, text="Imię:")
label_imie_wartosc = Label(ramka_pracownicy, text="...")
label_nazwisko_szczegoly = Label(ramka_pracownicy, text="Nazwisko:")
label_nazwisko_wartosc = Label(ramka_pracownicy, text="...")
label_stanowisko_szczegoly = Label(ramka_pracownicy, text="Stanowisko:")
label_stanowisko_wartosc = Label(ramka_pracownicy, text="...")
label_firma_pracownika_szczegoly = Label(ramka_pracownicy, text="Firma:")
label_firma_pracownika_wartosc = Label(ramka_pracownicy, text="...")
label_lokalizacja_pracownika_szczegoly = Label(ramka_pracownicy, text="Lokalizacja:")
label_lokalizacja_pracownika_wartosc = Label(ramka_pracownicy, text="...")

label_pracownicy.grid(row=0, column=0, columnspan=3)
listbox_pracownicy.grid(row=1, column=0, columnspan=3)
button_pokaz_pracownika.grid(row=2, column=0)
button_usun_pracownika.grid(row=2, column=1)
button_edytuj_pracownika.grid(row=2, column=2)

label_imie.grid(row=3, column=0, sticky=W)
entry_imie.grid(row=3, column=1)
label_nazwisko.grid(row=4, column=0, sticky=W)
entry_nazwisko.grid(row=4, column=1)
label_stanowisko.grid(row=5, column=0, sticky=W)
entry_stanowisko.grid(row=5, column=1)
label_firma_pracownika.grid(row=6, column=0, sticky=W)
entry_firma_pracownika.grid(row=6, column=1)
label_lokalizacja_pracownika.grid(row=7, column=0, sticky=W)
entry_lokalizacja_pracownika.grid(row=7, column=1)
button_dodaj_pracownika.grid(row=8, column=0, columnspan=2)

label_szczegoly_pracownika.grid(row=9, column=0, sticky=W)

label_imie_szczegoly.grid(row=10, column=0, sticky=W)
label_imie_wartosc.grid(row=10, column=1, sticky=W)
label_nazwisko_szczegoly.grid(row=11, column=0, sticky=W)
label_nazwisko_wartosc.grid(row=11, column=1, sticky=W)
label_stanowisko_szczegoly.grid(row=12, column=0, sticky=W)
label_stanowisko_wartosc.grid(row=12, column=1, sticky=W)
label_firma_pracownika_szczegoly.grid(row=13, column=0, sticky=W)
label_firma_pracownika_wartosc.grid(row=13, column=1, sticky=W)
label_lokalizacja_pracownika_szczegoly.grid(row=14, column=0, sticky=W)
label_lokalizacja_pracownika_wartosc.grid(row=14, column=1, sticky=W)

# wybiernaie po naziwe


label_wyszukaj_firme = Label(ramka_wyniki, text="Nazwa firmy:")
entry_wyszukaj_firme = Entry(ramka_wyniki)
button_firmy_mapa = Button(ramka_wyniki, text="Pokaż tylko firmy", command=show_only_company_markers)
button_przesylki_firmy = Button(ramka_wyniki, text="Pokaż przesyłki firmy", command=show_company_parcels)
button_pracownicy_firmy = Button(ramka_wyniki, text="Pokaż pracowników firmy", command=show_company_employees)
button_pokaz_wszystko = Button(ramka_wyniki, text="Pokaż wszystko", command=show_all_markers)
listbox_wyniki = Listbox(ramka_wyniki, width=60, height=7)

label_wyszukaj_firme.grid(row=0, column=0)
entry_wyszukaj_firme.grid(row=0, column=1)

button_firmy_mapa.grid(row=0, column=2)
button_przesylki_firmy.grid(row=0, column=3)
button_pracownicy_firmy.grid(row=0, column=4)
button_pokaz_wszystko.grid(row=0, column=5)

listbox_wyniki.grid(row=1, column=0, columnspan=6)
# mapa


map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1300, height=350, corner_radius=4)
map_widget.set_zoom(6)
map_widget.set_position(52.2, 21.0)

map_widget.grid(row=0, column=0)

# dane wjsciowe


for company in companies_data:
    new_company = CourierCompany(
        nazwa=company["nazwa"],
        rok_zalozenia=company["rok_zalozenia"],
        liczba_pracownikow=company["liczba_pracownikow"],
        lokalizacja=company["lokalizacja"]
    )

    companies.append(new_company)

show_companies()

for parcel in parcels_data:
    new_parcel = Parcel(
        numer_przesylki=parcel["numer_przesylki"],
        nadawca=parcel["nadawca"],
        odbiorca=parcel["odbiorca"],
        status=parcel["status"],
        firma_kurierska=parcel["firma_kurierska"],
        lokalizacja=parcel["lokalizacja"]
    )

    parcels.append(new_parcel)

show_parcels()

for employee in employees_data:
    new_employee = Employee(
        imie=employee["imie"],
        nazwisko=employee["nazwisko"],
        stanowisko=employee["stanowisko"],
        firma_kurierska=employee["firma_kurierska"],
        lokalizacja=employee["lokalizacja"]
    )

    employees.append(new_employee)

show_employees()

root.mainloop()
