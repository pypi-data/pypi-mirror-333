from binascii import hexlify, unhexlify
from builtins import bytes
from typing import List


def data_from_hexstring(hexstring):
    databytes = bytes.fromhex(hexstring)
    return databytes
    """
    databytes = bytearray()
    try:
        databytes.extend([ord(c) for c in unhexlify(hexstring)])
    #Catch Odd-length String Error
    except TypeError:
        pass

    return databytes"""


def hexstring_from_data(databytes):
    hex_databytes = hexlify(databytes).decode("utf-8")
    return hex_databytes


class CycleInfo(object):
    def __init__(self, src, dest, rate_num, ack=False, num_frames=None):
        self.src = int(src)
        self.dest = int(dest)
        self.rate_num = int(rate_num)
        self.ack = bool(ack)

        if num_frames == None:
            self.num_frames = Rates[rate_num].numframes
        else:
            self.num_frames = int(num_frames)

    # This allows us to see if two cycleinfo objects match
    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class DrqParams(object):
    def __repr__(self):
        return "SRC: {} DST: {} ACK: {} NUMBYTES: {} FRAME#: {}".format(self.src, self.dest, self.ack, self.num_bytes,
                                                                        self.frame_num)

    def __init__(self, src, dest, ack, num_bytes, frame_num):
        self.src = int(src)
        self.dest = int(dest)
        self.ack = bool(ack)
        self.num_bytes = int(num_bytes)
        self.frame_num = int(frame_num)


class Ack(object):
    def __repr__(self):
        return "SRC: {} DST: {} FRAME#: {}".format(self.src, self.dest, self.frame_num)

    def __init__(self, src, dest, ack, frame_num):
        self.src = int(src)
        self.dest = int(dest)
        self.ack = bool(ack)
        self.frame_num = int(frame_num)


class CdrAck(Ack):
    def __init__(self, isodate, rxseqnum, src, dest, minirate, miniframe_ack, dataframe_ack):
        super().__init__(src, dest, ack, frame_num=dataframe_ack)
        self.isodate = isodate
        self.rxseqnum = rxseqnum
        self.minirate = minirate
        self.miniframe_ack = miniframe_ack
        self.dataframe_ack = dataframe_ack

    def __repr__(self):
        return f"CDR Ack Sequence #: {self.rxseqnum} SRC: {self.src} DST: {self.dest} Minirate: {self.minirate} Miniframe ACK: {self.miniframe_ack:>08b} Dataframe ACK: {self.dataframe_ack:>016b})"


class Camua(object):
    def __init__(self, src, dest, data):
        self.src = src
        self.dest = dest
        self.data = bytearray(data)

    def __repr__(self):
        return "SRC: {} DST: {} DATA: {}".format(self.src, self.dest, repr(self.data))


class Campr(object):
    def __init__(self, src, dest, owtt):
        self.src = src
        self.dest = dest
        self.owtt = owtt


class Causb2(object):
    def __init__(self, df, iso8601_time, azimuth_deg, elevation_deg, owtt_s, timing_mode,
                 ire0, ire1, ire2, ire3,
                 ndetects):

        self.df = df
        self.iso8601_time = iso8601_time
        self.azimuth_deg = azimuth_deg
        self.elevation_deg = elevation_deg
        self.owtt_s = owtt_s
        self.timing_mode = timing_mode

        self.ire0 = ire0
        self.ire1 = ire1
        self.ire2 = ire2
        self.ire3 = ire3

        self.ndetects = ndetects


class Catjn(object):
    def __init__(self, dest_id, ack, hex_header, hex_data, reserved=0):
        self.reserved = reserved
        self.dest_id = dest_id
        self.ack = ack
        self.hex_header = hex_header
        self.hex_data = hex_data

    def __repr__(self, *args, **kwargs):
        return "DEST_ID: {} ACK: {} HEX_HEADER: {} HEX_DATA: {} RESERVED: {}".format(
            self.dest_id,
            self.ack,
            self.hex_header,
            self.hex_data,
            self.reserved,
            )


class Cajrx(object):
    def __init__(self, header_crc_check, src_id, dest_id, ack, hex_header, data_crc_check, nbytes, hex_data):
        self.header_crc_check = header_crc_check
        self.src_id = src_id
        self.dest_id = dest_id
        self.ack = ack
        self.hex_header = hex_header
        self.data_crc_check = data_crc_check
        self.nbytes = nbytes
        self.hex_data = hex_data
        self.cyclestats = None

    def add_cyclestats(self, cyclestats):
        self.cyclestats = cyclestats

    def __repr__(self, *args, **kwargs):
        return "HEADER_CRC_CHECK: {} SRC_ID: {} DEST_ID: {} ACK: {} HEX_HEADER: {} DATA_CRC_CHECK: {} NBYTES: {} HEX_DATA: {} CYCLE_STATS: {}".format(
            self.header_crc_check,
            self.src_id,
            self.dest_id,
            self.ack,
            self.hex_header,
            self.data_crc_check,
            self.nbytes,
            self.hex_data,
            self.cyclestats,
            )


