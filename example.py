#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, logging
from smssluzbacz import SmsApiLite, SmsApiException

log = logging.getLogger(__name__)

def main(args=sys.argv):
    if len(args) < 5 or "-h" in args or "--help" in args:
        print "Usage: ./%s <Login> <Password> <PhoneNumber> <MessageText>" % os.path.basename(args[0])
        sys.exit(2)

    try:
        api = SmsApiLite(args[1], args[2])
        api.send(args[3], args[4])
    except SmsApiException as e:
        log.error('SMS API error occured: %s', e.message)
        raise

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(message)s', level=logging.DEBUG)
    main()

