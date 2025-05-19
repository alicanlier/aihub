'''renames the folders, and the files according to json parameters'''
import os, shutil, docx

def get_file_list(dir_path):
    # uses os.listdir() to get a list of all files and folders in the directory,
    # then uses a list comprehension to filter only the files and not the folders.
    # lastly, returns a list of tuples which contain dir_paths, file names and item types ('file').
    head, tail = os.path.split(dir_path)
    result_list = [(dir_path, f, 'file') for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    if not result_list:
        print(f'\n\tThere are no files in "{tail}" directory.')
        result_list = []
    else:
        # print(f'File list in the directory "{tail}":', [x[1] for x in result_list], '\n')
        pass
    return result_list

def get_dir_list(dir_path):
    # uses os.listdir() to get a list of all files and folders in the directory,
    # then uses a list comprehension to filter only the folders and not the files
    # lastly, returns a list of tuples which contain dir_paths, dir names (subdir) and item types ('folder').
    head, tail = os.path.split(dir_path)
    result_list = [(dir_path, f, 'folder') for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
    if not result_list:
        print(f'\n\tThere are no folders in "{tail}" directory.')
        result_list = []
    else:
        # print(f'Folder list in the directory "{tail}":', [x[1] for x in result_list], '\n')
        pass
    return result_list

def get_file_dir_list(dir_path):
    # calls get_file_list and get_dir_list methods to create a combined list of
    # files and folders in a directory
    file_list = get_file_list(dir_path)
    folder_list = get_dir_list(dir_path)
    head, tail = os.path.split(dir_path)
    if not file_list and not folder_list:
        print(f'\n\tThere is no content in "{tail}" directory.')
    else:
        if folder_list:
            # print(f'Folder list in the directory "{tail}":', folder_list)
            pass
        if file_list:
            # print(f'File list in the directory "{tail}":', file_list)
            pass
    return folder_list+file_list

def ask_move_dir_content(dir_path, new_dir_path):
    # moves either all content or only folders or only files in a directory to a new directory
    # after prompting the user to choose one from former three options.
    # asks user if he wants to remove the empty directory if all content is moved.
    try:
        if os.listdir(dir_path):
            user_input = input("\nMove all directory content(1), only folders(2) or only files(3)? (1/2/3) ")
            print()
            if user_input == '1':
                n = 0
                if os.listdir(dir_path):
                    for item in os.listdir(dir_path):
                        item_path = os.path.join(dir_path, item)
                        move_item(item_path, new_dir_path)
                        n +=1
                    print(f"\n\t{n} items in the directory \"{os.path.split(dir_path)[1]}\" have been moved to the new directory \"{os.path.split(new_dir_path)[1]}\".")
                    ask_remove_item(dir_path)
                else:
                    print(f"\n\tThe directory \"{os.path.split(dir_path)[1]}\" is empty. Empty directory has been moved into \"{os.path.split(new_dir_path)[1]}\".")
                    ask_remove_item(dir_path)
            elif user_input == '2':
                n_folder = 0
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isdir(item_path):
                        move_item(item_path, new_dir_path)
                        n_folder += 1
                if n_folder == 0:
                    print(f"\n\tThere are no folders to move in the directory \"{dir_path}\".")
                else:
                    print(f"\n\t{n_folder} folders in the directory \"{dir_path}\" have been moved into the directory \"{new_dir_path}\".")
                if not os.listdir(dir_path):
                    print(f"\n\tAll content of the directory \"{dir_path}\" have been moved to new directory, it is empty now.")
                    ask_remove_item(dir_path)
            elif user_input == '3':
                n_file = 0
                for item in os.listdir(dir_path):
                    item_path = os.path.join(dir_path, item)
                    if os.path.isfile(item_path):
                        move_item(item_path, new_dir_path)
                        n_file +=1
                if n_file == 0:
                    print(f"\n\tThere are no files to move in the directory \"{dir_path}\".")
                else:
                    print(f"\n\t{n_file} files in the directory \"{os.path.split(dir_path)[1]}\" have been moved into the directory \"{os.path.split(new_dir_path)[1]}\".")
                if not os.listdir(dir_path):
                    # print(f"\n\tAll content of the directory \"{os.path.split(dir_path)[1]}\" have been moved to another directory, it is empty now.")
                    ask_remove_item(dir_path)
            else:
                print("Wrong command entry. Try again!")
                return

            # checking the remaining content in case of user_input of 2 or 3
            head, tail = os.path.split(dir_path)
            if user_input == '2' and os.listdir(dir_path):
                print(f"\n\t{len(os.listdir(dir_path))} files have been left in the directory \"{tail}\" as follows: \n\t{os.listdir(dir_path)}.")
            elif user_input == '3' and os.listdir(dir_path):
                print(f"\n\t{len(os.listdir(dir_path))} folders have been left in the directory \"{tail}\" as follows: \n\t{os.listdir(dir_path)}.")

        else:
            print(f"\n\tThe directory \"{dir_path}\" has no content to move.")
            ask_remove_item(dir_path)
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def move_item(item_path, new_dir_path):
    try:
        # asks to move a single file or folder of which an item path and new directory are provided.
        dir_path, item_name = os.path.split(item_path)
        type = ''
        if os.path.isdir(item_path):
            shutil.move(item_path, new_dir_path)
            type = 'Folder'
        else:
            new_item_path = os.path.join(new_dir_path, item_name)
            os.rename(item_path, new_item_path)
            type = "File"
        print(f"\t{type} \"{item_name}\" has been moved into the directory \"{os.path.split(new_dir_path)[1]}\".")
        return new_item_path
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_move_item(dir_path, new_dir_path):
    # asks to move a single file or folder of which an directory path and new directory are provided.
    # item name is prompted to user.
    item_name = input(f"\nWhat is the item in the directory \"{os.path.split(dir_path)[1]}\" you want to move? ")
    item_path = os.path.join(dir_path, item_name)
    move_item(item_path, new_dir_path)

def remove_item(item_path):
    try:
        if os.path.isdir(item_path):
            dir_path = item_path
            up_dir_path, dir_name = os.path.split(dir_path)
            n_content = len(os.listdir(dir_path)); n_folder = len(get_file_list(dir_path)); n_file = len(get_dir_list(dir_path))
            if n_content > 0:
                print(f"\n\tThere are {n_content} items ({n_folder} folders/{n_file} files) in the directory \"{dir_name}\".")
            else:
                print(f"\n\tAll content of the directory \"{dir_name}\" have been moved or it is empty.")

            if n_content > 0:
                shutil.rmtree(dir_path)
                print(f"\n\tThe directory \"{dir_name}\" in the upper directory \"{os.path.split(up_dir_path)[1]}\" has been deleted together with its {n_content} contents.")
            else:
                os.rmdir(dir_path)
                print(f"\n\tThe directory \"{dir_name}\" in the upper directory \"{os.path.split(up_dir_path)[1]}\" has been deleted (it was empty).")

        else:
            os.remove(item_path)
            dir_path2, file_name = os.path.split(item_path)
            print(f"\n\tThe file \"{file_name}\" in the directory \"{os.path.split(dir_path2)[0]}\" have been deleted.")
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_remove_item(item_path):
    try:
        if os.path.isdir(item_path):
            dir_path = item_path
            up_dir_path, dir_name = os.path.split(dir_path)
            n_content = len(os.listdir(dir_path)); n_folder = len(get_file_list(dir_path)); n_file = len(get_dir_list(dir_path))
            if n_content > 0:
                print(f"\n\tThere are {n_content} items ({n_folder} folders/{n_file} files) in the directory \"{dir_name}\".")
            else:
                print(f"\n\tAll content of the directory \"{dir_name}\" have been moved or it is empty.")

            choice = input("\nRemove entire folder with all its content(1) / keep folder & remove only the content(2) "
                           "\nkeep folder & files & remove only subfolders(3) / keep folder & subfolders & remove only files(4)"
                           "\nsee the content of the folder(5) / exit(0): ")
            if choice == '1':
                if n_content > 0:
                    shutil.rmtree(dir_path)
                    print(f"\n\tThe directory \"{dir_name}\" in the upper directory \"{os.path.split(up_dir_path)[1]}\" has been deleted together with its {n_content} contents.")
                else:
                    os.rmdir(dir_path)
                    print(f"\n\tThe directory \"{dir_name}\" in the upper directory \"{os.path.split(up_dir_path)[1]}\" has been deleted (it was empty).")
            elif choice == '2':
                if n_content > 0:
                    for x in get_file_dir_list(dir_path):
                        item_path = os.path.join(x[0], x[1])
                        if os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                        else:
                            os.remove(item_path)
                    print(f"\n\t{n_content} items ({n_folder} folders/{n_file} files) of the directory \"{dir_name}\" have been deleted.")
                else:
                    print(f"\n\tAll content of the directory \"{dir_name}\" have been moved or it is empty.")
            elif choice == '3':
                for x in get_dir_list(dir_path):
                    item_path = os.path.join(x[0], x[1])
                    shutil.rmtree(item_path)
                    print(f"\n\t{n_folder} folders of the directory \"{dir_name}\" have been deleted.")
            elif choice == '4':
                for x in get_file_list(dir_path):
                    item_path = os.path.join(x[0], x[1])
                    os.remove(item_path)
                    print(f"\n\t{n_file} files of the directory \"{dir_name}\" have been deleted.")
            elif choice == '5':
                print(f'\n\"{dir_name}\" directory content:\n')
                for x in get_file_dir_list(dir_path):
                    print(f'\t{x[1]} ({x[2]})')
            elif choice == '0':
                pass
            else:
                print("\nEnter a valid number please.")
                ask_remove_item(dir_path)
        else:
            os.remove(item_path)
            dir_path2, file_name = os.path.split(item_path)
            print(f"\n\tThe file \"{file_name}\" in the directory \"{os.path.split(dir_path2)[0]}\" have been deleted.")
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def copy_item(item_path, new_dir_path):
    try:
        head1, tail1 = os.path.split(item_path)
        head2, tail2 = os.path.split(new_dir_path)
        if os.path.isdir(item_path):
            shutil.copytree(item_path, new_dir_path)
            print(f"Folder {tail1} has been copied into {tail2} directory with its entire content.")
        else:
            shutil.copy2(item_path, new_dir_path)
            print(f"File {tail1} has been copied into {tail2} directory.")
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_copy_item(item_path, new_dir_path):
    try:
        head1, tail1 = os.path.split(item_path)
        head2, tail2 = os.path.split(new_dir_path)
        if os.path.isdir(item_path):
            choice = input("\nWould you like to copy the entire folder(1) or only its contents -subfolders/files- (2)?(1/2) ")
            if choice == '1':
                shutil.copytree(item_path, new_dir_path)
                print(f"Folder {tail1} has been copied into {tail2} directory with its entire content.")
            elif choice == '2':
                for x in get_file_dir_list(item_path):
                    copy_item(os.path.join(x[0], x[1]), new_dir_path)
                print(f"{len(get_file_dir_list(item_path))} items in {tail1} directory have been copied into {tail2} directory.")
            else:
                ask_copy_item(item_path, new_dir_path)
        else:
            choice = input("\nWould you like to rename the file when copying?(y/n) ")
            if choice.lower() == 'y':
                new_file_name = input("\nWhat is the new name of file (with extension)? ")
                new_file_path = os.path.join(new_dir_path, new_file_name)
                shutil.copy(item_path, new_file_path)
                print(f"File {tail1} in {os.path.split(head1)[1]} directory has been copied into {tail2} directory & renamed to {new_file_name}.")
            elif choice.lower() == 'n':
                shutil.copy2(item_path, new_dir_path)
                print(f"File {tail1} has been copied into {tail2} directory.")
            else:
                ask_copy_item(item_path, new_dir_path)
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def rename(item_path, new_name):
    try:
        # renames a file or folder of which item path and a new name are provided in the same directory.
        dir_path, item_name = os.path.split(item_path)
        new_item_path = os.path.join(dir_path, new_name)
        os.rename(item_path, new_item_path)
        print(f"\n\tItem \"{item_name}\" has been renamed to \"{new_name}\".")
        return new_item_path
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def rename_by_item_name(dir_path, item_name, new_name):
    # renames a file or folder of which directory path, item name and a new name are provided
    # in the same directory.
    item_path = os.path.join(dir_path, item_name)
    rename(item_path, new_name)

def rename_move(dir_path, item_name, new_dir_path, new_name):
    try:
        item_path = os.path.join(dir_path, item_name)
        new_item_path = os.path.join(new_dir_path, new_name)
        os.rename(item_path, new_item_path)
        print(f"\n\tItem \"{item_name}\" has been renamed to \"{new_name}\" & moved into the folder \"{os.path.split(new_dir_path)[1]}\".")
        return new_item_path
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def rename_all_by_tag(dir_path, tag):
    try:
        # renames all files & folders in a directory by appending same tag to the end of each item name.
        item_list = os.listdir(dir_path)
        print("before:",item_list)
        for item in item_list:
            item_path = os.path.join(dir_path, item)
            if os.path.isdir(item_path):
                new_path = item_path + tag
                os.rename(item_path, new_path)
                print(f"\n\tFolder \"{item}\" has been renamed.")
            else:
                split = item.split('.')
                new_name = split[0] + tag + '.'+split[1]
                new_path = os.path.join(dir_path, new_name)
                os.rename(item_path, new_path)
                print(f"\n\tFile \"{item}\" has been renamed.")
        print("\tAfter tag addition:",os.listdir(dir_path))
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_search_rename(dir_path):
    try:
        # accepts a directory, asks for the search name and the new name to rename to, then returns the new item path.
        item_name = input(f"\nWhat is the name of the item you want to change? ")
        item = search_dir_for_word(dir_path, item_name)
        if item:
            item_path = os.path.join(dir_path, item_name)
        else:
            print(f'\n\tThere is no item with the name \"{item_name}\" in the directory \"{dir_path}\".')
            return
        new_name = input(f"\nWhat is the new name you want to give to the item? ")
        new_path = os.path.join(dir_path, new_name)
        os.rename(item_path, new_path)
        print(f"\n\t{item[0][2].capitalize()} \"{item_name}\" has been renamed to \"{new_name}\".")
        return new_path
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_search_all_rename(root_path):
    try:
        item_name = input(f"\nWhat is the name of the item you want to change? ")
        search_list = []
        for dirpath, dirnames, filenames in os.walk(root_path):
            if item_name in dirnames or item_name in filenames:
                item_path = os.path.join(dirpath, item_name)
                type = 'file' if os.path.isfile(item_path) else 'folder'
                search_list.append((dirpath, item_name, type))
        if search_list:
            result_list = []
            print(f'\n\tFound {len(search_list)}  items with the name \"{item_name}\" in the directory \"{root_path}\" & its subdirectories.')
            choice = input("\nWould you like to rename all matches to the same name(1) or separately(2)? (1/2) ")
            if choice == '1':
                user_input = input("\nWrite the new name you want to rename all matching items: ")
                for item in search_list:
                    os.rename(os.path.join(item[0], item[1]), os.path.join(item[0], user_input))
                    new_item = (item[0], user_input, item[2])
                    result_list.append(new_item)
            else:
                for item in search_list:
                    new_name = input(f"\nWhat is the new name you want to give to the {item[2]} {item[1]} in the directory {item[0]}? ")
                    os.rename(os.path.join(item[0], item[1]), os.path.join(item[0], new_name))
                    new_item = (item[0], new_name, item[2])
                    result_list.append(new_item)
            print(f'\n{len(search_list)} items in the directory {root_path} & its subdirectories have been renamed.')
            search_list = result_list
        else:
            print(f'\nThere are no matches in the directory {root_path} & its subdirectories for the searched item name.')
        return search_list
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def search_dir_for_word(dir_path, word):
    try:
        # searches in a directory if a partial or full word exists in file or folder names,
        # and returns a list of tuples of (dir_path, item name and item type).
        search_list = []; n_folder = 0; n_file = 0
        for item in os.listdir(dir_path):
            if word in item:
                item_path = os.path.join(dir_path, item)
                if os.path.isdir(item_path):
                    search_list.append((dir_path, item, 'folder'))
                    n_folder += 1
                else:
                    search_list.append((dir_path, item, 'file'))
                    n_file += 1
        if search_list:
            print(f"\n\t{n_folder} folders & {n_file} files have been found in the directory \"{dir_path}\".")
        return search_list
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_search_dir_for_word(dir_path):
    word = input("\nWhat keyword are you looking for? ")
    print()
    return search_dir_for_word(dir_path, word)

def search_all_for_word(root_dir, word):
    try:
        # searches in a directory and its subdirectories if a partial or full word exists in file or folder names,
        # and returns a list of tuples of (dir_path, item name and item type).
        all_search_list = search_dir_for_word(root_dir, word)
        print('\n\tSearching for its subdirectories...\n')
        n_dir = 0; n_file = 0; dircount = 0
        for x in all_search_list:
            if set(x) & set('folder'): n_dir += 1
            if x[2] == 'file': n_file += 1
        n_item_in_root_dir = n_dir + n_file
        for item in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, item)
            if os.path.isdir(subdir_path):
                dircount += 1; _n_dir = 0; _n_file = 0;
                search_list = []
                for dirpath, dirnames, filenames in os.walk(subdir_path):
                    for item_name in dirnames:
                        if word in item_name:
                            search_list.append((dirpath, item_name, 'folder'))
                            _n_dir += 1; n_dir += 1
                    for item_name in filenames:
                        if word in item_name:
                            search_list.append((dirpath, item_name, 'file'))
                            _n_file += 1; n_file += 1
                if _n_dir+_n_file > 0:
                    print(f'\n\t{_n_dir} folders & {_n_file} files have been found in the subdirectory \"{subdir_path}\".')
                all_search_list += search_list
        if all_search_list:
            print(f"\n\t{n_dir} folders & {n_file} files including the word \"{word}\" have been found in the directory "
                  f"\"{root_dir}\" ({n_item_in_root_dir} items) & its {dircount} subdirectories ({n_dir+n_file-n_item_in_root_dir} items).\n")
        return all_search_list
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_search_all_for_word (root_dir):
    word = input("\nWhat keyword are you looking for? ")
    print()
    return search_all_for_word(root_dir, word)

# def search_dir_for_word(dir_path, item_name):
#     # searches for an item name within a directory and returns a tuple composed of dir_path, item_name and type if it exists therein.
#     search_list = []
#     if item_name in os.listdir(dir_path):
#         item_path = os.path.join(dir_path, item_name)
#         type = "folder" if os.path.isdir(item_path) else "file"
#         print(f"\n\t1 matching {type} has been found in directory \"{dir_path}\".\n")
#         search_list.append((dir_path, item_name, type))
#     else:
#         print(f"\n\tThere is no item named \"{item_name}\" in the directory \"{dir_path}\".\n")
#     return search_list

# def ask_search_dir_for_word(dir_path):
#     search_list = []
#     item_name = input("\nWhat item name are you looking for? ")
#     search_dir_for_word(dir_path, item_name)

# def search_all_for_word(root_dir, item_name):
#     # searches for an item name in a directory and subdirectories, and returns a list of (dirpath, item name, type) tuple for all matches.
#     search_list = []
#     n_dir = 0; n_file = 0;
#     for dirpath, dirnames, filenames in os.walk(root_dir):
#         if item_name in dirnames:
#             # print(f"Found folder \"{item_name}\" in directory \"{dirpath}\".")
#             search_list.append((dirpath, item_name, 'folder'))
#             n_dir += 1
#         if item_name in filenames:
#             # print(f"Found file \"{item_name}\" in directory \"{dirpath}\".")
#             search_list.append((dirpath, item_name, 'file'))
#             n_file += 1
#     if search_list:
#         print(f"\n\t{n_dir} subdirectories and {n_file} files with the name \"{item_name}\" have been found in the directory \"{root_dir}\" or its subdirectories.\n")
#         # print subdirectories which include the searched item in separate lines (windows format)
#         user_input = input("\nWould you like to print name of subdirectories including the searched item in separate lines?(y/n) ")
#         if user_input.lower() == 'y':
#             for result in search_list:
#                 print(result[0])
#         print()
#     return search_list

def rename_by_removing_tag(item_path, tag):
    try:
        substring = tag
        dir_path, item_name = os.path.split(item_path)
        if substring in item_name:
            index = item_name.find(substring)
            new_name = item_name[:index]+item_name[index+len(substring):]
            rename(item_path, new_name)
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def rename_all_by_removing_tag(dir_path, tag):
    try:
        item_list = get_file_dir_list(dir_path)
        substring = tag
        path_list = []
        for item in item_list:
            item_name = item[1]
            if substring in item_name:
                index = item_name.find(substring)
                new_name = item_name[:index] + item_name[(index+len(substring)):]
                path_list.append((os.path.join(dir_path, item_name), new_name))
        for path in path_list:
            rename(path[0], path[1])
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def ask_for_print(result_list):
    try:
        user_input = input("\nChoose the way to print the result list: dir paths of items (1), item names (2), "
                           "\nitem paths (3) in separate lines or no need to print (4 or any key)?(1/2/3/4): ")
        print()
        if user_input == '1':
            result_set = set()
            for x in result_list:
                result_set.add(x[0])
            for y in result_set:
                print('\t' + y)
        if user_input == '2':
            sorted_list = sorted(result_list, key=lambda x: (x[2] == 'file', x[1]))
            for x in sorted_list:
                print('\t' + x[1], f'({x[2]})')
        elif user_input == '3':
            # sorted_list = sorted(result_list, key=lambda x: x[2], reverse=True)
            sorted_list = sorted(result_list, key=lambda x: (x[2] == 'file', x[1]))
            for x in sorted_list:
                print('\t' + x[0] + '\\' + x[1], f'({x[2]})')
        else:
            return
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def correct_path(path):
    # corrects any windows path to python path by changing single backslash to double backslashes.
    tokens = path.split("\\")
    corrected_path = ''
    for token in tokens:
        if corrected_path == '':
            corrected_path = token
        else:
            corrected_path = corrected_path+r'\\'+token
    return corrected_path

def create(dir_path):
    try:
        type = input("\nDo you want to create a file(1) or a folder(2) or a folder/subfolder(3)? ")
        item_name = input(f"What is the name of the item you want to create (for 3: folder/subfolder)? ")
        if type == '1':
            item_path = os.path.join(dir_path, item_name)
            if not search_dir_for_word(dir_path, item_name):
                with open(item_path, 'w'):
                    pass
            else:
                print(f"A file named \"{item_name}\" already exists in the directory \"{os.path.split(dir_path)[1]}\". Choose another name.")
                create(dir_path)
        elif type == '2':
            if not search_dir_for_word(dir_path, item_name):
                os.mkdir(os.path.join(dir_path, item_name))
            else:
                if os.path.isfile(search_dir_for_word(dir_path, item_name)):
                    os.mkdir(os.path.join(dir_path, item_name))
                else:
                    print(f"There is already a folder named \"{item_name}\" in the directory \"{os.path.split(dir_path)[1]}\". Choose another name.")
                    create(dir_path)
        elif type == '3':
            if '/' in item_name:
                try:
                    os.makedirs(os.path.join(dir_path, item_name))  # item_name = folder/subfolder
                except:
                    print(f"There is already a folder/subfolder named \"{item_name}\" in the directory \"{os.path.split(dir_path)[1]}\". Choose another name.")
                    create(dir_path)
            else:
                print("Enter a name in the following format: folder/subfolder.")
                create(dir_path)
        else:
            pass
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def search_within_file (file_path, word):
    try:
        dir_path, file_name = os.path.split(file_path)
        filename, file_extension = os.path.splitext(file_path)
        word_count = 0
        if file_extension.lower() == 'csv':
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if word in row:
                        word_count += 1
        elif file_extension.lower() == 'txt':
            with open(file_path, 'r', encoding='utf-8') as file:
                if word in file.read():
                    word_count += 1
        elif file_extension.lower() == 'docx' or file_extension.lower() == 'doc':
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                if word in paragraph.text:
                    word_count += 1
        else:
            pass
        if word_count > 0:
            print(f"The word {word} has been used at least {word_count} times in the file {file_name}.")
        else:
            print(f"The word {word} does not exist in the file {file_name}.")
        return word_count
    except Exception as e:
        print("An error occurred:", type(e).__name__)

def help():
    # print(
    '''ALL METHODS:
    1. get_file_list(dir_path) / 2. get_dir_list(dir_path) / 3. get_content_list(dir_path) / 4. ask_move_dir_content(dir_path, new_dir_path) / 
    5. move_item(item_path, new_dir_path) / 6. ask_move_item(dir_path, new_dir_path) / 7. remove_item(item_path) / 8. ask_remove_item(item_path) /
    9. copy_item(item_path, new_dir_path) / 10. ask_copy_item(item_path, new_dir_path) / 11. rename_by_item_path(item_path, new_name) / 
    12. rename_by_item_name(dir_path, item_name, new_name) / 13. rename_all_by_tag(dir_path, tag) / 14. ask_search_rename(dir_path) /   
    15. ask_search_all_rename(root_path) / 16. search_dir_for_word(dir_path, word) / 17. ask_search_dir_for_word(dir_path) / 
    18. search_all_for_word(root_dir, word) / 19. ask_search_all_for_word (root_dir) / 20. rename_by_removing_tag(item_path, tag) / 
    21. rename_all_by_removing_tag(dir_path, tag) / 22. ask_for_print(result_list) / 23. correct_path(path) / 24. help()'''
    # )

    print('''
    METHODS:
    1. get_file_list(dir_path)  # returns a list of tuples (dir_path, item_name, type) for files
    2. get_dir_list(dir_path)  # returns a list of tuples (dir_path, item_name, type) for subdirs
    3. get_content_list(dir_path)  # returns a list of tuples (dir_path, item_name, type) for subdirs & files 
    4. ask_move_dir_content(dir_path, new_dir_path)  # asks if whole content/only folders/only files to move
    5. ask_move_item(dir_path, new_dir_path)  # asks for file/folder name input within the method
    6. ask_remove_item(item_path)  # asks whether to remove whole folder or just its content
    7. ask_copy_item(item_path, new_dir_path)  # asks to copy whole folder or just the content/asks whether to rename the file when copying 
    8. rename_by_item_name(dir_path, item_name, new_name)
    9. rename_move(dir_path, item_name, new_dir_path, new_name)
    A. rename_all_by_tag(dir_path, tag)  # appends the given tag to all files and primary subdirs within the given directory
    B. ask_search_rename(dir_path)  # asks for keyword to search in the given directory, then asks for new name for the matching item
    C. ask_search_all_rename(root_path)  # asks for keyword to search in the given directory & its all levels subdirs, then asks for new name for each item
    D. ask_search_dir_for_word(dir_path)  # asks for keyword to search in the given directory, returns a list of tuples (dir_path, item_name, type)
    E. ask_search_all_for_word (root_dir)   # asks for keyword to search in the given directory & its all levels subdirs, returns a list of tuples (dir_path, item_name, type)
    F. rename_by_removing_tag(item_path, tag)  # removes the given tag (substring) from the name of the given file/folder (renaming)
    G. rename_all_by_removing_tag(dir_path, tag)  # removes the given tag (substring) from names of all contents of the given directory (renaming)
    H. help (either of h/H/help)
    I. search_within_file (file_path, word)  # searches for the given keyword within txt, csv & word files/returns the least word count
    J. change the directory path you are working on
    K. create(dir_path)  # creates file or folder or folder/subfolder (either of k/K/create)
    0. exit''')

if __name__ == '__main__':
    help()
    dir_path = input("\nEnter the directory path to work on: ")
    while True:
        choice = input("\nEnter method choice (0-9, A-J): ")
        if choice == "1":
            print("Performing get_file_list...")
            ask_for_print(get_file_list(dir_path))
        elif choice == "2":
            print("Performing get_dir_list...")
            ask_for_print(get_dir_list(dir_path))
        elif choice == "3":
            print("Performing get_file_dir_list...")
            ask_for_print(get_file_dir_list(dir_path))
        elif choice == "4":
            print("Performing ask_move_dir_content...")
            new_dir_path = input("Enter the new directory path: ")
            ask_move_dir_content(dir_path, new_dir_path)
        elif choice == "5":
            print("Performing ask_move_item...")
            new_dir_path = input("Enter the new directory path: ")
            ask_move_item(dir_path, new_dir_path)
        elif choice == "6":
            print("Performing ask_remove_item...")
            item_name = input("Enter the file/folder name to remove: ")
            item_path = os.path.join(dir_path, item_name)
            ask_remove_item(item_path)
        elif choice == "7":
            print("Performing ask_copy_item...")
            item_name = input("Enter the file/folder name to copy: ")
            new_dir_path = input("Enter the new directory path: ")
            ask_copy_item(item_path, new_dir_path)
        elif choice == "8":
            print("Performing rename_by_item_name...")
            item_name = input("Enter the file/folder name to rename: ")
            new_name = input("Enter the new file/folder name: ")
            rename_by_item_name(dir_path, item_name, new_name)
        elif choice == "9":
            print("Performing rename_move...")
            item_name = input("Enter the file/folder name to rename: ")
            new_dir_path = input("Enter the new directory path: ")
            new_name = input("Enter the new file/folder name: ")
            rename_move(dir_path, item_name, new_dir_path, new_name)
        elif choice.lower() == "a":
            print("Performing rename_all_by_tag...")
            tag = input("Enter the tag to append to the names of folder contents: ")
            rename_all_by_tag(dir_path, tag)
        elif choice.lower() == "b":
            print("Performing ask_search_rename...")
            ask_search_rename(dir_path)
        elif choice.lower() == "c":
            print("Performing ask_search_all_rename...")
            ask_search_all_rename(root_path=dir_path)
        elif choice.lower() == "d":
            print("Performing ask_search_dir_for_word...")
            ask_search_dir_for_word(dir_path)
        elif choice.lower() == "e":
            print("Performing ask_search_all_for_word ...")
            ask_search_all_for_word(root_dir=dir_path)
        elif choice.lower() == "f":
            print("Performing rename_by_removing_tag...")
            item_name = input("Enter the file/folder name to rename: ")
            item_path = os.path.join(dir_path, item_name)
            tag = input("Enter the tag to delete from the name of the given file/folder: ")
            rename_by_removing_tag(item_path, tag)
        elif choice.lower() == "g":
            print("Performing rename_all_by_removing_tag...")
            tag = input("Enter the tag to delete from the name of the given file/folder: ")
            rename_all_by_removing_tag(dir_path, tag)
        elif choice.lower() == "h" or choice.lower() == "help":
            help()
        elif choice.lower() == "i":
            print("Performing search_within_file ...")
            item_name = input("Enter the file name to inquire: ")
            file_path = os.path.join(dir_path, item_name)
            word = input("Enter the keyword you are looking for: ")
            search_within_file(file_path, word)
        elif choice.lower() == "j":
            dir_path = input("Enter new directory path: ")
        elif choice.lower() == "k" or choice.lower() == "create":
            print("Performing create...")
            create(dir_path)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number or letter from among 0-9 & A-K.")

    #######################################################################################################################################

    # list_koen = search_all_for_word (dir_path, 'ko-en')
    # list_방송 = search_all_for_word(dir_path, '방송')
    # matches = []
    # print()
    # for x in list_방송:
    #     if 'ko-en' in x[0]:
    #         matches.append(x)
    #
    # for x in matches:
    #     print(f'\t{x}')
    #     item_path = os.path.join(x[0], x[1])
    #     new_item_path = os.path.join(x[0],'방송koen')
    #     os.rename(item_path, new_item_path)

    # list2 = search_all_for_word(dir_path, 'openssl')

    '''
    list_방송koen = search_all_for_word(dir_path, '방송koen')

    for x in list_방송koen:
        print(f'\t{x}')
        item_path = os.path.join(x[0], x[1])
        head, tail = os.path.split(x[0])
        new_dir_path = os.path.join(head, 'broadcast')
        shutil.copytree(item_path, new_dir_path)

    list_방송koen2 = search_all_for_word(dir_path, '방송koen')

    for x in list_방송koen2:
        print(f'\t{x}')


    result_list = ask_search_all_for_word(dir_path)
    if result_list:
        ask_for_print(result_list)


    rl = get_file_list(dir_path)
    ask_for_print(rl)
    
    '''
    # result_list = search_all_for_word(dir_path, "방송")
    # for x in result_list:
    #     item_path = os.path.join(x[0], x[1])
    # while True:
    #     ask_search_all_rename(dir_path)
    # D:\aihub data3\006.한-영 및 한-중 음성발화 데이터

    # for x in get_dir_list(dir_path):
    #     if 'csv' in x[1]:
    #         item_path = os.path.join(x[0], x[1])
    #         move_item(item_path, new_dir_path)