class Casst(object):
    def __init__(self, sst_version, in_water_spl_dB, detector, num_samples, summary):
        self.sst_version = sst_version
        self.in_water_spl_dB = in_water_spl_dB
        self.detector = detector
        self.num_samples = num_samples

        self.summary = summary

    def __doc__(self, *args, **kwargs):
        return '''
        SST-- SoundSTatistics            
            -Print descriptive statistics about the in-water Sound Pressure Level (SPL).  
        
        How it works: 
        -------------
        Observations are accumulated beginning after the previous CASST was printed.  These samples of SPL data are stored in a ring buffer with enough memory to hold 250-ish observations which is roughly 10 seconds-worth (or the classic CAREV period) given a detector probe length of 200 symbols.  The buffer of observations is cleared after every time it is printed; the final field in the SST message reports the number of samples that were accumulated.  The SPL samples are tied to a specific detector and config; each SPL observation is the average SPL, in dB, over the detector's probe length (in baseband samples, something like 40 mS).
        

        MicroModem HW & SW configuration that affects CASST output:
        -----------------------------------------------------------
        ***Currently only works for PSK detectors operating at 10 kHz or 25 kHz (i.e. BND 1, BND 3 and BND 0 **with FC0 configured properly)
        Detector:
            -Must be using a PSK detector, o/wise, all 0's in output
        Carrier:
            -Only tuned for 25 kHz and 10 kHz, anything else will return 0's for SPL 
        Bandwidth:
            -This determines your passband for the SPL estimate 
        FML:
            -Sweep length - i.e. window size for averaging; modifies number of baseband samples in observation
        AGN:
            -Analog gain setting for the detector (modem's front end) 
        Hardware:
            -hwd.Vpreamp_gain_dB: transducer's preamp gain, measured from ducer to modem by convention. default is 40 dB for preamp matched to BTech 25 kHz ducer. 
            -hwd.transducer_sensitivity_dB: transducer sensitivity in dB, measured from wavefront in water to preamp by convention. default is -193 dB for BTech 25 kHz ducer. 


        Single Shot, Prints $CASST immediatly: 
        --------------------------------------
            -$CCSST,1 -------------------- um.send_single_shot_sst()

        Continuous Printing (prints with each CAREV):  
        --------------------------------------
            -To enable: $CCCFG,SST,1 ----- um.set_config(type='SST', 1)
            -To disable: $CCCFG,SST,0 ---- um.set_config(type='SST', 0)
            -To query: $CCCFQ,SST -------- um.get_config(type='SST')


        $CASST,0,58.728850,1,400,57.862410,58.381225,58.523375,58.728850,59.203695,191,*70
               |   |       |  |    |         |         |         |         |        |______ number of elements in SPL history.  Each element is the average of a unique set of nObservationSamples of baseband data
               |   |       |  |    |         |         |         |         |_______________ sample maximum of SPL history (in dB).  Max of five-number summary (descriptive statistics)               
               |   |       |  |    |         |         |         |_________________________ upper quartile of SPL history (in dB).  Third quartile of five-number summary (descriptive statistics) 
               |   |       |  |    |         |         |___________________________________ median value of SPL history (in dB).  Middle value of five-number summary (descriptive statistics) 
               |   |       |  |    |         |_____________________________________________ lower quartile of SPL history (in dB).  First quartile of five-number summary (descriptive statistics)     
               |   |       |  |    |_______________________________________________________ sample minimum of SPL history (in dB).  Min of five-number summary (descriptive statistics)            
               |   |       |  |____________________________________________________________ nObservationSamples: number of baseband samples in the detector's probe
               |   |       |_______________________________________________________________ detector used during SPL calculation. This enum represents the detector type (e.g., psk chan, fsk chan, etc...) *only supports psk chan as of 3.2.2
               |   |_______________________________________________________________________ in-water Sound Pressure Level (SPL) in dB. This is the average SPL over the last nObservationSamples (see above for nObservationSamples definition)
               |___________________________________________________________________________ SST version                   
        '''

    def __repr__(self, *args, **kwargs):
        return "SST_VER: {} IN_WATER_SPL_DB: {} DETECTOR: {} #SAMPLES: {} SUMMARY: {}".format(
            self.sst_version,
            self.in_water_spl_dB,
            self.detector,
            self.num_samples,
            self.summary,
            )


class DataFrame(object):
    def __init__(self, src, dest, ack, frame_num, data, bad_crc=False):
        self.bad_crc = bad_crc
        self.src = src
        self.dest = dest
        self.ack = ack
        self.frame_num = frame_num
        if data:
            self.data = bytearray(data)
        else:
            self.data = None

    def __repr__(self):
        return "SRC: {} DST: {} ACK: {} FRAME#: {} BAD_CRC: {} DATA: {}".format(self.src, self.dest, self.ack,
                                                                                self.frame_num, self.bad_crc,
                                                                                repr(self.data))


