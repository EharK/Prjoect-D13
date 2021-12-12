import pandas as pd
import turtle
import threading

scrn = turtle.Screen()
scrn.bgcolor("darkgray")
racecar = turtle.Turtle()
graph = turtle.Turtle()

graph.up()
graph.fd(200)
graph.down()

for i in range(1000):
    racecar.lt(70)
    racecar.fd(100)
    graph.lt(70)
    graph.fd(100)





scrn.exitonclick()

# multiprocessing   ->  shares data in between
# threading         ->  does not share data
