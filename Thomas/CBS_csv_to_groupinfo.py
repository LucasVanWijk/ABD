def get_info_piramide():

    def index_containing_substring(the_list, substring):
        '''
        https://stackoverflow.com/questions/2170900/get-first-list-index-containing-sub-string
        '''

        for i, s in enumerate(the_list):
            if substring in s:
                return i
        return -1

    #  https://opendata.cbs.nl/statline/#/CBS/nl/dataset/7461bev/table?ts=1614870199236
    info = open("Thomas/Bevolking.csv", "r+").readlines()
    info = info[index_containing_substring(info,"0 tot 5"):-1]
    info = [x.rstrip() for x in info]

    age_dictionary = {
        "Child" : 0,
        "Student" : 0,
        "Adult":0,
        "Elderly":0,
        }
        
    total = 0
    for row in info:
        
        age,amount = row.replace('"','').split(";")
        age = int(age.split(" ")[0])
        total += int(amount)
        if age < 15:            # 0-15, boven 15 telt niet mee
            age_dictionary["Child"] += int(amount)

        elif age < 25:          # 15-25, boven 25 telt niet mee
            age_dictionary["Student"] += int(amount)
            
        elif age < 65:          # 25-65, boven 25 telt niet mee
            age_dictionary["Adult"] += int(amount)

        else:                   # en alles boven 65
            age_dictionary["Elderly"] += int(amount)

    for i in age_dictionary.keys():
        age_dictionary[i] = age_dictionary[i] / total

    return age_dictionary