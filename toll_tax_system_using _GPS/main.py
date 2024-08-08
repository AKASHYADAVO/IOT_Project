
//AKAASH YADAV
from servo_motor import ServoMotor
from lcd_module import LCDModule
from toll_booth import TollBooth
from toll_booth_server import TollBoothServer
from toll_booth_web_server import TollBoothWebServer

if __name__ == '__main__':
    # Toll booth setup
    servo_motor = ServoMotor(17)  # GPIO 17
    lcd_module = LCDModule()
    toll_booth = TollBooth(None, servo_motor, lcd_module)  # Toll booth does not use a GPS module

    # Set initial balances for users
    toll_booth.set_balance('user1', 20.0)
    toll_booth.set_balance('user2', 50.0)

    toll_booth_server = TollBoothServer(toll_booth)
    toll_booth_web_server = TollBoothWebServer(toll_booth)

    toll_booth_server.start()
    toll_booth_web_server.start()
