#This python code will display the visualization of the simplified radar chart and the state of each booth

import time
import serial
import struct
import traceback
import pygame
import math
import sys
import random

MSG_HEADER_SIZE = 16
LIDAR_REF       = 70

Booth1_angle_start=33
Booth1_angle_end=43

Booth2_angle_start=68
Booth2_angle_end=78

Booth3_angle_start=103
Booth3_angle_end=113

Booth4_angle_start=138
Booth4_angle_end=148

boothstauts=[0,0,0,0]

def read_packet(f):
    header_bytes = f.read(MSG_HEADER_SIZE)

    if len(header_bytes) < MSG_HEADER_SIZE:
        # must be out of messages
        return False

    header_data = struct.unpack(">H8sHHH", header_bytes)
    print("header sentinels: " + str(hex(header_data[0])) + ", " + str(hex(header_data[4])))

    message_type = header_data[1].split(b'\0', 1)[0]  # remove the null characters from the string
    print(message_type)
    print("message size: " + str(header_data[2]))

    if message_type == b"text":
        text_bytes = f.read(header_data[2])
        print("text message: " + str(text_bytes))

    elif message_type == b"DATA":
        bytes = f.read(header_data[2])
        data = struct.unpack(">hhhhH", bytes)
        print("DATA message: " + "Distance: "+str(data[1]) + ", " + "Angle: "+str(data[2]) +" time=" + str(data[4]))
        # Position  angle           # Lidar data                #None

        # angle=random.randint(0,180)       #Without Dragon board testing
        # lidar=random.randint(60,100)
        # data1=[0,lidar,angle]

        visualization(data)
    elif message_type == b"buttons":
        buttons_bytes = f.read(header_data[2])
        print("buttons message: " + str(hex(buttons_bytes[1])) + ", time=" + str(buttons_bytes[2]))

    return True

