"""
    Spirent Network Emulator ReST Client
    This module is Python ReST client for SNE ReST API
"""


__Version_ = '0.2'
__Author__ = 'Poornima Wari'


('\n'
 '    ----------------------\n'
 '    Modification History\n'
 '    --------------------\n'
 '    0.2 : 8/12/2021 Poornima Wari\n'
 '          - updated error message with http error content\n'
 '                                 \n '     
 '    0.1 : 5/5/2021 Poornima Wari\n'
 '          - Initial Code\n'
 '           \n'
 '\n')


import requests                      # we need to to interact with SNE ReST
import os                            # we need it for log path
import logging                       # we need it for logger messages
import json                          # we need this for json format
import sys                           # we need it to trace the error
from datetime import datetime        # we need it for creating log folder
import platform                      # we need it to log the python version
import functools                    # we need it for log decorator
# python3 supports urllib.parse and python2 supports urlparse
# we need this is to build the url
try:
    from urllib.parse import urlunsplit
except ImportError:
    from urlparse import urlunsplit  # ignore, if it shows red for python3, this line for python2


# Helper functions
# define wrapper class , we will call our function in that
def log_decorator(function):
    """
        This is to log the request and return result of the http verbs
    :param function: function object
    :return: logs the start and end results
    """
    @functools.wraps(function)
    def inner_function(*args, **kwargs):
        # log beginning of function and agrs / kwargs if any
        logging.info('starting method (' + function.__name__ + ') arguments ' + str(args) + ' ' + str(kwargs))
        try:
            # get the return value from the function
            value = function(*args, **kwargs)
            logging.info('return value from method (' + function.__name__ + ') ' + str(value))
        except:
            # log exception in-case
            logging.error('Error: {}.{},line:{}'.format(sys.exc_info()[0], sys.exc_info()[1],
                                             sys.exc_info()[2].tb_lineno))
            raise
        return value
    return inner_function

def process_response(raw_response):
    """
    Process's the response and returns format

    :param raw_response: http request response
    :return: retuen resonse in json or text based on the format or just return content

    """

    # Note Currently SNE supports text or application/json response
    # get the content - type
    content_type = raw_response.headers.get('content-type')
    result = ''
    if 'text' in content_type:
        result = raw_response.text
    elif 'application/json' in content_type:
        result = raw_response.json()
    else:
        result = raw_response.content

    return result


