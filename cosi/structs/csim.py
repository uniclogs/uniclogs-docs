# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Csim(KaitaiStruct):
    """:field dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field src_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field dest_ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field rpt_callsign: ax25_frame.ax25_header.repeater.rpt_instance[0].rpt_callsign_raw.callsign_ror.callsign
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field l0_status: ax25_frame.payload.ax25_info.l0_status
    :field l0_acpt_cnt: ax25_frame.payload.ax25_info.l0_acpt_cnt
    :field l0_rjct_cnt: ax25_frame.payload.ax25_info.l0_rjct_cnt
    :field hw_sec_cnt: ax25_frame.payload.ax25_info.hw_sec_cnt
    :field time_tag: ax25_frame.payload.ax25_info.time_tag
    :field pld_tlm_ack_cnt: ax25_frame.payload.ax25_info.pld_tlm_ack_cnt
    :field pld_cmd_cnt: ax25_frame.payload.ax25_info.pld_cmd_cnt
    :field pld_tlm_to_cnt: ax25_frame.payload.ax25_info.pld_tlm_to_cnt
    :field pld_tlm_nak_cnt: ax25_frame.payload.ax25_info.pld_tlm_nak_cnt
    :field cmd_status: ax25_frame.payload.ax25_info.cmd_status
    :field realtime_cmd_accept_count: ax25_frame.payload.ax25_info.realtime_cmd_accept_count
    :field realtime_cmd_reject_count: ax25_frame.payload.ax25_info.realtime_cmd_reject_count
    :field stored_cmd_accept_cnt: ax25_frame.payload.ax25_info.stored_cmd_accept_cnt
    :field stored_cmd_reject_cnt: ax25_frame.payload.ax25_info.stored_cmd_reject_cnt
    :field macros_status_1: ax25_frame.payload.ax25_info.macros_status_1
    :field scrub_status_overall: ax25_frame.payload.ax25_info.scrub_status_overall
    :field scrub_count: ax25_frame.payload.ax25_info.scrub_count
    :field image_booted: ax25_frame.payload.ax25_info.image_booted
    :field image_auto_failover: ax25_frame.payload.ax25_info.image_auto_failover
    :field tai_seconds: ax25_frame.payload.ax25_info.tai_seconds
    :field time_valid: ax25_frame.payload.ax25_info.time_valid
    :field position_wrt_eci1: ax25_frame.payload.ax25_info.position_wrt_eci1
    :field position_wrt_eci2: ax25_frame.payload.ax25_info.position_wrt_eci2
    :field position_wrt_eci3: ax25_frame.payload.ax25_info.position_wrt_eci3
    :field velocity_wrt_eci1: ax25_frame.payload.ax25_info.velocity_wrt_eci1
    :field velocity_wrt_eci2: ax25_frame.payload.ax25_info.velocity_wrt_eci2
    :field velocity_wrt_eci3: ax25_frame.payload.ax25_info.velocity_wrt_eci3
    :field nadir_vector_body1: ax25_frame.payload.ax25_info.nadir_vector_body1
    :field nadir_vector_body2: ax25_frame.payload.ax25_info.nadir_vector_body2
    :field nadir_vector_body3: ax25_frame.payload.ax25_info.nadir_vector_body3
    :field sun_vector_body1: ax25_frame.payload.ax25_info.sun_vector_body1
    :field sun_vector_body2: ax25_frame.payload.ax25_info.sun_vector_body2
    :field sun_vector_body3: ax25_frame.payload.ax25_info.sun_vector_body3
    :field sun_position_wrt_eci1: ax25_frame.payload.ax25_info.sun_position_wrt_eci1
    :field sun_position_wrt_eci2: ax25_frame.payload.ax25_info.sun_position_wrt_eci2
    :field sun_position_wrt_eci3: ax25_frame.payload.ax25_info.sun_position_wrt_eci3
    :field moon_position_wrt_eci1: ax25_frame.payload.ax25_info.moon_position_wrt_eci1
    :field moon_position_wrt_eci2: ax25_frame.payload.ax25_info.moon_position_wrt_eci2
    :field moon_position_wrt_eci3: ax25_frame.payload.ax25_info.moon_position_wrt_eci3
    :field refs_valid: ax25_frame.payload.ax25_info.refs_valid
    :field esm_valid: ax25_frame.payload.ax25_info.esm_valid
    :field run_low_rate_task: ax25_frame.payload.ax25_info.run_low_rate_task
    :field q_body_wrt_eci1: ax25_frame.payload.ax25_info.q_body_wrt_eci1
    :field q_body_wrt_eci2: ax25_frame.payload.ax25_info.q_body_wrt_eci2
    :field q_body_wrt_eci3: ax25_frame.payload.ax25_info.q_body_wrt_eci3
    :field q_body_wrt_eci4: ax25_frame.payload.ax25_info.q_body_wrt_eci4
    :field body_rate1_dps: ax25_frame.payload.ax25_info.body_rate1_dps
    :field body_rate2_dps: ax25_frame.payload.ax25_info.body_rate2_dps
    :field body_rate3_dps: ax25_frame.payload.ax25_info.body_rate3_dps
    :field bad_att_timer: ax25_frame.payload.ax25_info.bad_att_timer
    :field bad_rate_timer: ax25_frame.payload.ax25_info.bad_rate_timer
    :field reinit_count: ax25_frame.payload.ax25_info.reinit_count
    :field gnc_status_1: ax25_frame.payload.ax25_info.gnc_status_1
    :field hr_cycle_safe_mode: ax25_frame.payload.ax25_info.hr_cycle_safe_mode
    :field rotisserie_rate_dps: ax25_frame.payload.ax25_info.rotisserie_rate_dps
    :field adcs_mode: ax25_frame.payload.ax25_info.adcs_mode
    :field gnc_status_2: ax25_frame.payload.ax25_info.gnc_status_2
    :field filtered_speed_rpm1: ax25_frame.payload.ax25_info.filtered_speed_rpm1
    :field filtered_speed_rpm2: ax25_frame.payload.ax25_info.filtered_speed_rpm2
    :field filtered_speed_rpm3: ax25_frame.payload.ax25_info.filtered_speed_rpm3
    :field operating_mode1: ax25_frame.payload.ax25_info.operating_mode1
    :field operating_mode2: ax25_frame.payload.ax25_info.operating_mode2
    :field operating_mode3: ax25_frame.payload.ax25_info.operating_mode3
    :field operating_mode: ax25_frame.payload.ax25_info.operating_mode
    :field star_id_step: ax25_frame.payload.ax25_info.star_id_step
    :field att_status: ax25_frame.payload.ax25_info.att_status
    :field det_timeout_count: ax25_frame.payload.ax25_info.det_timeout_count
    :field num_attitude_stars: ax25_frame.payload.ax25_info.num_attitude_stars
    :field position_error1: ax25_frame.payload.ax25_info.position_error1
    :field position_error2: ax25_frame.payload.ax25_info.position_error2
    :field position_error3: ax25_frame.payload.ax25_info.position_error3
    :field eigen_error: ax25_frame.payload.ax25_info.eigen_error
    :field time_into_search: ax25_frame.payload.ax25_info.time_into_search
    :field wait_timer: ax25_frame.payload.ax25_info.wait_timer
    :field sun_point_angle_error: ax25_frame.payload.ax25_info.sun_point_angle_error
    :field sun_point_state: ax25_frame.payload.ax25_info.sun_point_state
    :field momentum_vector_body1: ax25_frame.payload.ax25_info.momentum_vector_body1
    :field momentum_vector_body2: ax25_frame.payload.ax25_info.momentum_vector_body2
    :field momentum_vector_body3: ax25_frame.payload.ax25_info.momentum_vector_body3
    :field total_momentum_mag: ax25_frame.payload.ax25_info.total_momentum_mag
    :field duty_cycle1: ax25_frame.payload.ax25_info.duty_cycle1
    :field duty_cycle2: ax25_frame.payload.ax25_info.duty_cycle2
    :field duty_cycle3: ax25_frame.payload.ax25_info.duty_cycle3
    :field torque_rod_mode1: ax25_frame.payload.ax25_info.torque_rod_mode1
    :field torque_rod_mode2: ax25_frame.payload.ax25_info.torque_rod_mode2
    :field torque_rod_mode3: ax25_frame.payload.ax25_info.torque_rod_mode3
    :field mag_source_used: ax25_frame.payload.ax25_info.mag_source_used
    :field momentum_vector_valid: ax25_frame.payload.ax25_info.momentum_vector_valid
    :field sun_vector_body1_meas: ax25_frame.payload.ax25_info.sun_vector_body1_meas
    :field sun_vector_body2_meas: ax25_frame.payload.ax25_info.sun_vector_body2_meas
    :field sun_vector_body3_meas: ax25_frame.payload.ax25_info.sun_vector_body3_meas
    :field sun_vector_status: ax25_frame.payload.ax25_info.sun_vector_status
    :field css_invalid_count: ax25_frame.payload.ax25_info.css_invalid_count
    :field sun_sensor_used: ax25_frame.payload.ax25_info.sun_sensor_used
    :field mag_vector_body1: ax25_frame.payload.ax25_info.mag_vector_body1
    :field mag_vector_body2: ax25_frame.payload.ax25_info.mag_vector_body2
    :field mag_vector_body3: ax25_frame.payload.ax25_info.mag_vector_body3
    :field mag_invalid_count: ax25_frame.payload.ax25_info.mag_invalid_count
    :field mag_vector_valid: ax25_frame.payload.ax25_info.mag_vector_valid
    :field mag_sensor_used: ax25_frame.payload.ax25_info.mag_sensor_used
    :field imu_invalid_count: ax25_frame.payload.ax25_info.imu_invalid_count
    :field new_packet_count: ax25_frame.payload.ax25_info.new_packet_count
    :field imu_vector_valid: ax25_frame.payload.ax25_info.imu_vector_valid
    :field hr_run_count: ax25_frame.payload.ax25_info.hr_run_count
    :field hr_exec_time_ms1: ax25_frame.payload.ax25_info.hr_exec_time_ms1
    :field hr_exec_time_ms2: ax25_frame.payload.ax25_info.hr_exec_time_ms2
    :field hr_exec_time_ms3: ax25_frame.payload.ax25_info.hr_exec_time_ms3
    :field hr_exec_time_ms4: ax25_frame.payload.ax25_info.hr_exec_time_ms4
    :field hr_exec_time_ms5: ax25_frame.payload.ax25_info.hr_exec_time_ms5
    :field payload_sec_since_last_tlm: ax25_frame.payload.ax25_info.payload_sec_since_last_tlm
    :field payload_tlm_rx_count: ax25_frame.payload.ax25_info.payload_tlm_rx_count
    :field payload_tlm_ack_count: ax25_frame.payload.ax25_info.payload_tlm_ack_count
    :field payload_tlm_nak_count: ax25_frame.payload.ax25_info.payload_tlm_nak_count
    :field voltage_12p0: ax25_frame.payload.ax25_info.voltage_12p0
    :field voltage_8p0: ax25_frame.payload.ax25_info.voltage_8p0
    :field voltage_5p0: ax25_frame.payload.ax25_info.voltage_5p0
    :field voltage_3p3: ax25_frame.payload.ax25_info.voltage_3p3
    :field det_temp: ax25_frame.payload.ax25_info.det_temp
    :field det2_temp: ax25_frame.payload.ax25_info.det2_temp
    :field box1_temp: ax25_frame.payload.ax25_info.box1_temp
    :field imu_temp: ax25_frame.payload.ax25_info.imu_temp
    :field motor1_temp: ax25_frame.payload.ax25_info.motor1_temp
    :field motor2_temp: ax25_frame.payload.ax25_info.motor2_temp
    :field motor3_temp: ax25_frame.payload.ax25_info.motor3_temp
    :field bus_voltage: ax25_frame.payload.ax25_info.bus_voltage
    :field battery_voltage: ax25_frame.payload.ax25_info.battery_voltage
    :field battery_current: ax25_frame.payload.ax25_info.battery_current
    :field battery1_temp: ax25_frame.payload.ax25_info.battery1_temp
    :field battery2_temp: ax25_frame.payload.ax25_info.battery2_temp
    :field user_analog1: ax25_frame.payload.ax25_info.user_analog1
    :field user_analog2: ax25_frame.payload.ax25_info.user_analog2
    :field operating_mode: ax25_frame.payload.ax25_info.operating_mode
    :field star_id_step: ax25_frame.payload.ax25_info.star_id_step
    :field att_status: ax25_frame.payload.ax25_info.att_status
    :field det_timeout_count: ax25_frame.payload.ax25_info.det_timeout_count
    :field num_attitude_stars: ax25_frame.payload.ax25_info.num_attitude_stars
    :field cycles_since_crc_data: ax25_frame.payload.ax25_info.cycles_since_crc_data
    :field gps_lock_count: ax25_frame.payload.ax25_info.gps_lock_count
    :field gps_valid: ax25_frame.payload.ax25_info.gps_valid
    :field gps_enabled: ax25_frame.payload.ax25_info.gps_enabled
    :field macros_status_2: ax25_frame.payload.ax25_info.macros_status_2
    :field sd_minute_cur: ax25_frame.payload.ax25_info.sd_minute_cur
    :field sd_percent_used_total: ax25_frame.payload.ax25_info.sd_percent_used_total
    :field sd_percent_used_fsw: ax25_frame.payload.ax25_info.sd_percent_used_fsw
    :field sd_percent_used_soh: ax25_frame.payload.ax25_info.sd_percent_used_soh
    :field sd_percent_used_line: ax25_frame.payload.ax25_info.sd_percent_used_line
    :field sd_percent_used_tbl: ax25_frame.payload.ax25_info.sd_percent_used_tbl
    :field sd_percent_used_pay: ax25_frame.payload.ax25_info.sd_percent_used_pay
    :field sdr_tx_frames: ax25_frame.payload.ax25_info.sdr_tx_frames
    :field sdr_rx_frames: ax25_frame.payload.ax25_info.sdr_rx_frames
    :field sdr_tx: ax25_frame.payload.ax25_info.sdr_tx
    :field sdr_tx_power: ax25_frame.payload.ax25_info.sdr_tx_power
    :field sdr_rx_lock: ax25_frame.payload.ax25_info.sdr_rx_lock
    :field sdr_rx_power: ax25_frame.payload.ax25_info.sdr_rx_power
    :field sdr_rx_freq_offset: ax25_frame.payload.ax25_info.sdr_rx_freq_offset
    :field sdr_temp: ax25_frame.payload.ax25_info.sdr_temp
    :field sdr_comm_error: ax25_frame.payload.ax25_info.sdr_comm_error
    :field sq_channel: ax25_frame.payload.ax25_info.sq_channel
    :field sq_trap_count: ax25_frame.payload.ax25_info.sq_trap_count
    :field sq_temp: ax25_frame.payload.ax25_info.sq_temp
    :field aid_status: ax25_frame.payload.ax25_info.aid_status
    :field star_id_status: ax25_frame.payload.ax25_info.star_id_status
    :field power_status: ax25_frame.payload.ax25_info.power_status
    
    Attention: `rpt_callsign` cannot be accessed because `rpt_instance` is an
    array of unknown size at the beginning of the parsing process! Left an
    example in here.
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = self._root.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = self._root.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = self._root.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = self._root.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = self._root.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = self._root.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = self._root.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            _on = self.frame_length
            if _on == 131:
                self._raw_ax25_info = self._io.read_bytes_full()
                io = KaitaiStream(BytesIO(self._raw_ax25_info))
                self.ax25_info = self._root.BeaconShort(io, self, self._root)
            elif _on == 272:
                self._raw_ax25_info = self._io.read_bytes_full()
                io = KaitaiStream(BytesIO(self._raw_ax25_info))
                self.ax25_info = self._root.BeaconLong(io, self, self._root)
            else:
                self.ax25_info = self._io.read_bytes_full()

        @property
        def frame_length(self):
            if hasattr(self, '_m_frame_length'):
                return self._m_frame_length if hasattr(self, '_m_frame_length') else None

            self._m_frame_length = self._io.size()
            return self._m_frame_length if hasattr(self, '_m_frame_length') else None


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class BeaconShort(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset_0 = [None] * (4)
            for i in range(4):
                self.offset_0[i] = self._io.read_u1()

            self.imu_invalid_count = self._io.read_u2be()
            self.new_packet_count = self._io.read_u1()
            self.imu_vector_valid = self._io.read_u1()
            self.hr_run_count = self._io.read_u4be()
            self.hr_exec_time_ms1 = self._io.read_u1()
            self.hr_exec_time_ms2 = self._io.read_u1()
            self.hr_exec_time_ms3 = self._io.read_u1()
            self.hr_exec_time_ms4 = self._io.read_u1()
            self.hr_exec_time_ms5 = self._io.read_u1()
            self.payload_sec_since_last_tlm = self._io.read_u4be()
            self.payload_tlm_rx_count = self._io.read_u2be()
            self.payload_tlm_ack_count = self._io.read_u2be()
            self.payload_tlm_nak_count = self._io.read_u2be()
            self.voltage_12p0 = self._io.read_u1()
            self.voltage_8p0 = self._io.read_u1()
            self.voltage_5p0 = self._io.read_u1()
            self.voltage_3p3 = self._io.read_u1()
            self.det_temp = self._io.read_s1()
            self.det2_temp = self._io.read_s1()
            self.box1_temp = self._io.read_s2be()
            self.imu_temp = self._io.read_s2be()
            self.motor1_temp = self._io.read_s2be()
            self.motor2_temp = self._io.read_s2be()
            self.motor3_temp = self._io.read_s2be()
            self.bus_voltage = self._io.read_s2be()
            self.battery_voltage = self._io.read_u2be()
            self.battery_current = self._io.read_s2be()
            self.battery1_temp = self._io.read_s2be()
            self.battery2_temp = self._io.read_s2be()
            self.user_analog1 = self._io.read_s4be()
            self.user_analog2 = self._io.read_s4be()
            self.operating_mode = self._io.read_u1()
            self.star_id_step = self._io.read_u1()
            self.att_status = self._io.read_u1()
            self.det_timeout_count = self._io.read_u2be()
            self.num_attitude_stars = self._io.read_u1()
            self.cycles_since_crc_data = self._io.read_u4be()
            self.gps_lock_count = self._io.read_u2be()
            self.gps_valid = self._io.read_u1()
            self.gps_enabled = self._io.read_u1()
            self.macros_status_2 = self._io.read_u2be()
            self.sd_minute_cur = self._io.read_u4be()
            self.sd_percent_used_total = self._io.read_u1()
            self.sd_percent_used_fsw = self._io.read_u1()
            self.sd_percent_used_soh = self._io.read_u1()
            self.sd_percent_used_line = self._io.read_u1()
            self.sd_percent_used_tbl = self._io.read_u1()
            self.sd_percent_used_pay = self._io.read_u1()
            self.sdr_tx_frames = self._io.read_u4be()
            self.sdr_rx_frames = self._io.read_u4be()
            self.sdr_tx = self._io.read_u1()
            self.sdr_tx_power = self._io.read_s1()
            self.sdr_rx_lock = self._io.read_u1()
            self.sdr_rx_power = self._io.read_s1()
            self.sdr_rx_freq_offset = self._io.read_s4be()
            self.sdr_temp = self._io.read_s1()
            self.sdr_comm_error = self._io.read_u1()
            self.sq_channel = self._io.read_s1()
            self.sq_trap_count = self._io.read_u1()
            self.sq_temp = self._io.read_u1()
            self.aid_status = self._io.read_u2be()
            self.star_id_status = self._io.read_u1()
            self.power_status = self._io.read_u4be()


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self.ax25_info = self._io.read_bytes_full()


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = self._root.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = self._root.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = self._root.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class BeaconLong(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.offset_0 = [None] * (12)
            for i in range(12):
                self.offset_0[i] = self._io.read_u1()

            self.l0_status = self._io.read_u1()
            self.l0_acpt_cnt = self._io.read_u1()
            self.l0_rjct_cnt = self._io.read_u1()
            self.hw_sec_cnt = self._io.read_u1()
            self.offset_1 = [None] * (8)
            for i in range(8):
                self.offset_1[i] = self._io.read_u1()

            self.time_tag = self._io.read_u4be()
            self.offset_2 = [None] * (4)
            for i in range(4):
                self.offset_2[i] = self._io.read_u1()

            self.pld_tlm_ack_cnt = self._io.read_u1()
            self.pld_cmd_cnt = self._io.read_u1()
            self.pld_tlm_to_cnt = self._io.read_u1()
            self.pld_tlm_nak_cnt = self._io.read_u1()
            self.spare_end = self._io.read_u8be()
            self.cmd_status = self._io.read_u1()
            self.realtime_cmd_accept_count = self._io.read_u1()
            self.realtime_cmd_reject_count = self._io.read_u1()
            self.stored_cmd_accept_cnt = self._io.read_u1()
            self.stored_cmd_reject_cnt = self._io.read_u1()
            self.macros_status_1 = self._io.read_u2be()
            self.scrub_status_overall = self._io.read_s1()
            self.scrub_count = self._io.read_u1()
            self.image_booted = self._io.read_u1()
            self.image_auto_failover = self._io.read_u1()
            self.tai_seconds = self._io.read_f8be()
            self.time_valid = self._io.read_u1()
            self.position_wrt_eci1 = self._io.read_s4be()
            self.position_wrt_eci2 = self._io.read_s4be()
            self.position_wrt_eci3 = self._io.read_s4be()
            self.velocity_wrt_eci1 = self._io.read_s4be()
            self.velocity_wrt_eci2 = self._io.read_s4be()
            self.velocity_wrt_eci3 = self._io.read_s4be()
            self.nadir_vector_body1 = self._io.read_s2be()
            self.nadir_vector_body2 = self._io.read_s2be()
            self.nadir_vector_body3 = self._io.read_s2be()
            self.sun_vector_body1 = self._io.read_s2be()
            self.sun_vector_body2 = self._io.read_s2be()
            self.sun_vector_body3 = self._io.read_s2be()
            self.sun_position_wrt_eci1 = self._io.read_s4be()
            self.sun_position_wrt_eci2 = self._io.read_s4be()
            self.sun_position_wrt_eci3 = self._io.read_s4be()
            self.moon_position_wrt_eci1 = self._io.read_s4be()
            self.moon_position_wrt_eci2 = self._io.read_s4be()
            self.moon_position_wrt_eci3 = self._io.read_s4be()
            self.refs_valid = self._io.read_u1()
            self.esm_valid = self._io.read_u1()
            self.run_low_rate_task = self._io.read_u1()
            self.q_body_wrt_eci1 = self._io.read_s4be()
            self.q_body_wrt_eci2 = self._io.read_s4be()
            self.q_body_wrt_eci3 = self._io.read_s4be()
            self.q_body_wrt_eci4 = self._io.read_s4be()
            self.body_rate1_dps = self._io.read_s4be()
            self.body_rate2_dps = self._io.read_s4be()
            self.body_rate3_dps = self._io.read_s4be()
            self.bad_att_timer = self._io.read_u4be()
            self.bad_rate_timer = self._io.read_u4be()
            self.reinit_count = self._io.read_u4be()
            self.gnc_status_1 = self._io.read_u4be()
            self.hr_cycle_safe_mode = self._io.read_u4be()
            self.rotisserie_rate_dps = self._io.read_s2be()
            self.adcs_mode = self._io.read_u1()
            self.gnc_status_2 = self._io.read_u2be()
            self.filtered_speed_rpm1 = self._io.read_s2be()
            self.filtered_speed_rpm2 = self._io.read_s2be()
            self.filtered_speed_rpm3 = self._io.read_s2be()
            self.operating_mode1 = self._io.read_u1()
            self.operating_mode2 = self._io.read_u1()
            self.operating_mode3 = self._io.read_u1()
            self.operating_mode = self._io.read_u1()
            self.star_id_step = self._io.read_u1()
            self.att_status = self._io.read_u1()
            self.det_timeout_count = self._io.read_u2be()
            self.num_attitude_stars = self._io.read_u1()
            self.position_error1 = self._io.read_s4be()
            self.position_error2 = self._io.read_s4be()
            self.position_error3 = self._io.read_s4be()
            self.eigen_error = self._io.read_u4be()
            self.time_into_search = self._io.read_u2be()
            self.wait_timer = self._io.read_u2be()
            self.sun_point_angle_error = self._io.read_u2be()
            self.sun_point_state = self._io.read_u1()
            self.momentum_vector_body1 = self._io.read_s2be()
            self.momentum_vector_body2 = self._io.read_s2be()
            self.momentum_vector_body3 = self._io.read_s2be()
            self.total_momentum_mag = self._io.read_u2be()
            self.duty_cycle1 = self._io.read_s1()
            self.duty_cycle2 = self._io.read_s1()
            self.duty_cycle3 = self._io.read_s1()
            self.torque_rod_mode1 = self._io.read_u1()
            self.torque_rod_mode2 = self._io.read_u1()
            self.torque_rod_mode3 = self._io.read_u1()
            self.mag_source_used = self._io.read_u1()
            self.momentum_vector_valid = self._io.read_u1()
            self.sun_vector_body1_meas = self._io.read_s2be()
            self.sun_vector_body2_meas = self._io.read_s2be()
            self.sun_vector_body3_meas = self._io.read_s2be()
            self.sun_vector_status = self._io.read_u1()
            self.css_invalid_count = self._io.read_u2be()
            self.sun_sensor_used = self._io.read_u1()
            self.mag_vector_body1 = self._io.read_s2be()
            self.mag_vector_body2 = self._io.read_s2be()
            self.mag_vector_body3 = self._io.read_s2be()
            self.mag_invalid_count = self._io.read_u2be()
            self.mag_vector_valid = self._io.read_u1()
            self.mag_sensor_used = self._io.read_u1()


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            io = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = self._root.Callsign(io, self, self._root)



