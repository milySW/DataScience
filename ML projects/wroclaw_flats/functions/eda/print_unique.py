def print_unique(data):
    print('Liczba kategorii w kolumnie "Location": ', len(data["Location"].unique()))
    print("")
    print("Kategorie w kolumnach:")
    for i in ["Dealer", "Building", "Furnished", "Rooms", "Floor"]:
        print("")
        print(i, ": ", data[i].unique())
