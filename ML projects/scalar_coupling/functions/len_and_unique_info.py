def len_and_unique_info(list_of_datasets, list_of_names):
    for index, element in enumerate(list_of_datasets):
        print(list_of_names[index] + "|")
        print("-" * (len(list_of_names[index]) + 1))
        print("shape: \t \t \t", element.shape)
        print(element.nunique())
        print("")

        print("-" * 50)