class SpirentNetworkEmulator:
    """
        This module is Python ReST Client for Spirent Network Emulator
            Supports HTTP-Verbs : get,put,post and delete
        Command Syntax/Example :

            sne_object = SpirentNetworkEmulator(sne_ip,sne_username)

            1: Get the Build version
                end_point = '/instrument/software/buildversion'
                sne_object.get(end_point)

            2: Get the maps
                end_point = '/maps'
                sne_object.get(end_point)

            3: Load map.json file
                end_point = '/maps/json?shareWithAll=true'
                sne_object.post(end_point,file=file_name)

            4: Load the map into SNE, ready to be started
                end_point = '/maps/<mapid>/load'
                sne_object.post(end_point)

            5: Star the map
                end_point = '/maps/<mapId>/start'
                sne_object.put(end_point)

            6: Updates the current settings of a packet drop impairment
                end_point = '/maps/<MapID>/impairments/<ImpID>/packetdrop'
                true,false = 'true','false' # SNE is case sensitive
                drop_payload = {
                      "packetDropMode": "standardDropMode",
                      "enabled": true,
                      "timeConstraints": {
                        "enableTimeConstraints": false,
                        "startDelay": 1000,
                        "duration": 5000
                      },
                      "packetDropSettings": {
                        "standardDropMode": {
                          "packetDropCount": drop_count,
                          "perPacketCount": 100,
                          "dropMethod": "dropEvenly"
                        }
                      }
                    }
                sne_object.put(end_point, payload=drop_payload)

            7: Deletes a loaded capture replay file
                end_point = '/files/capturereplay/<pcapFile>'
                sne_object.delete(end_point)
    """
    def __init__(self, sne_ip, username, password='', log_level="INFO", log_path=None):

        self.log_path = log_path
        self.username = username
        self.password = password
        self.sne_ip = sne_ip
        self.log_path = os.path.abspath('logs')

        # get the current time and date to create logs
        now = datetime.now()
        time_date = now.strftime("%H%M%S%m%d%Y")
        latest_log = time_date

        # override with user specified path
        if log_path:
            self.log_path = os.path.join(log_path, 'logs')

        # create log folder if it doesnt exist
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

        self.log_path = os.path.expanduser(self.log_path)

        # set the log file name
        self.log_file = os.path.join(self.log_path, 'sne_rest_client_' + latest_log + '.log')

        # set the logger
        if log_level.lower() == 'debug':
            self.log_level = 'DEBUG'
        elif log_level.lower() == 'error':
            self.log_level = 'ERROR'
        elif log_level.lower() == 'warning':
            self.log_level = 'WARNING'
        elif log_level.lower() == 'critical':
            self.log_level = 'CRITICAL'
        else:
            self.log_level = 'INFO'

        # set the logging format
        logging.basicConfig(filename=self.log_file, filemode='w', level=self.log_level, format='%(asctime)s %('
                                                                                               'levelname)-8s %('
                                                                                               'message)s')

        # creating logger object
        logger = logging.getLogger(self.log_file)

        # log the python version
        logging.info("Python verstion " + platform.python_version())
        logging.info("Executing Spirent Network Emulator __init__")
        # suppress all logging messages from deeply nested module but the critical
        # get to the root and set it to critical

        logging.getLogger('requests').setLevel(logging.CRITICAL)

        # build api -> ex http://<SNE_IP>/api
        self.scheme = 'http'
        self.__url = urlunsplit((self.scheme, self.sne_ip, 'api', '', ''))

        logging.info('URL : '+self.__url)

        # authorize SNE
        logging.info('Authorizing SNE_IP :'+self.sne_ip+' username :'+self.username+' password :'+self.password)

        # we need bearer token for authorization
        self.__bearer_token = None

        # username password dictionary
        self.__data = json.dumps({
            "username": self.username,
            "password": self.password
        })

        # header dictionary
        self.__headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # establish session and store the handle
        self.__session = requests.session()

        # authorize the session
        raw_response = self.__session.post(self.__url + '/users/authenticate', headers=self.__headers, data=self.__data)

        # error handling in case of failure
        if not raw_response.ok:
            try :
                error_content = raw_response.content
                raw_response.raise_for_status()
            except Exception as error_massage:
                logging.critical('Failed to Authorize' + str(error_massage) + ' ' + str(error_content))
                raise requests.HTTPError(error_massage, error_content)


        if raw_response.status_code == 200:
            logging.info('Successfully Authorized :) ')

            # extract the authentication token
            self.__bearer_token = raw_response.json()['token']

            # update authorization token to the session header
            self.__session.headers.update(Authorization='Bearer ' + self.__bearer_token)

        # get the SNE version
        sne_version = self.__session.get(self.__url+'/instrument/software/buildversion')
        logging.info('SNE Version : ' + sne_version.json())

    @log_decorator
    def get(self, end_points, **kwargs):
        """
        :param end_points: end points
        :param **kwargs: key:value
        :return: result in json or text
        """
        result = self.process_request('get', end_points, **kwargs)
        return result

    @log_decorator
    def post(self, end_points, **kwargs):
        """
        :param end_points: end point
        :param **kwargs: key:value Ex file=filename or payload=dictionary
        :return: result in json or text
        """
        result = self.process_request('post', end_points, **kwargs)
        return result

    @log_decorator
    def put(self, end_points, **kwargs):
        """
        :param end_points: end point
        :param **kwargs: key:value Ex : payload = dictionary
        :return: result in json or text
        """
        result = self.process_request('put', end_points, **kwargs)
        return result

    @log_decorator
    def delete(self, end_points, **kwargs):
        """
        :param end_points: end points
        :param payload: data
        :return:raw_responsejson format
        """
        result = self.process_request('delete', end_points, **kwargs)
        return result

    def process_request(self, httpverb, endpoints, **kwargs):
        """
        process's the http method and return result (fail or pass)

        :param httpverb: method to process
        :param endpoints: url endpoints
        :param kwargs: key values : ex data = {} or payload = {} or files = []
        :return: returns the response or the error
        """

        # check if endpoints starts with '/' and update if not present
        if not endpoints.startswith('/'):
            endpoints = '/' + endpoints

        # we have already added api to __url
        if endpoints.startswith('/api'):
            endpoints = endpoints.replace('/api','')

        # add endpoints to the base url
        url = self.__url + endpoints
        #logging.info('Processing method -> ' + httpverb + '-> url :' + url)

        payload = {}
        file_data = None
        raw_response = None

        # check for the payload and files in kwargs
        if len(list(kwargs.keys())) > 0:
            for key1 in kwargs.keys():
                if 'payload' in key1 or 'data' in key1:
                    # convert python object to json string
                    payload = json.dumps(kwargs[key1])
                elif 'file' in key1:
                    # in case you want to post the file
                    file_name = kwargs[key1]
                    file_data = [('mapFileFormFile', (file_name, open(file_name, 'rb'), 'application/json'))]

        # process the http verb
        if httpverb.lower() == 'get':
            raw_response = self.__session.get(url)
        elif httpverb.lower() == 'put':
            self.__session.headers.update(self.__headers)
            raw_response = self.__session.put(url, data=payload)
        elif httpverb.lower() == 'post':
            raw_response = self.__session.post(url, data=payload, files=file_data)
        elif httpverb.lower() == 'delete':
            raw_response = self.__session.delete(url)
        else:
            # looks like method did not match, raise exception
            logging.error('ERROR : The HTTP-VERB ' + httpverb + ' not found. Must be "GET PUT POST and DELETE"')
            raise ValueError('ERROR : The HTTP-VERB ' + httpverb + ' not found. Must be "GET PUT POST and DELETE"')

        if not raw_response.ok:
            # ERROR handling
            try :
                raw_response.raise_for_status()
            except Exception as error_massage:
                error_content = raw_response.content
                logging.critical(str(error_massage) + ' ' + str(error_content))
                raise requests.HTTPError(error_massage, error_content)

        # process the response
        end_result = process_response(raw_response)
        return end_result

    # This is internal use only. DO NOT TRY this command
    # delete url http://10.140.96.99/webui/maps?mapId=3696f066-90fd-498b-8abb-a2cb23687167
    @log_decorator
    def delete_map(self, end_points):
        delete_url = urlunsplit((self.scheme, self.sne_ip, 'webui/maps','mapId='+end_points, ''))
        logging.info('Processing delete_url')

        return self.__session.delete(delete_url)

def main():
    #rest_client = SpirentNetworkEmulator('10.140.96.99', 'pwari', log_path='/Users/pwari/workspace',log_level='debug')
    rest_client = SpirentNetworkEmulator('10.140.96.99', 'pwari')
    response = rest_client.get('instrument/software/buildversion')
    return response

if __name__ == "__main__":
    print(main())