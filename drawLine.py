# Take input from user and draw a line there
# eg: h20 (draws horizontal line at 20 pixels)

import imageio
import argparse
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import sys

def draw_horizontal(x, im):
  im[x:x+1,:] = 0 #color
  plt.imshow(im)
  plt.draw()

def draw_vertical(y, im):
  im[:,y:y+1] = 0 #color
  plt.imshow(im)
  plt.draw()

def crop(axis, lb, ub, im):
  if axis == 'x':
    ub = int(min(ub, im.shape[0]))
    im = im[lb:ub,:]
  else:
    ub = int(min(ub, im.shape[1]))
    im = im[:,lb:ub]
  plt.imshow(im)
  plt.draw()
  return im

def dispatch(stdin, image):
  if stdin in ["q", "exit", "quit"]:
    sys.exit(0)
  elif stdin == "":
    print("Displaying image as is.")
    plt.imshow(image)
    plt.draw()
  elif stdin[0:4] == "save":
    if stdin[4:] == "":
      print("Must provide a file name for new file")
    imageio.imwrite(stdin[5:], image)
    print("Saved edited image to" + stdin[4:])
    sys.exit(0)
  elif stdin[0:4] == "crop":
    try:
      _, axis, lb, ub = stdin.split(' ')
      if axis not in ['x', 'y']:
        raise ValueError("Invalid axis")
      return crop(axis, int(lb), float(ub), image)
    except ValueError:
      print("The correct syntax for crop is \"crop x/y lb ub\"")
  else:
    imcopy = np.empty_like(image)
    imcopy[:] = image
    lines = stdin.split(',')
    for line in lines:
      if line[0] == 'h':
        try:
          px = int(line[1:])
          draw_horizontal(px, imcopy)
        except ValueError:
          print(line[1:], "is not an integer")
      elif line[0] == 'v':
        try:
          px = int(line[1:])
          draw_vertical(px, imcopy)
        except ValueError:
          print(line[1:], "is not an integer")
      else:
        print(line[0], "is not either 'v' or 'h'")
  return image

# acceptable grammar:
# where () is used to group, | signifies OR, list() signifies comma separated
# potential repetition, and INT signifies an integer
# list(LINE) | crop_fn | EMPTY | EXIT
# line := ("h"|"v")INT
# crop_fn := crop ("x"|"y") INT INT
# EXIT := "q" | "quit" | "exit"
# EMPTY := ""
def main(args):
  color = args.color
  plt.ion()
  try:
    im = imageio.imread(args.imagefile)
  except IOError:
    print("File not found.")
    return

  while(True):
    print("Enter a list of lines (eg \"h20\" or \"v100\")")
    print("or crop x/y lbound ubound")
    stdin = raw_input()
    im = dispatch(stdin, im)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=
    'Draws a line on the given image at specified location(s)')
  parser.add_argument('imagefile',
    help='accepts image file extensions handled by imageio')
  parser.add_argument('--color', default='red',
    help='the color to fill the drawn lines (eg blue, red, green) ')
  args = parser.parse_args()
  main(args)