def visualization(data):
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((1200, 700))
    pygame.display.set_caption("Main project G2")
    # pygame：0----->x
    #        |
    #        ↓
    #        y
    # Define a queue to collect data received by the serial port
    list_line = []
    for i in range(40):
        list_line.append((100, 50))  # Populate useless data

    # Define two lists to store continuously changing colors to achieve color gradient, such as dark green to green
    green_color = []
    red_color = []

    for i in range(39, -1, -1):  # The range parameter is the number of lines you draw at a time
        color = 255 - i * 6  # The colors go from blackest to brightest
        green_color.append((0, color, 0))
        red_color.append((color, 0, 0))
    while True:
        ################################
        #Keep the window open until the user closes it#
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #############################################################
        distance = data[1]  # data[1]=Detection range   this is the data. I don't know what lidar sensor provide
                            # if it is in raw data, It should be change in to cm please tell me
                            # if it is in cm , no change

        rad = math.radians(data[2]) #input angle degree as mention 'position' in MODULE_DESIGN

        list_line.append((distance, rad))  # Data is added to the queue
        if len(list_line) > 40:  # Draw a maximum of 40 lines at a time
            list_line.pop(0)

        # Background covering
        screen.fill((0, 0, 0))

        for i in range(40):
            if list_line[i][0] < LIDAR_REF:  # The distance is less than the reference value, red line
                pygame.draw.line(screen, red_color[i], (600, 620),(600 - 600 * math.cos(list_line[i][1]), 620 - 600 * math.sin(list_line[i][1])), 3)
            else:
                pygame.draw.line(screen, green_color[i], (600, 620),(600 - 600 * math.cos(list_line[i][1]), 620 - 600 * math.sin(list_line[i][1])), 3)



        if distance < LIDAR_REF:  # Corresponding distance and warning text
            screen.blit(pygame.font.Font(None, 25).render("Find", 1, "red"), (200, 630))
            screen.blit(pygame.font.Font(None, 25).render(str(distance) + "cm", 1, "green"),(490, 630))

        else:
            screen.blit(pygame.font.Font(None, 25).render("Not Find ", 1, "green"), (180, 630))
            screen.blit(pygame.font.Font(None, 25).render("xx", 1, "green"), (490, 630))



        if Booth1_angle_start<data[2]<Booth1_angle_end:
            if distance < LIDAR_REF:
                boothstauts[0]=1
            else:
                boothstauts[0] = 0
        elif Booth2_angle_start < data[2] < Booth2_angle_end:
            if distance < LIDAR_REF:
                boothstauts[1]=1
            else:
                boothstauts[1]=0
        elif Booth3_angle_start<data[2]<Booth3_angle_end:
            if distance < LIDAR_REF:
                boothstauts[2]=1
            else:
                boothstauts[2]=0
        elif Booth4_angle_start < data[2] < Booth4_angle_end:
            if distance < LIDAR_REF:
                boothstauts[3] = 1
            else:
                boothstauts[3] = 0

        if boothstauts[0] == 1:
            screen.blit(pygame.font.Font(None, 25).render("Fall ", 1, (251, 10, 10)), (180, 660))
        else:
            screen.blit(pygame.font.Font(None, 25).render("Empyt", 1, (10, 10, 251)), (180, 660))
        if boothstauts[1] == 1:
            screen.blit(pygame.font.Font(None, 25).render("Fall ", 1, (251, 10, 10)), (380, 660))
        else:
            screen.blit(pygame.font.Font(None, 25).render("Empyt", 1, (10, 10, 251)), (380, 660))
        if boothstauts[2] == 1:
            screen.blit(pygame.font.Font(None, 25).render("Fall ", 1, (251, 10, 10)), (580, 660))
        else:
            screen.blit(pygame.font.Font(None, 25).render("Empyt", 1, (10, 10, 251)), (580, 660))
        if boothstauts[3] == 1:
            screen.blit(pygame.font.Font(None, 25).render("Fall ", 1, (251, 10, 10)), (780, 660))
        else:
            screen.blit(pygame.font.Font(None, 25).render("Empyt", 1, (10, 10, 251)), (780, 660))

        #########################################################################################################
        # Background for making radar maps
        #########################################################################################################
        # Draw bottom lines and text messages
        pygame.draw.line(screen, "green", (0, 620), (1200, 620), 5)
        screen.blit(pygame.font.Font(None, 25).render("Objects:", 1, "green"), (100, 630))
        screen.blit(pygame.font.Font(None, 25).render("Distance:", 1, "green"), (410, 630))
        screen.blit(pygame.font.Font(None, 25).render("Angle:", 1, "green"), (680, 630))
        screen.blit(
            pygame.font.Font(None, 25).render(str(int(data[2])) + "°", 1, "green"),
            (760, 630))
        screen.blit(pygame.font.Font(None, 25).render("Main Project: ", 1, (92, 255, 255)),
                    (930, 630))
        screen.blit(pygame.font.Font(None, 25).render("G2", 1, (251, 114, 153)), (1050, 630))

        screen.blit(pygame.font.Font(None, 25).render("Booth 1: ", 1, (251, 114, 153)), (100, 660))
        screen.blit(pygame.font.Font(None, 25).render("Booth 2: ", 1, (251, 114, 153)), (300, 660))
        screen.blit(pygame.font.Font(None, 25).render("Booth 3: ", 1, (251, 114, 153)), (500, 660))
        screen.blit(pygame.font.Font(None, 25).render("Booth 4: ", 1, (251, 114, 153)), (700, 660))
        # Draw semicircles and lines with special angles
        # Reference from CSDN
        pygame.draw.arc(screen, "green", (600 - 125, 620 - 125, 250, 250), math.radians(0), math.radians(181), width=3)
        pygame.draw.arc(screen, "green", (600 - 250, 620 - 250, 500, 500), math.radians(0), math.radians(181), width=3)
        pygame.draw.arc(screen, "green", (600 - 375, 620 - 375, 750, 750), math.radians(0), math.radians(180.5),width=3)
        pygame.draw.arc(screen, "green", (600 - 500, 620 - 500, 1000, 1000), math.radians(0), math.radians(180.5), width=3)
        pygame.draw.line(screen, "green", (600, 620), (600 - 600 * math.cos(math.radians(30)), 620 - 600 * math.sin(math.radians(30))), 3)
        pygame.draw.line(screen, "green", (600, 620),(600 - 600 * math.cos(math.radians(60)), 620 - 600 * math.sin(math.radians(60))), 3)
        pygame.draw.line(screen, "green", (600, 620), (600, 20), 3)
        pygame.draw.line(screen, "green", (600, 620),(600 - 600 * math.cos(math.radians(120)), 620 - 600 * math.sin(math.radians(120))), 3)
        pygame.draw.line(screen, "green", (600, 620),(600 - 600 * math.cos(math.radians(150)), 620 - 600 * math.sin(math.radians(150))), 3)
        # Distance and Angle text
        screen.blit(pygame.font.Font(None, 30).render("30°", 1, "green"), (45, 320))
        screen.blit(pygame.font.Font(None, 30).render("60°", 1, "green"), (240, 90))
        screen.blit(pygame.font.Font(None, 30).render("90°", 1, "green"), (535, 10))
        screen.blit(pygame.font.Font(None, 30).render("120°", 1, "green"), (820, 90))
        screen.blit(pygame.font.Font(None, 30).render("150°", 1, "green"), (1120, 320))
        screen.blit(pygame.font.Font(None, 20).render("5cm", 1, "green"), (730, 590))
        screen.blit(pygame.font.Font(None, 20).render("10cm", 1, "green"), (855, 590))
        screen.blit(pygame.font.Font(None, 20).render("15cm", 1, "green"), (980, 590))
        screen.blit(pygame.font.Font(None, 20).render("20cm", 1, "green"), (1105, 590))
        # Update the screen
        pygame.display.update()
        # Dragon board running speed
        pygame.time.Clock().tick(24*10^6)
        return True


def read_serial(com_port):
    serialPort = serial.Serial(port=com_port, baudrate=9600, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialString = ""  # Used to hold data coming over UART

    while True:

        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            try:
                if not read_packet(serialPort):
                    break
            except Exception as e:
                # Logs the error appropriately.
                print(traceback.format_exc())
                break

        else:
            time.sleep(0.05)


# main program entry point
if __name__ == '__main__':
    # read_file('C:/Users/Stewart Worrall/Documents/data/test.hex')
    read_serial("COM10")

