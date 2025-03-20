__author__ = 'Eric'

from bitstring import BitStream, BitArray
import bitstring
from datetime import datetime
from acomms.messageparams import data_from_hexstring
from bidict import bidict
import traceback


mission_modes = bidict({0: "Mission completed",
                        1: "Manual",
                        2: "Test",
                        3: "Fault",
                        4: "Home",
                        5: "Alt Mission",
                        6: "Mission",
                        })

ranger_mission_modes = {1: "Pre-mission",
                        2: "Run",
                        5: "Completed"}

# Objective names from VIP.  It looks like these sometimes change with VIP version.
objective_names = bidict({0: 'None',
                          1: 'Manual',
                          2: 'Bench Test',
                          3: 'Acoustic Test',
                          4: 'Hysteresis Test',
                          5: 'Fin Wiggle Test',
                          6: 'Abort',
                          7: 'Fin Step',
                          8: 'Wait Run',
                          11: 'Set Position',
                          12: 'Wait Depth',
                          13: 'Surface',
                          19: 'Wait Prop',
                          20: 'Compass Cal',
                          21: 'Navigate',
                          22: 'Navigate Rows',
                          23: 'Wait Magnet',
                          24: 'Loiter',
                          25: 'Get GPS Fix',
                          27: 'Drop Decent',
                          28: 'Drop Ascent',
                          29: 'RECON',
                          32: 'Reacquire',
                          37: 'Drive Decent',
                          39: 'Circle',
                          42: 'Dock Cable',
                          43: 'Find',
                          44: 'Stand Off',
                          47: 'INS Reset',
                          49: 'Circular Cal',
                          50: 'Autotune',
                          51: 'CCL C3',
                          53: 'Undock Cable',
                          54: 'Unstuck',
                          62: 'Dock Mooring',
                          63: 'Undock Mooring',
                          65: 'Surface Loiter',
                          66: 'Find Max',
                          68: 'Relative Loiter',
                          69: 'PHINS C7 DVL Cal',
                          })

command_codes = {1: "Abort to end",
                 2: "Abort immediately",
                 3: "Start mission",
                 7: "Enable ranger ping",
                 8: "Disable ranger ping",
                 15: "Dump redirect commands",
                 17: "Abort to start",
                 18: "Abort to destination",
                 19: "Dump redirect except current"}


def LatLon(object):
    def __init__(self, lat_degrees=None, lon_degrees=None, lat_minutes=0, lon_minutes=None, lat_seconds=0, lon_seconds=None):
        if lat_degrees is not None:
            self._lat_degrees = float(lat_degrees)
            self._lat_degrees += lat_minutes/60
            self._lat_degrees += lat_seconds/(60*60)

        if lon_degrees is not None:
            self._lon_degrees = float(lon_degrees)
            self._lon_degrees += lon_minutes/60
            self._lon_degrees += lon_seconds/(60*60)


def decode_latlon(bit_array):
    if bit_array is None:
        raise ValueError

    # switch to big endian
    bit_array.byteswap()

    # sign extend
    if bit_array[0] == 1:
        bit_array.prepend('0xFF')
    else:
        bit_array.prepend('0x00')

    # Do conversion and return
    return bit_array.intbe * (180.0 / (2**23 - 1))


def encode_latlon(lat_or_lon):
    encoded = lat_or_lon * ((2**23 - 1) / 180.0)

    s = bitstring.pack('int:24', encoded)
    s.byteswap()

    return s


def decode_time_date(databits, year=None):
    databits.byteswap()

    month = databits.read('uint:4')
    day = databits.read('uint:5')
    hour = databits.read('uint:5')
    minute = databits.read('uint:6')
    second = databits.read('uint:4') * 4

    if year == None:
        year = datetime.utcnow().year

    return datetime(year, month, day, hour, minute, second)


