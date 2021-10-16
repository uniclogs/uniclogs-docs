Glossary
========

.. glossary::
    :sorted:

    C3
        **Command-Communication-and-Control board**. See the `github repository <https://github.com/oresat/oresat-c3>`_ for more information.

    CubeSat
        A relatively small satellite made up of one or more Units (U). A Unit is 10cs x 10cs x 10cs in volume. (For example, OreSat 1 will be a 2U satellite, i.e. 10cs x 10cs x 20cs).

    Daemon
        A long-running Linux process that runs in the background.

    Demodulate
      The process of extracting information from a Radio-Frequency (RF) signal carrier wave.

    Doppler Correction
        The process of automatically correcting for frequency shifting that naturally occurs when observing a moving transmission source. *(i.e. a satellite in orbit)*.

    EDL
        **Engineering Data Link.** A bi-directional data link between the UniClOGS ground station and the OreSat spacecraft. Specifically it's UpLink is sent by UniClOGS on L band and received by OreSat, and it's DownLink is sent by OreSat on UHF and received by UniClOGS. It can contain critical engineering data, software updates for OreSat’s subsystems, or files from OreSat’s subsystems.

    L band
        Microwave band above UHF. The range of radio frequencies from 1GHz to 2 GHz.

    OreSat
        The Portland State Aerospace Society's open-source and open-hardware CubeSat project. See the `OreSat website <https://www.oresat.org>`_ for more information.

    PSAS
        **Portland State Aerosapce Society**. A student aerospace group at Portland State University. See the `PSAS website <https://www.pdxaerospace.org>`_ for more information.

    RTL-SDR:
        A relatively inexpensive Software Defined Radio (SDR) that can connect to any antenna via SMA, demodulate RF signals, and convert them to a digital format.

    SatNOGS
        A network of crowd-sourced ground-stations coordinated and operated by the Libre Space Foundation. See the `SatNOGS website <https://satnogs.org/about>`_ for more information.

    SDR
        **Software Define Radio**. Radio communications that are traditionally implemented in hardware are instead implemented in software.

    UHF
        **Ultra High Frequency.** The range of radio frequencies from 300 MHz to 1 GHz.

    UniClOGS
        **University Class Operation Ground Station**. A ground-station made by and for PSAS. It will be the sole receiver of EDL packets. Since UniClOGS is also a registered SatNOGS ground-station, it can also receive telemetry packets from SatNOGS-registered satellites. See the `hardware repository <https://github.com/oresat/uniclogs-hardware>`_ and `software repository <https://github.com/oresat/uniclogs-software>`_ for more information.

    VHF
        Very High Frequency. The range of radio frequencies from 30 MHz to 300 MHz.
