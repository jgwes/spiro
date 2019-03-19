import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd

# class that draws a spirograph
class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):

        # instantiate turtle object
        self.t = turtle.Turtle()
        # define cursor shape as turtle -- more choices at
        self.t.shape('turtle')
        # set the angle increment (step) for the parametric drawing at 5 degrees
        self.step = 5
        # set the drawing complete flag
        self.drawingComplete = False

        # set the parameters
        self.setparams(xc, yc, col, R, r, l)

        # intialize the drawing
        self.restart()

    # set the parameters
    def setparams(self, xc, yc, col, R, r, l):
        # store the coordinates of the center of the curve
        self.xc = xc
        self.yc = yc
        # convert the radius of each circle to an integer
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        # reduce r/R to its smallest form by dividing with the GCD
        gcdVal = gcd(self.r, self.R)
        # determine the periodicity of the curve
        self.nRot = self.r//gcdVal

        # get ratio of radii - used in parametric equation to model motion of the pen
        self.k = r/float(R)

        # set color
        self.t.color(*col)

        # store the current angle
        self.a = 0

    # initialize the drawing
    # resets the drawing parameters for the Spiro object and gets ready for a draw
    def restart(self):
        # set the flaghttps
        self.drawingComplete = True

        # show the Turtle
        self.t.showturtle()

        # go to the first point & lift point of pen
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0

        # compute x and y coordinates with angle set to 0 to get curve's starting point
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))

        # move the pen to the starting point computed above
        self.t.pos(self.xc + x, self.yc + y)
        self.t.down()

    # draw the entire curve in a continuous line
    def draw(self):
        # draw the rest of the points
        R, k, l = self.R, self.K, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            # compute x and y coordinates for each value of the i parameter
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        # drawing is complete so hide Turtle/cursor
        self.t.hideturtle()

    # update by one step
    def update(self):
        # skip if done
        if self.drawingComplete:
            return
        # increment the current angle
        self.a += self.step
        # draw a step
        R, k, l = self.R, self.k, self.l
        # calculate the (x,y) corresponding to the current angle & move the cursor (t) there
        # and drawing the line segment in the process
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.xy + y)
        # if drawing is complete, set the flag
        if self.a >= 360*self.nRot:
        # determine if you have reached the periodicity if so quit
            self.drawingComplete = True
            # drawing is done so hide Turtle
            self.t.hideturtle()

    # def clear(self):
        self.t.clear()


# class SpiroAnimator allows to draw random spiros simultaneously
# this class uses a timer to draw the curves one segment at a time,
# and updates the graphics periodically
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # set the timer (deltaT) value in milliseconds
        self.deltaT = 10
        # get the window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        # create the Spiro objects
        self.spiros = [] # create empty array of Spiro objects
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams() # creat random tuple of params
            # set the spiro parameters
            spiro = Spiro(*rparams) # use * operator to convert rparams tuple to list of parameters
            self.spiros.append(spiro)
        # call timer
        turtle.ontimer(self.update, self.deltaT) # set ontimer to call update() every deltaT milliseconds

    # genRandomParams
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(50, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        xy = random.randint(-height//2, height//2)
        col = (random.random(),
                random.random(),
                random.random())
        return (xc, yc, col, R, r, l)

    # restart the spiro drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set the spiro parameters
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    # class update method called by the timer to update all spiro objects
    # used in the animation
    def update(self):
        #update all spiros
        nComplete = 0
        for sprio in self.spiros:
            # update
            spiro.update()
            # count completed spiros
            if spiro.drawingComplete:
                nComplete += 1
        # restart if all spiros are completed
        if nComplete == len(self.spiros):
            self.restart()
        # call the ontimer
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle cursor on and off
    def toggleTurtles(self):
        for spiro in self.spiros:
            if sprio.t.invisible():
                spiro.t.hideturtle()
            else:
                sprio.t.showturtle()

    # save drawings as PNG files
    def saveDrawing():
        # hide turtle cursor
        turtle.hideTurtle()
        # generate unique filenames
        dateStr = (datetime.now()).strftime("%d$b%Y-%h%M%S")
        fileName = 'spiro-' + dateStr
        print('Saving drawing to %s.eps/png' % fileName)
        # get tkinter canvas
        canvas = turtle.getcanvas()
        # save postscript Image
        canvas.postscript(file = fileName + '.eps')
        # use PIL to convert to png
        img = Image.open(fileName + '.eps')
        img.save(fileName + '.png', 'png')
        # show turtle
        turtle.showturtle()

# main() function
def main():
    # use sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr = """This program draws spirographs using the Turtle module.
    When run with no arguments, this program draws random spirographs.

    Terminology:
    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r.
    """
    parser = argparse.ArgumentParser(description=descStr)

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")


    # parse args
    args = parser.parse_args()

    # set to 80% screen width
    turtle.setup(width=0.8)

    # set cursor shape
    turtle.shape('turtle')

    # set title
    turtle.title("Spirographs!")
    # add key handler for saving images
    saveDrawing = ""
    turtle.onkey(saveDrawing, "s")
    # start listening
    turtle.listen()

    # hide main turtle cursor
    turtle.hideturtle()

    # checks args and draw
    if args.sparams:
        params = [float(x) for x in args.sparams]
        # draw spirograph with given parameters
        # black by default
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        # create animator object
        spiroAnim = SpiroAnimator(4)
        # add key handler to toggle turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # add key handler to restart animation
        turtle.onkey(spiroAnim.restart, "space")

    # start turtle main loop
    turtle.mainloop()

# call main
if __name__ == '__main__':
    main()