class CCPGT(object):
    def __init__(self, txfreq, txcode, timeout_ms, codelen, rxfreq, rxcode1, rxcode2, rxcode3, rxcode4, reserved1=0,
                 reserved2=0):
        self.txfreq = txfreq
        self.codelen = codelen
        self.txcode = txcode
        self.timeout_ms = timeout_ms
        self.rxfreq = rxfreq
        self.rxcode1 = rxcode1
        self.rxcode2 = rxcode2
        self.rxcode3 = rxcode3
        self.rxcode4 = rxcode4
        self.reserved1 = reserved1
        self.reserved2 = reserved2

    def __repr__(self):
        return "TXHz: {} RXHz: {} TXCODE: {}".format(self.txfreq, self.rxfreq, self.txcode)


class Packet(object):
    def __init__(self, cycleinfo, frames=None):
        self.cycleinfo = cycleinfo

        if frames != None:
            self.frames = frames
        else:
            self.frames = []

    def append_framedata(self, framedata):
        # TODO: Make sure we have room for another frame, and that the data fits in the frame.
        newframe = DataFrame(self.cycleinfo.src, self.cycleinfo.dest, self.cycleinfo.ack,
                             (len(self.frames) + 1), framedata)
        self.frames.append(newframe)


class NavPingDigitalTransponder(object):
    """$SNPDT"""
    def __init__(self, cmd_args: List, timeout: int, flags: List) -> None:
        self.grp = cmd_args[0]
        self.chn = cmd_args[1]
        self.lf = True if cmd_args[2] else False
        self.hf = True if not self.lf else False
        self.nav_agn = cmd_args[3]
        self.timeout = timeout
        self.flags = flags

    def __repr__(self):
        return f"SNPDT(GRP: {self.grp} CHN: {self.chn} FREQ: {'low' if self.lf else 'hi'} " \
               f"TIMEOUT: {self.timeout} FLAGS: {self.flags})"


class NavPingGenericTransponder(object):
    """$SNPGT"""
    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return f"SNPGT{[f'{k}={v}' for k, v in self.__dict__.items() if not k.startswith('_')]}"


class NavStatistics(object):
    """$SNNST"""
    def __init__(self, version, ftx, ttx, query_time, agn, tat, transponder_replies):
        self.version = version
        self.ftx = ftx
        self.ttx = ttx
        self.query_time = query_time
        self.nav_agn = agn
        self.tat = tat
        for idx, each in enumerate(transponder_replies):
            try:
                if idx == 0 and each['xpond'] == 1:
                    attr = 'xpond_A'
                elif idx == 1 and each['xpond'] == 2:
                    attr = 'xpond_B'
                elif idx == 2 and each['xpond'] == 3:
                    attr = 'xpond_C'
                elif idx == 3 and each['xpond'] == 4:
                    attr = 'xpond_D'
                else:
                    raise ValueError()
            except ValueError:
                pass
            else:
                del each['xpond']
                setattr(self, attr, each)

    def __repr__(self):
        return f"SNNST(A1: {self.xpond_A} B2: {self.xpond_B} C3: {self.xpond_C} D4: {self.xpond_D})"


class NavTurnTimes(object):
    """$SNTTA"""
    def __init__(self, time_of_ping: float, travel_times: List[float]) -> None:
        self.time_of_ping = time_of_ping
        self.travel_times = travel_times
        self.a_flag = self.travel_times[0]
        self.b_flag = self.travel_times[1]
        self.c_flag = self.travel_times[2]
        self.d_flag = self.travel_times[3]

    def __repr__(self):
        return f"SNTTA(Outgoing Ping Time: {self.time_of_ping} " \
               f"A_OWTT: {self.a_flag} " \
               f"B_OWTT: {self.b_flag} " \
               f"C_OWTT: {self.c_flag} " \
               f"D_OWTT: {self.d_flag})"


class PacketRate(object):
    def __init__(self, name, number, framesize, numframes):
        self.name = name
        self.number = number
        self.framesize = framesize
        self.numframes = numframes

    def getpacketsize(self):
        return self.framesize * self.numframes

    maxpacketsize = property(getpacketsize)


Rates = {0: PacketRate('FH-FSK', 0, 32, 1),
         1: PacketRate('BCH 128:8', 1, 64, 3),
         2: PacketRate('DSS 1/15 (64B frames)', 2, 64, 3),
         3: PacketRate('DSS 1/7', 3, 256, 2),
         4: PacketRate('BCH 64:10', 4, 256, 2),
         5: PacketRate('Hamming 14:9', 5, 256, 8),
         6: PacketRate('DSS 1/15 (32B frames)', 6, 32, 6)}

FDPMiniRates = {1: PacketRate('BCH 128:8', 1, 90, 1),
                3: PacketRate('BCH 64:10', 3, 90, 1),
                5: PacketRate('Hamming 14:9', 5, 90, 1)}
FDPDataRates = {1: PacketRate('BCH 128:8', 1, 64, 3),
                3: PacketRate('BCH 64:10', 3, 256, 2),
                5: PacketRate('Hamming 14:9', 5, 256, 8)}
LDRRates = {7: PacketRate('BCH 64:10', 1, 260, 1)}
