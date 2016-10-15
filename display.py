import serial
import onebus

ser = serial.Serial('/dev/ttyS0')

def clear():
    ser.write([254, 128]) # set cursor to start
    ser.write(b''.join([b' ' for i in range(16)]))
    ser.write(b''.join([b' ' for i in range(16)]))
    ser.write([254, 128]) # set cursor to start


def main():
    arrivals = onebus.get_arrival_times()
    rows = onebus.get_display_rows(arrivals)
    print("Got rows: {}".format(rows))
    clear()
    for row in rows:
        output_str = '{: <16}'.format(row[:16])
        #print("Output:{}".format(output_str))
        ser.write(output_str.encode('ascii'))

if __name__ == '__main__':
    main()
