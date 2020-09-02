import os
import shutil
import re
import tkinter.filedialog as fdialog
import tkinter.simpledialog as sdialog

def stripAndCapitalize(inputString):
    inputString = re.sub("[^a-zA-Z0-9]", "", inputString).strip()
    inputString = inputString[0].upper() + inputString[1:20] + "MgcStr"
    return inputString

verbose = 1

working_dir = os.path.dirname(os.path.realpath(__file__))
path = fdialog.askopenfilename(filetypes=[(".cs Files","*.cs"), (".gen Files","*.gen")], initialdir=working_dir, title="Pick a source file")
start_line = sdialog.askinteger("Start Line", "Please enter a valid start line")
end_line = sdialog.askinteger("End line", "Please enter a valid end line")
if os.path.exists(path) and os.path.isfile(path):
    shutil.copy(path, path + ".original")
    file_str = ""
    file_set = set()
    keys_set = set()
    file_dict = dict()
    file_list = list()
    const_fields = ""
    with open(path, "r") as f:
        file_list = f.readlines()
    regex = r'(?<!\\)".+?(?<!\\)"'
    for i in range(start_line - 1, end_line):
        matches = re.findall(regex, file_list[i])
        for j in matches:
            file_set.add(j)
    for i in file_set:
        key = stripAndCapitalize(i)
        if key in keys_set:
            while True:
                key += "_"
                if key not in keys_set:
                    keys_set.add(key)
                    break
        else:
            keys_set.add(key)
        if verbose:
            print(f"private const string {key} = {i};")
        file_dict[key] = i
    file_str = "".join(file_list)
    for key, value in file_dict.items():
        file_str = file_str.replace(value, key)
        const_fields += f"\n        private const string {key} = {value};"
    file_splitted = file_str.split("{")
    file_splitted[2] = const_fields + file_splitted[2]
    file_str = "{".join(file_splitted)
    with open(path, "w") as f:
        f.write(file_str)