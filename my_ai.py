old_ball_par = []

import pygame, sys, time, random, os
from pygame.locals import *

import math


def chaser(paddle_frect, other_paddle_frect, ball_frect, table_size):
    '''return "up" or "down", depending on which way the paddle should go to
    align its centre with the centre of the ball, assuming the ball will
    not be moving

    Arguments:
    paddle_frect: a rectangle representing the coordinates of the paddle
                  paddle_frect.pos[0], paddle_frect.pos[1] is the top-left
                  corner of the rectangle.
                  paddle_frect.size[0], paddle_frect.size[1] are the dimensions
                  of the paddle along the x and y axis, respectively

    other_paddle_frect:
                  a rectangle representing the opponent paddle. It is formatted
                  in the same way as paddle_frect
    ball_frect:   a rectangle representing the ball. It is formatted in the
                  same way as paddle_frect
    table_size:   table_size[0], table_size[1] are the dimensions of the table,
                  along the x and the y axis respectively

    The coordinates look as follows:

     0             x
     |------------->
     |
     |
     |
 y   v
    '''
    trace_ball(ball_frect)
    if len(old_ball_par) != 2:
        return "up"

    if paddle_frect.pos[0] > table_size[0]//2:
        if old_ball_par[0][0] > old_ball_par[1][0]:
            if paddle_frect.pos[1] + paddle_frect.size[1]/2  > table_size[1]/2:
                return "up"
            else:
                return "down"
        else:
            if paddle_frect.pos[1] + paddle_frect.size[1]/3 < get_ball_y(ball_frect, table_size, paddle_frect):
                return "down"
            else:
                return "up"
    else:
        if old_ball_par[0][0] < old_ball_par[1][0]:
            if paddle_frect.pos[1] + paddle_frect.size[1]/2  > table_size[1]/2:
                return "up"
            else:
                return "down"
        else:
            if paddle_frect.pos[1] + paddle_frect.size[1]/3 < get_ball_y(ball_frect, table_size, paddle_frect):
                return "down"
            else:
                return "up"


def trace_ball(ball_frect):
    if not old_ball_par:
        old_ball_par.append((ball_frect.pos[0], ball_frect.pos[1]))
    else:
        if len(old_ball_par) == 1:
            old_ball_par.append((ball_frect.pos[0], ball_frect.pos[1]))
        else:
            old_ball_par[0] = old_ball_par[1]
            old_ball_par[1] = (ball_frect.pos[0], ball_frect.pos[1])


def get_ball_y(ball_frect, table_size, paddle_frect):

    table_size = (440, 280)
    paddle_size = (10, 70)
    ball_size = (15, 15)
    paddle_speed = 1
    max_angle = 45

    paddle_bounce = 1.2
    wall_bounce = 1.00
    dust_error = 0.00
    init_speed_mag = 2
    timeout = .10
    clock_rate = 80
    turn_wait_rate = 3
    score_to_win = 3

    paddle_to_wall = table_size[0] - paddle_frect.pos[0]

    if paddle_frect.pos[0] > table_size[0]//2:
        if len(old_ball_par) == 2:
            if old_ball_par[1][0] != old_ball_par[0][0]:

                speed = (old_ball_par[1][0]-old_ball_par[0][0], old_ball_par[1][1]-old_ball_par[0][1])
                ball = Ball(table_size, ball_size, paddle_bounce, wall_bounce, dust_error, init_speed_mag, speed, ball_frect.pos)

                count = 0
                while ball.frect.pos[0] < table_size[0] - paddle_to_wall:    
                    ball.move(None, table_size)
                    count += 1
                    if count > 1000:
                        break
                    #print(ball.frect.pos[1])

                y = ball.frect.pos[1]
                #debug_info = 'y: ' + str(y)
                #targating(ball_frect, table_size, paddle_frect)
                #print debug_info
                return y
        if len(old_ball_par):
            return ball_frect.pos[1]

    else:
        if len(old_ball_par) == 2:
            if old_ball_par[1][0] != old_ball_par[0][0] and old_ball_par[1] != table_size[1]//2:

                speed = (old_ball_par[1][0]-old_ball_par[0][0], old_ball_par[1][1]-old_ball_par[0][1])
                ball = Ball(table_size, ball_size, paddle_bounce, wall_bounce, dust_error, init_speed_mag, speed, ball_frect.pos)

                count = 0
                while ball.frect.pos[0] > paddle_frect.pos[0]:    
                    ball.move(None, table_size)
                    count += 1
                    if count > 1000:
                        break
                    #print(ball.frect.pos[0])

                y = ball.frect.pos[1]
                #debug_info = 'y: ' + str(y)
                #targating(ball_frect, table_size, paddle_frect)
                #print debug_info
                return y
        if len(old_ball_par):
            return ball_frect.pos[1]



