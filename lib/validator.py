__author__ = 'olga'

import errors
import os
import cgi

class Validator(object):

    def __init__(self, action, data):
        self.data = data
        self.validate_method = {
            'init': self.validate_data_init,
            'charge': self.validate_data_charge,
            # new validators come here
            # 'name': self.validate_data_name,
        }
        self.validate_method[action]()


    def __validate_process(self, mandatory_field_list, optional_fields_dict={}):
        data = self.__check_mandatory_args(mandatory_field_list)
        data = self.__check_optional_args(data, optional_fields_dict)
        return data

    def __check_mandatory_args(self, name_list):
        data = {}
        try:
            # Check mandatory fields
            for each in name_list:
                data[each] = self.data[each]
        except KeyError, e:
            raise errors.MissingFieldException(e)

        return data

    def __check_optional_args(self, initial_data, options_dict):
        for option_name, default_value in options_dict:
            initial_data[option_name] = self.data.get(option_name, default_value)

        return initial_data

    # Here comes all validate methods

    def validate_data_init(self):
        mandatory_field_list = ['rs', 'merchant_transaction_id', 'description', 'amount', 'currency', 'name_on_card',
                                'street', 'zip', 'city', 'country', 'phone', 'merchant_site_url']
        optional_fields_dict = { 'user_ip': cgi.escape(os.environ["REMOTE_ADDR"]), 'state': 'NA', 'email': '',
                                 'card_bin': '', 'bin_name': '', 'bin_phone': '' }
        return self.__validate_process(mandatory_field_list, optional_fields_dict)

    def validate_data_charge(self):
        mandatory_field_list = ['init_transaction_id', 'cc', 'cvv', 'expire']
        optional_fields_dict = { 'f_extended': 5 }
        return self.__validate_process(mandatory_field_list, optional_fields_dict)


