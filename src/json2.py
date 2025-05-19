import csv
import json

json_str = '''
{
  "version": "1.0",
  "subject": "외국어 음성 데이터",
  "data_name": "한영 음성발화 데이터",
  "date": "2021-10-17",
  "typeInfo": {
    "category": "방송",
    "subcategory": "다큐멘터리",
    "place": "스튜디오",
    "speakers": [
      {
        "speaker_id": "fen212",
        "gender": "여",
        "area": "US",
        "age": "23"
      }
    ],
    "language": "영어",
    "language_pair": "ko-en",
    "topic": "방송_다큐_0314"
  },
  "dialogs": [
    {
      "speaker_id": "fen212",
      "text": "It was within budget and the kitchen was very nice.",
      "startTime": "5.956",
      "endTime": "11.305",
      "tags": "joy"
    }, {
      "speaker_id": "fen212",
      "text": "In the past, that method worked.",
      "startTime": "1235.062",
      "endTime": "1238.511",
      "tags": "none"
    }
  ]
}
'''

# Parse the JSON string into a dictionary
data = json.loads(json_str)

# Create a list of column names for the CSV file
columns = []
columns = ['version', 'subject', 'data_name', 'date',
                'category', 'subcategory', 'place', #'typeInfo'
                'language', 'language_pair', 'topic', #'typeInfo'
                'speaker_id', 'gender', 'area', 'age', #'typeInfo'>'speakers'
                'text', 'startTime', 'endTime', 'tags'] #'dialogs'

def dict_list_check():
    if isinstance(data[key], dict):

    elif isinstance(data[key], list):
        for x in data[key]:
            if isinstance(x, dict):
                columns.add

for key in data:
    if isinstance(data[key], dict):

    elif isinstance(data[key], list):
        for x in data[key]:
            if isinstance(x, dict):
                columns.add
    else:
        columns.add(key)
        row[key] = data[key]




        for inner_key in key:
            if not isinstance(inner_key, dict):
                row[key + '_' + inner_key] = data[key][inner_key]
            else:
                for x in



            # Open a CSV file in write mode and write the headers
with open('output.csv', mode='w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=column_names)
    writer.writeheader()

    # Iterate over each key and write a row for each value unless it is another dictionary.
    # If a dictionary is encountered, new columns will be made for its keys.
    row = {}

    # Add the values of the outer keys to the row
    for key in data:
        if not isinstance(data[key], dict):
            row[key] = data[key]
        else:
            for inner_key in key:
                if not isinstance(inner_key, dict):
                    row[key+'_'+inner_key] = data[key][inner_key]
                else:
                    for x in

        '''
        if key != 'dialogs':
            if isinstance(data[key], dict):
                # Add extra columns for the inner keys
                for inner_key in data[key]:
                    if isinstance(inner_key, dict):
                        for in_inner_key in inner_key:
                            row[in_inner_key] = data[key][inner_key][in_inner_key]
                    else:
                        row[inner_key] = data[key][inner_key]
            else:
                row[key] = data[key]
        '''

    # Add the values of the dialog keys to the row
    for dialog in data['dialogs']: # Each dialog is a dict
        for key in dialog:
            # print(key, dialog)
            row[key] = dialog[key]

    writer.writerow(row)
