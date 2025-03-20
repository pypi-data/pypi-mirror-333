# Initialize an L9110 I2C driver
    Parameters
        i2c_address (int): The i2c address of the L9110 chip. Default is 0x40.
        i2c_bus_number (int): The number of the I2C bus to use. Default is 1.
    Example: Initialize l9110 object with default address and default i2c bus
        l9110 = L9110()
    Example: Initialize object l9110 with address 0x42 and i2c bus 1
        l9110 = L9110(i2c_address=0x42, i2c_bus_number=1)

# rc_data_send(rc_motor, degree)
    Create a list of data to be sent to the L9110 in RC servo mode.
        Args:
            rc_motor (int): 1 for S1 or 2 for S2.
            degree (int): 0-180 of the servo's position.
        Returns:
            list: A list of data to be sent via i2c.
    Example: control servo 1 with 150 degree
        servo_data = l9110.rc_data_send(l9110.S1, 150)

# dc_data_send(dc, percent, direction)
    Create a list of data to be sent to the L9110 in DC motor mode.
        Args:
            dc (int): 0 for MA or 1 for MB.
            percent (int): Speed percentage (0-100) of the DC motor.
            direction (int): 0 for clockwise (CW) or 1 for counterclockwise (CCW).
        Returns:
            list: A list of data to be sent via i2c.
    Example: control DC motor with 50% speed and clockwise
        dc_data = l9110.dc_data_send(l9110.MA, 50, l9110.CW)

# set_address(old_address, new_address)
    Change the I2C address of the L9110 device.
        Args:
            old_address (int): The current I2C address of the device.
            new_address (int): The new I2C address to be set for the device.
        Raises:
            IOError: If there is an error in communication with the device.
    Example: set i2c address to 0x42
        set_address(0x40, 0x42)