import pickle 

ISO_currency_dict = {
    '$' : 'USD',
    '£' : 'GBP',
    '¥': 'JPY',
    '֏': 'AMD',
    '؋': 'AFN',
    '৲': 'BDT',
    '৳': 'BDT',
    '৻': 'VES',
    '૱': 'KHR',
    '௹': 'LKR',
    '฿': 'THB',
    '៛': 'KHR',
    'euro' : 'EUR',
    'euros' : 'EUR',
    'Euro' : 'EUR',
    'Euros' : 'EUR',
    'Eur' : 'EUR',
    'US$' : 'USD',
    'USD': 'USD',
    'EUR': 'EUR',
    'GBP': 'GBP',
    'JPY': 'JPY',
    'INR': 'INR',
    'AUD': 'AUD',
    'CAD': 'CAD',
    'HK': 'HKD',
    'ISK': 'ISK',
    'RMB': 'CNY',
    'SEK': 'SEK',
    'CHF': 'CHF',
    
    #'\u20a0-\u20bd': below
    '₡': 'CRC', #Costa Rican Colón
    '₤': 'ITL', # Italian Lira
    '₥': 'DEM', # German Mark
    '₦': 'NGN', # Nigerian Naira
    '₧': 'ESP', # Spanish Peseta
    '₨': 'INR', # Indian Rupee
    '₩': 'KRW', # South Korean Won
    '₪': 'ILS', # Israeli New Shekel
    '₫': 'VND', # Vietnamese Đồng
    '€': 'EUR', # Euro
    '₭': 'LAK', # Lao Kip
    '₮': 'MNT', # Mongolian Tugrik
    '₯': 'GRD', # Greek Drachma
    '₱': 'PHP', # Philippine Peso
    '₲': 'PYG', # Paraguayan Guarani
    '₴': 'UAH', # Ukrainian Hryvnia
    '₵': 'GHS', # Ghanaian Cedi    
}

    
# save dictionary to ISOcurrency.pkl file
with open('ISOcurrency.pkl', 'wb') as iso_file:
    pickle.dump(ISO_currency_dict, iso_file)

iso_file.close()