# SETTINGS
#######################################################
# feed_speed = 0.01
mov_pause_duration = 0.8

# User input
num_takes = int(input('Number of takes (default 20): ') or 20)
shutter_duration = float(input('Focus time (seconds, default 3): ') or 3.0)
focus_pause_duration = float(input('Take time (seconds, default 1): ') or 1.0)


# DEFINITIONS
#######################################################
def G_move(axis, dist):
  code = 'G0 '
  code += axis + str(dist)
  # code += ' F' + str(feed_speed)
  code += ' (Linear move)'
  return(code)

def G_pause(duration):
  return('G4 P' + str(duration) + '; Pause')

def G_shutter():
  code = []
  code.append(G_pause(mov_pause_duration))
  code.append('M9 ; Shutter on')
  code.append(G_pause(shutter_duration))
  code.append('M8 ; Shutter off')
  code.append(G_pause(focus_pause_duration))
  return (code)

def G_header(t):
  return ('; ***** ' + str.upper(t) + ' *****')

def write_file():
  with open('output/arduino.gcode', 'w') as file:
    i = 0
    for line in gcode:
      file.write('N' + '{:0>4d}'.format(i) + '   ' + line + '\n')
      i += 1
    print ('\narduino.gcode succesfully saved (' + str(len(gcode)) + ' lines)')


# SCRIPT
#######################################################
print('\nWorking...')

# Calculated variables
turn_distance = '{:.3f}'.format(1/num_takes)

# Initialize gcode output with first line
gcode = [G_header('initialization')]
gcode.append('M8 ; Initialize shutter/coolant to OFF position')
gcode.append('G91 ; Switch to relative coordinates')
gcode.append('G92 X0 Y0 Z0 ; Set all axis to 0')

# First shot
gcode.append(G_header('begin turn motion'))
gcode += G_shutter()

# Move-shutter loop
for i in range(num_takes - 1):
  gcode.append(G_move('X', turn_distance))
  gcode += G_shutter()
  if i % 10 == 9:
    turn = str(i+1)
    gcode.append(G_header(turn + ' turns'))

# Finalize file
# gcode.append('M84 ; Steppers off')

# Run!
write_file()
