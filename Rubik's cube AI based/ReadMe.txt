#######################################################################################################################################
# I wrote a Python script with Tensorflow to model the Rubik's cube as tensors and to allow the user to manipulate
the cube using the Python input () function
(ref. https://www.w3schools.com/python/python_user input.asp). The Python script is to output suitably
formatted text to the display. We created a simple menu system is to be created to allow the user to the following:

1.Rotate the right side of the cube 90 degrees forwards.
2.Rotate the right side of the cube 90 degrees backwards.
3.Rotate the left side of the cube 90 degrees forwards.
4.Rotate the left side of the cube 90 degrees backwards.
6.Rotate the top side of the cube 90 degrees left.
7.Rotate the top side of the cube 90 degrees right.
8.Rotate the bottom side of the cube 90 degrees left.
9.Rotate the bottom side of the cube 90 degrees right.
10.Display a text representation of the cube on the display as a 2D net.
11.Quit the Python script run.
Considering the the 3D cube as a 2D net and we identified how the elements on each face move according to the actions of the user. Each face of the cube will contain 9 elements, where each element has a colour
and position. When the script is run, the cube defaults to the completed cube as shown in the above image.