#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging, urllib

log = logging.getLogger(__name__)

class SmsApiLite():
    ''' Implements 'Lite' version of sms.sluzba.cz HTTP API
    The only possibility of lite version is to send POST/GET request to send SMS
    with no advanced options and operations.
    '''
    
    # number of characters after message will be automatically truncated
    truncate_limit = 459
    
    def __init__(self, login, password):
        ''' Initialize new lite client

        Args:
        login: Username for sms.sluzba.cz account
        password: Password for account
        '''
        self._login = login
        self._password = password
        log.debug('Initiated %s for user: %s', self.__class__.__name__, self._login)

    def send(self, number, text, use_https=True, use_post=True):
        ''' Send SMS, raise SmsApiException if something other than 200 is returned

        Args:
        number: phone number, international or 9-digit format.
        text: SMS message text.
        use_https: If HTTPS should be used. True by default.
        use_post: If HTTP POST method should be used instead of GET. True by default.
        '''
        log.info('Sending SMS to number: %s, message text: %s', number, text)
        url = '%s://smsgateapi.sluzba.cz/apilite20/sms' % ('https' if use_https else 'http')
        
        params = urllib.urlencode({
                'login': self._login,
                'password': self._password,
                'number': number,
                'text': text
                })

        if not use_post:
            # use HTTP GET to query API
            url = '?'.join([url, params])
            
        log.debug('Use HTTPS: %s, Use HTTP POST: %s, API URL: %s', use_https, use_post, url)

        if text and len(text) > self.truncate_limit:
            log.warn('Message text exceeds %d characters and will be automatically truncated', self.truncate_limit)

        if use_post:
            # HTTP POST, explicit params
            sock = urllib.urlopen(url, params)
        else:
            # HTTP GET, params present in URl
            sock = urllib.urlopen(url)

        response = sock.read()
        sock.close()

        if response:
            log.debug('Response received: %s', response)
            if response[0:3] == '200':
                log.info('SMS sent successfully')
            else:
                raise SmsApiException(response) 
                
        else:
            raise SmsApiException('Unexpected empty response')

class SmsApiException(Exception):
    """Raised when SMS API operation failed"""
    def __init__(self, message):
        self.message = message
