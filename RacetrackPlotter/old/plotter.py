from graphics import *
import csv

def main():
   load_data() 

def show_data(lines):
    win = GraphWin("Plotter", 100, 100)
    c = Circle(Point(50,50), 10)
    c.draw(win)
    while True:
        win.getMouse()
    win.close()

def load_data(filename='data.txt'): 
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 0:
                print("New Line")
            else:
                print(f"X: {row[0]}, Y: {row[1]}")

if __name__ == "__main__":
    main()
