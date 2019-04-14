import math
import turtle

# draws a circle
def drawCircleTurtle(x, y, r):
    #move to start of circle
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()

    #draw the circle
    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))

drawCircleTurtle(100,100,100)
turtle.mainloop()
