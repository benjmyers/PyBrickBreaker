## Meredith Myers Project 5
## 002
## Basic Program

from Tkinter import *


class blockData(object):
    pass
block = blockData()

class ballClass(object):
    pass
ball = ballClass()

# Handles paddle movement
def mouseMoved(event):
    global paddleID, canvas

    xV = event.x
    curBBox = canvas.bbox(paddleID)
   
    px = curBBox[0]
    p2x = curBBox[2]
     
    X = xV - px
    newPX = -X+xV
   
  
    if (xV >= 10) and (xV <= 450):
        canvas.move(paddleID, xV - px, 0)
    else:
        pass

# Begins the game
def startBall(event):
    global canvas, string2, lbl2
    
    string2.set("")
    canvas.after(50, moveBall)
    
def moveBall():
    global ballID, canvas, paddleID, blockID, leftWall, topWall, rightWall, blocks, score, string, string2
    
    # Get the current bounding box
    boundingBox = canvas.bbox(ballID)
    left = boundingBox[0]
    top = boundingBox[1]
    right = boundingBox[2]
    bottom = boundingBox[3]

    #check for collisions and determine what the ball has collided with
    over = canvas.find_overlapping(left,top,right,bottom)
    z = len(over)
    
    if z == 1:
        obj = over[0]
    else:
        for i in range(z):
            if over[i] == ballID:
                pass
            else:
                obj = over[i]
   
    # If the collision is with a block
    if obj in blocks:
        dx = -0.1
        dy = -0.1        
        score += 1
        string.set("Score: "+(str(score)))
        
        # While the collision is still being detected, move back
        newx = left
        newy = top
        newx2 = right
        newy2 = bottom
        
        while obj in over:
            
            # get new x,y coordinate
            newx = newx - dx
            newy = newy - dy
            newx2 = newx2 - dx
            newy2 = newy2 - dy
            over = canvas.find_overlapping(newx,newy,newx2,newy2)
       
        # When the collision is no longer detected, look at the ball and block's bbox
        bboxBlock = canvas.bbox(obj)
        xBlk = bboxBlock[0]
        yBlk = bboxBlock[1]
        x2Blk = bboxBlock[2]
        y2Blk = bboxBlock[3]
        # Compute the overlaps
        y = y2Blk - newy
       
        if ball.dx < 0:
            x = x2Blk - newx
          
        else:
            x = newx2 - xBlk
         
        # Flip the appropriate speeds
        if x > y:
            #print("if",x,y)
            ball.dy = -ball.dy
            blocks.remove(obj)
            canvas.delete(obj)
            canvas.move(ballID, ball.dx, ball.dy)
        elif y > x:
            #print("elif",x,y)
            ball.dx = -ball.dx
            blocks.remove(obj)
            canvas.delete(obj)
            canvas.move(ballID, ball.dx, ball.dy)
        else:
            #print("else",x,y)
            ball.dy = -ball.dy
            ball.dx = -ball.dx
            blocks.remove(obj)
            canvas.delete(obj)
            canvas.move(ballID, ball.dx, ball.dy)

    # Handle paddle bounces         
    elif obj == paddleID:
        paddleBox = canvas.bbox(paddleID)
        paddleLeft = paddleBox[0]
        paddleRight = paddleBox[2]
        paddleMiddle = (paddleLeft + paddleRight)/2 # detect middle of the paddle
        ball.dx += 0.6*(left - paddleMiddle)
        ball.dy = -ball.dy# Make dy negative so after hitting the paddle the ball is going up.
        canvas.move(ballID, ball.dx, ball.dy)

    # Handle wall bounces    
    elif (obj == leftWall) or (obj == rightWall):
        ball.dx = -ball.dx
        canvas.move(ballID, ball.dx, ball.dy)
        
    elif obj == topWall:
        ball.dx = -ball.dx
        ball.dy = -ball.dy
        canvas.move(ballID, ball.dx, ball.dy)

    # Handle free motion
    else:
        canvas.move(ballID, ball.dx, ball.dy)
        
    #Check if game is over
    if bottom > 530:
        string2.set("GAME OVER!")
    else:
        canvas.after(50, moveBall)
        
def main():
    global paddleID, canvas, ballID, blockID, leftWall, topWall, rightWall, blocks, score, string, string2, lbl2
    
    root = Tk()
    root.grid()
    root.title("Py Brick Breaker")
    
    canvas = Canvas(root,width=500,height=525,bg = "black")
    canvas.grid(row=0,column=0)
    
    #Create walls
    leftWall = canvas.create_rectangle([-100,0,10,525], fill = "white")
    rightWall = canvas.create_rectangle([490,0,600,525], fill = "white")
    topWall = canvas.create_rectangle([10,-100,500,10], fill = "white")
    
    #Create paddle
    paddleID = canvas.create_rectangle([50,490,90,600],fill="green")
    canvas.bind("<B1-Motion>",mouseMoved)
    
    #Create ball
    ballID = canvas.create_oval([242,282,258,298],fill="green")
    bbox = canvas.bbox(ballID)
    ball.x = bbox[0]
    ball.y = bbox[1]
    ball.x2 = bbox[2]
    ball.y2 = bbox[3]
    ball.dx = 0
    ball.dy = 5

    #Create changable game start/over label
    string2 = StringVar()
    string2.set("Press Enter to Begin")
    lbl2 = Label(root,textvariable = string2, fg = "white", bg = "black")
    lbl2.grid(row = 0, column = 0)
    root.bind("<Return>",startBall) 

    #Create blocks
    blocks = []
    block.xLoc = 50
    block.yLoc = 50
    block.xsize = 30
    block.ysize = 20    
    for x in range(4):
        for y in range(13):
            
            blockID = canvas.create_rectangle([block.xLoc,block.yLoc,
                                       block.xLoc+block.xsize,
                                       block.yLoc+block.ysize], fill="green")
            canvas.grid()
            blocks.append(blockID)
            block.xLoc += 30
        block.yLoc += 20
        block.xLoc = 50

    #Create changable score label
    score = 0
    string = StringVar()
    string.set("Score: "+(str(score)))
    lbl = Label(root,textvariable = string, fg = "white", bg = "black")
    lbl.grid(row = 0, column = 0, sticky = S+E+W)
    
    root.mainloop()
    
main()    
