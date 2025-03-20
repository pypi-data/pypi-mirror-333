import smbus

class L9110:
    def __init__(self, i2c_address=0x40, i2c_bus_number=1):
        self.i2c_address = i2c_address
        self.bus = smbus.SMBus(i2c_bus_number)

        self.MODE_RC = 0
        self.S1 = 1
        self.S2 = 2
        self.MODE_DC = 1
        self.MA = 0
        self.MB = 1
        self.CW = 0
        self.CCW = 1
        self.MODE_SET_ADDR = 2

    def _map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    def rc_data_send(self, rc_motor, degree):
        """
        Create a list of data to be sent to the L9110 in RC servo mode.

        Args:
            rc_motor (int): 1 for S1 or 2 for S2.
            degree (int): 0-180 of the servo's position.

        Returns:
            list: A list of data to be sent via i2c.
        """
        data = [self.i2c_address, self.MODE_RC, 0, 0, 0, 0]
        pulse = self._map_range(degree, 0, 180, 500, 2500)

        data[2] = rc_motor
        data[3] = pulse >> 8
        data[4] = pulse & 0xFF
        data[5] = sum(data)
        return data

    def dc_data_send(self, dc, percent, direction):
        """
        Create a list of data to be sent to the L9110 in DC motor mode.

        Args:
            dc (int): 0 for MA or 1 for MB.
            percent (int): Speed percentage (0-100) of the DC motor.
            direction (int): 0 for clockwise (CW) or 1 for counterclockwise (CCW).

        Returns:
            list: A list of data to be sent via i2c.
        """

        data = [self.i2c_address, self.MODE_DC, 0, 0, 0, 0]
        data[2] = dc
        data[3] = self._map_range(percent, 0, 100, 0, 255)
        data[4] = direction
        data[5] = sum(data)
        return data

    def set_address(self, old_address, new_address):
        """
        Change the I2C address of the L9110 device.

        Args:
            old_address (int): The current I2C address of the device.
            new_address (int): The new I2C address to be set for the device.

        Raises:
            IOError: If there is an error in communication with the device.
        """

        try:
            self.bus.write_i2c_block_data(old_address, new_address, [self.MODE_SET_ADDR, 0, 0, 0, new_address + self.MODE_SET_ADDR])
            print('Set address successful')
            print('New address is:', hex(new_address))
        except IOError as e:
            print('Error:', e)

    def send_i2c_data(self, data):
        """
        Send the given data to the L9110 via i2c.

        Args:
            data (list): A list of data to be sent via i2c. The first element is
                the i2c address of the device, and the other elements are the
                data to be sent.

        Raises:
            IOError: If there is an error in communication with the device.
        """
        try:
            self.bus.write_i2c_block_data(data[0], data[0], data[1:])
        except IOError as e:
            print('Error:', e)
