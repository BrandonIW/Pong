#Step1 - Define initial scoreboard/playing field, paddle, and pong ball                                           - Done

#Step2 - Move the paddles up/down via arrow keys and track the coordinates that it covers upon each move          - Done
    #  - This isn't like snake where we're in constant motion. Instead we're just moving a certain number of blocks
    #  - up/down and then stopping

#Step3 - Check coordinates and move paddle to opposite ends if outside of boundary                                - Done
#Step3 - Define Start Game Button
#Step4 - Define the ball's initial movement when the game starts. Likely needs separate thread
#Step5 - Define the ball's bounce off the paddle in a specific direction if it hits the paddle or the boundary
#Step6 - Upon hitting a paddle, paddle that we control must switch
#Step7 - If the Ball hits coordinates beyond the paddle, reset and score += 1 for the paddle we're controlling
#Step8 - If we hit 10 points or whatever, display PlayerX wins, do you wanna play again etc.
#Step9 - Get rid of print statements everywhere


from tkinter import Tk, Canvas, IntVar, Label, Frame
from itertools import cycle
from time import sleep
from functools import wraps
from random import uniform
from secrets import choice
from threading import Thread
from multiprocessing import Process

class Pong:


    #### Define default screen size for the playing area
    WIDTH = 600
    HEIGHT = 550

    #### Defines velocities for ball. We want X velocity to always be a decent speed, otherwise the ball might take forever
    #### to hit one end, so xvelocity will be 2 or -2. Y velocity doesn't really matter as much in terms of speed, so we
    #### can give it some good randomness
    xVelocity = choice([2,-2])
    yVelocity = uniform(-3,3)


    def __init__(self):
        ### Define Window
        self.window = Tk()
        self.window.title("Pong by https://github.com/BrandonIW")
        self.window.geometry("600x600")
        self.window.config(background="black")


        #### Define Frame to contain score and reset. Use pack_propagate to ensure the frame's dimensions override the
        #### child dimensions
        self.frame_score_reset_start=Frame(self.window, bg = "white", width = 600, height=50)
        self.frame_score_reset_start.pack(side = "top")
        self.frame_score_reset_start.pack_propagate(0)


        ### Define score board
        self.Left_Score = 0
        self.Left_Score_Var = IntVar()
        self.Label_Left = Label(self.frame_score_reset_start,
                                textvariable = self.Left_Score_Var,
                                font=('consolas',30),
                                bg = 'white',padx = 120)

        self.Right_Score = 0
        self.Right_score_Var = IntVar()
        self.Label_Right = Label(self.frame_score_reset_start,
                                 textvariable = self.Left_Score_Var,
                                 font=('consolas',30),
                                 bg = 'white',padx = 120)

        self.Label_Right.pack(side = "right")
        self.Label_Left.pack(side = "left")


        ### Define playing field canvas
        self.canvas = Canvas(self.window,width=Pong.WIDTH, height=Pong.HEIGHT, bg = 'black')
        self.canvas.pack(side = "bottom")


        ### Define Paddles & Starting Locations
        self.paddle_Left = self.canvas.create_rectangle(20,
                                                    (Pong.HEIGHT / 2),
                                                    35,
                                                    (Pong.HEIGHT / 2)+55,
                                                    fill = "white")


        self.paddle_Right = self.canvas.create_rectangle(580,
                                                    (Pong.HEIGHT / 2),
                                                    565,
                                                    (Pong.HEIGHT / 2)+55,
                                                    fill = "white")


        ### Define the pong ball & Starting Location
        self.pong_ball = self.canvas.create_oval((Pong.WIDTH / 2),
                                                 (Pong.HEIGHT / 2),
                                                 (Pong.WIDTH / 2) + 25,
                                                 (Pong.HEIGHT / 2) + 25,
                                                 fill = "white")
        self.pong_width = self.canvas.bbox(self.pong_ball)[2] - self.canvas.bbox(self.pong_ball)[0]
        self.pong_height = self.canvas.bbox(self.pong_ball)[3] - self.canvas.bbox(self.pong_ball)[1]

        ### List of both of our paddle objects. We choose one of our paddles as the starting point
        self.paddle_list = [self.paddle_Right, self.paddle_Left]
        self.current_paddle = next(cycle(self.paddle_list))

        ### Define coordinates to track
        self.Right_Coords = self.canvas.coords(self.paddle_Right)
        self.Left_Coords = self.canvas.coords(self.paddle_Left)


    def _check_coord(func):
        @wraps(func)
        def wrapper(self,*args,**kwargs):
            print(self.Right_Coords)
            print(self.Left_Coords)
            func(self,*args,**kwargs)
        return wrapper


    def main(self):
        ### Select Movement. Use lambda to get arguments into the function. Arg1 = the current paddle.
        ### Arg2 = Current paddle's coordinates as a list

        while True:
            self.ball_movement()
            self.window.bind("<Up>",lambda event, a=self.current_paddle, b=self.canvas.coords(self.current_paddle): self.move_up(event,a,b))
            self.window.bind("<Down>",lambda event, a=self.current_paddle, b=self.canvas.coords(self.current_paddle): self.move_down(event,a,b))
            self.window.update()


    def ball_movement(self):
        coordinates = self.canvas.coords(self.pong_ball)                # Gets the coordinates of pong ball


        if coordinates[0] >= (Pong.WIDTH - self.pong_width) or coordinates[0] <= -1:
            Pong.xVelocity = Pong.xVelocity * -1
        if coordinates[1] >= (Pong.HEIGHT - self.pong_height) or coordinates[1] <= -1:
            Pong.yVelocity = Pong.yVelocity * -1

        self.canvas.move(self.pong_ball,Pong.xVelocity,Pong.yVelocity)
        self.window.update() # Update the window for any changes
        sleep(0.01)          # The thread will then pause for 0.01 sec



    ################ Main movement functions ################

    ### QOL just so we can keep track of coordinates for troubleshooting
    @_check_coord
    def move_up(self,event,paddle,coordinates):

        ### Unpack coordinates of the current paddle
        x,y,x2,y2 = coordinates

        ### Move current paddle up 10 pixels
        self.canvas.coords(paddle,x,y-15,x2,y2-15)

        ### Take coordinates of the new paddle location, and update the paddle's coordinates. If paddle is outside of
        ### boundary, reverse location of paddle
        if paddle == 2:
            self.Right_Coords = self.canvas.coords(paddle)
            self._check_boundry(paddle,self.Right_Coords)

        if paddle == 1:
            self.Left_Coords = self.canvas.coords(paddle)
            self._check_boundry(paddle,self.Left_Coords)


    @_check_coord
    def move_down(self,event,paddle,coordinates):

        ### Unpack coordinates of the current paddle
        x,y,x2,y2 = coordinates

        ### Move current paddle up 10 pixels
        self.canvas.coords(paddle,x,y+15,x2,y2+15)

        ### Take coordinates of the new paddle location, and update the paddle's coordinates
        if paddle == 2:
            self.Right_Coords = self.canvas.coords(paddle)
            self._check_boundry(paddle,self.Right_Coords)

        if paddle == 1:
            self.Left_Coords = self.canvas.coords(paddle)
            self._check_boundry(paddle,self.Left_Coords)

        self.window.update()


### If we move the paddle to boundary, we swap positions to the top
    def _check_boundry(self,paddle,coodinates):
        if coodinates[1] == -55:
            self.canvas.coords(paddle,565,545,580,600)

        elif coodinates[3] == 615:
            self.canvas.coords(paddle,565,-40,580,15)

        self.window.update()



            # #### Check if collision, which will return a boolean. If True, grow the snake, spawn another food, increment score
            # if self._check_collision(self.canvas.bbox(self.snakehead),self.canvas.bbox(self.food)):
            #     self._food_relocate()
            #     self._spawn_body("up")
            #     self.scorevar.set(self._increment_score(self.score))


if __name__ == '__main__':
    game1 = Pong()
    game1.main()
