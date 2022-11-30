from niveau1 import FiniteStateMachine


class ledBlinkers:
    def __init__(self):
        pass


class eyesBlinkers:
    def __init__(self):
        pass


class GoPiGo3:
    def __init__(self):
        pass

        def volt(self):
            """
            This method returns the battery voltage of the `GoPiGo3`_.

            :return: The battery voltage of the `GoPiGo3`_.
            :rtype: float

            """
            voltage = self.get_voltage_battery()
            return voltage

    [docs]

    def set_speed(self, in_speed):
        """
        This method sets the speed of the `GoPiGo3`_ specified by ``in_speed`` argument.

        The speed is measured in *DPS = degrees per second* of the robot's wheel(s).

        :param int in_speed: The speed at which the robot is set to run - speed between **0-1000** DPS.

        .. warning::

             **0-1000** DPS are the *preferred* speeds for the `GoPiGo3`_ robot.
             The speed variable can be basically set to any positive value, but factors like *voltage*, *load*, *battery amp rating*, etc, will determine the effective speed of the motors.

             Experiments should be run by every user, as each case is unique.

        """
        try:
            self.speed = int(in_speed)
        except:
            self.speed = self.DEFAULT_SPEED
        self.set_motor_limits(self.MOTOR_LEFT + self.MOTOR_RIGHT,
                              dps=self.speed)

    [docs]

    def get_speed(self):
        """
        Use this method for getting the speed of your `GoPiGo3`_.

        :return: The speed of the robot measured between **0-1000** DPS.
        :rtype: int

        """
        return int(self.speed)

    [docs]

    def reset_speed(self):
        """
        This method resets the speed to its original value.

        """
        self.set_speed(self.DEFAULT_SPEED)

    [docs]

    def stop(self):
        """
        This method stops the `GoPiGo3`_ from moving.
        It brings the `GoPiGo3`_ to a full stop.

        .. note::

             This method is used in conjuction with the following methods:

                 * :py:meth:`~easygopigo3.EasyGoPiGo3.backward`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.right`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.left`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.forward`

        """
        self.set_motor_dps(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        time.sleep(0.1)
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, self.MOTOR_FLOAT)
        time.sleep(0.1)

    [docs]

    def forward(self):
        """
        Move the `GoPiGo3`_ forward.

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to **300** - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        """
        self.set_motor_dps(self.MOTOR_LEFT + self.MOTOR_RIGHT,
                           self.NO_LIMIT_SPEED)

    [docs]

    def drive_cm(self, dist, blocking=True):
        """
        Move the `GoPiGo3`_ forward / backward for ``dist`` amount of centimeters.

        | For moving the `GoPiGo3`_ robot forward, the ``dist`` parameter has to be *positive*.
        | For moving the `GoPiGo3`_ robot backward, the ``dist`` parameter has to be *negative*.

        :param float dist: The distance in ``cm`` the `GoPiGo3`_ has to move.
        :param boolean blocking = True: Set it as a blocking or non-blocking method.

        ``blocking`` parameter can take the following values:

             * ``True`` so that the method will wait for the `GoPiGo3`_ robot to finish moving.
             * ``False`` so that the method will exit immediately while the `GoPiGo3`_ robot will continue moving.

        """
        # dist is in cm
        # if dist is negative, this becomes a backward move

        dist_mm = dist * 10

        # the number of degrees each wheel needs to turn
        WheelTurnDegrees = ((dist_mm / self.WHEEL_CIRCUMFERENCE) * 360)

        # get the starting position of each motor
        StartPositionLeft = self.get_motor_encoder(self.MOTOR_LEFT)
        StartPositionRight = self.get_motor_encoder(self.MOTOR_RIGHT)

        self.set_motor_position(self.MOTOR_LEFT,
                                (StartPositionLeft + WheelTurnDegrees))
        self.set_motor_position(self.MOTOR_RIGHT,
                                (StartPositionRight + WheelTurnDegrees))

        if blocking:
            while self.target_reached(
                    StartPositionLeft + WheelTurnDegrees,
                    StartPositionRight + WheelTurnDegrees) is False:
                time.sleep(0.1)

    [docs]

    def drive_inches(self, dist, blocking=True):
        """
        Move the `GoPiGo3`_ forward / backward for ``dist`` amount of inches.

        | For moving the `GoPiGo3`_ robot forward, the ``dist`` parameter has to be *positive*.
        | For moving the `GoPiGo3`_ robot backward, the ``dist`` parameter has to be *negative*.

        :param float dist: The distance in ``inches`` the `GoPiGo3`_ has to move.
        :param boolean blocking = True: Set it as a blocking or non-blocking method.

        ``blocking`` parameter can take the following values:

             * ``True`` so that the method will wait for the `GoPiGo3`_ robot to finish moving.
             * ``False`` so that the method will exit immediately while the `GoPiGo3`_ robot will continue moving.

        """
        self.drive_cm(dist * 2.54, blocking)

    [docs]

    def drive_degrees(self, degrees, blocking=True):
        """
        Move the `GoPiGo3`_ forward / backward for ``degrees / 360`` wheel rotations.

        | For moving the `GoPiGo3`_ robot forward, the ``degrees`` parameter has to be *positive*.
        | For moving the `GoPiGo3`_ robot backward, the ``degrees`` parameter has to be *negative*.

        :param float degrees: Distance based on how many wheel rotations are made. Calculated by ``degrees / 360``.
        :param boolean blocking = True: Set it as a blocking or non-blocking method.

        ``blocking`` parameter can take the following values:

             * ``True`` so that the method will wait for the `GoPiGo3`_ robot to finish rotating.
             * ``False`` so that the method will exit immediately while the `GoPiGo3`_ robot will continue rotating.

        For instance, the following function call is going to drive the `GoPiGo3`_ robot forward for *310 / 360* wheel rotations, which equates to aproximately *86%*
        of the `GoPiGo3`_'s wheel circumference.

        .. code-block:: python

            gpg3_obj.drive_degrees(310)

        On the other hand, changing the polarity of the argument we're passing, is going to make the `GoPiGo3`_ robot move backward.

        .. code-block:: python

            gpg3_obj.drive_degrees(-30.5)

        This line of code makes the `GoPiGo3`_ robot go backward for *30.5 / 360* rotations, which is roughly *8.5%* of the `GoPiGo3`_'s wheel circumference.

        """
        # these degrees are meant to be wheel rotations.
        # 360 degrees would be a full wheel rotation
        # not the same as turn_degrees() which is a robot rotation
        # degrees is in degrees, not radians
        # if degrees is negative, this becomes a backward move

        # get the starting position of each motor
        StartPositionLeft = self.get_motor_encoder(self.MOTOR_LEFT)
        StartPositionRight = self.get_motor_encoder(self.MOTOR_RIGHT)

        self.set_motor_position(self.MOTOR_LEFT,
                                (StartPositionLeft + degrees))
        self.set_motor_position(self.MOTOR_RIGHT,
                                (StartPositionRight + degrees))

        if blocking:
            while self.target_reached(
                    StartPositionLeft + degrees,
                    StartPositionRight + degrees) is False:
                time.sleep(0.1)
        return

    [docs]

    def backward(self):
        """
        Move the `GoPiGo3`_ backward.

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to ``300`` - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        """
        self.set_motor_dps(self.MOTOR_LEFT + self.MOTOR_RIGHT,
                           self.NO_LIMIT_SPEED * -1)

    [docs]

    def right(self):
        """
        Move the `GoPiGo3`_ to the right.

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to **300** - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        .. important::
             | The robot will activate only the left motor, whilst the right motor will be completely stopped.
             | This causes the robot to rotate in very short circles.

        """
        self.set_motor_dps(self.MOTOR_LEFT, self.NO_LIMIT_SPEED)
        self.set_motor_dps(self.MOTOR_RIGHT, 0)

    [docs]

    def spin_right(self):
        """
        Rotate the `GoPiGo3` towards the right while staying on the same spot.

        This differs from the :py:meth:`~easygopigo3.EasyGoPiGo3.right` method as both wheels will be rotating but in different directions.
        This causes the robot to spin in place, as if doing a pirouette.

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to **300** - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        .. important::
             You can achieve the same effect by calling ``steer(100, -100)`` (method :py:meth:`~easygopigo3.EasyGoPiGo3.steer`).

        """

        self.set_motor_dps(self.MOTOR_LEFT, self.NO_LIMIT_SPEED)
        self.set_motor_dps(self.MOTOR_RIGHT, self.NO_LIMIT_SPEED * -1)

    [docs]

    def left(self):
        """
        Move the `GoPiGo3`_ to the left.

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to **300** - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        .. important::
             | The robot will activate only the right motor, whilst the left motor will be completely stopped.
             | This causes the robot to rotate in very short circles.

        """
        self.set_motor_dps(self.MOTOR_LEFT, 0)
        self.set_motor_dps(self.MOTOR_RIGHT, self.NO_LIMIT_SPEED)

    [docs]

    def spin_left(self):
        """
        Rotate the `GoPiGo3` towards the left while staying on the same spot.

        This differs from the :py:meth:`~easygopigo3.EasyGoPiGo3.left` method as both wheels will be rotating but in different directions.
        This causes the robot to spin in place, as if doing a pirouette.

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to **300** - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        .. important::
             You can achieve the same effect by calling ``steer(-100, 100)`` (method :py:meth:`~easygopigo3.EasyGoPiGo3.steer`).

        """
        self.set_motor_dps(self.MOTOR_LEFT, self.NO_LIMIT_SPEED * -1)
        self.set_motor_dps(self.MOTOR_RIGHT, self.NO_LIMIT_SPEED)

    [docs]

    def steer(self, left_percent, right_percent):
        """
        Control each motor in order to get a variety of turning movements.

        Each motor is assigned a percentage of the current speed value.
        While there is no limit on the values of ``left_percent`` and ``right_percent`` parameters,
        they are expected to be between **-100** and **100**.

        :param int left_percent: Percentage of current speed value that gets applied to left motor. The range is between **-100** (for backward rotation) and **100** (for forward rotation).
        :param int right_percent: Percentage of current speed value that gets applied to right motor. The range is between **-100** (for backward rotation) and **100** (for forward rotation).

        For setting the motor speed, use :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed`.
        Default ``speed`` is set to **300** - see :py:meth:`~easygopigo3.EasyGoPiGo3.__init__`.

        .. important::
             Setting both ``left_percent`` and ``right_percent`` parameters to **100** will result in the same behavior as the :py:meth:`~easygopigo3.EasyGoPiGo3.forward` method.
             The other behavior for :py:meth:`~easygopigo3.EasyGoPiGo3.backward` method will be experienced if both parameters are set to **-100**.

             Setting both ``left_percent`` and ``right_percent`` to **0** will stop the GoPiGo from moving.

        """
        self.set_motor_dps(self.MOTOR_LEFT, self.get_speed() * left_percent / 100)
        self.set_motor_dps(self.MOTOR_RIGHT, self.get_speed() * right_percent / 100)

    [docs]

    def orbit(self, degrees, radius_cm=0, blocking=True):
        """
        Control the GoPiGo so it will orbit around an object.

        :param int degrees: Degrees to steer. **360** for full rotation. Negative for left turn.
        :param int radius_cm: Radius in `cm` of the circle to drive. Default is **0** (turn in place).
        :param boolean blocking = True: Set it as a blocking or non-blocking method.

        .. important::
           Note that while in non-blocking mode the speed cannot be changed before the end of the orbit as it would negate all orbit calculations.
           After a non-blocking call, :py:meth:`~easygopigo3.EasyGoPiGo3.set_speed` has to be called before any other movement.
        """
        speed = self.get_speed()
        radius = radius_cm * 10

        # the total distance to drive in mm
        drive_distance = math.pi * abs(radius) * abs(degrees) / 180  # / 180 is shorter than radius * 2 / 360

        # the distance in mm to add to one motor and subtract from the other
        drive_difference = ((self.WHEEL_BASE_CIRCUMFERENCE * degrees) / 360)

        # the number of degrees each wheel needs to turn on average to get the necessary distance
        distance_degrees = ((drive_distance / self.WHEEL_CIRCUMFERENCE) * 360)

        # the difference between motor travel in degrees
        difference_degrees = ((drive_difference / self.WHEEL_CIRCUMFERENCE) * 360)

        # the distance each wheel needs to turn
        left_target = (distance_degrees + difference_degrees)
        right_target = (distance_degrees - difference_degrees)

        # if it's a left turn
        if degrees < 0:
            MOTOR_FAST = self.MOTOR_RIGHT
            MOTOR_SLOW = self.MOTOR_LEFT
            fast_target = right_target
            slow_target = left_target
        else:
            MOTOR_FAST = self.MOTOR_LEFT
            MOTOR_SLOW = self.MOTOR_RIGHT
            fast_target = left_target
            slow_target = right_target

        # determine driving direction from the speed
        direction = 1
        speed_with_direction = speed
        if speed < 0:
            direction = -1
            speed_with_direction = -speed

        # calculate the motor speed for each motor
        fast_speed = speed_with_direction
        slow_speed = abs((speed_with_direction * slow_target) / fast_target)

        # set the motor speeds
        self.set_motor_limits(MOTOR_FAST, dps=fast_speed)
        self.set_motor_limits(MOTOR_SLOW, dps=slow_speed)

        # get the starting position of each motor
        StartPositionLeft = self.get_motor_encoder(self.MOTOR_LEFT)
        StartPositionRight = self.get_motor_encoder(self.MOTOR_RIGHT)

        # Set each motor target position
        self.set_motor_position(self.MOTOR_LEFT, (StartPositionLeft + (left_target * direction)))
        self.set_motor_position(self.MOTOR_RIGHT, (StartPositionRight + (right_target * direction)))

        if blocking:
            while self.target_reached(
                    StartPositionLeft + (left_target * direction),
                    StartPositionRight + (right_target * direction)) is False:
                time.sleep(0.1)

            # reset to original speed once done
            # if non-blocking, then the user is responsible in resetting the speed
            self.set_speed(speed)

        return

    [docs]

    def target_reached(self, left_target_degrees, right_target_degrees):
        """
        Checks if (*wheels have rotated for a given number of degrees*):

             * The left *wheel* has rotated for ``left_target_degrees`` degrees.
             * The right *wheel* has rotated for ``right_target_degrees`` degrees.

        If both conditions are met, it returns ``True``, otherwise it's ``False``.

        :param int left_target_degrees: Target degrees for the *left* wheel.
        :param int right_target_degrees: Target degrees for the *right* wheel.

        :return: Whether both wheels have reached their target.
        :rtype: boolean.

        For checking if the `GoPiGo3`_ robot has moved **forward** for ``360 / 360`` wheel rotations, we'd use the following code snippet.

        .. code-block:: python

            # both variables are measured in degrees
            left_motor_target = 360
            right_motor_target = 360

            # reset the encoders
            gpg3_obj.reset_encoders()
            # and make the robot move forward
            gpg3_obj.forward()

            while gpg3_obj.target_reached(left_motor_target, right_motor_target):
                # give the robot some time to move
                sleep(0.05)

            # now lets stop the robot
            # otherwise it would keep on going
            gpg3_obj.stop()

        On the other hand, for moving the `GoPiGo3`_ robot to the **right** for ``187 / 360`` wheel rotations of the left wheel, we'd use the following code snippet.

        .. code-block:: python

            # both variables are measured in degrees
            left_motor_target = 187
            right_motor_target = 0

            # reset the encoders
            gpg3_obj.reset_encoders()
            # and make the robot move to the right
            gpg3_obj.right()

            while gpg3_obj.target_reached(left_motor_target, right_motor_target):
                # give the robot some time to move
                sleep(0.05)

            # now lets stop the robot
            # otherwise it would keep on going
            gpg3_obj.stop()

        .. note::

            You *can* use this method in conjunction with the following methods:

                 * :py:meth:`~easygopigo3.EasyGoPiGo3.drive_cm`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.drive_inches`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.drive_degrees`

            when they are used in *non-blocking* mode.

            And almost *everytime* with the following ones:

                 * :py:meth:`~easygopigo3.EasyGoPiGo3.backward`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.right`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.left`
                 * :py:meth:`~easygopigo3.EasyGoPiGo3.forward`

        """
        tolerance = 5
        min_left_target = left_target_degrees - tolerance
        max_left_target = left_target_degrees + tolerance
        min_right_target = right_target_degrees - tolerance
        max_right_target = right_target_degrees + tolerance

        current_left_position = self.get_motor_encoder(self.MOTOR_LEFT)
        current_right_position = self.get_motor_encoder(self.MOTOR_RIGHT)

        if current_left_position > min_left_target and \
                current_left_position < max_left_target and \
                current_right_position > min_right_target and \
                current_right_position < max_right_target:
            return True
        else:
            return False

    [docs]

    def reset_encoders(self, blocking=True):
        """
        Resets both the encoders back to **0**.

        :param boolean blocking = True: Set it as a blocking or non-blocking method.

        ``blocking`` parameter can take the following values:

             * ``True`` so that the method will wait for the `GoPiGo3`_ motors to finish resetting.
             * ``False`` so that the method will exit immediately while the `GoPiGo3`_ motors will continue to reset. Sending another motor command to the motors while the reset is under way might lead to confusing behavior.

        """
        self.set_motor_power(self.MOTOR_LEFT + self.MOTOR_RIGHT, 0)
        left_target = self.get_motor_encoder(self.MOTOR_LEFT)
        right_target = self.get_motor_encoder(self.MOTOR_RIGHT)
        self.offset_motor_encoder(self.MOTOR_LEFT, left_target)
        self.offset_motor_encoder(self.MOTOR_RIGHT, right_target)

        motor_left_previous = None
        motor_right_previous = None

        if blocking:
            # Note to self. using target_reached() here didn't work.
            # So instead let's keep waiting till the motors stop moving
            while motor_left_previous != self.MOTOR_LEFT or motor_right_previous != self.MOTOR_RIGHT:
                motor_left_previous = self.MOTOR_LEFT
                motor_right_previous = self.MOTOR_RIGHT
                time.sleep(0.025)

    [docs]

    def read_encoders(self):
        """
        Reads the encoders' position in degrees. 360 degrees represent 1 full rotation (or 360 degrees) of a wheel.

        :returns: A tuple containing the position in degrees of each encoder. The 1st element is for the left motor and the 2nd is for the right motor.
        :rtype: tuple(int,int)

        """

        left_encoder = self.get_motor_encoder(self.MOTOR_LEFT)
        right_encoder = self.get_motor_encoder(self.MOTOR_RIGHT)
        encoders = (left_encoder, right_encoder)

        return encoders

    [docs]

    def read_encoders_average(self, units="cm"):
        """
        Reads the encoders' position in degrees. 360 degrees represent 1 full rotation (or 360 degrees) of a wheel.

        :param string units: By default it's "cm", but it could also be "in" for inches. Anything else will return raw encoder average.

        :returns: The average of the two wheel encoder values.
        :rtype: int
        """

        left, right = self.read_encoders()
        average = (left + right) / 2
        if units == "cm":
            average = ((average / 360) * self.WHEEL_CIRCUMFERENCE) / 10
        elif units == "in" or units == "inches" or units == "inch":
            average = ((average / 360) * self.WHEEL_CIRCUMFERENCE) / (10 * 2.54)
        else:
            pass
            # do no conversion
        return average

    [docs]

    def turn_degrees(self, degrees, blocking=True):
        """
        Makes the `GoPiGo3`_ robot turn at a specific angle while staying in the same spot.

        :param float degrees: The angle in degress at which the `GoPiGo3`_ has to turn. For rotating the robot to the left, ``degrees`` has to negative, and make it turn to the right, ``degrees`` has to be positive.
        :param boolean blocking = True: Set it as a blocking or non-blocking method.

        ``blocking`` parameter can take the following values:

             * ``True`` so that the method will wait for the `GoPiGo3`_ robot to finish moving.
             * ``False`` so that the method will exit immediately while the `GoPiGo3`_ robot will continue moving.

        In order to better understand what does this method do, let's take a look at the following graphical representation.

        .. image:: ../images/gpg3_robot.svg

        In the image, we have multiple identifiers:

             * The "*heading*": it represents the robot's heading. By default, "rotating" the robot by 0 degrees is going to make the robot stay in place.
             * The "*wheel circle circumference*": this is the circle that's described by the 2 motors moving in opposite direction.
             * The "*GoPiGo3*": the robot we're playing with. The robot's body isn't draw in this representation as it's not the main focus here.
             * The "*wheels*": these are just the `GoPiGo3`_'s wheels - selfexplanatory.

        The effect of this class method is that the `GoPiGo3`_ will rotate in the same spot (depending on ``degrees`` parameter), while the wheels will be describing a perfect circle.

        So, in order to calculate how much the motors have to spin, we divide the *angle* (at which we want to rotate the robot) by 360 degrees and we get a float number between 0 and 1 (think of it as a percentage).
        We then multiply this value with the *wheel circle circumference* (which is the circumference of the circle the robot's wheels describe when rotating in the same place).


        At the end we get the distance each wheel has to travel in order to rotate the robot by ``degrees`` degrees.

        """
        # this is the method to use if you want the robot to turn 90 degrees
        # or any other amount. This method is based on robot orientation
        # and not wheel rotation
        # the distance in mm that each wheel needs to travel
        WheelTravelDistance = ((self.WHEEL_BASE_CIRCUMFERENCE * degrees) / 360)

        # the number of degrees each wheel needs to turn
        WheelTurnDegrees = ((WheelTravelDistance / self.WHEEL_CIRCUMFERENCE) *
                            360)

        # get the starting position of each motor
        StartPositionLeft = self.get_motor_encoder(self.MOTOR_LEFT)
        StartPositionRight = self.get_motor_encoder(self.MOTOR_RIGHT)

        # Set each motor target
        self.set_motor_position(self.MOTOR_LEFT,
                                (StartPositionLeft + WheelTurnDegrees))
        self.set_motor_position(self.MOTOR_RIGHT,
                                (StartPositionRight - WheelTurnDegrees))

        if blocking:
            while self.target_reached(
                    StartPositionLeft + WheelTurnDegrees,
                    StartPositionRight - WheelTurnDegrees) is False:
                time.sleep(0.1)

    [docs]

    def blinker_on(self, id):
        """
        Turns *ON* one of the 2 red blinkers that `GoPiGo3`_ has.

        :param int|str id: **0** / **1** for the right / left led or string literals can be used : ``"right"`` and ``"left"``.


        """
        if id == 1 or id == "left":
            self.set_led(self.LED_LEFT_BLINKER, 255)
        if id == 0 or id == "right":
            self.set_led(self.LED_RIGHT_BLINKER, 255)

    [docs]

    def blinker_off(self, id):
        """
        Turns *OFF* one of the 2 red blinkers that `GoPiGo3`_ has.

        :param int|str id: **0** / **1** for the right / left led or string literals can be used : ``"right"`` and ``"left"``.

        """
        if id == 1 or id == "left":
            self.set_led(self.LED_LEFT_BLINKER, 0)
        if id == 0 or id == "right":
            self.set_led(self.LED_RIGHT_BLINKER, 0)

    [docs]

    def led_on(self, id):
        """
        Turns *ON* one of the 2 red blinkers that `GoPiGo3`_ has.
        The same as :py:meth:`~easygopigo3.EasyGoPiGo3.blinker_on`.

        :param int|str id: **0** / **1** for the right / left led or string literals can be used : ``"right"``` and ``"left"``.

        """
        self.blinker_on(id)

    [docs]

    def led_off(self, id):
        """
        Turns *OFF* one of the 2 red blinkers that `GoPiGo3`_ has.
        The same as :py:meth:`~easygopigo3.EasyGoPiGo3.blinker_off`.

        :param int|str id: **0** / **1** for the right / left led or string literals can be used : ``"right"`` and ``"left"``.

        """
        self.blinker_off(id)

    [docs]

    def set_left_eye_color(self, color):
        """
        Sets the LED color for Dexter mascot's left eye.

        :param tuple(int,int,int) color: 8-bit RGB tuple that represents the left eye's color.
        :raises TypeError: When ``color`` parameter is not valid.

        .. important::

             After setting the eye's color, call :py:meth:`~easygopigo3.EasyGoPiGo3.open_left_eye` or :py:meth:`~easygopigo3.EasyGoPiGo3.open_eyes` to update the color,
             or otherwise the left eye's color won't change.

        """
        if isinstance(color, tuple) and len(color) == 3:
            self.left_eye_color = color
        else:
            raise TypeError("Eye color not valid")

    [docs]

    def set_right_eye_color(self, color):
        """
        Sets the LED color for Dexter mascot's right eye.

        :param tuple(int,int,int) color: 8-bit RGB tuple that represents the right eye's color.
        :raises TypeError: When ``color`` parameter is not valid.

        .. important::

             After setting the eye's color, call :py:meth:`~easygopigo3.EasyGoPiGo3.open_right_eye` or :py:meth:`~easygopigo3.EasyGoPiGo3.open_eyes` to update the color,
             or otherwise the right eye's color won't change.

        """
        if isinstance(color, tuple) and len(color) == 3:
            self.right_eye_color = color
        else:
            raise TypeError("Eye color not valid")

    [docs]

    def set_eye_color(self, color):
        """
        Sets the LED color for Dexter mascot's eyes.

        :param tuple(int,int,int) color: 8-bit RGB tuple that represents the eyes' color.
        :raises TypeError: When ``color`` parameter is not valid.

        .. important::

             After setting the eyes' color, call :py:meth:`~easygopigo3.EasyGoPiGo3.open_eyes` to update the color of both eyes,
             or otherwise the color won't change.

        """
        self.set_left_eye_color(color)
        self.set_right_eye_color(color)

    [docs]

    def open_left_eye(self):
        """
        Turns *ON* Dexter mascot's left eye.

        """
        self.set_led(self.LED_LEFT_EYE,
                     self.left_eye_color[0],
                     self.left_eye_color[1],
                     self.left_eye_color[2],
                     )

    [docs]

    def open_right_eye(self):
        """
        Turns *ON* Dexter mascot's right eye.

        """
        self.set_led(self.LED_RIGHT_EYE,
                     self.right_eye_color[0],
                     self.right_eye_color[1],
                     self.right_eye_color[2],
                     )

    [docs]

    def open_eyes(self):
        """
        Turns *ON* Dexter mascot's eyes.

        """
        self.open_left_eye()
        self.open_right_eye()

    [docs]

    def close_left_eye(self):
        """
        Turns *OFF* Dexter mascot's left eye.

        """
        self.set_led(self.LED_LEFT_EYE, 0, 0, 0)

    [docs]

    def close_right_eye(self):
        """
        Turns *OFF* Dexter mascot's right eye.

        """
        self.set_led(self.LED_RIGHT_EYE, 0, 0, 0)

    [docs]

    def close_eyes(self):
        """
        Turns *OFF* Dexter mascot's eyes.

        """
        self.close_left_eye()
        self.close_right_eye()

    [docs]

    def init_light_sensor(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.LightSensor` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.LightSensor` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.LightSensor` class.

        """
        return easysensors.LightSensor(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_sound_sensor(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.SoundSensor` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.SoundSensor` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.SoundSensor` class.

        """
        return easysensors.SoundSensor(port, self, use_mutex=self.use_mutex)

    # def init_loudness_sensor(self, port = "AD1"):
    #     """
    #     | Initialises a :py:class:`~easysensors.LoudnessSensor` object and then returns it.
    #     """

    [docs]

    def init_loudness_sensor(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.LoudnessSensor` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.LoudnessSensor` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.LoudnessSensor` class.

        """
        return easysensors.LoudnessSensor(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_ultrasonic_sensor(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.UltraSonicSensor` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.UltraSonicSensor` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.UltraSonicSensor` class.

        """
        return easysensors.UltraSonicSensor(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_buzzer(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.Buzzer` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.Buzzer` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.Buzzer` class.

        """
        return easysensors.Buzzer(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_led(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.Led` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.Led` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.Led` class.

        """
        return easysensors.Led(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_button_sensor(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.ButtonSensor` object and then returns it.

        :param str port = "AD1": Can be either ``"AD1"`` or ``"AD2"``. By default it's set to be ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.ButtonSensor` class and with the port set to ``port``'s value.

        The ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.ButtonSensor` class.

        """
        return easysensors.ButtonSensor(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_line_follower(self, port="I2C"):
        """
        Initialises a :py:class:`~di_sensors.easy_line_follower.EasyLineFollower` object and then returns it.

        :param str port = "I2C": The only option for this parameter for the old Line Follower Sensor (red board) is ``"I2C"`` and for the `Line Follower Sensor`_ (black board) it can also be ``"AD1"``/``"AD2"``. The default value for this parameter is already set to ``"I2C"``.
        :returns: An instance of the :py:class:`~di_sensors.easy_line_follower.EasyLineFollower` class and with the port set to ``port``'s value.

        The ``"I2C"``, ``"AD1"`` and ``"AD2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        .. tip::

             | The sensor can be connected to any of the I2C ports.
             | You can connect different I2C devices simultaneously provided that:

                * The I2C devices have different addresses.
                * The I2C devices are recognizeable by the `GoPiGo3`_ platform.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~di_sensors.easy_line_follower.EasyLineFollower` class.

        """
        if di_sensors_available is False:
            raise ImportError("di_sensors library not found")

        lf = easy_line_follower.EasyLineFollower(port, use_mutex=self.use_mutex)
        if lf._sensor_id == 0:
            raise OSError("line follower is not reachable")

        return lf

    [docs]

    def init_servo(self, port="SERVO1"):
        """
        Initialises a :py:class:`~easysensors.Servo` object and then returns it.

        :param str port = "SERVO1": Can be either ``"SERVO1"`` or ``"SERVO2"``. By default it's set to be ``"SERVO1"``.
        :returns: An instance of the :py:class:`~easysensors.Servo` class and with the port set to ``port``'s value.

        The ``"SERVO1"`` and ``"SERVO2"`` ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.Servo` class.

        """
        return easysensors.Servo(port, self, use_mutex=self.use_mutex)

    [docs]

    def init_distance_sensor(self, port="I2C"):
        """

        Initialises a :py:class:`~di_sensors.easy_distance_sensor.EasyDistanceSensor` object and then returns it.

        :param str port = "I2C": The options for this parameter are ``"I2C"`` by default, ``"AD1"``, or ``"AD2"``.
        :returns: An instance of the :py:class:`~di_sensors.easy_distance_sensor.EasyDistanceSensor` class and with the port set to ``port``'s value.
        :raises ImportError: When the :py:mod:`di_sensors` module can't be found. Check the `DI-Sensors`_ documentation on how to install the libraries.

        The ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~di_sensors.easy_distance_sensor.EasyDistanceSensor` class.

        .. tip::

             | The sensor can be connected to any of the I2C ports.
             | You can connect different I2C devices simultaneously provided that:

                * The I2C devices have different addresses.
                * The I2C devices are recognizeable by the `GoPiGo3`_ platform.

             | If the devices share the same address, like two distance sensors for example, you can still use them with the GoPiGo3 provided at least one is connected via the ``"AD1"``, or ``"AD2"``, port.

        """
        if di_sensors_available is False:
            raise ImportError("di_sensors library not available")

        try:
            d = easy_distance_sensor.EasyDistanceSensor(port=port, use_mutex=self.use_mutex)
        except Exception as e:
            # print(e)
            d = None

        return d

    [docs]

    def init_light_color_sensor(self, port="I2C", led_state=True):
        """

        Initialises a :py:class:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor` object and then returns it.

        :param str port = "I2C": The options for this parameter are ``"I2C"`` by default, ``"AD1"``, or ``"AD2"``.
        :param boolean led_state = False: Turns the onboard LED on or off. It's best to have it on in order to detect color, and off in order to detect light value.
        :returns: An instance of the :py:class:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor` class and with the port set to ``port``'s value.
        :raises ImportError: When the :py:mod:`di_sensors` module can't be found. Check the `DI-Sensors`_ documentation on how to install the libraries.

        The ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~di_sensors.easy_light_color_sensor.EasyLightColorSensor` class.

        .. tip::

             | The sensor can be connected to any of the I2C ports.
             | You can connect different I2C devices simultaneously provided that:

                * The I2C devices have different addresses.
                * The I2C devices are recognizeable by the `GoPiGo3`_ platform.

             | If the devices share the same address, like two light/color sensors for example, you can still use them with the GoPiGo3 provided at least one is connected via the ``"AD1"``, or ``"AD2"``, port.

        """
        if di_sensors_available is False:
            raise ImportError("di_sensors library not available")

        try:
            lc = easy_light_color_sensor.EasyLightColorSensor(port=port, led_state=led_state, use_mutex=self.use_mutex)
        except Exception as e:
            # print(e)
            lc = None

        return lc

    [docs]

    def init_imu_sensor(self, port="I2C"):
        """

        Initialises a :py:class:`~di_sensors.easy_inertial_measurement_unit.EasyIMUSensor` object and then returns it.

        :param str port = "AD1": The options for this parameter are ``"AD1"`` by default, ``"AD2"``.
        :returns: An instance of the :py:class:`~di_sensors.easy_inertial_measurement_unit.EasyIMUSensor` class and with the port set to ``port``'s value.
        :raises ImportError: When the :py:mod:`di_sensors` module can't be found. Check the `DI-Sensors`_ documentation on how to install the libraries.

        The ports are mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~di_sensors.easy_inertial_measurement_unit.EasyIMUSensor` class.

        .. tip::

             | The sensor can be connected to any of the I2C ports.
             | You can connect different I2C devices simultaneously provided that:

                * The I2C devices have different addresses.
                * The I2C devices are recognizeable by the `GoPiGo3`_ platform.

             | If the devices share the same address, like two IMU sensors for example, you can still use them with the GoPiGo3 provided at least one is connected via the ``"AD1"``, or ``"AD2"``, port.

        """

        if di_sensors_available is False:
            raise ImportError("di_sensors library not available")

        try:
            imu = easy_inertial_measurement_unit.EasyIMUSensor(port=port, use_mutex=self.use_mutex)
        except Exception as e:
            # print(e)
            imu = None

        return imu

    [docs]

    def init_dht_sensor(self, sensor_type=0):
        """
        Initialises a :py:class:`~easysensors.DHTSensor` object and then returns it.

        :param int sensor_type = 0: Choose ``sensor_type = 0`` when you have the blue-coloured DHT sensor or ``sensor_type = 1`` when it's white.
        :returns: An instance of the :py:class:`~easysensors.DHTSensor` class and with the port set to ``port``'s value.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.DHTSensor` class.

        .. important::

            The only port to which this device can be connected is the ``"SERIAL"`` port, so therefore, there's no need
            for a parameter which specifies the port of device because we've only got one available.

            The ``"SERIAL"`` port is mapped to the following :ref:`hardware-ports-section`.

        """
        return easysensors.DHTSensor(self, sensor_type, self.use_mutex)

    [docs]

    def init_remote(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.Remote` object and then returns it.

        :param str port = "AD1": Can be set to either ``"AD1"`` or ``"AD2"``. Set by default to ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.Remote` class and with the port set to ``port``'s value.

        The ``"AD1"`` port is mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.Remote` class.

        """
        return easysensors.Remote(port, self, self.use_mutex)

    [docs]

    def init_motion_sensor(self, port="AD1"):
        """
        Initialises a :py:class:`~easysensors.MotionSensor` object and then returns it

        :param str port = "AD1": Can be set to either ``"AD1"`` or ``"AD2"``. Set by default to ``"AD1"``.
        :returns: An instance of the :py:class:`~easysensors.MotionSensor` class and with the port set to ``port``'s value.

        The ``"AD1"`` port is mapped to the following :ref:`hardware-ports-section`.

        The ``use_mutex`` parameter of the :py:meth:`~easygopigo3.EasyGoPiGo3.__init__` constructor is passed down to the constructor of :py:class:`~easysensors.MotionSensor` class.

        """

        return easysensors.MotionSensor(port, self, self.use_mutex)


class Robot:
    def __init__(self, robot: 'GoPiGo3', led_blinkers: 'ledBlinkers', eye_blinkers: 'eyesBlinkers'):
        self.robot = robot
        self.led_blinkers = led_blinkers
        self.eye_blinkers = eye_blinkers

    def start(self):
        pass


class C64Project(FiniteStateMachine):
    def __init__(self):
        self.robot = Robot()
        layout = FiniteStateMachine.Layout()

        # layout.initial_state = self.__off
        # layout.add_state(self.__off)

        super().__init__(layout)

    def start(self) -> None:
        print("It's Starting Time!")


if __name__ == '__main__':
    C64Project()