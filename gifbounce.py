# Make a picture into a bouncing gif
# See http://knowyourmeme.com/memes/intensifies for examples

# Open image
# Create shifted versions
# Make gif out of them
import imageio

filenames = ['nootnoot.png', 'nootnoot2.png', 'nootnoot3.png']

images = []
for filename in filenames:
  images.append(imageio.imread(filename))
imageio.mimsave('noot.gif', images)

