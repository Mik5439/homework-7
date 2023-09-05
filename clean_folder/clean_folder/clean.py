import shutil
import sys
from pathlib import Path

# Dictionary with extensions
EXTENSIONS_DICT = {
    'images': ('.jpeg', '.png', '.jpg', '.svg', '.dng'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.djvu', '.rtf'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar')
}

# Extensions list
EXTENSIONS_LIST = []
for value in EXTENSIONS_DICT.values():
    for exten in value:
        EXTENSIONS_LIST.append(exten)      

# Folder list
FOLDER_LIST = ['unknown_extension']
for key in EXTENSIONS_DICT.keys():
    FOLDER_LIST.append(key)

#Symbols for normalization
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
trans = {}


main_folder: Path | None = None


def main():
    global main_folder

    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()

    root_folder = Path(sys.argv[1])
    # root_folder => Path("D:\Maya\Desktop\Хлам")

    if (not root_folder.exists()) or (not root_folder.is_dir()):
        print('Path incorrect')
        exit()

    main_folder = root_folder
    fill_translate()
    cleaner(root_folder)


def cleaner(folder: Path):
    for file in folder.iterdir():
        
        if file.is_file():
            sort_file(file)

        if file.is_dir():
            cleaner(file)
            if not any(file.iterdir()):
                if file.name not in FOLDER_LIST:
                    file.rmdir()


def sort_file(file: Path):
    file_suffix = file.suffix.lower()
    file_name = file.stem

    if file_suffix in EXTENSIONS_LIST:
        for key, values in EXTENSIONS_DICT.items():
            if file_suffix in values:
                normalized_file_name = normalize(file_name)
                new_file_name = normalized_file_name + file_suffix
                end_folder = main_folder.joinpath(key)

                end_folder.mkdir(exist_ok=True)
                new_file_path = end_folder.joinpath(new_file_name)
                file.rename(new_file_path)
    
                if key == 'archives':
                    base_archive_dir = end_folder.joinpath(normalized_file_name)
                    base_archive_dir.mkdir(exist_ok=True)
                    shutil.unpack_archive(new_file_path, base_archive_dir)
    else:
        normalized_file_name = normalize(file_name)
        new_file_name = normalized_file_name + file_suffix
        end_folder = main_folder.joinpath("unknown_extension")
        end_folder.mkdir(exist_ok=True)
        new_file_path = end_folder.joinpath(new_file_name)
        file.rename(new_file_path)

def fill_translate():
    for cyril, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        trans[ord(cyril)] = latin
        trans[ord(cyril.upper())] = latin.upper()


def normalize(file_name: str) -> str:
    normalized_name = file_name.translate(trans)

    for i in normalized_name:
        if not i.isdigit() and not i.isalpha() and i != '_':
            normalized_name = normalized_name.replace(i, '_')

    return normalized_name


if __name__ == '__main__':
    main()
    print("Finished!!!")
    exit()