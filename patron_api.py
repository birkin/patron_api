# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json, logging, pprint, re
import requests


logger = logging.getLogger(__name__)


class PatronAPI( object ):
    """ Grabs & parses patron-api output. """

    def grab_data( self, barcode ):
        """ Grabs and parses patron-api html. """
        html = self.grab_raw_data( barcode )
        d = self.parse_data( html )
        output = json.dumps( d, sort_keys=True, indent=2 )
        return output

    def grab_raw_data( self, barcode ):
        """ Makes http request.
            Called by grab_data() """
        temp_data = """
            <HTML><BODY>
            PATRN NAME[pn]=Demolast, Demofirst<BR>
            P BARCODE[pb]=1 2222 33333 4444<BR>
            </BODY></HTML>
            """.strip()
        return temp_data

    def parse_data( self, html ):
        """ Converts html to dct.
            Called by grab_data() """
        logger.debug( 'html, `%s`' % html )
        lines = html.split( '\n' )
        logger.debug( 'lines, `%s`' % pprint.pformat(lines) )
        trimmed_lines = self.trim_lines( lines )
        d = {}
        for line in trimmed_lines:
            ( key, value ) = self.parse_line( line )
            d[key] = value
        return d

    def trim_lines( self, lines ):
        """ Trims and slices lines.
            Called by parse_data() """
        trimmed_lines = []
        sliced_lines = lines[1:-1]
        for line in sliced_lines:
            trimmed_lines.append( line.strip() )
        logger.debug( 'trimmed_lines, `%s`' % pprint.pformat(trimmed_lines) )
        return trimmed_lines

    def parse_line( self, line ):
        """ Parses line into key and dct-value.
            Called by parse_data() """
        regex_pattern = """
            Aa        # label
            """
        search_result = re.search( regex_pattern, line, re.VERBOSE )
        logger.debug( 'search_result, `%s`' % search_result )
        return search_result





    # end class PatronAPI
