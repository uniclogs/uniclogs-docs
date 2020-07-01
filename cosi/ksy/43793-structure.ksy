---
meta:
  id: csim
  title: CSIM-FD decoder struct
  endian: be
doc: |
  :field dest_callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
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

seq:
  - id: ax25_frame
    type: ax25_frame
    doc-ref: 'https://www.tapr.org/pub_ax25.html'

types:
  ax25_frame:
    seq:
      - id: ax25_header
        type: ax25_header
      - id: payload
        type:
          switch-on: ax25_header.ctl & 0x13
          cases:
            0x03: ui_frame
            0x13: ui_frame
            0x00: i_frame
            0x02: i_frame
            0x10: i_frame
            0x12: i_frame
            # 0x11: s_frame

  ax25_header:
    seq:
      - id: dest_callsign_raw
        type: callsign_raw
      - id: dest_ssid_raw
        type: ssid_mask
      - id: src_callsign_raw
        type: callsign_raw
      - id: src_ssid_raw
        type: ssid_mask
      - id: repeater
        type: repeater
        if: (src_ssid_raw.ssid_mask & 0x01) == 0
        doc: 'Repeater flag is set!'
      - id: ctl
        type: u1

  repeater:
    seq:
      - id: rpt_instance
        type: repeaters
        repeat: until
        repeat-until: ((_.rpt_ssid_raw.ssid_mask & 0x1) == 0x1)
        doc: 'Repeat until no repeater flag is set!'

  repeaters:
    seq:
      - id: rpt_callsign_raw
        type: callsign_raw
      - id: rpt_ssid_raw
        type: ssid_mask

  callsign_raw:
    seq:
      - id: callsign_ror
        process: ror(1)
        size: 6
        type: callsign

  callsign:
    seq:
      - id: callsign
        type: str
        encoding: ASCII
        size: 6

  ssid_mask:
    seq:
      - id: ssid_mask
        type: u1
    instances:
      ssid:
        value: (ssid_mask & 0x0f) >> 1

  i_frame:
    seq:
      - id: pid
        type: u1
      - id: ax25_info
        size-eos: true

  ui_frame:
    seq:
      - id: pid
        type: u1
      - id: ax25_info
        type:
          switch-on: frame_length
          cases:
            131: beacon_short
            272: beacon_long
        size-eos: true
    instances:
      frame_length:
        value: _io.size


  beacon_long:
    seq:
      - id: offset_0
        type: u1
        repeat: expr
        repeat-expr: 12
      - id: l0_status
        -orig-id: L0_Status
        type: u1
        doc: |
          L0 System Status
          value = l0_status [n]
      - id: l0_acpt_cnt
        -orig-id: L0_ACPT_CNT
        type: u1
        doc: |
          Level 0 Accept Counter
          value = l0_acpt_cnt [n]
      - id: l0_rjct_cnt
        -orig-id: L0_RJCT_CNT
        type: u1
        doc: |
          Level 0 Reject Counter
          value = l0_rjct_cnt [n]
      - id: hw_sec_cnt
        -orig-id: HW_SEC_CNT
        type: u1
        doc: |
          Hardware Second Counter
          value = hw_sec_cnt [s]
      - id: offset_1
        type: u1
        repeat: expr
        repeat-expr: 8
      - id: time_tag
        -orig-id: TIME_TAG
        type: u4
        doc: |
          Time Tag of Last Incoming Command
          value = time_tag [usec]
      - id: offset_2
        type: u1
        repeat: expr
        repeat-expr: 4
      - id: pld_tlm_ack_cnt
        -orig-id: PLD_TLM_ACK_CNT
        type: u1
        doc: |
          Number of accepted telemetry packets
          value = pld_tlm_ack_cnt [n]
      - id: pld_cmd_cnt
        -orig-id: PLD_CMD_CNT
        type: u1
        doc: |
          Number of commands sent
          value = pld_cmd_cnt [n]
      - id: pld_tlm_to_cnt
        -orig-id: PLD_TLM_TO_CNT
        type: u1
        doc: |
          Number of timeouts waiting for telemetry
          value = pld_tlm_to_cnt [n]
      - id: pld_tlm_nak_cnt
        -orig-id: PLD_TLM_NAK_CNT
        type: u1
        doc: |
          Number of rejected telemetry packets
          value = pld_tlm_nak_cnt [n]
      - id: spare_end
        -orig-id: SPARE_END
        type: u8
      - id: cmd_status
        -orig-id: CMD_STATUS
        type: u1
        doc: |
          Command Status
          value = cmd_status [n]
          0/OK
          1/BAD_APID
          2/BAD_OPCODE
          3/BAD_DATA
          4/NOW_READING
          5/DONE_READING
          6/IDLE
          7/NO_CMD_DATA
          8/CMD_SRVC_OVERRUN
          9/CMD_APID_OVERRUN
          10/INCORRECT_WHEEL_MODE
          11/BAD_ELEMENT
          12/TABLES_BUSY
          13/FLASH_NOT_ARMED
          14/THRUSTERS_DISABLED
          15/ATT_ERR_TOO_HIGH
          16/ASYNC_REFUSED
          17/DRIVER_ERROR
      - id: realtime_cmd_accept_count
        -orig-id: REALTIME_CMD_ACCEPT_COUNT
        type: u1
        doc: |
          Realtime Command Accept Count
          value = realtime_cmd_accept_count [n]
      - id: realtime_cmd_reject_count
        -orig-id: REALTIME_CMD_REJECT_COUNT
        type: u1
        doc: |
          Realtime Command Reject Count
          value = realtime_command_reject_count [n]
      - id: stored_cmd_accept_cnt
        -orig-id: STORED_CMD_ACCEPT_COUNT
        type: u1
        doc: |
          Stored Command Accept Count
          value = stored_command_accept_count [n]
      - id: stored_cmd_reject_cnt
        -orig-id: STORED_CMD_REJECT_COUNT
        type: u1
        doc: |
          Stored Command Reject Count
          value = stored_command_reject_count [n]
      - id: macros_status_1
        -orig-id: MACROS_STATUS_1
        type: u2
        doc: |
          Macros Status
          value = macros_status_1 [n]
      - id: scrub_status_overall
        -orig-id: SCRUB_STATUS_OVERALL
        type: s1
        doc: |
          Scrub Status Overall
          value = scrub_status_overall [n]
      - id: scrub_count
        -orig-id: SCRUB_COUNT
        type: u1
        doc: |
          Number of times flash scrubbing has run
          value = scrub_count [n]
      - id: image_booted
        -orig-id: IMAGE_BOOTED
        type: u1
        doc: |
          Which image was booted
          value = image_booted [n]
          0/PRIMARY
          1/REDUNDANT
      - id: image_auto_failover
        -orig-id: IMAGE_AUTO_FAILOVER
        type: u1
        doc: |
          Automatic image failover occured
          value = image_auto_failover [n]
          0/OK
          1/FAIL
      - id: tai_seconds
        -orig-id: TAI_SECONDS
        type: f8
        doc: |
          TAI Seconds
          value = tai_seconds [sec]
      - id: time_valid
        -orig-id: TIME_VALID
        type: u1
        doc: |
          Time Valid
          value = time_valid [n]
          0/NO
          1/YES
      - id: position_wrt_eci1
        -orig-id: POSITION_WRT_ECI1
        type: s4
        doc: |
          Orbit Position ECI
          value = 2.00E-05 * position_wrt_eci1 [km]
      - id: position_wrt_eci2
        -orig-id: POSITION_WRT_ECI2
        type: s4
        doc: |
          Orbit Position ECI
          value = 2.00E-05 * position_wrt_eci2 [km]
      - id: position_wrt_eci3
        -orig-id: POSITION_WRT_ECI3
        type: s4
        doc: |
          Orbit Position ECI
          value = 2.00E-05 * position_wrt_eci3 [km]
      - id: velocity_wrt_eci1
        -orig-id: VELOCITY_WRT_ECI1
        type: s4
        doc: |
          Orbit Velocity ECI
          value = 5.00E-09 * velocity_wrt_eci1 [km/sec]
      - id: velocity_wrt_eci2
        -orig-id: VELOCITY_WRT_ECI2
        type: s4
        doc: |
          Orbit Velocity ECI
          value = 5.00E-09 * velocity_wrt_eci2 [km/sec]
      - id: velocity_wrt_eci3
        -orig-id: VELOCITY_WRT_ECI3
        type: s4
        doc: |
          Orbit Velocity ECI
          value = 5.00E-09 * velocity_wrt_eci3 [km/sec]
      - id: nadir_vector_body1
        -orig-id: NADIR_VECTOR_BODY1
        type: s2
        doc: |
          Nadir Vector in Body
          value = 4.00E-05 * nadir_vector_body1 [n]
      - id: nadir_vector_body2
        -orig-id: NADIR_VECTOR_BODY2
        type: s2
        doc: |
          Nadir Vector in Body
          value = 4.00E-05 * nadir_vector_body2 [n]
      - id: nadir_vector_body3
        -orig-id: NADIR_VECTOR_BODY3
        type: s2
        doc: |
          Nadir Vector in Body
          value = 4.00E-05 * nadir_vector_body3 [n]
      - id: sun_vector_body1
        -orig-id: SUN_VECTOR_BODY1
        type: s2
        doc: |
          Sun vector in spacecraft body frame
          value = 4.00E-05 * sun_vector_body1 [n]
      - id: sun_vector_body2
        -orig-id: SUN_VECTOR_BODY2
        type: s2
        doc: |
          Sun vector in spacecraft body frame
          value = 4.00E-05 * sun_vector_body2 [n]
      - id: sun_vector_body3
        -orig-id: SUN_VECTOR_BODY3
        type: s2
        doc: |
          Sun vector in spacecraft body frame
          value = 4.00E-05 * sun_vector_body3 [n]
      - id: sun_position_wrt_eci1
        -orig-id: SUN_POSITION_WRT_ECI1
        type: s4
        doc: |
          Sun Position ECI
          value = 0.0714 * sun_position_wrt_eci1 [km]
      - id: sun_position_wrt_eci2
        -orig-id: SUN_POSITION_WRT_ECI2
        type: s4
        doc: |
          Sun Position ECI
          value = 0.0714 * sun_position_wrt_eci2 [km]
      - id: sun_position_wrt_eci3
        -orig-id: SUN_POSITION_WRT_ECI3
        type: s4
        doc: |
          Sun Position ECI
          value = 0.0714 * sun_position_wrt_eci3 [km]
      - id: moon_position_wrt_eci1
        -orig-id: MOON_POSITION_WRT_ECI1
        type: s4
        doc: |
          Moon Position ECI
          value = 0.00019999999 * moon_position_wrt_eci1 [km]
      - id: moon_position_wrt_eci2
        -orig-id: MOON_POSITION_WRT_ECI2
        type: s4
        doc: |
          Moon Position ECI
          value = 0.00019999999 * moon_position_wrt_eci2 [km]
      - id: moon_position_wrt_eci3
        -orig-id: MOON_POSITION_WRT_ECI3
        type: s4
        doc: |
          Moon Position ECI
          value = 0.00019999999 * moon_position_wrt_eci3 [km]
      - id: refs_valid
        -orig-id: REFS_VALID
        type: u1
        doc: |
          Refs valid
          value = refs_valid [n]
          0/NO
          1/YES
      - id: esm_valid
        -orig-id: ESM_VALID
        type: u1
        doc: |
          Earth, Sun, Moon valid
          value = esm_valid [n]
          0/NO
          1/YES
      - id: run_low_rate_task
        -orig-id: RUN_LOW_RATE_TASK
        type: u1
        doc: |
          RunLowRateTask
          value = run_low_rate_task [n]
          0/NO
          1/YES
      - id: q_body_wrt_eci1
        -orig-id: Q_BODY_WRT_ECI1
        type: s4
        doc: |
          Attitude Quaternion
          value = 5.00E-10 * q_body_wrt_eci1 [n]
      - id: q_body_wrt_eci2
        -orig-id: Q_BODY_WRT_ECI2
        type: s4
        doc: |
          Attitude Quaternion
          value = 5.00E-10 * q_body_wrt_eci2 [n]
      - id: q_body_wrt_eci3
        -orig-id: Q_BODY_WRT_ECI3
        type: s4
        doc: |
          Attitude Quaternion
          value = 5.00E-10 * q_body_wrt_eci3 [n]
      - id: q_body_wrt_eci4
        -orig-id: Q_BODY_WRT_ECI4
        type: s4
        doc: |
          Attitude Quaternion
          value = 5.00E-10 * q_body_wrt_eci4 [n]
      - id: body_rate1_dps
        -orig-id: BODY_RATE1_DPS
        type: s4
        doc: |
          Body Frame Rate (deg/s)
          value = 2.86E-07 * body_rate1_dps [deg/sec]
      - id: body_rate2_dps
        -orig-id: BODY_RATE2_DPS
        type: s4
        doc: |
          Body Frame Rate (deg/s)
          value = 2.86E-07 * body_rate2_dps [deg/sec]
      - id: body_rate3_dps
        -orig-id: BODY_RATE3_DPS
        type: s4
        doc: |
          Body Frame Rate (deg/s)
          value = 2.86E-07 * body_rate3_dps [deg/sec]
      - id: bad_att_timer
        -orig-id: BAD_ATT_TIMER
        type: u4
        doc: |
          BadAttTimer
          value = bad_att_timer [cycles]
      - id: bad_rate_timer
        -orig-id: BAD_RATE_TIMER
        type: u4
        doc: |
          BadRateTimer
          value = bad_rate_timer [cycles]
      - id: reinit_count
        -orig-id: REINIT_COUNT
        type: u4
        doc: |
          Attitude Filter Reinit Count
          value = reinit_count [n]
      - id: gnc_status_1
        -orig-id: GNC_STATUS_1
        type: u4
        doc: |
          GNC Status
          value = gnc_status [n]
      - id: hr_cycle_safe_mode
        -orig-id: HR_CYCLE_SAFE_MODE
        type: u4
        doc: |
          HR Run Count at Time of Safe Mode
          value = hr_cycle_safe_mode [cycles]
      - id: rotisserie_rate_dps
        -orig-id: ROTISSERIE_RATE_DPS
        type: s2
        doc: |
          Desired Sun Rot Rate (deg/s)
          value = 0.002292 * rotisserie_rate_dps [deg/sec]
      - id: adcs_mode
        -orig-id: ADCS_MODE
        type: u1
        doc: |
          ADCS Mode
          value = adcs_mode [n]
      - id: gnc_status_2
        -orig-id: GNC_STATUS_2
        type: u2
        doc: |
          GNC Status
          value = gnc_status [n]
      - id: filtered_speed_rpm1
        -orig-id: FILTERED_SPEED_RPM1
        type: s2
        doc: |
          Wheel Meas Speed
          value = 0.4 * filtered_speed_rpm1 [rpm]
      - id: filtered_speed_rpm2
        -orig-id: FILTERED_SPEED_RPM2
        type: s2
        doc: |
          Wheel Meas Speed
          value = 0.4 * filtered_speed_rpm2 [rpm]
      - id: filtered_speed_rpm3
        -orig-id: FILTERED_SPEED_RPM3
        type: s2
        doc: |
          Wheel Meas Speed
          value = 0.4 * filtered_speed_rpm3 [rpm]
      - id: operating_mode1
        -orig-id: OPERATING_MODE1
        type: u1
        doc: |
          Wheel Operating Mode
          value = operating_mode1 [n]
          0/IDLE
          1/INT
          2/EXT
      - id: operating_mode2
        -orig-id: OPERATING_MODE2
        type: u1
        doc: |
          Wheel Operating Mode
          value = operating_mode2 [n]
          0/IDLE
          1/INT
          2/EXT
      - id: operating_mode3
        -orig-id: OPERATING_MODE3
        type: u1
        doc: |
          Wheel Operating Mode
          value = operating_mode3 [n]
          0/IDLE
          1/INT
          2/EXT
      - id: operating_mode
        -orig-id: OPERATING_MODE
        type: u1
        doc: |
          Tracker Operating Mode
          value = operating_mode [n]
      - id: star_id_step
        -orig-id: STAR_ID_STEP
        type: u1
        doc: |
          Star ID Step
          value = star_id_step [n]
      - id: att_status
        -orig-id: ATT_STATUS
        type: u1
        doc: |
          Tracker Attitude Status
          value = att_status [n]
      - id: det_timeout_count
        -orig-id: DET_TIMEOUT_COUNT
        type: u2
        doc: |
          Number of detector timeouts
          value = det_timeout_count [counts]
      - id: num_attitude_stars
        -orig-id: NUM_ATTITUDE_STARS
        type: u1
        doc: |
          Number Stars Used in Att
          value = num_attitude_stars [n]
      - id: position_error1
        -orig-id: POSITION_ERROR1
        type: s4
        doc: |
          Attitude Error
          value = 2.00E-09 * position_error1 [rad]
      - id: position_error2
        -orig-id: POSITION_ERROR2
        type: s4
        doc: |
          Attitude Error
          value = 2.00E-09 * position_error2 [rad]
      - id: position_error3
        -orig-id: POSITION_ERROR3
        type: s4
        doc: |
          Attitude Error
          value = 2.00E-09 * position_error3 [rad]
      - id: eigen_error
        -orig-id: EIGEN_ERROR
        type: u4
        doc: |
          Eigen Error
          value = 1.52E-09 * eigen_error [rad]
      - id: time_into_search
        -orig-id: TIME_INTO_SEARCH
        type: u2
        doc: |
          Time Into Sun Search
          value = time_into_search [sec]
      - id: wait_timer
        -orig-id: WAIT_TIMER
        type: u2
        doc: |
          Sun Search Wait Timer
          value = wait_timer [sec]
      - id: sun_point_angle_error
        -orig-id: SUN_POINT_ANGLE_ERROR
        type: u2
        doc: |
          Sun Point Angle Error
          value = 0.0029999998 * sun_point_angle_error [deg]
      - id: sun_point_state
        -orig-id: SUN_POINT_STATE
        type: u1
        doc: |
          Sun Point State
          value = sun_point_angle_error [n]
      - id: momentum_vector_body1
        -orig-id: MOMENTUM_VECTOR_BODY1
        type: s2
        doc: |
          System Momentum in Body Frame
          value = 0.00019999999 * momentum_vector_body1 [Nms]
      - id: momentum_vector_body2
        -orig-id: MOMENTUM_VECTOR_BODY2
        type: s2
        doc: |
          System Momentum in Body Frame
          value = 0.00019999999 * momentum_vector_body2 [Nms]
      - id: momentum_vector_body3
        -orig-id: MOMENTUM_VECTOR_BODY3
        type: s2
        doc: |
          System Momentum in Body Frame
          value = 0.00019999999 * momentum_vector_body3 [Nms]
      - id: total_momentum_mag
        -orig-id: TOTAL_MOMENTUM_MAG
        type: u2
        doc: |
          System Momentum Magnitude
          value = 0.00050000002 * total_momentum_mag [Nms]
      - id: duty_cycle1
        -orig-id: DUTY_CYCLE1
        type: s1
        doc: |
          Torque Rod Duty Cycle
          value = duty_cycle1 [n]
      - id: duty_cycle2
        -orig-id: DUTY_CYCLE2
        type: s1
        doc: |
          Torque Rod Duty Cycle
          value = duty_cycle2 [n]
      - id: duty_cycle3
        -orig-id: DUTY_CYCLE3
        type: s1
        doc: |
          Torque Rod Duty Cycle
          value = duty_cycle3 [n]
      - id: torque_rod_mode1
        -orig-id: TORQUE_ROD_MODE1
        type: u1
        doc: |
          Torque Rod Ctrl Mode
          value = torque_rod_mode1 [n]
      - id: torque_rod_mode2
        -orig-id: TORQUE_ROD_MODE2
        type: u1
        doc: |
          Torque Rod Ctrl Mode
          value = torque_rod_mode2 [n]
      - id: torque_rod_mode3
        -orig-id: TORQUE_ROD_MODE3
        type: u1
        doc: |
          Torque Rod Ctrl Mode
          value = torque_rod_mode3 [n]
      - id: mag_source_used
        -orig-id: MAG_SOURCE_USED
        type: u1
        doc: |
          Mag Field Source
          value = mag_source_used [n]
      - id: momentum_vector_valid
        -orig-id: MOMENTUM_VECTOR_VALID
        type: u1
        doc: |
          Momentum Vector Valid
          value = momentum_vector_valid [n]
          0/NO
          1/YES
      - id: sun_vector_body1_meas
        -orig-id: SUN_VECTOR_BODY1
        type: s2
        doc: |
          Meas Sun Body Vector
          value = 1.00E-04 * sun_vector_body1_meas [n]
      - id: sun_vector_body2_meas
        -orig-id: SUN_VECTOR_BODY2
        type: s2
        doc: |
          Meas Sun Body Vector
          value = 1.00E-04 * sun_vector_body2_meas [n]
      - id: sun_vector_body3_meas
        -orig-id: SUN_VECTOR_BODY3
        type: s2
        doc: |
          Meas Sun Body Vector
          value = 1.00E-04 * sun_vector_body3_meas [n]
      - id: sun_vector_status
        -orig-id: SUN_VECTOR_STATUS
        type: u1
        doc: |
          Meas Sun Body Vector Status
          value = sun_vector_status [n]
          0/GOOD
          1/COARSE
          2/BAD
      - id: css_invalid_count
        -orig-id: CSS_INVALID_COUNT
        type: u2
        doc: |
          CSS Invalid Measurement Count
          value = css_invalid_count [n]
      - id: sun_sensor_used
        -orig-id: SUN_SENSOR_USED
        type: u1
        doc: |
          Sun Sensor Package Used
          value = sun_sensor_used [n]
      - id: mag_vector_body1
        -orig-id: MAG_VECTOR_BODY1
        type: s2
        doc: |
          Meas Mag Field Body
          value = 5.00E-09 * mag_vector_body1 [T]
      - id: mag_vector_body2
        -orig-id: MAG_VECTOR_BODY2
        type: s2
        doc: |
          Meas Mag Field Body
          value = 5.00E-09 * mag_vector_body2 [T]
      - id: mag_vector_body3
        -orig-id: MAG_VECTOR_BODY3
        type: s2
        doc: |
          Meas Mag Field Body
          value = 5.00E-09 * mag_vector_body3 [T]
      - id: mag_invalid_count
        -orig-id: MAG_INVALID_COUNT
        type: u2
        doc: |
          Cycles with invalid Measured Mag Data
          value = mag_invalid_count [counts]
      - id: mag_vector_valid
        -orig-id: MAG_VECTOR_VALID
        type: u1
        doc: |
          Meas Mag Field Valid
          value = mag_vector_valid [n]
          0/NO
          1/YES
      - id: mag_sensor_used
        -orig-id: MAG_SENSOR_USED
        type: u1
        doc: |
          Mag Sensor Used
          value = mag_sensor_used [n]

  beacon_short:
    seq:
      - id: offset_0
        type: u1
        repeat: expr
        repeat-expr: 4
      - id: imu_invalid_count
        -orig-id: IMU_INVALID_COUNT
        type: u2
        doc: |
          IMU Invalid Count
          value = imu_invalid_count [n]
      - id: new_packet_count
        -orig-id: NEW_PACKET_COUNT
        type: u1
        doc: |
          IMU Packet Count
          value = new_packet_count [n]
      - id: imu_vector_valid
        -orig-id: IMU_VECTOR_VALID
        type: u1
        doc: |
          IMU Rate Valid
          value = imu_vector_valid [n]
          0/NO
          1/YES
      - id: hr_run_count
        -orig-id: HR_RUN_COUNT
        type: u4
        doc: |
          High Rate Run Count
          value = hr_run_count [n]
      - id: hr_exec_time_ms1
        -orig-id: HR_EXEC_TIME_MS1
        type: u1
        doc: |
          High Rate Duration
          value = hr_exec_time_ms1 [n]
      - id: hr_exec_time_ms2
        -orig-id: HR_EXEC_TIME_MS2
        type: u1
        doc: |
          High Rate Duration
          value = hr_exec_time_ms2 [n]
      - id: hr_exec_time_ms3
        -orig-id: HR_EXEC_TIME_MS3
        type: u1
        doc: |
          High Rate Duration
          value = hr_exec_time_ms3 [n]
      - id: hr_exec_time_ms4
        -orig-id: HR_EXEC_TIME_MS4
        type: u1
        doc: |
          High Rate Duration
          value = hr_exec_time_ms4 [n]
      - id: hr_exec_time_ms5
        -orig-id: HR_EXEC_TIME_MS5
        type: u1
        doc: |
          High Rate Duration
          value = hr_exec_time_ms5 [n]
      - id: payload_sec_since_last_tlm
        -orig-id: PAYLOAD_SEC_SINCE_LAST_TLM
        type: u4
        doc: |
          Seconds since last TLM received (by SW)
          value = payload_sec_since_last_tlm [sec]
      - id: payload_tlm_rx_count
        -orig-id: PAYLOAD_TLM_RX_COUNT
        type: u2
        doc: |
          Payload Tlm Receive Counter (by SW)
          value = payload_tlm_rx_count [n]
      - id: payload_tlm_ack_count
        -orig-id: PAYLOAD_TLM_ACK_COUNT
        type: u2
        doc: |
          Payload Tlm ACK Counter
          value = payload_tlm_ack_count [n]
      - id: payload_tlm_nak_count
        -orig-id: PAYLOAD_TLM_NAK_COUNT
        type: u2
        doc: |
          Payload Tlm NAK Counter
          value = payload_tlm_nak_count [n]
      - id: voltage_12p0
        -orig-id: VOLTAGE_12P0
        type: u1
        doc: |
          Voltage_12p0
          value = 0.1 * voltage_12p0 [V]
      - id: voltage_8p0
        -orig-id: VOLTAGE_8P0
        type: u1
        doc: |
          Voltage_8p0
          value = 0.1 * voltage_8p0 [V]
      - id: voltage_5p0
        -orig-id: VOLTAGE_5P0
        type: u1
        doc: |
          Voltage_5p0
          value = 0.025 * voltage_5p0 [V]
      - id: voltage_3p3
        -orig-id: VOLTAGE_3P3
        type: u1
        doc: |
          Voltage_3p3
          value = 0.015 * voltage_3p3 [V]
      - id: det_temp
        -orig-id: DET_TEMP
        type: s1
        doc: |
          Tracker Detector temperature
          value = 0.8 * det_temp [degC]
      - id: det2_temp
        -orig-id: DET2_TEMP
        type: s1
        doc: |
          Tracker 2 Detector temperature
          value = 0.8 * det2_temp [degC]
      - id: box1_temp
        -orig-id: BOX1_TEMP
        type: s2
        doc: |
          Box 1 Temp
          value = 0.0049999999 * box1_temp [degC]
      - id: imu_temp
        -orig-id: IMU_TEMP
        type: s2
        doc: |
          IMU Temp
          value = 0.0049999999 * imu_temp [degC]
      - id: motor1_temp
        -orig-id: MOTOR1_TEMP
        type: s2
        doc: |
          Wheel 1 Temp
          value = 0.0049999999 * motor1_temp [degC]
      - id: motor2_temp
        -orig-id: MOTOR2_TEMP
        type: s2
        doc: |
          Wheel 2 Temp
          value = 0.0049999999 * motor2_temp [degC]
      - id: motor3_temp
        -orig-id: MOTOR3_TEMP
        type: s2
        doc: |
          Wheel 3 Temp
          value = 0.0049999999 * motor3_temp [degC]
      - id: bus_voltage
        -orig-id: BUS_VOLTAGE
        type: s2
        doc: |
          Bus Voltage
          value = 0.001 * bus_voltage [V]
      - id: battery_voltage
        -orig-id: BATTERY_VOLTAGE
        type: u2
        doc: |
          Battery Voltage
          value = 0.0020000001 * battery_voltage [V]
      - id: battery_current
        -orig-id: BATTERY_CURRENT
        type: s2
        doc: |
          Battery Current
          value = 0.0020000001 * battery_current [A]
      - id: battery1_temp
        -orig-id: BATTERY1_TEMP
        type: s2
        doc: |
          Battery 1 Temp
          value = 0.0049999999 * battery1_temp [degC]
      - id: battery2_temp
        -orig-id: BATTERY2_TEMP
        type: s2
        doc: |
          Battery 2 Temp
          value = 0.0049999999 * battery2_temp [degC]
      - id: user_analog1
        -orig-id: USER_ANALOG1
        type: s4
        doc: |
          User Analogs
          value = 0.0050000002 * user_analog1 [n]
      - id: user_analog2
        -orig-id: USER_ANALOG2
        type: s4
        doc: |
          User Analogs
          value = 0.0050000002 * user_analog2 [n]
      - id: operating_mode
        -orig-id: OPERATING_MODE
        type: u1
        doc: |
          Tracker Operating Mode
          value = operating_mode [n]
      - id: star_id_step
        -orig-id: STAR_ID_STEP
        type: u1
        doc: |
          Star ID Step
          value = star_id_step [n]
      - id: att_status
        -orig-id: ATT_STATUS
        type: u1
        doc: |
          Tracker Attitude Status
          value = att_status [n]
      - id: det_timeout_count
        -orig-id: DET_TIMEOUT_COUNT
        type: u2
        doc: |
          Number of detector timeouts
          value = det_timeout_count [counts]
      - id: num_attitude_stars
        -orig-id: NUM_ATTITUDE_STARS
        type: u1
        doc: |
          Num Stars Used in Att
          value = num_attitude_stars [n]
      - id: cycles_since_crc_data
        -orig-id: CYCLES_SINCE_CRC_DATA
        type: u4
        doc: |
          Cycles Since Correct CRC GPS Data
          value = cycles_sinse_crc_data [n]
      - id: gps_lock_count
        -orig-id: GPS_LOCK_COUNT
        type: u2
        doc: |
          spare
          value = gps_lock_count [n]
      - id: gps_valid
        -orig-id: GPS_VALID
        type: u1
        doc: |
          GPS Valid
          value = gps_valid [n]
          0/NO
          1/YES
      - id: gps_enabled
        -orig-id: GPS_ENABLED
        type: u1
        doc: |
          GPS Enabled
          value = gps_enabled [n]
          0/NO
          1/YES
      - id: macros_status_2
        -orig-id: MACROS_STATUS_2
        type: u2
        doc: |
          Macros Status
          value = macros_status_2 [n]
      - id: sd_minute_cur
        -orig-id: SD_MINUTE_CUR
        type: u4
        doc: |
          SD Card Current Minute Number
          value = sd_minute_cur [n]
      - id: sd_percent_used_total
        -orig-id: SD_PERCENT_USED_TOTAL
        type: u1
        doc: |
          SD Card Used Space Percentage Total
          value = sd_percent_used_total [%]
      - id: sd_percent_used_fsw
        -orig-id: SD_PERCENT_USED_FSW
        type: u1
        doc: |
          SD Card Used Space Percentage For Fsw Database
          value = sd_percent_used_fsw [%]
      - id: sd_percent_used_soh
        -orig-id: SD_PERCENT_USED_SOH
        type: u1
        doc: |
          SD Card Used Space Percentage For Soh Database
          value = sd_percent_used_soh [%]
      - id: sd_percent_used_line
        -orig-id: SD_PERCENT_USED_LINE
        type: u1
        doc: |
          SD Card Used Space Percentage For Line Database
          value = sd_percent_used_line [%]
      - id: sd_percent_used_tbl
        -orig-id: SD_PERCENT_USED_TBL
        type: u1
        doc: |
          SD Card Used Space Percentage For Tbl Database
          value = sd_percent_used_tbl [%]
      - id: sd_percent_used_pay
        -orig-id: SD_PERCENT_USED_PAY
        type: u1
        doc: |
          SD Card Used Space Percentage For pay Database
          value = sd_percent_used_pay [%]
      - id: sdr_tx_frames
        -orig-id: SDR_TX_FRAMES
        type: u4
        doc: |
          BCT-SDR tx frame counter
          value = sdr_tx_frames [n]
      - id: sdr_rx_frames
        -orig-id: SDR_RX_FRAMES
        type: u4
        doc: |
          BCT-SDR rx valid frame counter
          value = sdr_tx_frames [n]
      - id: sdr_tx
        -orig-id: SDR_TX
        type: u1
        doc: |
          BCT-SDR tx state
          value = sdr_tx [n]
          0/NO
          1/YES
      - id: sdr_tx_power
        -orig-id: SDR_TX_POWER
        type: s1
        doc: |
          BCT-SDR tx power
          value = sdr_tx_power [dBm]
      - id: sdr_rx_lock
        -orig-id: SDR_RX_LOCK
        type: u1
        doc: |
          BCT-SDR rx pll lock
          value = sdr_rx_lock [n]
          0/NO
          1/YES
      - id: sdr_rx_power
        -orig-id: SDR_RX_POWER
        type: s1
        doc: |
          BCT-SDR rx power level
          value = sdr_rx_power [dBm]
      - id: sdr_rx_freq_offset
        -orig-id: SDR_RX_FREQ_OFFSET
        type: s4
        doc: |
          BCT-SDR rx frequency offset
          value = sdr_rx_freq_offset [Hz]
      - id: sdr_temp
        -orig-id: SDR_TEMP
        type: s1
        doc: |
          BCT-SDR temperature
          value = sdr_temp [degC]
      - id: sdr_comm_error
        -orig-id: SDR_comm_error
        type: u1
        doc: |
          BCT-SDR Comm Error
          value = sdr_comm_error [n]
          0/NO
          1/YES
      - id: sq_channel
        -orig-id: SQ_CHANNEL
        type: s1
        doc: |
          SpaceQuest Current Channel Selection
          value = sq_channel [n]
      - id: sq_trap_count
        -orig-id: SQ_TRAP_COUNT
        type: u1
        doc: |
          SpaceQuest Trap-Error Cycle Count
          value = sq_trap_count [n]
      - id: sq_temp
        -orig-id: SQ_TEMP
        type: u1
        doc: |
          SpaceQuest Temperature
          value = sq_temp [degC]
      - id: aid_status
        -orig-id: AID_STATUS
        type: u2
        doc: |
          Tracker Aiding Status
          value = aid_status [n]
      - id: star_id_status
        -orig-id: STAR_ID_STATUS
        type: u1
        doc: |
          Tracker Performing StarId
          value = star_id_status [n]
      - id: power_status
        -orig-id: POWER_STATUS
        type: u4
        doc: |
          Power Status
          value = power_status [n]