class Ball:
    def __init__(self, table_size, size, paddle_bounce, wall_bounce, dust_error, init_speed_mag, speed, pos):
        self.frect = fRect(pos, size)
        self.speed = speed
        self.size = size
        self.paddle_bounce = paddle_bounce
        self.wall_bounce = wall_bounce
        self.dust_error = dust_error
        self.init_speed_mag = init_speed_mag
        self.prev_bounce = None

    def get_center(self):
        return (self.frect.pos[0] + .5*self.frect.size[0], self.frect.pos[1] + .5*self.frect.size[1])


    def get_speed_mag(self):
        return math.sqrt(self.speed[0]**2+self.speed[1]**2)

    def factor_accelerate(self, factor):
        self.speed = (factor*self.speed[0], factor*self.speed[1])



    def move(self, paddles, table_size):
        moved = 0
        walls_Rects = [Rect((-100, -100), (table_size[0]+200, 100)),
                       Rect((-100, table_size[1]), (table_size[0]+200, 100))]

        if paddles == None:
            paddles = []

        for wall_rect in walls_Rects:
            if self.frect.get_rect().colliderect(wall_rect):
                c = 0
                #print "in wall. speed: ", self.speed
                while self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1])
                    c += 1 # this basically tells us how far the ball has traveled into the wall
                r1 = 1+2*(random.random()-.5)*self.dust_error
                r2 = 1+2*(random.random()-.5)*self.dust_error

                self.speed = (self.wall_bounce*self.speed[0]*r1, -self.wall_bounce*self.speed[1]*r2)
                while c > 0 or self.frect.get_rect().colliderect(wall_rect):
                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1])
                    c -= 1 # move by roughly the same amount as the ball had traveled into the wall
                moved = 1
                #print "out of wall, position, speed: ", self.frect.pos, self.speed

        for paddle in paddles:
            if self.frect.intersect(paddle.frect):
                if (paddle.facing == 1 and self.get_center()[0] < paddle.frect.pos[0] + paddle.frect.size[0]/2) or \
                (paddle.facing == 0 and self.get_center()[0] > paddle.frect.pos[0] + paddle.frect.size[0]/2):
                    continue
                
                c = 0
                
                while self.frect.intersect(paddle.frect) and not self.frect.get_rect().colliderect(walls_Rects[0]) and not self.frect.get_rect().colliderect(walls_Rects[1]):
                    self.frect.move_ip(-.1*self.speed[0], -.1*self.speed[1])
                    
                    c += 1
                theta = paddle.get_angle(self.frect.pos[1]+.5*self.frect.size[1])
                

                v = self.speed

                v = [math.cos(theta)*v[0]-math.sin(theta)*v[1],
                             math.sin(theta)*v[0]+math.cos(theta)*v[1]]

                v[0] = -v[0]

                v = [math.cos(-theta)*v[0]-math.sin(-theta)*v[1],
                              math.cos(-theta)*v[1]+math.sin(-theta)*v[0]]


                # Bona fide hack: enforce a lower bound on horizontal speed and disallow back reflection
                if  v[0]*(2*paddle.facing-1) < 1: # ball is not traveling (a) away from paddle (b) at a sufficient speed
                    v[1] = (v[1]/abs(v[1]))*math.sqrt(v[0]**2 + v[1]**2 - 1) # transform y velocity so as to maintain the speed
                    v[0] = (2*paddle.facing-1) # note that minimal horiz speed will be lower than we're used to, where it was 0.95 prior to increase by *1.2

                #a bit hacky, prevent multiple bounces from accelerating
                #the ball too much
                if not paddle is self.prev_bounce:
                    self.speed = (v[0]*self.paddle_bounce, v[1]*self.paddle_bounce)
                else:
                    self.speed = (v[0], v[1])
                self.prev_bounce = paddle
                #print "transformed speed: ", self.speed

                while c > 0 or self.frect.intersect(paddle.frect):
                    #print "move_ip()"
                    self.frect.move_ip(.1*self.speed[0], .1*self.speed[1])
                    #print "ball position forward trace: ", self.frect.pos
                    c -= 1
                #print "pos final: (" + str(self.frect.pos[0]) + "," + str(self.frect.pos[1]) + ")"
                #print "speed x y: ", self.speed[0], self.speed[1]

                moved = 1
                #print "out of paddle, speed: ", self.speed

        # if we didn't take care of not driving the ball into a wall by backtracing above it could have happened that
        # we would end up inside the wall here due to the way we do paddle bounces
        # this happens because we backtrace (c++) using incoming velocity, but correct post-factum (c--) using new velocity
        # the velocity would then be transformed by a wall hit, and the ball would end up on the dark side of the wall

        if not moved:
            self.frect.move_ip(self.speed[0], self.speed[1])
            #print "moving "
        #print "poition: ", self.frect.pos



