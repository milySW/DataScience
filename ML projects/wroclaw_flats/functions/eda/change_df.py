from bs4 import BeautifulSoup
import requests
import datetime
import numpy as np


def repair_time(data, path):
    currentDT = datetime.datetime.now()
    today = str(currentDT.day) + "." + str(currentDT.month) + "." + str(currentDT.year)
    today_date = datetime.datetime.strptime(today, "%d.%m.%Y").date()

    for index, row in data.iterrows():
        source = requests.get(row["Link"]).text
        soup = BeautifulSoup(source, "lxml")
        if type(row["Date"]) == str and row["Time"] != "+30":
            my_date = datetime.datetime.strptime(row["Date"], "%d.%m.%Y").date()

            list_of_messages = [
                "To ogłoszenie jest nieaktualne.",
                "To ogłoszenie nie jest już dostępne",
            ]
            if list_of_messages[0] not in source and list_of_messages[1] not in source:
                if (today_date - my_date).days != row["Time"]:
                    if (today_date - my_date).days < 30:
                        data.loc[index, "Time"] = (today_date - my_date).days
                    else:
                        data.loc[index, "Time"] = 30

    data.to_csv(path + "data/data.csv", encoding="utf-8", index=False)


def add_column_with_status(data):
    today = datetime.datetime.now()
    array_of_sold_in_30 = np.zeros(len(data), dtype=int)

    index = 0
    for time, my_date in zip(data["Time"], data["Date"]):
        if time == "+30" or time == 30 or type(my_date) != str:
            index += 1
            continue
        my_date = datetime.datetime.strptime(my_date, "%d.%m.%Y").date()
        if (datetime.timedelta(time) + my_date).strftime("%d.%m.%Y") == today.strftime(
            "%d.%m.%Y"
        ):
            array_of_sold_in_30[index] = 2
        else:
            array_of_sold_in_30[index] = 1
        index += 1

    data["Sold_in_30"] = array_of_sold_in_30
    return data


def unify_buildings(data):
    data["Building"] = data["Building"].str.strip().str.lower()
    return data


def delete_euro_offers(data):
    data = data[~data["Price"].str.contains(r"€(?!$)")]
    return data


def unify_price(data):
    data["Price"] = [
        float(
            i.replace("zł", "")
            .replace(" ", "")
            .replace(",", ".")
            .replace("/miesiąc", "")
        )
        if type(i) != float
        else i
        for i in data["Price"]
    ]
    data["Rent"] = [
        float(
            i.replace("zł", "")
            .replace(" ", "")
            .replace(",", ".")
            .replace("/miesiąc", "")
        )
        if type(i) != float
        else i
        for i in data["Rent"]
    ]
    data["Area"] = [
        float(i.replace("²", "").replace("m", "").replace(" ", "").replace(",", "."))
        if type(i) != float
        else i
        for i in data["Area"]
    ]

    data["Price"] = data["Price"] + data["Rent"]
    data.drop(["Rent"], axis=1, inplace=True)

    return data


def unify_location(data):
    list_of_new_locations = []
    for i in data["Location"]:
        location_words = i.split(",")
        for j in location_words:
            if j.lower().strip() in [
                "krzyki",
                "fabryczna",
                "psie pole",
                "śródmieście",
                "stare miasto",
            ]:
                new_location = j
                break

        list_of_new_locations.append("Wrocław, " + new_location)

    data["Location"] = list_of_new_locations
    return data


def unify_dealer(data):
    data["Dealer"] = [
        "Osoby prywatnej"
        if i in ["Osoby prywatnej", "Oferta prywatna"]
        else "Biuro / Deweloper"
        for i in data["Dealer"]
    ]
    return data


def unify_rooms(data):
    list_of_rooms = []
    for i in data["Rooms"]:
        if "1" in str(i):
            list_of_rooms.append("1")
        elif "2" in str(i):
            list_of_rooms.append("2")
        elif "3" in str(i):
            list_of_rooms.append("3")
        elif str(i).strip().lower() != "kawalerka" and i != float("nan"):
            list_of_rooms.append("4 i więcej")
        else:
            list_of_rooms.append(i)

    data["Rooms"] = list_of_rooms

    return data


def unify_floor(data):
    list_of_floors = []

    for i in data["Floor"]:
        number = False
        for j in range(1, 11):
            if str(j) in str(i) and i not in ["Powyżej 10", "> 10"]:
                list_of_floors.append(str(j))
                number = True
                break

        if i in ["Powyżej 10", "> 10"]:
            list_of_floors.append("powyżej 10")

        elif str(i).lower().strip() == "parter":
            list_of_floors.append("parter")

        elif str(i).lower().strip() == "suterena":
            list_of_floors.append("suterena")

        elif not number:
            list_of_floors.append(i)

    data["Floor"] = list_of_floors

    return data


def binarize_furnished(data):
    data["Furnished"] = [1 if i == "Tak" else 0 for i in data["Furnished"]]
    return data


def define_the_boundaries(col, size):
    quantile_1 = col.quantile(q=0.25)
    quantile_3 = col.quantile(q=0.75)
    IQR = quantile_3 - quantile_1
    border_1 = quantile_1 - IQR * size
    border_2 = quantile_1 + IQR * size
    return border_1, border_2


def delete_outliers(data, col_names, size):
    indices_list = []
    for i in col_names:
        border_1, border_2 = define_the_boundaries(data[i], size)
        indices = data[i].between(border_1, border_2)
        indices_list.append(indices)

    indices = np.logical_and(*indices_list)
    return data[indices]


def delete_columns(data, col_names):
    for i in col_names:
        del data[i]
    return data


def add_mean(data, col, groupby_list):
    for i in groupby_list:
        if type(i) != list:
            name = i
        elif type(i) == list:
            name = "_".join(i)
        data[col + "_to_" + name + "_mean"] = data[col] / data.groupby(i)[
            col
        ].transform("mean")
    return data
