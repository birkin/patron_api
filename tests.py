# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, os, unittest
from p_api import PatronAPI


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
        self.PATRON_BARCODE = unicode( os.environ['PAPI__TEST_PATRON_BARCODE'] )
        defaults = { 'PATRON_API_URL_PATTERN': unicode(os.environ['PAPI__PATRON_API_URL_PATTERN']) }
        self.papi = PatronAPI( defaults )

    def test_grab_data(self):
        """ Tests response is json of hashes.
            May not be able to run this test locally due to port/ip filters. """
        output = self.papi.grab_data( self.PATRON_BARCODE )
        logger.debug( 'output, `%s`' % output )
        d = json.loads( output )
        self.assertEqual(
            self.PATRON_BARCODE,
            d['p_barcode']['converted_value']
            )

    def test_parse_line(self):
        """ Tests that dict is returned for line. """
        line = 'P TYPE[p47]=7<BR>'
        self.assertEqual(
            { u'label': u'P TYPE', u'code': u'p47', u'value': u'7' },
            self.papi.parse_line( line )
            )
        ## problem line
        line = 'LINK REC[p^]=in<BR>'
        self.assertEqual(
            { u'label': u'LINK REC', u'code': u'p^', u'value': u'in' },
            self.papi.parse_line( line )
            )

    def test_parse_label(self):
        """ Tests regex perception of number in label. """
        ## text with space
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
        ## text with hyphen
        line = 'E-MAIL[pe]=First_Last@brown.edu<BR>'
        self.assertEqual(
            'E-MAIL',
            self.papi.parse_label( line )
            )

    def test_parse_code(self):
        """ Tests code extract from updated_line. """
        ## exclamation point
        updated_line = '[p!]=p<BR>'
        self.assertEqual(
            ( '[p!]', 'p!' ),  # ( sliced_code, code )
            self.papi.parse_code( updated_line )
            )
        ## caret
        updated_line = '[p^]=in<BR>'
        self.assertEqual(
            ( '[p^]', 'p^' ),  # ( sliced_code, code )
            self.papi.parse_code( updated_line )
            )

    def test_parse_value(self):
        """ Tests simple slice for value. """
        updated_line = '=First_Last@brown.edu<BR>'
        self.assertEqual(
            'First_Last@brown.edu',
            self.papi.parse_value( updated_line )
            )



if __name__ == '__main__':
    unittest.main()
