# import the pygame module, so you can use it
import pygame

#import the module we use to load our points
import pointloader

#import our scaler
import scale_to_pixels

#CONSTANTS
x_dim = 800
y_dim = 800
scale = [100,100]
# define a main function
def main():
    print('Main')
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("minimal program")


    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((x_dim,y_dim))
    
    #Draw lines
    data = pointloader.load_data()
    data = scale_to_pixels.scale_pts(data, scale)
    for lines in data:
        print(lines)
        pygame.draw.lines(screen, (255,255,255), False, lines, 5)
        
    pygame.display.flip()
    # define a variable to control the main loop
    running = True
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
    # run the main function only if this module is executed as the main script
    # (if you import this as a module then nothing is executed)
    
if __name__=="__main__":
    # call the main function
    main()
