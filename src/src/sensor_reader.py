import serial

ser = serial.Serial('COM7', 9600, timeout=2)

print("Serial connected")

while True:
    line = ser.readline().decode().strip()

    if line:
        print("Raw data:", line)

        try:
            # Expected format: N: 4 P: 5 K: 11
            parts = line.split()

            N = int(parts[1])
            P = int(parts[3])
            K = int(parts[5])

            print(f"N: {N}  P: {P}  K: {K}")

        except Exception:
            print("Invalid data format")
