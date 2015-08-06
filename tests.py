# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, os, unittest
from patron_api import PatronAPI


## logging
LOG_PATH = unicode( os.environ['PAPI__LOG_PATH'], 'utf-8' )
logging.basicConfig(
    filename=LOG_PATH, level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
    )
logger = logging.getLogger(__name__)
logger.debug( 'log setup' )


class PatronApiTests( unittest.TestCase ):

    def setUp(self):
        self.PATRON_BARCODE = unicode( os.environ['PAPI__TEST_PATRON_BARCODE'], 'utf-8' )

    def test_barcode(self):
        """ Tests response is json of hashes. """
        papi = PatronAPI()
        output = papi.grab_data( self.PATRON_BARCODE )
        logger.debug( 'output, `%s`' % output )
        d = json.loads( output )
        self.assertEqual(
            self.PATRON_BARCODE,
            d['p_barcode']['converted_value']
            )


if __name__ == '__main__':
    unittest.main()
