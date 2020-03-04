import requests
import pandas as pd
import datetime
import numpy as np

from bs4 import BeautifulSoup


def prepare_column(my_dict, col_name):
    my_column = []
    for i in my_dict:
        my_column.append(my_dict[i][col_name])
    return my_column


def make_clickable(url):
    """Funkcja pozwalająca na wyświetlenie obiektu dataframe 
        z linkiem do strony z ofertą"""

    return '<a target="_blank" href="{}">{}</a>'.format(url, "Link")


def search_all_sites():
    # lista cen mieszkań
    oferts_dict = {}

    # 1 - strona Olx
    basic_source = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/"

    # lista która będzie zawierać wszystkie strony
    list_of_sources = [basic_source]
    list_of_olx_links = []
    list_of_otodom_links = []

    source = requests.get(
        "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/wroclaw/"
    ).text
    soup = BeautifulSoup(source, "lxml")

    # klasa fieldset z atrybutem fleft przechowuje ilość stron
    number_of_pages = soup.find("fieldset", class_="fleft")

    # w podklasie input (są dwie) znajduje się ilość stron
    number_of_paages = number_of_pages.find_all("input")
    # print(number_of_paages) #pomocniczy print

    # odnosimy się do drugiej klasy input, następnie do jej atrybutu
    total_pages = int(number_of_paages[1]["class"][1].replace("}", ""))

    # tworzenie listy zawierającej adresy wszystkich stron
    for page_count in range(2, total_pages):
        list_of_sources.append(basic_source + "?page=" + str(page_count))
    # print(list_of_sources) #pomocniczy print

    for sources in list_of_sources:
        sourceE = requests.get(sources).text
        soupp = BeautifulSoup(sourceE, "lxml")

        for div in soupp.find_all("h3", class_="lheight22 margintop5"):
            link = div.a["href"]
            if "olx" in link:
                list_of_olx_links.append(link)
            elif "otodom" in link:
                list_of_otodom_links.append(link)
    return list_of_olx_links, list_of_otodom_links


def olx_scraper(list_of_olx_links):
    oferts_dict = {}
    for link in list_of_olx_links:
        page = requests.get(link).text
        ofert_soup = BeautifulSoup(page, "lxml")
        features_dict = {}
        try:
            price = ofert_soup.find("div", id="offeractions").strong.text

            titlebox = ofert_soup.find("div", class_="offer-titlebox")
            title = titlebox.h1.text.strip()

            titlebox_details = titlebox.find("div", class_="offer-titlebox__details")
            location = titlebox_details.strong.text.strip()
            id_number = titlebox_details.small.text.replace(
                "ID ogłoszenia: ", ""
            ).strip()
            date = titlebox_details.em.text.split(",")[1].strip()

            months_list = [
                " stycz",
                " lut",
                " mar",
                " kwie",
                " maj",
                " czerw",
                " lip",
                " sierp",
                " wrze",
                " październik",
                " listopad",
                " grud",
            ]

            for month in months_list:
                if month in date:
                    change = "." + str(months_list.index(month) + 1) + "."
                    date = date.split(" ")[0] + change + date.split(" ")[2]
                    break

            text = ofert_soup.find("div", id="textContent").text.strip()
            list_of_appliances = ["zmywark", "wind", "balkon"]
            list_of_appliances_names = ["dishwasher", "elevator", "balcony"]

            for i in list_of_appliances:
                if i in text:
                    features_dict[
                        list_of_appliances_names[list_of_appliances.index(i)]
                    ] = 1
                else:
                    features_dict[
                        list_of_appliances_names[list_of_appliances.index(i)]
                    ] = 0

            popularity = ofert_soup.find("div", id="offerbottombar").strong.text
            features_dict["popularity"] = popularity

            table = ofert_soup.find(
                "table", class_="details fixed marginbott20 margintop5 full"
            ).find_all("table", class_="item")
            table_dict = {
                "Oferta od": "dealer",
                "Poziom": "floor",
                "Umeblowane": "furnished",
                "Rodzaj zabudowy": "building",
                "Powierzchnia": "area",
                "Liczba pokoi": "rooms",
                "Czynsz (dodatkowo)": "rent",
            }

            features_dict["dealer"] = None
            features_dict["floor"] = None
            features_dict["furnished"] = None
            features_dict["building"] = None
            features_dict["area"] = None
            features_dict["rooms"] = None
            features_dict["rent"] = 0

            for i in table:
                table_dict_key = (
                    i.find("th").text.replace("\n", "").replace("\t", "").strip()
                )
                if table_dict_key in table_dict.keys():
                    var_key = table_dict[table_dict_key]
                    features_dict[var_key] = (
                        i.find("td", class_="value")
                        .text.replace("\n", "")
                        .replace("\t", "")
                    )

            time = date.split(".")
            currentDT = datetime.datetime.now()
            time = (
                (int(currentDT.day) - int(time[0]))
                + (int(currentDT.month) - int(time[1])) * 30
                + (int(currentDT.year) - int(time[2])) * 365
            )
            if time > 30:
                time = "+30"

            features_dict["price"] = price
            features_dict["title"] = title
            features_dict["location"] = location
            features_dict["id_number"] = id_number
            features_dict["date"] = date
            features_dict["time"] = time

            oferts_dict[link] = features_dict

        except AttributeError:
            pass
    return oferts_dict


