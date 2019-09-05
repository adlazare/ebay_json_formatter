import json
import os
import data_cleaning


def write_to_json(filename, json_data):
    path = os.getcwd()
    file_path = path + '/2_clean/' + filename

    with open(file_path, 'w') as f:
        json.dump(json_data, f, sort_keys=True, indent=1, ensure_ascii=False)


def load_json(filename):
    """
    Loads in the raw JSON from Cordell's Scrapy crawler
    :return:
    """
    path = os.getcwd()
    file_path = path + '/1_dirty/' + filename

    if os.stat(file_path).st_size == 0:
        # print(filename + " is empty - returning empty dict")
        empty_dict = {}

        return empty_dict
    elif os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)

        return data


def get_files():
    """
    Create a list of all JSON files in current directory
    :return:
    """
    path = os.getcwd() + '/1_dirty'

    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.json' in file:
                files.append(file)

    for f in files:
        print(f)

    return files


def prompt_user(files):
    print('\n')
    print('Select a file to re-format:')

    count = 1
    for f in files:
        print('    {0}) {1}'.format(str(count), f))
        count += 1
    print('\n')

    while True:
        print('Input a number and press Enter: ')

        file_index = input('> ')

        try:
            file_index = int(file_index)
            file_index -= 1

            if file_index > len(files):
                print('[!] Please select a valid option..\n')
            elif file_index < len(files):
                filename = files[file_index]
                break
            else:
                print('[!] Please select a valid option..\n')
        except ValueError:
            print('[!] Please select a valid option..\n')

    return filename


def iterator(product_list):
    """
    Iterate through product list, run cleaning operations
    :param product_list:
    :return:
    """
    updated_products = {"Product_Data": []}

    for product in product_list:
        product = data_cleaning.change_key_names(product)
        product = data_cleaning.remove_redundant_lists(product)
        product = data_cleaning.format_values(product)
        updated_products["Product_Data"].append(product)

    return updated_products


def main():
    """
    Script manager
    :return:
    """
    files = get_files()
    filename = prompt_user(files)

    product_list = load_json(filename)

    updated_products = iterator(product_list)

    shortname = filename.replace('.json', '')
    write_to_json(shortname + '_CLEAN.json', updated_products)

    print('[*] Complete!')

    return


main()
