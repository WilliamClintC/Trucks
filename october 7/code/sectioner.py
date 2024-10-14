import os

def extract_file_name(file_path):
    base_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_name)
    return file_name

import chardet

def detect_encoding(filepath):
    with open(filepath, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        return encoding
    
import re
import pickle

def text_collect(filename,id):
    pattern = re.compile(r"^\d+\.\d+\.\d+")
    sections = []
    current_section = None
    collected_text = []

    with open(filename, 'r',encoding=detect_encoding(filename),errors='replace') as file:
        for line in file:
            line = re.sub(r'[^\x00-\x7f]', r' ', line)
            line=line.lower()
            line = re.sub(r'[",!?*\[\]]', '', line)
            line = re.sub(r';', ' ', line)
            line = re.sub(r'\\', '', line)
            match = pattern.match(line)
            if match:
                if current_section:
                    sections.append({
                        "Section": current_section,
                        "Text": ' '.join(collected_text),
                        "Zoning Location": extract_file_name(filename)
                    })
                current_section = match.group()
                collected_text = [line[len(current_section):].strip()]
            elif current_section:
                collected_text.append(line.strip())

        if current_section:
            sections.append({
                "Section": current_section,
                "Text": ' '.join(collected_text),
                "Zoning Location": filename
            })

    with open(f"grouped_text{id}.pkl", 'ab') as pkl_file:
        pickle.dump(sections, pkl_file)

#clear the file
with open(f"grouped_text{id}.pkl", 'wb') as pkl_file:
    pass  # This will clear the file

import os
import glob

def process_files(directory):
    # Use glob to find all .txt files in the directory and subdirectories
    txt_files = glob.glob(os.path.join(directory, '**', '*.txt'), recursive=True)
    #print(txt_files)
    for file_path in txt_files:
        text_collect(filename=file_path,id=id)


id = int(os.getenv("SGE_TASK_ID", 1))
# Directory containing the text files
directory = f"/restricted/projectnb/trucks/William/Mleczko_and_Desmond/nzlud/municipal_codes_all/{id}/"


# Process all text files in the directory
process_files(directory)