def otodom_scraper(list_of_otodom_links):
    oferts_dict = {}
    for link in list_of_otodom_links:
        page = requests.get(link).text
        ofert_soup = BeautifulSoup(page, "lxml")
        features_dict = {}
        try:
            header = ofert_soup.find("header", class_="css-jcl595")
            price = header.find("div", class_="css-1vr19r7").text.strip()
            title = header.find("h1", class_="css-18igut2").text.strip()
            location = (
                "Wrocław"
                + header.find("div", class_=" css-0").text.strip().split("Wrocław")[1]
            )

            table_dict = {}
            for j in [
                i.text
                for i in ofert_soup.find("div", class_="css-1ci0qpi").find_all("li")
            ]:
                key, value = j.split(":")
                table_dict[key] = value

            features_dict["floor"] = None
            features_dict["building"] = None
            features_dict["area"] = None
            features_dict["rooms"] = None
            features_dict["rent"] = 0
            for i in table_dict.keys():
                if i.lower() == "piętro":
                    features_dict["floor"] = table_dict[i]
                if i.lower() == "rodzaj zabudowy":
                    features_dict["building"] = table_dict[i]
                if i.lower() == "powierzchnia":
                    features_dict["area"] = table_dict[i]
                if i.lower() == "liczba pokoi":
                    features_dict["rooms"] = table_dict[i]
                if i.lower() == "czynsz - dodatkowo":
                    features_dict["rent"] = table_dict[i]

            text = str(
                [
                    i.text.strip()
                    for i in ofert_soup.find("div", class_="css-18kacof-Te").find_all(
                        "p"
                    )
                ]
            )
            list_of_appliances = ["zmywark", "wind", "balkon"]
            list_of_appliances_names = ["dishwasher", "elevator", "balcony"]

            for i in list_of_appliances:
                if i in text:
                    features_dict[
                        list_of_appliances_names[list_of_appliances.index(i)]
                    ] = 1
                else:
                    features_dict[
                        list_of_appliances_names[list_of_appliances.index(i)]
                    ] = 0

            id_number = "O" + ofert_soup.find("div", class_="css-kos6vh").text.split(
                "Nr"
            )[1].replace(" oferty w Otodom: ", "")

            dealer = ofert_soup.find("div", class_="css-7hnk9y").text

            time = (
                ofert_soup.find("div", class_="css-lh1bxu")
                .text.split("Data")[1]
                .replace("dodania: ", "")
                .strip()
            )

            currentDT = datetime.datetime.now()
            if "in" in time:
                date = (
                    str(currentDT.day)
                    + "."
                    + str(currentDT.month)
                    + "."
                    + str(currentDT.year)
                )
                time = 0
            elif "a month" in time:
                date = currentDT - datetime.timedelta(30)
                date = str(date.day) + "." + str(date.month) + "." + str(date.year)
                time = "+30"
            elif "months" in time:
                date = currentDT - datetime.timedelta(30 * int(time.split(" ")[0]))
                date = str(date.day) + "." + str(date.month) + "." + str(date.year)
                time = "+30"
            elif "a day" in time:
                date = currentDT - datetime.timedelta(1)
                date = str(date.day) + "." + str(date.month) + "." + str(date.year)
                time = 1
            elif "day" in time:
                date = currentDT - datetime.timedelta(int(time.split(" ")[0]))
                date = str(date.day) + "." + str(date.month) + "." + str(date.year)
                time = int(time.split(" ")[0])
            else:
                date = None
                time = "+30"

            features_dict["price"] = price
            features_dict["title"] = title
            features_dict["location"] = location
            features_dict["id_number"] = id_number
            features_dict["popularity"] = None
            features_dict["furnished"] = None
            features_dict["dealer"] = dealer
            features_dict["time"] = time
            features_dict["date"] = date

            oferts_dict[link] = features_dict
        except AttributeError:
            pass

    return oferts_dict


