class TouchController:
    def __init__(self, serialPort):
        self.serialPort = serialPort

    def Touch(self, pin: int, charge_t: int, charge_s: int, timeout: int):
        cmd = "touch({0}, {1}, {2}, {3})".format(pin, charge_t, charge_s, timeout)
        self.serialPort.WriteCommand(cmd)

        res = self.serialPort.ReadRespone()
        
        val = False
        if res.success:
            try:
                return res.respone
            except:
                pass
        return val
