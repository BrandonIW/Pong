#Step1 - Define initial scoreboard/playing field, paddle, and pong ball                                           - Done

#Step2 - Move the paddles up/down via arrow keys and track the coordinates that it covers upon each move          - Done
    #  - This isn't like snake where we're in constant motion. Instead we're just moving a certain number of blocks
    #  - up/down and then stopping

#Step3 - Check coordinates and move paddle to opposite ends if outside of boundary                                - Done
#Step3 - Define Start Game Button
#Step4 - Define the ball's initial movement when the game starts. Likely needs separate thread                    - Done
#Step5 - Define the ball's bounce off the paddle in a specific direction if it hits the paddle or the boundary    - Done
#Step6 - Upon hitting a paddle, paddle that we control must switch                                                - Done
#Step7 - If the Ball hits coordinates beyond the paddle, reset and score += 1 for the paddle we're controlling    - Done


from tkinter import Tk, Canvas, IntVar, Label, Frame
from itertools import cycle
from time import sleep
from functools import wraps
from random import uniform


class Pong:


    #### Define default screen size for the playing area
    WIDTH = 600
    HEIGHT = 550

    #### Defines velocities for ball. We want X velocity to always be postive because right paddle starts,
    #### so xvelocity will be 2. Y velocity doesn't really matter as much in terms of speed, so we
    #### can give it some good randomness
    xVelocity = 3
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
        self.Right_Score_Var = IntVar()
        self.Label_Right = Label(self.frame_score_reset_start,
                                 textvariable = self.Right_Score_Var,
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


    def _increment_score(self,paddle):
        if paddle == 1:
            self.Left_Score = (self.Left_Score + 1)
            return self.Left_Score
        elif paddle == 2:
            self.Right_Score = (self.Right_Score + 1)
            return self.Right_Score


    def _check_coord(func):
        @wraps(func)
        def wrapper(self,*args,**kwargs):
            print(self.canvas.coords(self.current_paddle))
            func(self,*args,**kwargs)
        return wrapper


    def _check_collision(func):
        @wraps(func)
        def wrapper(self,*args,**kwargs):
            if self.current_paddle == 2:

                if (self.canvas.bbox(self.current_paddle)[3] + 25 > self.canvas.bbox(self.pong_ball)[3] > self.canvas.bbox(self.current_paddle)[1])\
                and (self.canvas.bbox(self.pong_ball)[2] > 570):

                    Pong.xVelocity = Pong.xVelocity * -1
                    self.current_paddle = self.paddle_Left

            elif self.current_paddle == 1:

                if (self.canvas.bbox(self.current_paddle)[3] + 25 > self.canvas.bbox(self.pong_ball)[3] > self.canvas.bbox(self.current_paddle)[1])\
                and (self.canvas.bbox(self.pong_ball)[0] < 30):

                    Pong.xVelocity = Pong.xVelocity * -1
                    self.current_paddle = self.paddle_Right


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

    @_check_collision
    def ball_movement(self):
        coordinates = self.canvas.coords(self.pong_ball)                # Gets the coordinates of pong ball

        if coordinates[0] >= (Pong.WIDTH - self.pong_width) or coordinates[0] <= -1: # If collision behind the paddle, increment and reset
            if self.current_paddle == 1:
                self.Left_Score_Var.set(self._increment_score(self.current_paddle))
            elif self.current_paddle == 2:
                self.Right_Score_Var.set(self._increment_score(self.current_paddle))

            self.canvas.coords(self.pong_ball,(Pong.WIDTH / 2),                     # Reset ball location
                               (Pong.HEIGHT / 2),
                               (Pong.WIDTH / 2) + 25,
                               (Pong.HEIGHT / 2) + 25,)

        if coordinates[1] >= (Pong.HEIGHT - self.pong_height) or coordinates[1] <= -1: # Bouncing off the top/bottom canvas
            Pong.yVelocity = Pong.yVelocity * -1

        self.canvas.move(self.pong_ball,Pong.xVelocity,Pong.yVelocity)
        self.window.update() # Update the window for any changes
        sleep(0.01)          # The thread will then pause for 0.01 sec


    def switch_paddle(self):
        self.current_paddle = self.paddle_Left


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
        if paddle == 2:
            if coodinates[1] == -55:
                self.canvas.coords(paddle,565,545,580,600)

            elif coodinates[3] == 615:
                self.canvas.coords(paddle,565,-40,580,15)

        if paddle == 1:
            if coodinates[1] == -55:
                self.canvas.coords(paddle,20,545,35,600)

            elif coodinates[3] == 615:
                self.canvas.coords(paddle,20,-40,35,15)

        self.window.update()



if __name__ == '__main__':
    game1 = Pong()
    game1.main()