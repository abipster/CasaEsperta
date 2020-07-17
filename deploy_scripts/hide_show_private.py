from os import listdir, rename
from os.path import isfile, join
from pathlib import Path


def replace(path, onlyfiles, replaceable, replacement):
    for filename in onlyfiles:
        filename = join(path, filename)
        with open(filename) as original_file:
            to_append = ""
            for line in original_file:
                to_append += line.replace(replaceable, replacement)
        open(filename, 'w').close()
        new_file = open(filename, "w")
        new_file.write(to_append)
        new_file.close()


def hide_show_strings(replaceable, replacement, folder_path):
    path = str(Path(folder_path))
    files = [f for f in listdir(path) if isfile(join(path, f))]
    replace(path, files, replaceable, replacement)

    print("Done!")


to_replace = "my_domain"
replace_with = "example"

path = str(Path("c:/path/to/file/to/process.md"))

hide_show_strings(to_replace, replace_with, path)
