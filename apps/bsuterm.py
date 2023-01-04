import serial
ser = serial.Serial('COM15')
ser_bytes = ser.readline()

while True:
    ser_bytes = ser.readline()
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    raw_data = decoded_bytes.split(",")
    data = [float(raw_data[0]), str(raw_data[1], float(raw_data[2]))]
    
