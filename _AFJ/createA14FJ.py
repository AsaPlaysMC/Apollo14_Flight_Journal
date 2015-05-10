__author__ = 'Feist'
import csv
from quik import FileLoader


def get_sec(s):
    l = s.split(':')
    if l[0][0:1] != "-":
        return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])
    else:
        return int(l[0]) * 3600 + (int(l[1]) * 60 * -1) + (int(l[2]) * -1)


def get_key(some_object):
    return some_object.sortnumber


class TranscriptItem(object):
    def __init__(self, sortnumber, timestamp, who, words, type):
        self.sortnumber = sortnumber
        self.timestamp = timestamp
        self.who = who
        self.words = words
        self.type = type

    def __repr__(self):
        return '{}: {} {} {}'.format(self.__class__.__name__,
                                     self.sortnumber,
                                     self.timestamp,
                                     self.who,
                                     self.words,
                                     self.type)


def get_combined_transcript_list():
    master_list = []
    # format: sortorder, timestamp, attribution, who, words
    # input_file_path = "../MISSION_DATA/temp_utterances.csv"
    input_file_path = "../MISSION_DATA/A14_CM_cleaned.csv"
    utterance_reader = csv.reader(open(input_file_path, "rU"), delimiter='|')
    for utterance_row in utterance_reader:
        if utterance_row[1] != "": # if not a TAPE change or title row
            temp_obj = TranscriptItem(get_sec(utterance_row[0]), utterance_row[0], utterance_row[1], utterance_row[2], "CM")
            master_list.append(temp_obj)

    input_file_path = "../MISSION_DATA/A14_TEC_cleaned.csv"
    utterance_reader = csv.reader(open(input_file_path, "rU"), delimiter='|')
    for utterance_row in utterance_reader:
        temp_obj = TranscriptItem(get_sec(utterance_row[0]), utterance_row[0], utterance_row[1], utterance_row[2], "TEC")
        master_list.append(temp_obj)

    return sorted(master_list, key=get_key, reverse=False)


output_file_name_and_path = "./_webroot/A14FJ_remaining.html"
output_file = open(output_file_name_and_path, "w")
output_file.write("")
output_file.close()

output_file = open(output_file_name_and_path, "a")

# WRITE HEADER
template_loader = FileLoader('templates')
item_template = template_loader.load_template('template_afj_header.html')
output_file.write(item_template.render({'datarow': 0}, loader=template_loader).encode('utf-8'))

cur_row = 0
# input_file_path = "../MISSION_DATA/A17 master TEC and PAO utterances.csv"
# utterance_reader = csv.reader(open(input_file_path, "rU"), delimiter='|')
combined_list = get_combined_transcript_list()

timestamp_start_int = 913950

for combined_list_item in combined_list:
    timeid = "timeid" + combined_list_item.timestamp.translate(None, ":")
    if combined_list_item.timestamp != "":  # if not a TAPE change or title row
        if int(combined_list_item.timestamp.translate(None, ":")) >= timestamp_start_int:
            cur_row += 1
            if type(combined_list_item) is TranscriptItem:
                words_modified = combined_list_item.words.replace("O2", "O<sub>2</sub>")
                words_modified = words_modified.replace("H2", "H<sub>2</sub>")
                # who_modified = combined_list_item.who.replace("CDR", "Cernan")
                # who_modified = who_modified.replace("CMP", "Evans")
                # who_modified = who_modified.replace("LMP", "Schmitt")
                item_template = template_loader.load_template('template_afj_item_utterance.html')
                output_file.write(item_template.render({'timeid': timeid,
                                                        'timestamp': combined_list_item.timestamp,
                                                        'who': combined_list_item.who,
                                                        'words': words_modified,
                                                        'type': combined_list_item.type},
                                                       loader=template_loader))
            # if cur_row > 100:
            #     break

# WRITE  FOOTER
item_template = template_loader.load_template('template_afj_footer.html')
output_file.write(item_template.render({'datarow': 0}, loader=template_loader).encode('utf-8'))
