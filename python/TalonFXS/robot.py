#!/usr/bin/env python3
"""
    This is a demo program for TalonFXS usage in Phoenix 6
"""
import wpilib
from wpilib import Timer, XboxController
from phoenix6 import hardware, controls, configs, signals, StatusCode

class MyRobot(wpilib.TimedRobot):
    """
    Example program that shows how to use TalonFXS
    in Phoenix 6 python
    """

    def robotInit(self):
        """Robot initialization function"""

        # Keep a reference to all the motor controllers used
        self.talonfxs = hardware.TalonFXS(1, "canivore")
        self.control = controls.DutyCycleOut(0)

        self.timer = Timer()
        self.timer.start()

        self.joystick = XboxController(0)

        # Configs for FXS, set motor type to Minion
        cfg = configs.TalonFXSConfiguration()
        cfg.commutation.motor_arrangement = signals.MotorArrangementValue.MINION_JST

        # Retry config apply up to 5 times, report if failure
        status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        for _ in range(0, 5):
            status = self.talonfxs.configurator.apply(cfg)
            if status.is_ok():
                break
        if not status.is_ok():
            print(f"Could not apply configs, error code: {status.name}")

    def teleopPeriodic(self):
        """Every 100ms, print the status of the StatusSignal"""

        self.talonfxs.set_control(self.control.with_output(self.joystick.getLeftY()))

        if self.timer.hasElapsed(0.1):
            self.timer.reset()
            # get_position automatically calls refresh(), no need to manually refresh.
            #
            # StatusSignals also implement the str dunder to provide a useful print of the signal
            pos = self.talonfxs.get_position()
            print(f"Positions is {str(pos)} with {pos.timestamp.get_latency()} seconds of latency")

            # Get the velocity StatusSignal without refreshing
            vel = self.talonfxs.get_velocity(False)
            # This time wait for the signal to reduce latency
            vel.wait_for_update(0.1)
            print(f"Velocity is {vel} with {vel.timestamp.get_latency()} seconds of latency")

            print("")


if __name__ == "__main__":
    wpilib.run(MyRobot)
