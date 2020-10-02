#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test Rx
# Author: ryan
# GNU Radio version: 3.8.1.0

from gnuradio import blocks
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


class test_rx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Test Rx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.samp_per_sym = samp_per_sym = 5

        ##################################################
        # Blocks
        ##################################################
        self.satellites_nrzi_decode_0 = satellites.nrzi_decode()
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.limesdr_source_0 = limesdr.source('', 0, '', False)


        self.limesdr_source_0.set_sample_rate(samp_rate)


        self.limesdr_source_0.set_center_freq(100e6, 0)

        self.limesdr_source_0.set_bandwidth(1.5e6, 0)


        self.limesdr_source_0.set_digital_filter(samp_rate, 0)


        self.limesdr_source_0.set_gain(1, 0)


        self.limesdr_source_0.set_antenna(255, 0)


        self.limesdr_source_0.calibrate(2.5e6, 0)
        self.digital_descrambler_bb_0 = digital.descrambler_bb(0x21, 0, 16)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.blocks_message_debug_0, 'print_pdu'))
        self.connect((self.blocks_complex_to_float_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.satellites_nrzi_decode_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.digital_descrambler_bb_0, 0), (self.satellites_hdlc_deframer_0, 0))
        self.connect((self.limesdr_source_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.satellites_nrzi_decode_0, 0), (self.digital_descrambler_bb_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.limesdr_source_0.set_digital_filter(self.samp_rate, 0)
        self.limesdr_source_0.set_digital_filter(self.samp_rate, 1)

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.digital_clock_recovery_mm_xx_0.set_omega(self.samp_per_sym*(1+0.0))





def main(top_block_cls=test_rx, options=None):
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
