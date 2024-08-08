//AKASH YADAV

class TollBooth:
    TOLL_LAT = 37.7749
    TOLL_LON = -122.4194
    TOLL_RADIUS = 0.01  # Radius in degrees
    TOLL_CHARGE = 10.0  # Toll charge amount

    def __init__(self, gps_module, servo_motor, lcd_module):
        self.gps_module = gps_module
        self.servo_motor = servo_motor
        self.lcd_module = lcd_module
        self.user_balance = {}  # Dictionary to store user balances
        self.car_data = []
        self.gate_status = "Closed"

    def set_balance(self, user_id, amount):
        """Set the initial balance for a user."""
        self.user_balance[user_id] = amount

    def update_balance(self, user_id, amount):
        """Update the balance for a user."""
        if user_id in self.user_balance:
            self.user_balance[user_id] += amount
        else:
            self.user_balance[user_id] = amount

    def get_balance(self, user_id):
        """Retrieve the current balance for a user."""
        return self.user_balance.get(user_id, 0)

    def is_within_toll_area(self, lat, lon):
        return (abs(self.TOLL_LAT - lat) <= self.TOLL_RADIUS and abs(self.TOLL_LON - lon) <= self.TOLL_RADIUS)

    def deduct_toll(self, user_id, amount):
        if self.user_balance[user_id] >= amount:
            self.user_balance[user_id] -= amount
            return True
        return False

    def handle_car_entry(self, user_id, lat, lon):
        self.car_data.append({'user_id': user_id, 'lat': lat, 'lon': lon})
        self.lcd_module.display_message(f"Car: {user_id}\nLat: {lat:.2f} Lon: {lon:.2f}")

        if self.is_within_toll_area(lat, lon):
            if self.deduct_toll(user_id, self.TOLL_CHARGE):
                self.gate_status = "Open"
                self.lcd_module.display_message("Toll charged\nGate opening")
                self.servo_motor.open_gate()
                self.gate_status = "Closed"
                self.lcd_module.display_message("Gate closed")
                return "Toll charged successfully. Gate opening."
            else:
                self.lcd_module.display_message("Insufficient\nbalance")
                return "Insufficient balance. Toll not charged."
        else:
            self.lcd_module.display_message("Outside toll\narea")
            return "You are outside the toll area."