class fRect:
    '''
    pygame's Rect class can only be used to represent whole integer vertices, so we create a rectangle class that can have floating point coordinates
    '''
    def __init__(self, pos, size):
        self.pos = (pos[0], pos[1])
        self.size = (size[0], size[1])
    def move(self, x, y):
        return fRect((self.pos[0]+x, self.pos[1]+y), self.size)

    def move_ip(self, x, y):
        self.pos = (self.pos[0] + x, self.pos[1] + y)

    def get_rect(self):
        return Rect(self.pos, self.size)

    def copy(self):
        return fRect(self.pos, self.size)

    def intersect(self, other_frect):
        # two rectangles intersect iff both x and y projections intersect
        for i in range(2):
            if self.pos[i] < other_frect.pos[i]: # projection of self begins to the left
                if other_frect.pos[i] >= self.pos[i] + self.size[i]:
                    return 0
            elif self.pos[i] > other_frect.pos[i]:
                if self.pos[i] >= other_frect.pos[i] + other_frect.size[i]:
                    return 0
        return self.size > 0 and other_frect.size > 0




class Paddle:
    def __init__(self, pos, size, speed, max_angle,  facing, timeout):
        self.frect = fRect((pos[0]-size[0]/2, pos[1]-size[1]/2), size)
        self.speed = speed
        self.size = size
        self.facing = facing
        self.max_angle = max_angle
        self.timeout = timeout

    def factor_accelerate(self, factor):
        self.speed = factor*self.speed


    def move(self, enemy_frect, ball_frect, table_size):
        direction = self.move_getter(self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size))
        #direction = timeout(self.move_getter, (self.frect.copy(), enemy_frect.copy(), ball_frect.copy(), tuple(table_size)), {}, self.timeout)
        if direction == "up":
            self.frect.move_ip(0, -self.speed)
        elif direction == "down":
            self.frect.move_ip(0, self.speed)

        to_bottom = (self.frect.pos[1]+self.frect.size[1])-table_size[1]

        if to_bottom > 0:
            self.frect.move_ip(0, -to_bottom)
        to_top = self.frect.pos[1]
        if to_top < 0:
            self.frect.move_ip(0, -to_top)


    def get_face_pts(self):
        return ((self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1]),
                (self.frect.pos[0] + self.frect.size[0]*self.facing, self.frect.pos[1] + self.frect.size[1]-1)
                )

    def get_angle(self, y):
        center = self.frect.pos[1]+self.size[1]/2
        rel_dist_from_c = ((y-center)/self.size[1])
        rel_dist_from_c = min(0.5, rel_dist_from_c)
        rel_dist_from_c = max(-0.5, rel_dist_from_c)
        sign = 1-2*self.facing

        return sign*rel_dist_from_c*self.max_angle*math.pi/180
