import binascii
import serial
import time
import serial.tools.list_ports
import subprocess


class Serial:
    def __init__(self):
        pass

    # 打开串口
    def loginSer(self, COM):
        global ser
        port = COM  # 设置端口号
        baudrate = 9600  # 设置波特率
        bytesize = 8  # 设置数据位
        stopbits = 1  # 设置停止位
        parity = "N"  # 设置校验位

        try:
            ser = serial.Serial(port, baudrate)
        except serial.SerialException as e:
            # pass
            print(e)
        if (ser.isOpen()):  # 判断串口是否打开
            pass
        else:
            ser.open()

    def get_current_COM(self):
        serial_list = []
        ports = list(serial.tools.list_ports.comports())
        if len(ports) != 0:
            for port in ports:
                if 'SERIAL' in port.description:
                    COM_name = port.device.replace("\n", "").replace(" ", "").replace("\r", "")
                    serial_list.append(COM_name)
            return serial_list
        else:
            return []

    def logoutSer(self):
        if ser.isOpen():
            ser.close()

    def send_status_cmd(self):
        num = ser.write(bytes.fromhex("A0 01 05 A6"))
        time.sleep(2)  # sleep() 与 inWaiting() 最好配对使用
        ser.inWaiting()
        data = str(binascii.b2a_hex(ser.read(num)))[2:-1]  # 十六进制显示方法2
        if "a00100a1" in data:
            return False
        elif "a00101a2" in data:
            return True

    def send_ser_connect_cmd(self, conn=True):
        if conn:
            ser.write(bytes.fromhex("A0 01 01 A2"))
        else:
            ser.write(bytes.fromhex("A0 01 00 A1"))
        time.sleep(1)

    def confirm_relay_opened(self, timeout=30):
        now_time = time.time()
        while True:
            self.confirm_relay_closed()
            print(11111111111111111111111111111111111111111)
            self.send_ser_connect_cmd(conn=True)
            print(2222222222222222222222222222222222)
            if self.send_status_cmd():
                break
            if time.time() > now_time + timeout:
                assert False, "@@@@无法打开继电器，请检查！！！！"
            time.sleep(1)

    def confirm_relay_closed(self, timeout=30):
        now_time = time.time()
        while True:
            self.send_ser_connect_cmd(conn=False)
            if not self.send_status_cmd():
                break
            if time.time() > now_time + timeout:
                assert False, "@@@@无法打开继电器，请检查！！！！"
            time.sleep(1)

    def check_usb_adb_connect_serial(self, device_name):
        self.confirm_relay_opened()
        print(self.invoke("adb devices"))
        if self.remove_space('%sdevice' % device_name) in self.remove_space(self.invoke("adb devices")):
            return True
        else:
            return False

    def check_usb_adb_connect_no_serial(self, device_name):
        if self.remove_space('%sdevice' % device_name) in self.remove_space(self.invoke("adb devices")):
            return True
        else:
            return False

    def invoke(self, cmd, runtime=30):
        try:
            output, errors = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE).communicate(
                timeout=runtime)
            o = output.decode("utf-8")
            return o
        except subprocess.TimeoutExpired as e:
            return

    def remove_space(self, text):
        return text.replace("\r", "").replace("\n", "").replace(" ", "").replace(" ", "").replace("\r", "").replace("\n", "").replace("\t", "")


if __name__ == '__main__':
    s = Serial()
    COM = ""
    COM_LIST = s.get_current_COM()
    if len(COM_LIST) == 0:
        raise Exception("没有可用的COM口，请检查！！！！")
    elif len(COM_LIST) == 1:
        COM = COM_LIST[0]
        s.loginSer(COM)
        s.confirm_relay_opened()
        s.confirm_relay_closed()
        s.logoutSer()
    else:
        raise Exception("多个可用的COM口，请输入需要测试的COM口")