def prepare_data_df(oferts_dict):
    my_columns = [
        "Price",
        "Rent",
        "Area",
        "Rooms",
        "Floor",
        "Location",
        "Dealer",
        "Building",
        "Furnished",
        "Dishwasher",
        "Elevator",
        "Balcony",
        "Popularity",
        "Time",
        "Date",
        "Title",
        "Id_number",
        "Link",
    ]
    data = pd.DataFrame(columns=my_columns)

    for i in my_columns[:-1]:
        col = prepare_column(oferts_dict, i.lower())
        data[i] = col
    data["Link"] = oferts_dict.keys()
    data.drop_duplicates(subset="Id_number", keep="first", inplace=True)
    return data


def fill_df(data, colab, add_days):
    try:
        path = ""
        if colab:
            path = "/content/gdrive/My Drive/Mieszkania_Wrocław/"
        all_data = pd.read_csv(path + "data/data.csv")
        all_data.to_csv(path + "data/data_backup.csv", encoding="utf-8", index=False)
    except FileNotFoundError:
        my_columns = [
            "Price",
            "Rent",
            "Area",
            "Rooms",
            "Floor",
            "Location",
            "Dealer",
            "Building",
            "Furnished",
            "Dishwasher",
            "Elevator",
            "Balcony",
            "Popularity",
            "Time",
            "Date",
            "Title",
            "Id_number",
            "Link",
        ]

        all_data = pd.DataFrame(columns=my_columns)

    currentDT = datetime.datetime.now()
    var_date = (
        str(currentDT.day) + "." + str(currentDT.month) + "." + str(currentDT.year)
    )
    bool_var = False
    if var_date not in all_data["Date"].values:
        bool_var = True

    for index, row in data.iterrows():
        if row["Id_number"] in all_data["Id_number"].values and bool_var:
            ind = all_data[all_data["Id_number"] == row["Id_number"]].index.item()
            if all_data.loc[ind, "Time"] != "+30":
                if all_data.loc[ind, "Time"] + add_days > 30:
                    all_data.loc[ind, "Time"] = "+30"
                else:
                    all_data.loc[ind, "Time"] += add_days
        elif row["Id_number"] not in all_data["Id_number"].values:
            all_data.loc[len(all_data)] = row

    all_data.to_csv(path + "data/data.csv", encoding="utf-8", index=False)
    return all_data
