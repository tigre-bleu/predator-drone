#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: GFSK Receiver
# Author: Gabriel Mariano Marcelino
# Generated: Tue Feb 12 09:08:07 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class gfsk_rx(grc_wxgui.top_block_gui):

    def __init__(self, default_bandwidth=1e6, default_baud=450000, default_bin_file_sink="/tmp/rx_data.bin", default_freq=2410e6, default_gain=1, default_ip_0='127.0.0.1', default_port_0=5000, default_samp=1000000, sdr_dev="uhd=0"):
        grc_wxgui.top_block_gui.__init__(self, title="GFSK Receiver")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.default_bandwidth = default_bandwidth
        self.default_baud = default_baud
        self.default_bin_file_sink = default_bin_file_sink
        self.default_freq = default_freq
        self.default_gain = default_gain
        self.default_ip_0 = default_ip_0
        self.default_port_0 = default_port_0
        self.default_samp = default_samp
        self.sdr_dev = sdr_dev

        ##################################################
        # Variables
        ##################################################
        self.sdr_rf_gain = sdr_rf_gain = 10
        self.sdr_if_gain = sdr_if_gain = 20
        self.sdr_bb_gain = sdr_bb_gain = 20
        self.samp_rate = samp_rate = default_samp
        self.freq = freq = default_freq
        self.baudrate = baudrate = default_baud
        self.bandwidth = bandwidth = default_bandwidth

        ##################################################
        # Blocks
        ##################################################
        _samp_rate_sizer = wx.BoxSizer(wx.VERTICAL)
        self._samp_rate_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_samp_rate_sizer,
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	label='Sample rate [S/s]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._samp_rate_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_samp_rate_sizer,
        	value=self.samp_rate,
        	callback=self.set_samp_rate,
        	minimum=100e3,
        	maximum=4e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_samp_rate_sizer, 1, 1, 1, 1)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label='Frequency [Hz]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=2400e6,
        	maximum=2515e6,
        	num_steps=115,
        	style=wx.SL_VERTICAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_freq_sizer, 0, 1, 1, 1)
        _bandwidth_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bandwidth_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	label='Bandwidth [Hz]',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._bandwidth_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	minimum=0,
        	maximum=10e6,
        	num_steps=60,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_bandwidth_sizer, 5, 1, 1, 1)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=default_freq,
        	y_per_div=10,
        	y_divs=9,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=default_samp,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=0.5,
        	title='',
        	peak_hold=False,
        	win=window.hanning,
        	size=([800,100]),
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 0, 0, 7, 1)
        self.uhd_usrp_source_0_0 = uhd.usrp_source(
        	",".join(("serial=307038D", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0_0.set_gain(0, 0)
        self.uhd_usrp_source_0_0.set_bandwidth(bandwidth, 0)
        _sdr_rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sdr_rf_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sdr_rf_gain_sizer,
        	value=self.sdr_rf_gain,
        	callback=self.set_sdr_rf_gain,
        	label='RF gain [dB]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._sdr_rf_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sdr_rf_gain_sizer,
        	value=self.sdr_rf_gain,
        	callback=self.set_sdr_rf_gain,
        	minimum=0,
        	maximum=20,
        	num_steps=20,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_sdr_rf_gain_sizer, 2, 1, 1, 1)
        _sdr_if_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sdr_if_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sdr_if_gain_sizer,
        	value=self.sdr_if_gain,
        	callback=self.set_sdr_if_gain,
        	label='IF gain [dB]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._sdr_if_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sdr_if_gain_sizer,
        	value=self.sdr_if_gain,
        	callback=self.set_sdr_if_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=30,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_sdr_if_gain_sizer, 3, 1, 1, 1)
        _sdr_bb_gain_sizer = wx.BoxSizer(wx.VERTICAL)
        self._sdr_bb_gain_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_sdr_bb_gain_sizer,
        	value=self.sdr_bb_gain,
        	callback=self.set_sdr_bb_gain,
        	label='BB gain [dB]',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._sdr_bb_gain_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_sdr_bb_gain_sizer,
        	value=self.sdr_bb_gain,
        	callback=self.set_sdr_bb_gain,
        	minimum=0,
        	maximum=30,
        	num_steps=30,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.GridAdd(_sdr_bb_gain_sizer, 4, 1, 1, 1)
        self._baudrate_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.baudrate,
        	callback=self.set_baudrate,
        	label='Baudrate [bps]',
        	converter=forms.int_converter(),
        )
        self.GridAdd(self._baudrate_text_box, 6, 1, 1, 1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_default_bandwidth(self):
        return self.default_bandwidth

    def set_default_bandwidth(self, default_bandwidth):
        self.default_bandwidth = default_bandwidth
        self.set_bandwidth(self.default_bandwidth)

    def get_default_baud(self):
        return self.default_baud

    def set_default_baud(self, default_baud):
        self.default_baud = default_baud
        self.set_baudrate(self.default_baud)

    def get_default_bin_file_sink(self):
        return self.default_bin_file_sink

    def set_default_bin_file_sink(self, default_bin_file_sink):
        self.default_bin_file_sink = default_bin_file_sink

    def get_default_freq(self):
        return self.default_freq

    def set_default_freq(self, default_freq):
        self.default_freq = default_freq
        self.set_freq(self.default_freq)
        self.wxgui_fftsink2_0.set_baseband_freq(self.default_freq)

    def get_default_gain(self):
        return self.default_gain

    def set_default_gain(self, default_gain):
        self.default_gain = default_gain

    def get_default_ip_0(self):
        return self.default_ip_0

    def set_default_ip_0(self, default_ip_0):
        self.default_ip_0 = default_ip_0

    def get_default_port_0(self):
        return self.default_port_0

    def set_default_port_0(self, default_port_0):
        self.default_port_0 = default_port_0

    def get_default_samp(self):
        return self.default_samp

    def set_default_samp(self, default_samp):
        self.default_samp = default_samp
        self.set_samp_rate(self.default_samp)
        self.wxgui_fftsink2_0.set_sample_rate(self.default_samp)

    def get_sdr_dev(self):
        return self.sdr_dev

    def set_sdr_dev(self, sdr_dev):
        self.sdr_dev = sdr_dev

    def get_sdr_rf_gain(self):
        return self.sdr_rf_gain

    def set_sdr_rf_gain(self, sdr_rf_gain):
        self.sdr_rf_gain = sdr_rf_gain
        self._sdr_rf_gain_slider.set_value(self.sdr_rf_gain)
        self._sdr_rf_gain_text_box.set_value(self.sdr_rf_gain)

    def get_sdr_if_gain(self):
        return self.sdr_if_gain

    def set_sdr_if_gain(self, sdr_if_gain):
        self.sdr_if_gain = sdr_if_gain
        self._sdr_if_gain_slider.set_value(self.sdr_if_gain)
        self._sdr_if_gain_text_box.set_value(self.sdr_if_gain)

    def get_sdr_bb_gain(self):
        return self.sdr_bb_gain

    def set_sdr_bb_gain(self, sdr_bb_gain):
        self.sdr_bb_gain = sdr_bb_gain
        self._sdr_bb_gain_slider.set_value(self.sdr_bb_gain)
        self._sdr_bb_gain_text_box.set_value(self.sdr_bb_gain)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self._samp_rate_slider.set_value(self.samp_rate)
        self._samp_rate_text_box.set_value(self.samp_rate)
        self.uhd_usrp_source_0_0.set_samp_rate(self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.uhd_usrp_source_0_0.set_center_freq(self.freq, 0)

    def get_baudrate(self):
        return self.baudrate

    def set_baudrate(self, baudrate):
        self.baudrate = baudrate
        self._baudrate_text_box.set_value(self.baudrate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self._bandwidth_slider.set_value(self.bandwidth)
        self._bandwidth_text_box.set_value(self.bandwidth)
        self.uhd_usrp_source_0_0.set_bandwidth(self.bandwidth, 0)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "-w", "--default-bandwidth", dest="default_bandwidth", type="eng_float", default=eng_notation.num_to_str(1e6),
        help="Set default_bandwidth [default=%default]")
    parser.add_option(
        "-b", "--default-baud", dest="default_baud", type="intx", default=450000,
        help="Set default_baud [default=%default]")
    parser.add_option(
        "-o", "--default-bin-file-sink", dest="default_bin_file_sink", type="string", default="/tmp/rx_data.bin",
        help="Set default_bin_file_sink [default=%default]")
    parser.add_option(
        "-f", "--default-freq", dest="default_freq", type="eng_float", default=eng_notation.num_to_str(2410e6),
        help="Set default_freq [default=%default]")
    parser.add_option(
        "-g", "--default-gain", dest="default_gain", type="intx", default=1,
        help="Set default_gain [default=%default]")
    parser.add_option(
        "-i", "--default-ip-0", dest="default_ip_0", type="string", default='127.0.0.1',
        help="Set default_ip_0 [default=%default]")
    parser.add_option(
        "-p", "--default-port-0", dest="default_port_0", type="intx", default=5000,
        help="Set default_port_0 [default=%default]")
    parser.add_option(
        "-s", "--default-samp", dest="default_samp", type="eng_float", default=eng_notation.num_to_str(1000000),
        help="Set default_samp [default=%default]")
    parser.add_option(
        "-d", "--sdr-dev", dest="sdr_dev", type="string", default="uhd=0",
        help="Set sdr_dev [default=%default]")
    return parser


def main(top_block_cls=gfsk_rx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls(default_bandwidth=options.default_bandwidth, default_baud=options.default_baud, default_bin_file_sink=options.default_bin_file_sink, default_freq=options.default_freq, default_gain=options.default_gain, default_ip_0=options.default_ip_0, default_port_0=options.default_port_0, default_samp=options.default_samp, sdr_dev=options.sdr_dev)
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
