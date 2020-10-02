#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test Tx
# Author: ryan
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import limesdr
import satellites


class test_tx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Tx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.samp_per_sym = samp_per_sym = 5

        ##################################################
        # Blocks
        ##################################################
        self.satellites_nrzi_encode_0 = satellites.nrzi_encode()
        self.satellites_hdlc_framer_0 = satellites.hdlc_framer(preamble_bytes=50, postamble_bytes=7)
        self.limesdr_sink_0 = limesdr.sink('', 0, '', '')


        self.limesdr_sink_0.set_sample_rate(samp_rate)


        self.limesdr_sink_0.set_center_freq(100e6, 0)

        self.limesdr_sink_0.set_bandwidth(5e6, 0)


        self.limesdr_sink_0.set_digital_filter(samp_rate, 0)


        self.limesdr_sink_0.set_gain(1, 0)


        self.limesdr_sink_0.set_antenna(255, 0)


        self.limesdr_sink_0.calibrate(2.5e6, 0)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x0, 16)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, samp_per_sym)
        self.blocks_random_pdu_0 = blocks.random_pdu(50, 200, 0xFF, 2)
        self.blocks_pdu_to_tagged_stream_0_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.5)
        self.blocks_message_debug_0_0 = blocks.message_debug()
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-0.5)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.blocks_message_debug_0_0, 'print_pdu'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.satellites_hdlc_framer_0, 'in'))
        self.msg_connect((self.satellites_hdlc_framer_0, 'out'), (self.blocks_pdu_to_tagged_stream_0_0, 'pdus'))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.satellites_nrzi_encode_0, 0))
        self.connect((self.satellites_nrzi_encode_0, 0), (self.blocks_repeat_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.limesdr_sink_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_sink_0.set_digital_filter(self.samp_rate, 1)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.blocks_repeat_0.set_interpolation(self.samp_per_sym)





def main(top_block_cls=test_tx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
