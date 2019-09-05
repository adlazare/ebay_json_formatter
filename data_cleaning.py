import re


def change_key_names(product):
    """
    Update the key names for the product DICT
    :param product:
    :return: cleaned product DICT
    """
    updated_product = {}
    key_pairs = [('PRODUCT_NAME', 'Name'),
                 ('PRODUCT_URL', 'URL'),
                 ('PRODUCT_PRICE', 'Price'),
                 ('PRODUCT_BIDS', 'x'),
                 ('PRODUCT_CONDITION', 'Condition'),
                 ('PRODUCT_BRAND', 'Brand'),
                 ('PRODUCT_MPN', 'x1'),
                 ('PRODUCT_MODEL', 'model_number'),
                 ('PRODUCT_COLOR', 'Color'),
                 ('PRODUCT_UPC', 'x2'),
                 ('ATTR_DATA', 'x3'),
                 ('PRODUCT_RATINGS_COUNT', 'x4'),
                 ('PRODUCT_STAR_RATING', 'Rating'),
                 ('QUANTITY_SOLD', 'x5'),
                 ('QUANTITY_AVAILABLE', 'x6'),
                 ('SELLER_NAME', 'Seller'),
                 ('SELLER_LOCATION', 'x7'),
                 ('SELLER_FEEDBACK_URL', 'Seller_url'),
                 ('SELLER_FEEDBACK_SCORE', 'x8'),
                 ('PRODUCT_IMAGE_URL', 'Image'),
                 ('EBAY_ITEM_NUMBER', 'Itemnumber')
                 ]

    for key, new_key in key_pairs:
        if key in product.keys():
            updated_product[new_key] = product[key]
        else:
            updated_product[new_key] = 'NA'

    keys_to_remove = ['x', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8']

    # Remove un-needed data-points
    for key in keys_to_remove:
        updated_product.pop(key)

    # print(json.dumps(updated_product, indent=4, sort_keys=True)) # pretty-print JSON

    return updated_product


def remove_redundant_lists(product):
    """
    Extracts strings from lists & updates the value
    Parse importer expects only strings or integers
    :return:
    """
    for key, value in product.items():
        if type(value) == list:
            if len(value) >= 1:
                product[key] = value[0]
            else:
                product[key] = "NA"

    return product


def format_values(product):
    """
    Clean extra data from strings
    :param product:
    :return:
    """
    if 'Rating' in product.keys():
        if product['Rating'] != 'NA':
            # remove leading newlines & tabs, convert string to float
            rating = product['Rating'].strip()
            rating = float(rating)
            product['Rating'] = rating
        elif product['Rating'] == 'NA':
            product['Rating'] = 0

    if 'Price' in product.keys():
        if product['Price'] != 'NA' and product['Price'] is not None:
            # split currency & price
            price = product['Price']

            try:
                test_val = int(price[0])
            except ValueError:
                test_val = 'str'
                pass

            # clean up price string - 2 formats (currency + price OR price + currency <- (edge case))
            # edge case sample: 420.00 PLN
            if type(test_val) is str:
                price_strings = re.split('([A-Z]{1,3})\s', price, 1)
                price = price_strings[-1]
                price = price.lstrip('$')
                price = price.rstrip('/ea')
                price = float(price)
                currency = price_strings[-2]
            elif type(test_val) is int:
                price_strings = re.split('([A-Z]{1,3})', price, 1)
                price = price_strings[0]
                price = price.lstrip('$')
                price = price.rstrip('/ea')
                price = float(price)
                currency = price_strings[1]

            product['Price'] = price
            product['Currency'] = currency
        else:
            product['Currency'] = 'NA'  # We need to assign the currency key/value in either case here

    if 'model_number' in product.keys():
        if product['model_number'] != 'NA':
            try:
                if product['model_number'].lower() == 'does not apply':
                    product['model_number'] = 'NA'
            except AttributeError:
                pass

    for k, v in product.items():
        try:
            if v.lower() == 'does not apply':
                product[k] = 'NA'
        except AttributeError:
            pass

    product['sellers'] = []

    return product
