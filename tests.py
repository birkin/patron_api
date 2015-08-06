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
        self.papi = PatronAPI()

    def test_grab_data(self):
        """ Tests response is json of hashes. """
        output = self.papi.grab_data( self.PATRON_BARCODE )
        logger.debug( 'output, `%s`' % output )
        d = json.loads( output )
        self.assertEqual(
            self.PATRON_BARCODE,
            d['p_barcode']['converted_value']
            )

    def test_parse_label(self):
        """ Tests regex perception of number in label. """
        ## all text
        line = 'P TYPE[p47]=7<BR>'
        self.assertEqual(
            'P TYPE',
            self.papi.parse_label( line )
            )
        ## numeral
        line = 'PCODE1[p44]=-<BR>'
        self.assertEqual(
            'PCODE1',
            self.papi.parse_label( line )
            )

    def test_parse_code(self):
        """ Tests regex perception of exclamation point. """
        updated_line = '[p!]=p<BR>'
        self.assertEqual(
            ( '[p!]', 'p!' ),  # ( sliced_code, code )
            self.papi.parse_code( updated_line )
            )




if __name__ == '__main__':
    unittest.main()