def encode_time_data(date_time):
    s = bitstring.pack('uint:4, uint:5, uint:5, uint:6, uint:4',
                       date_time.month, date_time.day,
                       date_time.hour, date_time.minute, (date_time.second // 4))
    s.byteswap()
    return s


def decode_depth(encoded_depth):
    if encoded_depth <= 1000:
        return encoded_depth * 0.1
    elif encoded_depth <= 1500:
        return 100 + (encoded_depth - 1000) * 0.2
    elif encoded_depth <= 3100:
        return 200 + (encoded_depth - 1500) * 0.5
    elif encoded_depth <= 8100:
        return 1000 + (encoded_depth - 3100)
    else:
        return 6000


def encode_depth(depth):
    """
    0 - 100 meters: 0 - 1000(10 cm resolution)
    100 - 200 meters: 1001 - 1500(20 cm resolution)
    200 - 1000 meters: 1501 - 3100(50 cm resolution)
    1000 - 6000 meters: 3101 - 8100(1 meter resolution)
    """
    if depth < 0:
        return 0
    elif depth < 100:
        return int((depth+0.05) / 0.1)
    elif depth < 200:
        return int((depth - 100 + 0.1) / 0.2 + 1000)
    elif depth < 1000:
        return int((depth - 200 + 0.25) / 0.5 + 1500)
    elif depth < 6000:
        return int((depth - 1000 + 0.5) + 3100)
    else:
        return 8100


def decode_mission_mode_and_depth(encoded_bits):
    encoded_bits.byteswap()

    mission_mode_code = encoded_bits[0:3].uint
    depth = decode_depth(encoded_bits[3:].uint)

    mission_mode = mission_modes[mission_mode_code]

    return (mission_mode, depth)


def encode_mission_mode_and_depth(mission_mode, depth):
    if not isinstance(mission_mode, int):
        mission_mode_code = mission_modes.inverse[mission_mode]
    else:
        mission_mode_code = mission_mode

    encoded_depth = encode_depth(depth)
    s = bitstring.pack('uint:3, uint:13', mission_mode_code, encoded_depth)
    s.byteswap()

    return s


def encode_gfi_oil_pitch(gfi_percent, oil, pitch):
    s = bitstring.pack('int:6, uint:5, uint:5',
                       pitch * 63.0 / 180,
                       oil * 31.0 / 100,
                       gfi_percent * 31.0 / 100)
    s.byteswap()
    return s


def convert_knots_to_meters_per_second(knots: float) -> float:
    return float(knots * 0.514444)


def dms_to_decimal(dms: str) -> float:
    from re import split
    """Converts a string of <DEG><[N|S|E|W]><MINDEC> to decimal degrees
      e.g. dms: 32N45.0000  -->  32.750000
      e.g. dms: 117W10.0000  --> -117.166667
    """
    assert isinstance(dms, str), f'/dms_to_decimal: Invalid DMS type: {type(dms)}'
    dms = dms.strip().upper()
    assert ('N' in dms or 'S' in dms or 'E' in dms or 'W' in dms), f'/dms_to_decimal: Invalid DMS value: {dms}'
    _deg, _min = [float(x) for x in split('[N|S|E|W]', dms)]
    _dec = _deg + (_min / 60)
    _dec *= -1 if 'S' in dms or 'W' in dms else 1  # convert to negative value if S or W
    if 'N' in dms or 'S' in dms:
        assert -90 <= _dec <= 90, f'/dms_to_decimal: Invalid decimal degree value (for latitude): {_deg}'
    else:
        assert -180 <= _dec <= 180, f'/dms_to_decimal: Invalid decimal degree value (for longitude): {_deg}'
    return _dec


def add_checksum(data: bytearray, pos: int = 1) -> bytearray:
    """Adds a checksum to the data bytearray in the specified position (default: 1)
      checksum is the XOR of all bytes in the data bytearray
      returns the data bytearray with the checksum added to idx position
    """
    assert isinstance(data, bytearray), f'/add_checksum: Invalid data type: {type(data)}'
    assert isinstance(pos, int), f'/add_checksum: Invalid position type: {type(data)}'
    assert 0 <= pos < len(data), f'/add_checksum: Invalid position: {pos} (len(data)={len(data)})'
    chksum = 0
    for b in data:      # XOR the hex string
        chksum ^= b
    print(f'chksum: {hex(chksum)}')
    data[pos] = chksum  # insert checksum @ idx-pos (0x 0b CS 00 cc 00...; CS= checksum, cc = command code)
    return data


class CclDecoder(object):
    ''' This attaches to the incoming dataframe queue and raises events when recognized messages are received
    '''

    @staticmethod
    def decode_dataframe(dataframe):
        msg_class = CclTypes[dataframe.data[0]]
        ccl_message = msg_class.from_data(dataframe.data)
        ccl_message['src'] = dataframe.src
        ccl_message['dest'] = dataframe.dest

        return ccl_message

    @staticmethod
    def decode_data(data):
        msg_class = CclTypes[data[0]]
        ccl_message = msg_class.from_data(data)

        return ccl_message

    @staticmethod
    def decode_hex_string(hex_data):
        data = data_from_hexstring(hex_data)
        msg_class = CclTypes[data[0]]
        ccl_message = msg_class.from_data(data)

        return ccl_message

    def __init__(self, modem):
        modem.rxframe_listeners.append(self.on_modem_rxframe)
        self.modem = modem
        self.ccl_listeners = []

    def on_modem_rxframe(self, dataframe):
        # Check for all the CCL types
        ccl_message = self.decode_dataframe(dataframe)
        self.on_ccl_received(ccl_message)

    def on_ccl_received(self, ccl_message):
        self.modem._daemon_log.debug(f"CCL Message Received: {ccl_message['mode']}")

        for listener in self.ccl_listeners:
            try:
                listener(ccl_message)
            except Exception as exc:
                self.modem._daemon_log.debug(f"CCL Message: {ccl_message}")
                try:
                    self._daemon_log.warn(f"Error in ccl_listener [{listener}]: {(exc,)}", exc_info=True)
                except:
                    self._daemon_log.warn(f"Error in ccl_listener [{listener}]: {exc}\n{traceback.format_exc()}")


class MdatCommandMessage(dict):
    fields = ('mode', 'command', 'command_code' 'parameter')

    def __init__(self, command_code=None, use_updated_firmware=True):
        if command_code is None:
            raise ValueError("Must specify a command code")
        elif command_code not in command_codes:
            raise TypeError(f"Invalid command code [{command_code}]; must be one of {command_codes.keys()}")
        self['mode'] = 'MDAT_COMMAND'
        self['command_code'] = command_code
        self['command'] = command_codes[command_code]
        self['parameter'] = bytearray(29)
        self._add_checksum = use_updated_firmware

    @property
    def as_data(self) -> bytearray:
        databytes = bytearray([11, 0])
        databytes.append(self['command_code'])
        databytes.extend(self['parameter'])
        if self._add_checksum:
            databytes = add_checksum(databytes, pos=1)
        return databytes

    @classmethod
    def from_data(cls, databytes) -> 'MdatCommandMessage':

        values = dict.fromkeys(MdatCommandMessage.fields)

        # accept either the full frame payload or just the data after the CCL type identifier
        if len(databytes) > 31:
            databytes = databytes[1:-1]

        values['mode'] = 'MDAT_COMMAND'

        chksum = True if databytes[0] else False
        values['command_code'] = databytes[2]
        values['command'] = command_codes[databytes[2]]
        values['parameter'] = databytes[3:-1]

        # Make a message
        mdat_command = cls(command_code=values['command_code'], use_updated_firmware=chksum)

        return mdat_command


class MdatRangerMessage(dict):
    fields = ('mode', 'latitude', 'longitude',
              'fix_age', 'heading', 'mission_mode',
              'depth', 'major_fault', 'mission_leg', 'num_legs', 'speed_kt',
              'battery_percent')

    @classmethod
    def from_data(cls, databytes) -> 'MdatRangerMessage':
        values = dict.fromkeys(MdatRangerMessage.fields)

        # accept either the full frame payload or just the data after the CCL type identifier
        if len(databytes) > 31:
            databytes = databytes[1:-1]

        values['mode'] = 'MDAT_RANGER'

        hex_string = ''.join('{:02x}'.format(x) for x in databytes)
        # Now, hex_string is a 62-character string

        # Latitude
        lat_deg = int(hex_string[1:3])
        lat_dir = 'N' if hex_string[3] == 'a' else 'S'
        lat_min = float(hex_string[4:10]) / 10000.
        values['latitude'] = "{}{}{}".format(lat_deg, lat_dir, lat_min)

        values['lat_deg'] = lat_deg
        values['lat_decmin'] = lat_min
        values['lat_dir'] = lat_dir

        # Longitude
        lon_deg = int(hex_string[10:13])
        lon_dir = 'E' if hex_string[13] == 'b' else 'W'
        lon_min = float(hex_string[14:20]) / 10000.

        values['longitude'] = "{}{}{}".format(lon_deg, lon_dir, lon_min)

        values['lon_deg'] = lon_deg
        values['lon_decmin'] = lon_min
        values['lon_dir'] = lon_dir

        values['mission_leg'] = int(hex_string[20:24])
        values['num_legs'] = int(hex_string[24:28])

        values['time_remaining'] = "{}:{}".format(hex_string[28:30], hex_string[30:32])

        values['battery_percent'] = int(hex_string[32:34])
        values['speed_kt'] = "{}.{}".format(hex_string[34], hex_string[35])

        values['heading'] = int(hex_string[36:39])

        values['fix_age'] = "{}:{}".format(hex_string[40:42], hex_string[42:44])

        values['depth'] = int(hex_string[44:46])

        values['mission_mode'] = ranger_mission_modes.get(int(hex_string[46:48]),
                                                          "Unknown mode ({})".format(hex_string[46:48]))

        values['major_fault'] = True if (hex_string[48] == '8') else False

        # Make a message
        mdat_ranger = cls(values)

        return mdat_ranger


class MdatStateMessage(dict):
    '''
    A single MDAT_STATE message
    '''

    # Note that we don't override the dict initializer.

    fields = ('mode', 'latitude', 'longitude',
              'fix_age', 'time_date', 'heading', 'mission_mode',
              'depth', 'faults_bits', 'mission_leg', 'estimated_velocity', 'objective_index',
              'power_watts', 'goal_latitude', 'goal_longitude', 'battery_percent', 'gfi_percent',
              'pitch', 'oil')

    # This automagically retrieves values from the dictionary when they are referenced as properties.
    # Whether this is awesome or sucks is open to debate.
    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise AttributeError(item)

    def __setattr__(self, item, value):
        """Maps attributes to values.
        Only if we are initialised
        """
        if not self.__dict__.has_key(
                '_MdatStateMessage__initialized'):  # this test allows attributes to be set in the __init__ method
            return dict.__setattr__(self, item, value)
        elif self.__dict__.has_key(item):  # any normal attributes are handled normally
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __str__(self):
        ''' Default human-readable version
        Doesn't show all parameters, just the most common ones.'''
        hrstr = "State Message:\t{ts}\t{lat}\t{lon}".format(
            ts=self['time_date'], lat=self['latitude'], lon=self['longitude'])

        return hrstr

    @classmethod
    def from_data(cls, databytes) -> 'MdatStateMessage':

        values = dict.fromkeys(MdatStateMessage.fields)

        # accept either the full frame payload or just the data after the CCL type identifier
        if len(databytes) > 31:
            databytes = databytes[1:]

        d = BitStream(bytes=databytes)

        values['mode'] = 'MDAT_STATE'

        lat_bits = BitArray(d.read('bits:24'))
        values['latitude'] = decode_latlon(lat_bits)

        lon_bits = BitArray(d.read('bits:24'))
        values['longitude'] = decode_latlon(lon_bits)

        values['fix_age'] = d.read('uint:8') * 4
        values['time_date'] = decode_time_date(d.read('bits:24'))
        values['heading'] = d.read('uint:8') * (360.0 / 255.0)

        mission_mode_depth_bits = d.read('bits:16')
        (values['mission_mode'], values['depth']) = decode_mission_mode_and_depth(mission_mode_depth_bits)
        values['faults_bits'] = d.read('bits:40')
        values['mission_leg'] = d.read('uint:8')
        values['estimated_velocity'] = d.read('uint:8') / 25.0
        values['objective_index'] = d.read('uint:8')
        values['power_watts'] = d.read('uint:8') * 4.0

        goal_lat_bits = BitArray(d.read('bits:24'))
        values['goal_latitude'] = decode_latlon(goal_lat_bits)
        goal_lon_bits = BitArray(d.read('bits:24'))
        values['goal_longitude'] = decode_latlon(goal_lon_bits)

        values['battery_percent'] = d.read('uint:8')

        gfi_pitch_oil_encoded = BitArray(d.read('bits:16'))
        gfi_pitch_oil_encoded.byteswap()
        values['gfi_percent'] = gfi_pitch_oil_encoded[11:].uint * 100.0 / 31.0
        values['oil'] = gfi_pitch_oil_encoded[6:11].uint * 100.0 / 31.0
        values['pitch'] = gfi_pitch_oil_encoded[0:6].int * 180.0 / 63.0

        # Make a message
        mdat_state = cls(values)

        return mdat_state

    @property
    def as_data(self) -> bytes:

        try:  # to pack fix_age into 8 bits (1-byte unsigned-int)
            bitstring.pack("uint:8", self['fix_age'] // 4)
        except bitstring.CreationError as _err:
            print(f"WARNING: MdatStateMessage.as_data: fix_age value {self['fix_age']} // 4 --> {_err}\n"
                  "\tArtificially limiting fix_age to 1020 (17.0 mins) due to uint:8 packing requirement...")
            _fix_age = 255  # 1020 // 4
        else:
            _fix_age = self['fix_age'] // 4

        try:  # to pack 'faults_bits' to 40 bits
            _bit_array = BitArray(uint=self['faults_bits'], length=40)
        except TypeError:  # unorderable type: BitStream
            _bit_array = BitArray(uint=self['faults_bits'].uint, length=40)

        s = bitstring.pack('uint:8, bits:24, bits:24, uint:8, bits:24, uint:8, bits:16, bits:40, uint:8, uint:8, '
                           'uint:8, uint:8, bits:24, bits:24, uint:8, bits:16',
                           14,  # MDAT_STATE
                           encode_latlon(self['latitude']),
                           encode_latlon(self['longitude']),
                           _fix_age,
                           encode_time_data(self['time_date']),
                           self['heading'] * (255.0 / 360.0),
                           encode_mission_mode_and_depth(self['mission_mode'], self['depth']),
                           _bit_array,
                           self['mission_leg'],
                           self['estimated_velocity'] * 25,
                           self['objective_index'],
                           self['power_watts'] // 4,
                           encode_latlon(self['goal_latitude']),
                           encode_latlon(self['goal_longitude']),
                           self['battery_percent'],
                           encode_gfi_oil_pitch(self['gfi_percent'], self['oil'], self['pitch'])
                           )
        return s.bytes

    @classmethod
    def from_ranger(cls, ranger: MdatRangerMessage) -> 'MdatStateMessage':
        """Converts a MdatRangerMessage to a MdatStateMessage
        MdatStateMessage differ from MdatRanger in the following:
          lat/lng: MdatRanger is deg_mindec, MdatState is decimal degrees
          fix_age: MdatRanger is MM:SS, MdatState is SSSS (seconds)
          mission_mode: MdatRanger uses ccl.ranger_mission_modes, MdatState uses ccl.mission_modes

          time_date: MdatRanger has no datetime info, MdatState has 'time_date'
          estimated_velocity: MdatRanger has speed_kt, MdatState has 'estimated_velocity'
          major_fault: MdatRanger has major_fault, MdatState has 'faults_bits'
          num_legs: MdatRanger has num_legs, MdatState has 'objective_index'

          battery_percent, heading, depth, mission_leg are all the same
        """
        # copy and remove the contradictory keys from ranger dict...
        _mdat = ranger.copy()
        _mdat.pop('mode')
        _mdat.pop('latitude')
        _mdat.pop('longitude')
        _mdat.pop('fix_age')
        _mdat.pop('mission_mode')

        # rebuild the mdat_state dict...
        _mdat['mode'] = 'MDAT_STATE'

        _mdat['latitude'] = dms_to_decimal(ranger['latitude'])
        _mdat['longitude'] = dms_to_decimal(ranger['longitude'])

        _fix_min, _fix_sec = ranger['fix_age'].split(':')
        _fix_age = int(_fix_min) * 60 + int(_fix_sec)
        _mdat['fix_age'] = _fix_age

        print(f"MdatRanger MissionMode: <{ranger['mission_mode']}>")
        if 'pre' in ranger['mission_mode'].lower():
            _mdat['mission_mode_code'] = 1
        elif ranger['mission_mode'].lower() in ('mission', 'run'):
            _mdat['mission_mode_code'] = 6
        elif ranger['mission_mode'].lower() in ('completed', 'done', 'finished'):
            _mdat['mission_mode_code'] = 0
        else:
            _mdat['mission_mode_code'] = 3

        _code = _mdat['mission_mode_code']
        print(f'MdatState MissionMode: <{_code}: {mission_modes[_code]}>')
        _mdat['mission_mode'] = mission_modes[_code]

        # convert the "similar" keys...
        _mdat['estimated_velocity'] = convert_knots_to_meters_per_second(float(ranger['speed_kt']))
        _mdat['faults_bits'] = 0 if not ranger['major_fault'] else 1  # TODO: is this accurate/desired?

        # TODO: is this accurate / desired?
        # _mdat['objective_index'] = ranger['num_legs']
        _mdat['objective_index'] = 0    # represents None (not incl in RANGER; based on objective_names)

        _mdat['time_date'] = datetime.utcnow() if 'current_time' not in ranger else ranger['current_time']

        # fill in the missing keys...
        _mdat['gfi_percent'] = 0.0
        _mdat['goal_latitude'] = 0.0
        _mdat['goal_longitude'] = 0.0
        _mdat['oil'] = 0.0
        _mdat['pitch'] = 0.0
        _mdat['power_watts'] = 0.0

        return cls(_mdat)


CclTypes = {11: MdatCommandMessage,     # 0x0B
            14: MdatStateMessage,       # 0x0E
            16: MdatRangerMessage}      # 0x10
