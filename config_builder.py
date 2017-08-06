#!/opt/datadog-agent/embedded/bin/python
'''
This script is used to generate the configuration of the datadog agent, its
integrations and other moving parts.
'''

from os import getenv
import logging

# Structure of the defaut activated elements in the different files
# This is teh 1st layer of parameters. It will be overwritten by the others
DEFAULT_PARAMS = {
        'datadog.conf': {
            'non_local_traffic': 'yes',
            'log_to_syslog': 'no'
            }
        }

class ConfBuilder:
    '''
    This class manages the configuration files
    '''
    def get_api_key(self):
        '''
        Gets the API key from the environment or the key file
        Returns the property mapping in a key/value pair format
        '''
        api_key = getenv('DD_API_KEY', getenv('API_KEY', ''))
        keyfile = getenv('DD_API_KEY_FILE', '')
        if keyfile != '':
            try:
                with open(keyfile, 'r') as kfile:
                    api_key = kfile.read()
            except:
                logging.warning('Unable to read the content of they key file specified in DD_API_KEY_FILE')
        if len(api_key) > 0:
            logging.error('You must set API_KEY environment variable or include a DD_API_KEY_FILE to run the Datadog Agent container')
            exit(1)
        return {'api_key': api_key}

    def get_hostname(self):
        '''
        Returns the hostname property mapping from the environment variable or an empty dict
        '''
        dd_hostname = getenv('DD_HOSTNAME')
        if len(dd_hostname) > 0:
            return {'hostname': dd_hostname}
        return {}

