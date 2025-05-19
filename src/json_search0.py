import find_rename as fr
import pandas as pd
import json, csv, re, os, random

def json_to_csv(input_file_path):
    # Load JSON file
    with open(input_file_path, encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Split the file path into directory path and extension
    dirname, basename = os.path.split(input_file_path)

    # Split the file name and extension
    filename, ext = os.path.splitext(basename)

    # Create the new file path with the desired extension
    output_file_path = os.path.join(dirname, filename + '.csv')

    def get_dict_keys(d):
        keys = []
        for k, v in d.items():
            if isinstance(v, dict):
                keys.extend(get_dict_keys(v))
            else:
                keys.append(k)
        if 'dialogs' in keys:
            keys.remove('dialogs')
        return keys

    # Write header row
    header = get_dict_keys(data)

    def get_value_by_keys(keys, data):
        """
        Given a list of keys and a dictionary, returns a list of the values
        associated with those keys in the dictionary.
        """
        values = []
        for k, v in data.items():
            if isinstance(v, dict):
                keys = get_dict_keys(v)
                values.extend(get_value_by_keys(keys, v))
            elif k in keys:
                values.append(v)
        return values

    # header2 = ['no'] + [x for x in get_dict_keys(data['dialogs'][0])]
    header2 = ['no', 'startTime', 'endTime', 'text', 'tags']

    # Open CSV file for writing
    with open(output_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(header)

        # Loop through JSON data and write each row to CSV file
        row=[]
        for value in get_value_by_keys(header, data):
            row.append(value)
        writer.writerow(row)

        writer.writerow([])
        writer.writerow(['dialogs'])

        writer.writerow(header2)
        header2.remove('no')
        for i, dialog in enumerate(data['dialogs']):
            row = []
            for h in header2:
                try:
                    row.append(dialog[h])
                except:
                    row.append('')
            row = [i+1] + row
            writer.writerow(row)

def dialogs_to_csv2(topic, item_path_ko, item_path_2):
    # Load JSON file
    with open(item_path_ko, encoding='utf-8') as json_file_ko:
        data_ko = json.load(json_file_ko)
    with open(item_path_2, encoding='utf-8') as json_file_2:
        data_lan2 = json.load(json_file_2)
        data_lan2_str = json.dumps(data_lan2, ensure_ascii=False)

    # Split the file path into directory path and extension
    dir_path, basename = os.path.split(item_path_ko)
    filename = ''
    dir_path_csv = ''
    lan2 = search_var(data_lan2_str, 'language')
    if lan2 == '영어':
        filename = topic + '_koen.csv'
        _lan2 = 'en'
    elif lan2 == '중국어':
        filename = topic + '_kozh.csv'
        _lan2 = 'zh'

    # split the directory path into the upper directory and the tail directory
    upper_dir_path, tail = os.path.split(dir_path)

    # construct the path of the new directory
    dir_path_csv = os.path.join(upper_dir_path, tail+'2_csv')

    # create the new directory
    try:
        os.makedirs(dir_path_csv, exist_ok=False)
    except:
        pass

    # Create the new file path with the desired extension
    output_file_path = os.path.join(dir_path_csv, topic + '.csv')

    # Write header row
    header = ['번호', 'TC IN', 'TC OUT', '한국어', lan2]
    header2 = ['no','startTime','endTime','ko','en']
    header3 = ['no', 'startTime', 'endTime', 'ko', 'en', 'speaker_id']


    # Open CSV file for writing
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(header)

        k = 1
        # if len(data_ko['dialogs']) < len(data_lan2['dialogs']
        data_ko['dialogs'] += [{'startTime':'', 'endTime':''}, {'startTime':'', 'endTime':''}, {'startTime':'', 'endTime':'', 'text':'END'}]
        data_lan2['dialogs'] += [{'startTime':'', 'endTime':''}, {'startTime':'', 'endTime':''}, {'startTime':'', 'endTime':'', 'text':'END'}]
        # Loop through JSON data and write each row to CSV file
        for i, dialog in enumerate(data_ko['dialogs']):
            if k <= len(data_ko['dialogs']) and k <= len(data_lan2['dialogs']):
                if 'startTime' in dialog and 'endTime' in dialog:
                    if 'text' in dialog and 'text' in data_lan2['dialogs'][k-1]:
                        row = [(i+1), dialog['startTime'], dialog['endTime'], dialog['text'], data_lan2['dialogs'][k-1]['text']]
                        writer.writerow(row)
                        k += 1
                    elif 'text' not in dialog and 'text' not in data_lan2['dialogs'][k-1]:
                        row = [(i+1), dialog['startTime'], dialog['endTime'], '', '']
                        writer.writerow(row)
                        k += 1
                    elif 'text' not in dialog and 'text' in data_lan2['dialogs'][k-1]:
                        row = [(i+1), dialog['startTime'], dialog['endTime'], '', '']
                        writer.writerow(row)
                    elif 'text' in dialog and 'text' not in data_lan2['dialogs'][k-1]:
                        while 'text' not in data_lan2['dialogs'][k-1]:
                            k += 1
                            if k > len(data_lan2['dialogs']):
                                k -= 1
                                break
                        if 'text' in data_lan2['dialogs'][k-1]:
                            row = [(i+1), dialog['startTime'], dialog['endTime'], dialog['text'], data_lan2['dialogs'][k-1]['text']]
                            writer.writerow(row)
                            k += 1

        writer.writerows(['',['','','', 'item_path_ko', f'item_path_{_lan2}'], ['', '','', item_path_ko, item_path_2]])

def dialogs_to_csv3(item_path_ko, item_path_2):
    pd.set_option('display.max_rows', 300)
    # Load JSON file
    with open(item_path_ko, encoding='utf-8') as json_file_ko:
        data_ko = json.load(json_file_ko)
    with open(item_path_2, encoding='utf-8') as json_file_2:
        data_lan2 = json.load(json_file_2)
        data_lan2_str = json.dumps(data_lan2, ensure_ascii=False)

    _lan2 = search_var(data_lan2_str, 'language')
    if _lan2 == '영어':
        lan2 = 'English'
    elif _lan2 == '중국어':
        lan2 = 'Chinese'

    df = pd.DataFrame({'Korean':[]})
    for d in data_ko['dialogs']:
        if 'text' in d:
            df.loc[len(df)] = [d['text']]

    if lan2:
        df[lan2] = [None] * len(df)
        i = 0
        for d in data_lan2['dialogs']:
            if 'text' in d:
                if i >= len(df):
                    df.loc[len(df)] = [None] * len(df.columns)
                df.loc[i, lan2] = d['text']
                i += 1

    df3 = pd.concat([df, df])

    print(item_path_ko, item_path_2)
    print(df.head(200))
    print(df.columns)
    print(df.loc[len(df)-1])
    print('len(df): ', len(df))
    print('len(data_ko[\'dialogs\'])',len(data_ko['dialogs']))
    print('len(data_lan2[\'dialogs\'])', len(data_lan2['dialogs']))
    print(len(df3))
    # print(df.loc[150])
    # print(df2.head(5))

def dialogs_to_csv(topic, item_path_ko, item_path_2):
    # Load JSON file
    with open(item_path_ko, encoding='utf-8') as json_file_ko:
        data_ko = json.load(json_file_ko)
    with open(item_path_2, encoding='utf-8') as json_file_2:
        data_lan2 = json.load(json_file_2)
        data_lan2_str = json.dumps(data_lan2, ensure_ascii=False)

    # Split the file path into directory path and extension
    dir_path, json_name = os.path.split(item_path_ko)
    up_dir_path, subcategory = os.path.split(dir_path)
    up_up_dir_path, category = os.path.split(up_dir_path)
    filename = ''
    dir_path_csv = ''
    _numbers = re.findall(r'\d+', topic)
    numbers = ''.join(_numbers)
    filename = category + '_' + subcategory + '_' + numbers
    lan2 = search_var(data_lan2_str, 'language')
    if lan2 == '영어':
        # filename = topic + '_koen.csv'
        _lan2 = 'en'
        lan2 = 'English'
    elif lan2 == '중국어':
        # filename = topic + '_kozh.csv'
        _lan2 = 'zh'
        lan2 = 'Chinese'

    # split the directory path into the upper directory and the tail directory
    upper_dir_path, tail = os.path.split(dir_path)

    # construct the path of the new directory
    dir_path_csv = os.path.join(upper_dir_path, tail+'_csv')

    # create the new directory
    try:
        os.makedirs(dir_path_csv, exist_ok=False)
    except:
        pass

    # Create the new file path with the desired extension
    output_file_path = os.path.join(dir_path_csv, filename + '.csv')

    # Write header row
    header = ['No', 'TC IN', 'TC OUT', 'Korean', lan2]
    header2 = ['No','startTime','endTime','ko','en']
    header3 = ['No', 'startTime', 'endTime', 'ko', 'en', 'speaker_id']
    header4 = ['No', 'Korean', lan2]


    # Open CSV file for writing
    with open(output_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(header4)

        count_ko = 0
        for dialog in data_ko['dialogs']:
            if 'text' in dialog and len(dialog['text'].strip()) > 0:
                row = [(count_ko + 1), dialog['text']]
                writer.writerow(row)
                count_ko += 1

    with open(output_file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)

        # Add a new column to the data
        # header_row = rows[0]
        # header_row.append(lan2)

    column2 = []
    for dialog in data_lan2['dialogs']:
        if 'text' in dialog and len(dialog['text'].strip()) > 0:
            column2.append(dialog['text'])

    for i, row in enumerate(rows[1:]):
        if i < len(column2):
            row.append(column2[i])
        else:
            row.append('')

    k = 0
    if len(column2) > len(rows)-1:
        len_dif = len(column2) - (len(rows)-1)
        while k < len_dif:
            try:
                rows.append([len(column2)+k,'',column2[len(rows)+k-1]])
            except:
                pass
            k += 1

    # print('count_ko: ', count_ko)
    # print('len(column2): ', len(column2))
    # print('len(rows)-1: ', len(rows)-1)
    # print("len(data_ko['dialogs']), len(data_lan2['dialogs'])", len(data_ko['dialogs']), len(data_lan2['dialogs']))
    # print(item_path_ko, item_path_2)

  # Write the modified data back to the CSV file
    with open(output_file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def find_json_couple(dir_path, csv_file_name):
    if csv_file_name == '':
        csv_file_name = input('What is the csv file name you are looking for? ')
    if dir_path == '':
        upper_dir_path = input('What is upper directory path you want to search your file within? ')
        print(fr.search_all_for_word(upper_dir_path, csv_file_name)) # prints file paths
        dir_path = input('Enter the dir_path of the csv_file: ')
    # basename, extension = os.path.splitext(csv_file_name)
    csv_file_path = os.path.join(dir_path, csv_file_name)
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        check = ''; json_couple = []
        for row in csv_reader:
            if check != '':
                json_couple.extend([row[3], row[4]])
                break
            if 'item_path_ko' in row:
                check = 'ok'
        return json_couple

def find_json_couple2(dir_path):
    find_json_couple(dir_path, '')

def find_json_couple3(csv_file_name):
    find_json_couple('', csv_file_name)

def coupling_files(dir_path):
    file_list = fr.get_file_list(dir_path)
    # result_list = []
    result_list2 = []
    result_set = set()
    json_koen_list = []
    for file in file_list:
        item_path = os.path.join(file[0], file[1])

        # Read the contents of the JSON file into a string
        with open(item_path, 'r', encoding='utf-8') as f:
            json_string = f.read()
        result_set.add(search_var(json_string, 'topic'))
        # result_list.append((search_var(json_string, 'topic'), search_var(json_string, 'language'), item_path))
        result_list2.append(search_var(json_string, 'topic'))
        result_list2.append(search_var(json_string, 'language'))
        result_list2.append(item_path)

    error_count = 0; true_count = 0
    for result in result_set:
        try:
            i = result_list2.index(result)
            k = result_list2.index(result, i+1, -1)
            if result_list2[i+1] == '한국어':
                json_koen_list.append((result, result_list2[i+2], result_list2[k+2]))
            else:
                json_koen_list.append((result, result_list2[k+2], result_list2[i+2]))
            true_count += 1
        except:
            print(f"\t{result} doesn't exist in one side, thus not coupling.")
            error_count += 1
            pass

    return sorted(json_koen_list, key=lambda x: x[0], reverse=False)

def search_var(json_string, var):
    # Load the JSON string into a Python dictionary
    data = json.loads(json_string)

    # Access the value of the 'var' key
    if var == 'subject':
        return data['subject']
    elif var == 'data_name':
        return data['data_name']
    elif var == 'date':
        return data['date']
    elif var == 'category':
        return data['typeInfo']['category']
    elif var == 'subcategory':
        return data['typeInfo']['subcategory']
    elif var == 'place':
        return data['typeInfo']['place']
    elif var == 'speakers':
        return data['typeInfo']['speakers']
    elif var == 'speaker_id':
        if len(data['typeInfo']['speakers']) == 1:
            return data['typeInfo']['speakers'][0]['speaker_id']
        else:
            speaker_list = []
            for x in data['typeInfo']['speakers']:
                speaker_list.append(x[0]['speaker_id'])
            return speaker_list
    elif var == 'gender':
        return data['typeInfo']['speakers'][0]['gender']
    elif var == 'area':
        return data['typeInfo']['speakers'][0]['area']
    elif var == 'age':
        return data['typeInfo']['speakers'][0]['age']
    elif var == 'language':
        return data['typeInfo']['language']
    elif var == 'language_pair':
        return data['typeInfo']['language_pair']
    elif var == 'topic':
        return data['typeInfo']['topic']
    elif var == 'dialogs':
        return data['dialogs'] #list of dictionaries
    elif var.find('speaker_id') != -1: # receives vars like 'speaker_id0', 'speaker_id1', 'speaker_id[2]' etc., and returns the text of that index (0,1,2 etc.).
        match = re.search(r'\d+', var)
        if match:
            index = int(match.group())
        return data['dialogs'][index]['speaker_id']
    elif var.find('text') != -1: # receives vars like 'text0', 'text1', 'text2' etc., and returns the text of that index (0,1,2 etc.).
        match = re.search(r'\d+', var)
        if match:
            index = int(match.group())
        try:
            text = data['dialogs'][index]['text']
            return text
        except NameError:
            print(f'\tNo text due to deletion at location {index} of dialogs parameter.')
            return ''
    elif var.find('startTime') != -1:
        match = re.search(r'\d+', var)
        if match:
            index = int(match.group())
        return data['dialogs'][index]['startTime']
    elif var.find('endTime') != -1:
        match = re.search(r'\d+', var)
        if match:
            index = int(match.group())
        return data['dialogs'][index]['endTime']
    elif var.find('tags') != -1:
        match = re.search(r'\d+', var)
        if match:
            index = int(match.group())
        return data['dialogs'][index]['tags']

def search_in_json_file(item_path, var):
    # Load JSON file
    with open(item_path) as json_file:
        # data = json.load(json_file) # json object is extracted
        data = json_file.read() # raw data is extracted
    return (search_var(data, var))

def search_in_json_file2(item_path, search_text):
    # Load JSON file
    with open(item_path) as json_file:
        data = json.load(json_file)
    text = json.dumps(data)
    count = text.count(search_text)
    print(f"\'{search_text}\' exists {count} times in the searched file.")
    return count

def search_in_csv(csv_file_path, search_text):
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.reader(csv_file_path)
        print(type(csv_reader))
        rows = []
        for row in csv_reader:
            if search_text in row:
                rows.append(row)
        print(rows)
        return rows

if __name__ == '__main__':
    # D:\aihub data2\006.한-영 및 한-중 음성발화 데이터\01.데이터\1.Training\라벨링데이터_0825_add\TL1\broadcast\다큐멘터리
    # D:\aihub data2\006.한-영 및 한-중 음성발화 데이터\01.데이터\1.Training\라벨링데이터_0825_add\TL1\broadcast\다큐멘터리_csv
    # 방송_다큐_0368.csv 방송_다큐_0001.csv
    # JSON PARAMETERS: subject data_name date typeInfo category subcategory place speakers speaker_id
    # gender area age language language_pair topic dialogs speaker_id text startTime endTime tags

    dir_path = input("\nEnter the directory path to work on: ")
    result1 = fr.search_all_for_word(dir_path, 'ko-zh')

    # result2 = fr.get_file_list(xxdir_path)
    # item1 = random.choice(result2)
    # item_path1 = os.path.join(item1[0], item1[1])
    # item2 = random.choice(result2)
    # item_path2 = os.path.join(item2[0], item2[1])
    # dialogs_to_csv('test', item_path1, item_path2)


    # set1 = set()
    # set2 = set()
    # for x in result1:
    #     item_path = os.path.join(x[0], x[1])
    #     list2 = fr.get_dir_list(item_path)
    #     for y in list2:
    #         set2.add(y[1])
    #         item_path2 = os.path.join(y[0], y[1])
    #         list3 = fr.get_dir_list(item_path2)
    #         for z in list3:
    #             set1.add(z[1])
    # list1 = list(set1)
    # list2 = list(set2)
    # print(list1)
    # print(list2)

    file_true_count = 0; file_error_count = 0
    line_true_count = 0; line_error_count = 0

    for r in result1:
        dir_path2 = os.path.join(r[0], r[1])
        result2 = fr.get_dir_list(dir_path2)
        for q in result2:
            dir_path3 = os.path.join(q[0], q[1])
            result3 = fr.get_dir_list(dir_path3)
            for p in result3:
                dir_path4 = os.path.join(p[0], p[1])
                for k, y in enumerate(coupling_files(dir_path4)):
                    try:
                        dialogs_to_csv(y[0], y[1], y[2])
                        file_true_count += 1
                    except:
                        file_error_count += 1
                        pass

    # for r in fr.get_dir_list(dir_path):
    #     dir_path2 = os.path.join(r[0], r[1])
    #     result2 = fr.get_dir_list(dir_path2)
    #     for k, y in enumerate(coupling_files(dir_path2)):
    #         try:
    #             dialogs_to_csv(y[0], y[1], y[2])
    #             file_true_count += 1
    #         except:
    #             file_error_count += 1
    #             pass

    print('file_true_count: ', file_true_count)
    print('file_error_count: ', file_error_count)
    print('line_true_count: ', line_true_count)
    print('line_error_count: ', line_error_count)

'''
    while True:
        print(''
    METHODS:
    1. json_to_csv(input_file_path)  ...creates csv file from json file
    2. dialogs_to_csv(topic, item_path_ko, item_path_2)  ...extracts dialogs from 2 json files & creates a csv file for language pair/names file on the topic
    3. dialogs_to_csv(topic, item_path_ko, item_path_2)  ...creates & returns a sample csv from a random json file couple in the chosen directory
    4. find_json_couple(dir_path, csv_file_name)  ...searches parent json file paths of csv file  
    5. coupling_files(dir_path)  ...searches json files which compose language pairs for the same topic & returns a tuple list
    6. search_in_json_file(item_path, var)  ...searches key variable name in the json file & returns corresponding value
    7. search_in_json_file2(item_path, search_text)  ...searches a text in the json file & returns the count
    8. search_in_csv(csv_file_path, search_text)  ...searches a text in the csv file & returns the list of rows containing the text/small 'b' is OK
    9. choose new directory  
    A. see directory content  ...small 'a' is OK
    0. Exit  '')

        choice = input("\nEnter method choice (0-9, A): ")

        if choice == "1":
            print("Performing json_to_csv...")
            input_file = input("Enter the file path or file name: ")
            if '\\' in input_file:
                input_file_path = input_file
            else:
                input_file_path = os.path.join(dir_path, item)
            json_to_csv(input_file_path)

        elif choice == "2":
            print("Performing dialogs_to_csv to return a csv file...")
            item_path_ko = input("Enter Korean file path: ")
            item_path_2 = input("Enter file path for other language: ")
            topic = input("Enter the topic/desired name of the csv file: ")
            dialogs_to_csv(topic, item_path_ko, item_path_2)

        elif choice == "3":
            print("Performing dialogs_to_csv to return a random sample csv file...")
            triple_list = coupling_files(dir_path)
            random_element = random.choice(triple_list)
            dialogs_to_csv(random_element[0], random_element[1], random_element[2])

        elif choice == "4":
            print("Performing find_json_couple...")
            file_name = input("Enter the file name (not path): ")
            print(find_json_couple(dir_path, file_name))

        elif choice == "5":
            print("Performing coupling_files...")
            triple_list = coupling_files(dir_path)
            fr.ask_for_print(triple_list)

        elif choice == "6":
            print("Performing search_in_json_file...")
            item = input("Enter the file path or file name: ")
            var = input("Enter the variable(key) you are looking for the value of: ")
            if '\\' in item:
                item_path = item
            else:
                item_path = os.path.join(dir_path, item)
            search_in_json_file(item_path, var)

        elif choice == "7":
            print("Performing search_in_json_file2...")
            item = input("Enter the file path or file name: ")
            search_text = input("Enter the text you want to search for: ")
            if '\\' in item:
                item_path = item
            else:
                item_path = os.path.join(dir_path, item)
            search_in_json_file2(item_path, search_text)

        elif choice == "8":
            print("Performing search_in_csv...")
            csv = input("Enter the file path or file name: ")
            search_text = input("Enter the text you want to search for: ")
            if '\\' in csv:
                csv_file_path = csv
            else:
                csv_file_path = os.path.join(dir_path, csv)
            search_in_csv(csv_file_path, search_text)

        elif choice == "9":
            dir_path = input("Enter new directory path: ")

        elif choice.lower() == "a":
            fr.ask_for_print(fr.get_file_dir_list(dir_path))

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number from 0-9 & A.")
'''


