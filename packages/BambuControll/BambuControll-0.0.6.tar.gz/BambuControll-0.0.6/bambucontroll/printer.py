import paho.mqtt.client as mqtt
from typing import Dict, Any
import ssl
import time
import json
import logging

class printer:
    def __init__(self, ip: str, printer_id: str, password: str, port: int = 8883, client_id: str = "BambuControll", username: str = "bblp"):
        """Initialize Bambu printer connection."""
        self.printer_ip = ip
        self.printer_id = printer_id
        self.topic = f"device/{printer_id}/report"
        self.port = port
        self.client_id = client_id
        self.username = username
        self.password = password
        self.debug = False
        self._setup_mqtt_client(self.client_id, self.username, self.password)
        self._connect_printer(port)
    
    class state:
        printer_data = {}
        first_message_received = False
        bed_temp = None
        extruder_temp = None
        aux_fan_speed = None
        chamber_fan_speed = None
        cooling_fan_speed = None
        task = None
        light = None
    
    def _setup_mqtt_client(self, client_id: str, username: str, password: str):
        """Set up MQTT client with SSL."""
        # Create MQTT client instance
        self.client = mqtt.Client(client_id=client_id, clean_session=True)
        # Set up TLS without certificate validation
        self.client.tls_set(certfile=None, 
                          keyfile=None,
                          cert_reqs=ssl.CERT_NONE,
                          tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.tls_insecure_set(True)
        # Set username and password
        self.client.username_pw_set(username, password)
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Set up MQTT callbacks."""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info(f"Connected successfully to {self.printer_ip}")
                client.subscribe(self.topic)
            else:
                logging.error(f"Connection failed with code {rc}")
        
        def on_message(client, userdata, msg):
            try:
                data = json.loads(msg.payload.decode())
                self._update_printer_state(data)
            except json.JSONDecodeError:
                logging.error("Failed to decode printer message")

        self.client.on_connect = on_connect
        self.client.on_message = on_message
    
    def _update_printer_state(self, data: dict[str, Any]):
        """Update internal printer state from MQTT message."""
        for category, values in data.items():
            if category not in self.state.printer_data:
                self.state.printer_data[category] = {}
            self.state.printer_data[category].update(values)
            self.state.printer_data[category]['last_updated'] = time.time()

        if 'print' in data:
            self.state.bed_temp = self.state.printer_data['print'].get('bed_temper')
            self.state.extruder_temp = self.state.printer_data['print'].get('nozzle_temper')
            self.state.aux_fan_speed = self.state.printer_data['print'].get('big_fan1_speed')
            self.state.task = self.state.printer_data['print'].get('mc_print_sub_stage')
            self.state.chamber_fan_speed = self.state.printer_data['print'].get('big_fan2_speed')
            self.state.cooling_fan_speed = self.state.printer_data['print'].get('cooling_fan_speed')

        if 'system' in data:
            self.state.light = self.state.printer_data['system'].get('led_mode')    
        self.state.first_message_received = True

        if self.debug:
            print(f"### Received from printer: {data}")
    
    
    def _connect_printer(self, port: int):
        """Establish connection to printer."""
        self.client.connect(self.printer_ip, port, keepalive=60)
        self.client.loop_start()
        time.sleep(2)  # Allow time for connection
        while not self.state.first_message_received:
            print("Waiting for first message...")
            time.sleep(1)
        print("First message received!")
    ################## Printer functions ##################
    ################## Printer functions ##################

    def push(self, filename = "default", under_temperature = 30, object_hight = 256, push_every = 40):
        object_hight = int(object_hight)
        self.set_bed_temperature(under_temperature, white=True, state="less")
        self.set_bed_temperature(0)

        # Check if object_hight is valid
        if object_hight > 256: object_hight = 256
        if object_hight < 0: object_hight = 0

        print("/////////////////// STARTING PUSHING ///////////////////")
        print(time.strftime("%H:%M:%S", time.localtime()))

        if filename == "default":
            # loop trough the object hight (from the top to the bottom)
            while True:
                # Calculate pushing hight
                while True:
                    if (object_hight % push_every) == 0: break
                    object_hight -= 1
                print(f"Pushing object hight: {object_hight}")
                
                if object_hight == 0: object_hight = 0.8

                push_gcode = f"""
G1 X1
G1 Z{object_hight} F4000
G1 Y0
G1 Y251

G1 X50
G1 Z{object_hight}
G1 Y0
G1 Y251

G1 X100
G1 Z{object_hight}
G1 Y0
G1 Y251

G1 X150
G1 Z{object_hight}
G1 Y0
G1 Y251

G1 X256
G1 Z{object_hight}
G1 Y0
G1 Y251

G1 X206
G1 Z{object_hight}
G1 Y0
G1 Y251

G1 X150
G1 Z{object_hight}
G1 Y0
G1 Y251

G1 X100
G1 Z{object_hight}
G1 Y0
G1 Y251

M220 S100  ; Reset feedrate magnitude
M201.2 K1.0 ; Reset acc magnitude
M73.2   R1.0 ;Reset left time magnitude
M1002 set_gcode_claim_speed_level : 0

M17 X0.8 Y0.8 Z0.5 ; lower motor current to 45% power
"""
                
                # Send the gcode
                for line in push_gcode.splitlines():
                    if line.strip() == "done":
                        break
                    print(f"Sending: {line.strip()}")
                    self.send_gcode(line)
                
                # Go to the next hight
                object_hight -= 1
                
                time.sleep(60)
                # Check if we are done
                if object_hight <= 1: break
                
        else:
            # Send the gcode file line by line
            with open(filename, "r") as file:
                for line in file:
                    if line.strip() == "done":
                        break
                    print(f"Sending: {line.strip()}")
                    self.send_gcode(line)
            time.sleep(100)
        print("/////////////////// ENDING PUSHING ///////////////////")
        print(time.strftime("%H:%M:%S", time.localtime()))
        printer.light("off")
        while printer.state.light != "off":
            print("/////////////////// ACTUALLY ENDING PUSHING ///////////////////")
            print(time.strftime("%H:%M:%S", time.localtime()))

    def wait_to_finish(self):
        while self.state.task == 0:
            time.sleep(.1)
        
        print(self, "Waiting for printer to finish", end="")
        while True:
            if self.state.task == 0:
                break
            time.sleep(.1)
            print(".", end="")
        print("")

    def set_extruder_temperature(self, temperature, white=False, state="exect"):
        """
        Set the extruder temperature to the given value.
        
        Args:
            temperature (int): The target temperature.
            white (bool, optional): If True, wait until the actual temperature is within 2 degrees of the target temperature. Defaults to False.
            state (str, optional): The state to wait for. Can be "exect", "more", or "less". Defaults to "exect".
        """
        self.send_gcode(f"M104 S{temperature}")
        print(f"Hotend Temp set to: {temperature}")
        while self.state.extruder_temp == None:
            print("Waiting to receive temperature!")
            time.sleep(2)
        if white:
            if state == "exect":
                while self.state.extruder_temp < temperature - 2 or self.state.extruder_temp > temperature + 2:
                    print(f"Hotend Temp: {self.state.extruder_temp} ==> {temperature}")
                    time.sleep(2)
                print(f"Hotend Temp: {self.state.extruder_temp} == {temperature}")
            elif state == "more":
                while self.state.extruder_temp < temperature - 2:
                    print(f"Hotend Temp: {self.state.extruder_temp} < {temperature}")
                    time.sleep(2)
                print(f"Hotend Temp: {self.state.extruder_temp} == {temperature}")
            elif state == "less":
                while self.state.extruder_temp > temperature + 2:
                    print(f"Hotend Temp: {self.state.extruder_temp} > {temperature}")
                    time.sleep(2)
                print(f"Hotend Temp: {self.state.extruder_temp} == {temperature}")
    
    def set_bed_temperature(self, temperature, white=False, state="exect"):
        """
        Set the bed temperature to the given value.
        
        Args:
            temperature (int): The target temperature.
            white (bool, optional): If True, wait until the actual temperature is within 2 degrees of the target temperature. Defaults to False.
            state (str, optional): The state to wait for. Can be "exect", "more", or "less". Defaults to "exect".
        """
        self.send_gcode(f"M140 S{temperature}")
        print(f"Bed Temp set to: {temperature}")
        while self.state.bed_temp == None:
            print("Whating to recive temperature!")
            time.sleep(2)
        if white:
            if state == "exect":
                while self.state.bed_temp < temperature - 2 or self.state.bed_temp > temperature + 2:
                    print(f"Bed Temp: {self.state.bed_temp} ==> {temperature}")
                    time.sleep(2)
                print(f"Bed Temp: {self.state.bed_temp} == {temperature}")
            elif state == "more":
                while self.state.bed_temp < temperature - 2:
                    print(f"Bed Temp: {self.state.bed_temp} < {temperature}")
                    time.sleep(2)
                print(f"Bed Temp: {self.state.bed_temp} == {temperature}")
            elif state == "less":
                while self.state.bed_temp > temperature + 2:
                    print(f"Bed Temp: {self.state.bed_temp} > {temperature}")
                    time.sleep(2)
                print(f"Bed Temp: {self.state.bed_temp} == {temperature}")

    def light(self, state = "on"):
        command_dict = {
            "system": {
                "sequence_id": "0",
                "command": "ledctrl",
                "led_node": "chamber_light",
                "led_mode": state,
                "led_on_time": 500,
                "led_off_time": 500,
                "loop_times": 0,
                "interval_time": 0
            }
        }
        self.client.publish(self.topic, json.dumps(command_dict))

    def background(self):
        self.light("on")
        self.send_gcode("M17 X0.3 Y0.3")
        self.send_gcode("G1 X230 F400")
        self.send_gcode("G1 Y40")
        self.send_gcode("G1 X40")
        self.send_gcode("G1 Y230")
        self.send_gcode("M17 X1 Y1 Z1")

    def send_gcode(self, command):
        command_dict = {
            "print": {
                "command": "gcode_line",
                "param": command,
                "sequence_id": "0"
            }
        }
        self.client.publish(self.topic, json.dumps(command_dict))
        time.sleep(0.1)
    
    def start_print(self, filename, plate = 1, use_ams=False, timelapse=False, flow_cali=False, bed_leveling=True, layer_inspect=False, vibration_calibration=False):
        command_dict = {
            "print": {
            "command": "project_file",
            "url": f"file:///sdcard/{filename}",
            "param": f"Metadata/plate_{plate}.gcode",
            "subtask_id": "0",
            "use_ams": use_ams,
            "timelapse": timelapse,
            "flow_cali": flow_cali,
            "bed_leveling": bed_leveling,
            "layer_inspect": layer_inspect,
            "vibration_cali": vibration_calibration
          }
        }
        self.client.publish(self.topic, json.dumps(command_dict))
        time.sleep(0.1)
    
    def cooling_fan(self, speed):
        self.send_gcode(f"M106 P1 S{speed}")
    
    def aux_fan(self, speed):
        self.send_gcode(f"M106 P2 S{speed}")
    
    def chamber_fan(self, speed):
        self.send_gcode(f"M106 P3 S{speed}")

    def home(self):
        self.send_gcode("G28")