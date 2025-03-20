#RenderBirdCore 0.1.8
#Created by Wojtekb30 (Wojciech B)
import pygame
from pygame.locals import *
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import time
import math
from PIL import Image
import numpy as np
import os
import struct
from OpenGL.arrays import vbo
from io import StringIO
import asyncio

class RenderBirdCore:
    def __init__(self, window_size_x=1280, window_size_y=720, window_title="RenderBird Program", depth_testing=True,
                 camera_x=0, camera_y=0, camera_z=0, camera_pitch=0, camera_yaw=0, camera_roll=0, camera_fov=45,
                 camera_minimum_render_distance=0.1, camera_maximum_render_distance=50.0,
                 camera_hitbox_width=0.5, camera_hitbox_height=0.5,camera_hitbox_depth=0.5,
                 enable_shading=False):
        pygame.init()
        RENDERBIRD_VERSION = "0.1.8"
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.screen = pygame.display.set_mode((self.window_size_x, self.window_size_y), DOUBLEBUF | OPENGL)
        pygame.display.set_caption(window_title)
        self.depth_testing_enabled = depth_testing
        if depth_testing:
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)  # Use the default depth function (objects closer to the camera are rendered first)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Initialize the camera
        self.camera = self.Camera_class(self.window_size_x, self.window_size_y, camera_x, camera_y, camera_z, camera_pitch, camera_yaw, camera_roll, camera_fov, camera_minimum_render_distance, camera_maximum_render_distance, camera_hitbox_width, camera_hitbox_height,camera_hitbox_depth)
        self.run_once_list = []
        self.running = True
        self.background_color = (0.0, 0.0, 0.0, 1.0)  # RGBA
        self.is_fullscreen = False
        
        #Shading (light)
        self.enabled_shading = enable_shading
        if enable_shading==True:
            glEnable(GL_LIGHTING)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            
        opengl_version = glGetString(GL_VERSION).decode('utf-8')
        print("Started OpenGL [" + opengl_version + "] and RenderBird " + RENDERBIRD_VERSION)
    
    def enter_fullscreen(self):
        """
        Switch to fullscreen mode
        """
        self.is_fullscreen = True
        self.screen = pygame.display.set_mode(
            (self.window_size_x, self.window_size_y),
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL
        )
        
    
    def exit_fullscreen(self):
        """
        Switch to windowed mode
        """
        self.is_fullscreen = False
        self.screen = pygame.display.set_mode(
            (self.window_size_x, self.window_size_y),
            pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.OPENGL
        )
        
    
    def toggle_fullscreen(self):
        """
        Toggle between fullscreen and windowed mode
        """
        if self.is_fullscreen:
            self.exit_fullscreen()
        else:
            self.enter_fullscreen()
    
    
    def enable_depth_testing(self, value: bool):
        """
        Use value argument to turn it on or off.
        With Depth Testing enabled, objects render in order as you see them. Objects closer to camera are rendered first.
        Without it, an object that is behind another object may render like if it was in front of it, which may look confusing to say at least.
        """
        self.depth_testing_enabled = value
        if value:
            glEnable(GL_DEPTH_TEST)
            glDepthFunc(GL_LESS)
        else:
            glDisable(GL_DEPTH_TEST)

    def GetPygameScreen(self):
        """
        Returns PyGame screen object
        """
        return self.screen


    class Camera_class:
        def __init__(self, view_width, view_height, x=0, y=0, z=0, pitch=0, yaw=0, roll=0, fov=45, minimum_render_distance=0.1, maximum_render_distance=50, hitbox_width=0.5, hitbox_height=0.5,hitbox_depth=0.5):
            """
            Initializes the camera (viewport) with position, rotation, and perspective settings.
            
            :param view_width: Width of the viewport.
            :param view_height: Height of the viewport.
            :param x: Initial X position.
            :param y: Initial Y position.
            :param z: Initial Z position.
            :param pitch: Initial pitch angle (rotation around X-axis).
            :param yaw: Initial yaw angle (rotation around Y-axis).
            :param roll: Initial roll angle (rotation around Z-axis).
            :param fov: Field of view angle.
            :param minimum_render_distance: Minimum render distance.
            :param maximum_render_distance: Maximum render distance.
            :param hitbox_width: Width of camera's hitbox used in collission detection.
            :param hitbox_height: Height of camera's hitbox used in collission detection.
            :param hitbox_depth: Depth of camera's hitbox used in collission detection.
            """
            
            self.view_width = view_width
            self.view_height = view_height
            self.position = [x, y, z]
            self.rotation = [pitch, yaw, roll]
            self.fov = fov
            self.min_render_distance = minimum_render_distance
            self.max_render_distance = maximum_render_distance
            self.forward_vector = [0, 0, -1]  # Initial forward direction
            self.setup_perspective()
            self.update_forward_vector()
            
            self.width = hitbox_width
            self.height = hitbox_height
            self.depth = hitbox_depth
        
        def update_forward_vector(self):
            """
            Updates the forward vector based on current pitch and yaw angles.
            """
            pitch_rad = math.radians(self.rotation[0])
            yaw_rad = math.radians(self.rotation[1])
            self.forward_vector = [
                math.cos(pitch_rad) * math.sin(yaw_rad),
                math.sin(pitch_rad),
                -math.cos(pitch_rad) * math.cos(yaw_rad)
            ]
            ##print(f"Updated Forward Vector: X={self.forward_vector[0]:.2f}, Y={self.forward_vector[1]:.2f}, Z={self.forward_vector[2]:.2f}")
        
        def rotate_pitch(self, delta_pitch, reverse=False):
            """
            Rotates the camera's pitch.
            
            :param delta_pitch: The amount to change the pitch by.
            :param reverse: If True, reverses the pitch direction.
            """
            if reverse:
                delta_pitch = -delta_pitch
            self.rotation[0] += delta_pitch
            self.rotation[0] = max(-90, min(90, self.rotation[0]))
            self.update_forward_vector()
            self.setup_perspective()
        
        def rotate_yaw(self, delta_yaw, reverse=False):
            """
            Rotates the camera's yaw.
            
            :param delta_yaw: The amount to change the yaw by.
            :param reverse: If True, reverses the yaw direction.
            """
            if reverse:
                delta_yaw = -delta_yaw
            self.rotation[1] += delta_yaw
            self.update_forward_vector()
            self.setup_perspective()
        
        def rotate(self, pitch, yaw, roll):
            """
            Rotates the camera by specified pitch, yaw, and roll angles.
            
            :param pitch: Change in pitch angle.
            :param yaw: Change in yaw angle.
            :param roll: Change in roll angle.
            """
            self.rotation[0] += pitch
            self.rotation[1] += yaw
            self.rotation[2] += roll
            self.update_forward_vector()
            self.setup_perspective()
        
        def setup_perspective(self):
            """
            Sets up the perspective projection and camera view using gluLookAt.
            """
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, (self.view_width / self.view_height), self.min_render_distance, self.max_render_distance)
            
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            
            target = [
                self.position[0] + self.forward_vector[0],
                self.position[1] + self.forward_vector[1],
                self.position[2] + self.forward_vector[2]
            ]
            
            gluLookAt(
                self.position[0], self.position[1], self.position[2],  
                target[0], target[1], target[2],                          
                0, 1, 0                                                  
            )
        
        def apply_rotation(self):
            """
            This method is retained for compatibility but is no longer used since gluLookAt is employed.
            """
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll
        
        def translate(self, dx, dy, dz):
            """
            Translates the camera by the given amounts.
            
            :param dx: Translation along the X-axis.
            :param dy: Translation along the Y-axis.
            :param dz: Translation along the Z-axis.
            """
            self.position[0] += dx
            self.position[1] += dy
            self.position[2] += dz
            self.setup_perspective()
        
        def move(self, x_transform, y_transform, z_transform):
            """
            Moves the camera based on input transformations, considering the current yaw angle.
            
            :param x_transform: Movement along the right vector (strafe).
            :param y_transform: Movement along the up vector.
            :param z_transform: Movement along the forward vector.
            """
            # Calculate movement in world coordinates based on yaw
            yaw_rad = math.radians(self.rotation[1])
            # Right vector (perpendicular to forward vector in the horizontal plane)
            right = [
                math.cos(yaw_rad),
                0,
                math.sin(yaw_rad)
            ]
            # Forward vector in the horizontal plane (ignoring pitch for strafing)
            forward = [
                math.sin(yaw_rad),
                0,
                -math.cos(yaw_rad)
            ]
            
            # Calculate the movement in world coordinates
            dx = x_transform * right[0] + z_transform * forward[0]
            dy = y_transform
            dz = x_transform * right[2] + z_transform * forward[2]
            
            self.translate(dx, dy, dz)
        
        def look_around(self, delta_x, delta_y, sensitivity=0.1, reverse_horiz=False, reverse_vert=False):
            """
            Adjusts the camera's yaw and pitch based on mouse movement.
            """
            delta_x = delta_x * sensitivity * (-1 if reverse_horiz else 1)
            delta_y = delta_y * sensitivity * (-1 if reverse_vert else 1)
            self.rotation[1] += delta_x  # Yaw
            self.rotation[0] = max(-90, min(90, self.rotation[0] + delta_y))  # Pitch
            pitch_rad = math.radians(self.rotation[0])
            yaw_rad = math.radians(self.rotation[1])
            cos_pitch = math.cos(pitch_rad)
            sin_pitch = math.sin(pitch_rad)
            cos_yaw = math.cos(yaw_rad)
            sin_yaw = math.sin(yaw_rad)
            self.forward_vector = [
                cos_pitch * sin_yaw,
                sin_pitch,
                -cos_pitch * cos_yaw
            ]

            self.setup_perspective()

    
        def use_mouse_camera_controls(self, window_size_x: int, window_size_y: int, sensitivity=0.1, sensitivity_factor=1.0,reverse_horizontally=False, reverse_vertically=False, mouse_cursor_visible=False):
            """
            Implements mouse-based camera controls by capturing mouse movement and adjusting the camera's orientation.
    
            :param window_size_x: Width of the window.
            :param window_size_y: Height of the window.
            :param sensitivity: Sensitivity factor for mouse movement.
            :param sensitivity_factor: Additional sensitivity scaling factor.
            :param reverse_horizontally: If True, reverses horizontal mouse movement.
            :param reverse_vertically: If True, reverses vertical mouse movement.
            :param mouse_cursor_visible: If True, makes the mouse cursor visible.
            """
            #pygame.event.set_grab(True) 
            pygame.mouse.set_visible(mouse_cursor_visible) 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    delta_x, delta_y = event.rel 
                    self.look_around(
                        delta_x * sensitivity,
                        delta_y * sensitivity,
                        sensitivity=sensitivity_factor, 
                        reverse_horiz=reverse_horizontally,
                        reverse_vert=~reverse_vertically
                    )
                pygame.mouse.set_pos(window_size_x // 2, window_size_y // 2)

        
        def get_world_position(self):
            """
            Returns the camera's position in world coordinates.
            
            :return: A list representing the camera's X, Y, Z position.
            """
            return self.position.copy()
        
        def detect_objects_in_view(self, objects, max_distance, angle_threshold):
            """
            Detects objects within the camera's view based on distance and angle threshold.
            
            :param objects: A list of objects with a 'position' attribute.
            :param max_distance: Maximum distance to detect objects.
            :param angle_threshold: Maximum angle (in degrees) from the forward vector to consider.
            :return: A list of detected objects.
            """
            detected_objects = []
            cam_pos = self.get_world_position()
            yaw_rad = math.radians(self.rotation[1])
            pitch_rad = math.radians(self.rotation[0])
            angle_threshold_rad = math.radians(angle_threshold)
            
            # Forward vector based on yaw and pitch
            forward = [
                math.cos(pitch_rad) * math.sin(yaw_rad),
                math.sin(pitch_rad),
                -math.cos(pitch_rad) * math.cos(yaw_rad)
            ]
            
            for obj in objects:
                obj_pos = obj.position
                cam_to_obj = [obj_pos[i] - cam_pos[i] for i in range(3)]
                distance = math.sqrt(sum(comp ** 2 for comp in cam_to_obj))
                
                if distance <= max_distance:
                    cam_to_obj_normalized = [comp / distance for comp in cam_to_obj]
                    dot_product = sum((forward[i] * cam_to_obj_normalized[i] for i in range(3)))
                    dot_product = max(min(dot_product, 1.0), -1.0)
                    angle = math.acos(dot_product)
                    angle_deg = math.degrees(angle)
                    
                    if angle <= angle_threshold_rad:
                        detected_objects.append(obj)
                        #print(f"Detected Object: {obj}")
            
            return detected_objects
        
        def draw_forward_vector(self, length=2.0):
            """
            Draws a line representing the camera's forward vector for debugging purposes.
            
            :param length: The length of the forward vector line.
            """
            glPushMatrix()
            glLoadIdentity()
            glBegin(GL_LINES)
            glColor3f(1.0, 0.0, 0.0)  # Red color for the forward vector
            cam_world_pos = self.get_world_position()
            glVertex3f(cam_world_pos[0], cam_world_pos[1], cam_world_pos[2])
            glVertex3f(
                cam_world_pos[0] + self.forward_vector[0] * length,
                cam_world_pos[1] + self.forward_vector[1] * length,
                cam_world_pos[2] + self.forward_vector[2] * length
            )
            glEnd()
            glPopMatrix()
            
        def check_collision(self, other):
            """
            Checks if the hitbox collides with something else using AABB.
            :param other: Another object with position, width, height, and depth attributes.
            :return: True if there is a collision, False otherwise.
            """
            if (abs(self.position[0] - other.position[0]) < (self.width / 2 + other.width / 2) and
                abs(self.position[1] - other.position[1]) < (self.height / 2 + other.height / 2) and
                abs(self.position[2] - other.position[2]) < (self.depth / 2 + other.depth / 2)):
                return True
            return False
        

    #Utility and functions:

    class RunAfterTime:
        """
        Allows to run a function after certain amount of time passes.
        """
        def __init__(self, seconds: float):
            """
            :param seconds: Seconds that must pass from initalization or last reset for the function to run.
            """
            self.seconds = seconds
            self.start_time = time.time()
            self.run_once_list = []
            
        def run_once(self, function, *args, remove_not_run=False):
            """
            Run a function one time.
            :param function: Function
            :param *args: The function's arguments
            :param remove_not_run: If True, it will remove the function from its memory, making it possible to run again.
            """
            function_name = function.__name__
            if remove_not_run:
                if function_name in self.run_once_list:
                    self.run_once_list.remove(function_name)
            else:
                if function_name not in self.run_once_list:
                    self.run_once_list.append(function_name)
                    return function(*args)
            return None
                
        def run_once_after_time(self, function, *args):
            """
            Run a function once after certain amount of time
            :param function: Function
            :param *args: The function's arguments
            """
            if time.time() >= self.start_time + self.seconds:
                return self.run_once(function, *args)
            return None
                
        def run_after_time(self, function, *args):
            """
            Run a function after certain amount of time, without lock to run it only once.
            :param function: Function
            :param *args: The function's arguments
            """
            if time.time() >= self.start_time + self.seconds:
                return function(*args)
            return None
        
        def reset_start_time(self):
            """
            Resets the timestamp since which the function waits to run functions.
            """
            self.start_time = time.time()
            return self.start_time
        
        def run_in_loop(self, function, *args):
            """
            Run a function in interval specified when creating object of the RunAfterTime class.
            :param function: Function
            :param *args: The function's arguments
            """
            if time.time() >= self.start_time + self.seconds:
                self.reset_start_time()
                return function(*args)
            return None


    def run_once(self, function, *args, remove_not_run=False):
        """
        Run a function one time.
        :param function: Function
        :param *args: The function's arguments
        :param remove_not_run: If True, it will remove the function from its memory, making it possible to run again.
        """
        function_name = function.__name__
        if remove_not_run:
            if function_name in self.run_once_list:
                self.run_once_list.remove(function_name)
        else:
            if function_name not in self.run_once_list:  
                self.run_once_list.append(function_name)
                return function(*args)
        return None


    def key_pressed(self, key_pygame_var):
        """
        Returns whenever a keyboard key was pressed.
        :param key_pygame_var: Key to check for, PyGame variable, for example K_w
        """
        keys = pygame.key.get_pressed()
        return keys[key_pygame_var]
    
    def update_display(self):
        """
        Update the display to render things.
        """
        pygame.display.flip()
        glFlush()
        
    def set_background_color(self, r: float, g: float, b: float):
        """
        Sets color of the background (or if you prefer sky)
        """
        if r > 1:
            r = r / 255
        if g > 1:
            g = g / 255
        if b > 1:
            b = b / 255
        self.background_color = (r, g, b, 1.0)

    def clear_screen(self):
        """
        Clear screen to get rid of old frame
        """
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def safe_close(self):
        """
        Closes the program ensuring PyGame and OpenGL stop too
        """
        print("Stopping PyGame and RenderBird. Goodbye!")
        pygame.time.wait(100)
        pygame.quit()
        sys.exit()
        exit()

    def handle_close_event(self):
        """
        Checks if program is commanded to close by the OS (for example because someone clicked X to close its window)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def handle_close_event_direct(self):
        """
        Checks if program is commanded to close by the OS (for example because someone clicked X to close its window)
        Runs safe_close() instead of just changing running bool variable to False.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.safe_close()

    def draw_world_axes(self,length=5.0):
        """
        Draws the world coordinate axes for debugging purposes.
        
        :param length: Length of each axis line.
        """
        glPushMatrix()
        glBegin(GL_LINES)
        
        # X-axis (Red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(length, 0, 0)
        
        # Y-axis (Green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, length, 0)
        
        # Z-axis (Blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, length)
        
        glEnd()
        glPopMatrix()

    def normalize_color(self, tuple_4_values):
        """
        Divides every color value in the tuple by 255, ensuring compatiblity with OpenGL.
        
        :param tuple_4_values: Tuple with 4 values for Red, Green, Blue and Transparency.
        
        Returns normalized tuple.
        """
        r = float(tuple_4_values[0]/255)
        g = float(tuple_4_values[1]/255)
        b = float(tuple_4_values[2]/255)
        t = float(tuple_4_values[3]/255)
        return (r,g,b,t)
    
    def denormalize_color(self, tuple_4_values):
        """
        Multiplies every color value in the tuple by 255, ensuring compatiblity with 2D elements and STL 3D model coloring.
        
        :param tuple_4_values: Tuple with 4 values for Red, Green, Blue and Transparency.
        
        Returns de-normalized tuple.
        """
        r = int(tuple_4_values[0]*255)
        g = int(tuple_4_values[1]*255)
        b = int(tuple_4_values[2]*255)
        t = int(tuple_4_values[3]*255)
        return (r,g,b,t)
        
    def calculate_side_from_middle(self, point, side_length):
        a = side_length/2
        return point - a
    
    def calculate_middle_from_side(self, point, side_length):
        a = side_length/2
        return point + a


    def RotateObjectToVector(self, obj, vector, factor=1.0, desired_roll=0):
        """
        Rotates a 3D object to face the direction specified by a vector.
        
        :param obj: The 3D object to rotate.
        :param vector: A tuple or list representing the direction vector (x, y, z).
        :param factor: A float representing the interpolation factor for smooth rotation. Use 1 for an immediate rotation or a value smaller than 1 for gradual rotation.
        :param desired_roll: Set desired roll value.
        """
        x, y, z = vector
        # Prevent division by zero
        if x == 0 and z == 0 and y == 0:
            print("Error: Zero-length vector provided for rotation.")
            return None
        target_yaw = math.degrees(math.atan2(x, -z))
        horizontal_distance = math.sqrt(x**2 + z**2)
        target_pitch = math.degrees(math.atan2(y, horizontal_distance))

        obj.rotation[0] += (target_pitch - obj.rotation[0]) * factor
        obj.rotation[1] += (target_yaw - obj.rotation[1]) * factor
        obj.rotation[2] = desired_roll


    class PreventMovingInsideObjects:
        '''
        With this class you can prevent an object from moving inside (clipping) an another object, including preventing camera from clipping inside objects.
        '''
        def __init__(self, object_to_affect, other_objects_list, step_size=0.01, max_correction_steps = 16):
            '''
            With this class you can prevent an object from moving inside an another object, including preventing camera from clipping inside objects. It is collission-based.
            :param object_to_affect: The object that you do not want to move (clip) inside other objects, for example camera.
            :param other_objects_list: List containing the other objects that you do not want the object to clip into.
            :param step_size: Correction step size used to move the object out of the another, the lower the smoother the process will look.
            :param max_correction_steps: Maximum steps of moving out of the another object.
            '''
            self.object_to_affect = object_to_affect
            self.internal_object_list = other_objects_list
            self.step_size = step_size
            self.max_correction_steps = max_correction_steps
            self.previous_valid_position = self.object_to_affect.position.copy()

        def check_and_correct(self):
            '''
            Run the function which checks if the object_to_affect collided with any of the another_objects and then moves it away to prevent clipping.
            This way you can prevent an object from moving inside an another object, including preventing camera from clipping inside objects.
            '''
            steps = 0 
            while steps < self.max_correction_steps:
                collision_detected = False
                for other_object in self.internal_object_list:
                    if self.object_to_affect.check_collision(other_object):
                        collision_detected = True

                        #Direction calculation
                        dx = self.object_to_affect.position[0] - other_object.position[0]
                        dy = self.object_to_affect.position[1] - other_object.position[1]
                        dz = self.object_to_affect.position[2] - other_object.position[2]

                        if abs(dx) >= abs(dy) and abs(dx) >= abs(dz):
                            self.object_to_affect.position[0] += self.step_size if dx > 0 else -self.step_size
                        elif abs(dy) >= abs(dx) and abs(dy) >= abs(dz):
                            self.object_to_affect.position[1] += self.step_size if dy > 0 else -self.step_size
                        else:
                            self.object_to_affect.position[2] += self.step_size if dz > 0 else -self.step_size
                        break

                if collision_detected == False:
                    self.previous_valid_position = self.object_to_affect.position.copy()
                    return None
                steps += 1
            self.object_to_affect.position = self.previous_valid_position.copy()
            return None

    class FPS_Limiter:
        """
        Allows to limit frames per second and program's speed in a consistent way, ensuring same top execution speed on all devices.
        """
        def __init__(self, max_fps: int):
            """
            :param max_fps: Maximum frames per second, recommended 30, 50 or 60
            """
            self.max_fps = max_fps
            self.first_time_reading = 0.0
        
        def code_start_point(self):
            """
            Put this at the beggining of your program's While (main)loop.
            Reads time when it starts.
            """
            self.first_time_reading = time.time()
        
        def code_end_point_limit_framerate(self):
            """
            Put this at the end of your program's While (main)loop.
            Waits until proper amount of time since code_start_point passed to ensure the top speed.
            """
            wait = 1 / self.max_fps
            while True:
                current_time = time.time()
                if current_time - self.first_time_reading >= wait:
                    break

    def MoveObjectAlongVector(self, obj, vector, factor=1.0):
        '''
        Move an object along a vector (for example a bullet along camera's forward vector).
        :param obj: The object to move (translate)
        :param vector: 3D vector, a tuple of 3 values, for example (0.1, 0.2, 0.3)
        :param factor: A value to multiply each element of the vector by, use it to change movement speed.
        '''
        obj.translate(float(vector[0]*factor),float(vector[1]*factor),float(vector[2]*factor))

    def ForceWhiteColorRendering(self):
        """
        Run glColor4f(1, 1, 1, 1) to reset shape rendering shade to white.
        Use this before shape rendering to fix any wrong color issues when rendering.
        """
        glColor4f(1, 1, 1, 1)
        
    def FixColorRendering(self):
        """
        Run ForceWhiteColorRendering [glColor4f(1, 1, 1, 1)] to reset shape rendering shade to white.
        Use this before shape rendering to fix any wrong color issues when rendering.
        """
        self.ForceWhiteColorRendering()
    
    def ForceColorRendering(self, r, g, b, t):
        """
        [Advanced] Run glColor4f(r,g,b,t) to force shape rendering in specific color.
        Might not work since objects manage that themselves and may override this.
        """
        glColor4f(r,g,b,t)

    #3D Objects:
                
    class Cube:
        """
        3D cube object, left for compatibility.
        Since you can create cubes with RectangularPrism, only it will be getting updates.
        """
        def __init__(self, size=1, position=(0, 0, 0), rotation=(0, 0, 0), rotation_speed=(0, 0, 0),
                     color_sides=False, frame_color=(1, 1, 1, 1),
                     color_front=(1, 1, 1, 1), color_back=(1, 1, 1, 1), color_left=(1, 1, 1, 1),
                     color_right=(1, 1, 1, 1), color_top=(1, 1, 1, 1), color_bottom=(1, 1, 1, 1)):
            self.size = size
            self.position = list(position)  # Ensure it's always a list
            self.rotation = list(rotation)  # (pitch, yaw, roll) angles
            self.rotation_speed = list(rotation_speed)  # Speed of rotation for each axis
            self.color_sides = color_sides
            self.frame_color = frame_color
            colors = {
                "front": color_front,
                "back": color_back,
                "left": color_left,
                "right": color_right,
                "top": color_top,
                "bottom": color_bottom,
            }
            self.colors = colors

        def translate(self, x_velocity=0, y_velocity=0, z_velocity=0):
            """Smoothly translates the cube in the 3D space."""
            self.position[0] += x_velocity
            self.position[1] += y_velocity
            self.position[2] += z_velocity

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Smoothly rotates the cube by specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Automatically rotates the cube using its rotation_speed."""
            self.rotation[0] += self.rotation_speed[0]
            self.rotation[1] += self.rotation_speed[1]
            self.rotation[2] += self.rotation_speed[2]

        def draw(self):
            """Draws the cube at its current position and with its current rotation."""
            half_size = self.size / 2
            vertices = [
                # Front face
                (half_size, -half_size, -half_size),
                (half_size, half_size, -half_size),
                (-half_size, half_size, -half_size),
                (-half_size, -half_size, -half_size),
                # Back face
                (half_size, -half_size, half_size),
                (half_size, half_size, half_size),
                (-half_size, -half_size, half_size),
                (-half_size, half_size, half_size),
            ]

            if self.color_sides:
                faces = [
                    (0, 1, 2, 3),  # Front face
                    (3, 2, 7, 6),  # Back face
                    (0, 3, 6, 4),  # Left face
                    (1, 5, 7, 2),  # Right face
                    (4, 5, 1, 0),  # Bottom face
                    (5, 4, 6, 7),  # Top face
                ]
            else:
                faces = [
                    (0, 1), (1, 2), (2, 3), (3, 0),
                    (4, 5), (5, 7), (7, 6), (6, 4),
                    (0, 4), (1, 5), (2, 7), (3, 6)
                ]

            color_mapping = {
                0: self.colors["front"],
                1: self.colors["top"],
                2: self.colors["left"],
                3: self.colors["right"],
                4: self.colors["bottom"],
                5: self.colors["back"]
            }

            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            if self.color_sides:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_LINES)

            for i, face in enumerate(faces):
                if self.color_sides:
                    if i < 6:  # Apply color mapping to faces
                        glColor4fv(color_mapping[i])
                    else:
                        glColor4fv(self.frame_color)
                else:
                    glColor4fv(self.frame_color)

                for vertex in face:
                    glVertex3fv(vertices[vertex])

            glEnd()
            glDisable(GL_BLEND)
            glPopMatrix()

        def check_collision(self, other):
            """
            Checks if this object collides with another object using AABB.
            :param other: Another object with a position and size/dimensions.
            :return: True if there is a collision, False otherwise.
            """
            if (abs(self.position[0] - other.position[0]) < (self.size / 2 + other.size / 2) and
                abs(self.position[1] - other.position[1]) < (self.size / 2 + other.size / 2) and
                abs(self.position[2] - other.position[2]) < (self.size / 2 + other.size / 2)):
                return True
            return False
                

    class RectangularPrism:
        """
        A 3D rectangular prism object.
        """
        def __init__(self, width=1, height=1, depth=1, position=(0, 0, 0), rotation=(0, 0, 0),
                     color_sides=False, frame_color=(1, 1, 1, 1),
                     color_front=(1, 1, 1, 1), color_back=(1, 1, 1, 1), color_left=(1, 1, 1, 1),
                     color_right=(1, 1, 1, 1), color_top=(1, 1, 1, 1), color_bottom=(1, 1, 1, 1)):
            """
            :param width: Width
            :param height: Height
            :param depth: Depth
            :param position: Position in 3D space (for example (0,0,0))
            :param rotation: Initial rotation in 3D space (for example (0,0,0))
            :param color_sides: If False, use frame_color to set color of the frame. Otherwise, the other arguments will be used.
            All color arguments expect a tuple with 4 numbers (Red, Green, Blue, Transparency).
            """
            self.width = width
            self.height = height
            self.depth = depth
            self.position = list(position)  
            self.rotation = list(rotation)  # (pitch, yaw, roll) angles
            self.rotation_speed = [0,0,0]  
            self.color_sides = color_sides
            self.frame_color = frame_color
            colors = {
                "front": color_front,
                "back": color_back,
                "left": color_left,
                "right": color_right,
                "top": color_top,
                "bottom": color_bottom,
            }
            self.colors = colors

        def translate(self, x_velocity=0, y_velocity=0, z_velocity=0):
            """Smoothly translates the prism in the 3D space."""
            self.position[0] += x_velocity
            self.position[1] += y_velocity
            self.position[2] += z_velocity

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Smoothly rotates the prism by specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Automatically rotates the prism using its rotation_speed."""
            self.rotation[0] += self.rotation_speed[0]
            self.rotation[1] += self.rotation_speed[1]
            self.rotation[2] += self.rotation_speed[2]

        def draw(self):
            """Draws the prism at its current position and with its current rotation."""
            half_width = self.width / 2
            half_height = self.height / 2
            half_depth = self.depth / 2
            vertices = [
                # Front face
                (half_width, -half_height, -half_depth),
                (half_width, half_height, -half_depth),
                (-half_width, half_height, -half_depth),
                (-half_width, -half_height, -half_depth),
                # Back face
                (half_width, -half_height, half_depth),
                (half_width, half_height, half_depth),
                (-half_width, -half_height, half_depth),
                (-half_width, half_height, half_depth),
            ]

            if self.color_sides:
                faces = [
                    (0, 1, 2, 3),  # Front face
                    (3, 2, 7, 6),  # Back face
                    (0, 3, 6, 4),  # Left face
                    (1, 5, 7, 2),  # Right face
                    (4, 5, 1, 0),  # Bottom face
                    (5, 4, 6, 7),  # Top face
                ]
            else:
                faces = [
                    (0, 1), (1, 2), (2, 3), (3, 0),
                    (4, 5), (5, 7), (7, 6), (6, 4),
                    (0, 4), (1, 5), (2, 7), (3, 6)
                ]

            color_mapping = {
                0: self.colors["front"],
                1: self.colors["top"],
                2: self.colors["left"],
                3: self.colors["right"],
                4: self.colors["bottom"],
                5: self.colors["back"]
            }

            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)  # Pitch
            glRotatef(self.rotation[1], 0, 1, 0)  # Yaw
            glRotatef(self.rotation[2], 0, 0, 1)  # Roll

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

            if self.color_sides:
                glBegin(GL_QUADS)
            else:
                glBegin(GL_LINES)

            for i, face in enumerate(faces):
                if self.color_sides:
                    if i < 6:  # Apply color mapping to faces
                        glColor4fv(color_mapping[i])
                    else:
                        glColor4fv(self.frame_color)
                else:
                    glColor4fv(self.frame_color)

                for vertex in face:
                    glVertex3fv(vertices[vertex])

            glEnd()
            glDisable(GL_BLEND)
            glPopMatrix()
        
        def check_collision(self, other):
            """
            Checks if this rectangular prism collides with another rectangular prism using AABB.
            :param other: Another object with position, width, height, and depth attributes.
            :return: True if there is a collision, False otherwise.
            """
            if (abs(self.position[0] - other.position[0]) < (self.width / 2 + other.width / 2) and
                abs(self.position[1] - other.position[1]) < (self.height / 2 + other.height / 2) and
                abs(self.position[2] - other.position[2]) < (self.depth / 2 + other.depth / 2)):
                return True
            return False


    class Model3D_STL:
        def __init__(self, stl_path, texture_path=None, color=(1, 1, 1, 1),
                     position=(0, 0, 0), scale=100.0, rotation=(0, 0, 0), use_pil_texture = False, pil_image_variable = None,
                     texturing_mode = 0, texture_repetitions = 1,
                     hitbox_height=1.0, hitbox_width=1.0, hitbox_depth=1.0):
            """
            Loads and renders a 3D model from an STL file with optional texture or plain color.
            :param stl_path: Path to the .STL 3D model file
            :param texture_path: Path to texture image file to use, set None for plain color.
            :param color: Plain color to use if there is no image texture used.
            :param position: X Y Z position in the world, tuple.
            :param scale: Scale of the rendered 3D model in %
            :param rotation: Tuple determining how to rotate the 3D model in degrees.
            :param use_pil_texture: Default false, determines if the program should use texture from file or PIL image variable.
            :param pil_image_variable: Provide a PIL Image variable here (not file path).
            :param texuring mode: Integer which determines how textures are rendered around object. Modes:
            0 - Legacy
            1 - Legacy with texture repetition
            2 - Texture on every side
            3 - Texture wrapped around model
            :param texture_repetitions: How many times to repeat the texture, works in texturing modes 1 and 2.
            """
            self.height = hitbox_height
            self.width = hitbox_width
            self.depth = hitbox_depth
            self.tex_mode = texturing_mode
            self.tex_repetitions = texture_repetitions
            self.stl_path = stl_path
            self.texture_path = texture_path
            self.color = color
            self.position = list(position)
            self.scale = scale / 100.0
            self.rotation = list(rotation)
            self.vertices = []
            self.normals = []
            self.faces = []
            self.texture_coords = []  
            self.texture_id = None
            self.use_pil_texture = use_pil_texture
            
            if pil_image_variable != None:
                self.pil_image_variable = pil_image_variable.convert('RGBA')
            else:
                self.pil_image_variable = None
            
            self.load_model()
            self.generate_texture_coordinates()
            self.create_buffers()
            self.load_texture()

        def load_model(self):
            """
            Parses the STL file and extracts vertices and faces.
            Supports both ASCII and binary STL formats.
            """
            try:
                with open(self.stl_path, 'rb') as file:
                    header = file.read(80)
                    try:
                        num_triangles = struct.unpack('<I', file.read(4))[0]
                        for _ in range(num_triangles):
                            data = file.read(50)  # 12 floats: normal (3), vertices (9), 2-byte attribute
                            if len(data) < 50:
                                break
                            unpacked = struct.unpack('<12fH', data)
                            normal = unpacked[0:3]
                            v1 = unpacked[3:6]
                            v2 = unpacked[6:9]
                            v3 = unpacked[9:12]
                            self.normals.append(self.normalize_vector(normal))
                            self.faces.append((len(self.vertices), len(self.vertices) + 1, len(self.vertices) + 2))
                            self.vertices.extend([v1, v2, v3])
                    except struct.error:
                        # ASCII STL handling
                        file.seek(0)
                        content = file.read().decode('utf-8', errors='ignore')
                        sio = StringIO(content)
                        current_normal = None
                        for line in sio:
                            parts = line.strip().split()
                            if not parts:
                                continue
                            if parts[0] == 'facet' and parts[1] == 'normal':
                                current_normal = self.normalize_vector(list(map(float, parts[2:5])))
                            elif parts[0] == 'vertex':
                                vertex = list(map(float, parts[1:4]))
                                self.vertices.append(vertex)
                            elif parts[0] == 'endfacet':
                                if len(self.vertices) >= 3:
                                    idx = len(self.vertices) - 3
                                    self.faces.append((idx, idx + 1, idx + 2))
                                    self.normals.append(current_normal)
            except Exception as e:
                raise SystemExit(f"Failed to load STL file '{self.stl_path}': {e}")

        def normalize_vector(self, vector):
            """Normalize a 3D vector to unit length."""
            length = math.sqrt(sum(coord ** 2 for coord in vector))
            if length > 0:
                return [coord / length for coord in vector]
            return vector

        def calculate_normal(self, v1, v2, v3):
            """
            Calculates the normal vector of a triangle defined by vertices v1, v2, v3.
            v1, v2, v3 are tuples or lists of three coordinates (x, y, z).
            Returns a normalized vector.
            """
            
            edge1 = (v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2])
            edge2 = (v3[0] - v1[0], v3[1] - v1[1], v3[2] - v1[2])

            normal = (
                edge1[1] * edge2[2] - edge1[2] * edge2[1],
                edge1[2] * edge2[0] - edge1[0] * edge2[2],
                edge1[0] * edge2[1] - edge1[1] * edge2[0],
            )

            
            length = (normal[0]**2 + normal[1]**2 + normal[2]**2)**0.5
            if length > 0:
                normal = (normal[0] / length, normal[1] / length, normal[2] / length)
            return normal

        def generate_texture_coordinates(self):
            if self.tex_mode == 0: #legacy mode
                if not self.vertices:
                    raise ValueError("No vertices found. Ensure the model is loaded before generating texture coordinates.")

                min_x = min(vertex[0] for vertex in self.vertices)
                max_x = max(vertex[0] for vertex in self.vertices)
                min_y = min(vertex[1] for vertex in self.vertices)
                max_y = max(vertex[1] for vertex in self.vertices)

                for vertex in self.vertices:
                    u = (vertex[0] - min_x) / (max_x - min_x) if max_x != min_x else 0
                    v = (vertex[1] - min_y) / (max_y - min_y) if max_y != min_y else 0
                    self.texture_coords.append((u, v))
            elif self.tex_mode == 1: #legacy with texture repetition mode
                if not self.vertices:
                    raise ValueError("No vertices found. Make sure the model is loaded before generating texture coordinates.")

                min_x = min(vertex[0] for vertex in self.vertices)
                max_x = max(vertex[0] for vertex in self.vertices)
                min_y = min(vertex[1] for vertex in self.vertices)
                max_y = max(vertex[1] for vertex in self.vertices)

                for vertex in self.vertices:
                    u = (vertex[0] - min_x) / (max_x - min_x) if max_x != min_x else 0
                    v = (vertex[1] - min_y) / (max_y - min_y) if max_y != min_y else 0

                    wrap_factor = self.tex_repetitions
                    u *= wrap_factor
                    v *= wrap_factor

                    self.texture_coords.append((u, v))
            elif self.tex_mode == 2: #Texture on every side mode
                if not self.faces:
                    raise ValueError("No faces found. Make sure the model is loaded before generating texture coordinates.")

                self.texture_coords = []

                min_x = min(vertex[0] for vertex in self.vertices)
                max_x = max(vertex[0] for vertex in self.vertices)
                min_y = min(vertex[1] for vertex in self.vertices)
                max_y = max(vertex[1] for vertex in self.vertices)
                min_z = min(vertex[2] for vertex in self.vertices)
                max_z = max(vertex[2] for vertex in self.vertices)

                def normalize(value, min_val, max_val):
                    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

                for face in self.faces:
                    v1, v2, v3 = [self.vertices[vertex_index] for vertex_index in face]
                    normal = self.calculate_normal(v1, v2, v3)
                    if abs(normal[0]) > abs(normal[1]) and abs(normal[0]) > abs(normal[2]):
                        #Dominant X-axis (YZ plane)
                        u_axis, v_axis = 1, 2
                    elif abs(normal[1]) > abs(normal[0]) and abs(normal[1]) > abs(normal[2]):
                        #Dominant Y-axis (XZ plane)
                        u_axis, v_axis = 0, 2
                    else:
                        #Dominant Z-axis (XY plane)
                        u_axis, v_axis = 0, 1

                    uv1 = (
                    normalize(v1[u_axis], [min_x, min_y, min_z][u_axis], [max_x, max_y, max_z][u_axis]),
                    normalize(v1[v_axis], [min_x, min_y, min_z][v_axis], [max_x, max_y, max_z][v_axis]),
                        )
                    uv2 = (
                    normalize(v2[u_axis], [min_x, min_y, min_z][u_axis], [max_x, max_y, max_z][u_axis]),
                    normalize(v2[v_axis], [min_x, min_y, min_z][v_axis], [max_x, max_y, max_z][v_axis]),
                        )
                    uv3 = (
                    normalize(v3[u_axis], [min_x, min_y, min_z][u_axis], [max_x, max_y, max_z][u_axis]),
                    normalize(v3[v_axis], [min_x, min_y, min_z][v_axis], [max_x, max_y, max_z][v_axis]),
                        )

                    wrap_factor = self.tex_repetitions
                    uv1 = (uv1[0] * wrap_factor, uv1[1] * wrap_factor)
                    uv2 = (uv2[0] * wrap_factor, uv2[1] * wrap_factor)
                    uv3 = (uv3[0] * wrap_factor, uv3[1] * wrap_factor)
                
                    self.texture_coords.extend([uv1, uv2, uv3])
            elif self.tex_mode == 3: #wrapped mode
                if not self.faces:
                    raise ValueError("No faces found. Make sure the model is loaded before generating texture coordinates.")

                self.texture_coords = []

                min_x = min(v[0] for v in self.vertices)
                max_x = max(v[0] for v in self.vertices)
                min_y = min(v[1] for v in self.vertices)
                max_y = max(v[1] for v in self.vertices)
                min_z = min(v[2] for v in self.vertices)
                max_z = max(v[2] for v in self.vertices)

                def normalize(value, min_val, max_val):
                    return (value - min_val) / (max_val - min_val) if max_val != min_val else 0

                for vertex in self.vertices:
                    x, y, z = vertex
                
                    u = normalize(math.atan2(z, x), -math.pi, math.pi)
                    v = normalize(y, min_y, max_y)

                    self.texture_coords.append((u, v))
            else:
                raise ValueError("Error: wrong texture rendering mode of Object3D_STL.")
                
        def create_buffers(self):
            """
            Creates Vertex Buffer Objects (VBOs) for efficient rendering.
            """
            vertex_data = []
            for i, vertex in enumerate(self.vertices):
                u, v = self.texture_coords[i]
                vertex_data.extend([*vertex, u, v])  # Add position and UV

            vertex_data = np.array(vertex_data, dtype=np.float32)
            index_data = np.array([index for face in self.faces for index in face], dtype=np.uint32)

            self.vertex_vbo = vbo.VBO(vertex_data)
            self.index_vbo = vbo.VBO(index_data, target=GL_ELEMENT_ARRAY_BUFFER)

        def load_texture(self):
            """
            Loads a texture image and binds it for OpenGL rendering with wrapping enabled.
            """
            try:
                if self.texture_path and os.path.exists(self.texture_path):
                    img = Image.open(self.texture_path).convert("RGBA")
                elif self.use_pil_texture == True and self.pil_image_variable != None:
                    img = self.pil_image_variable
                else:
                    img = Image.new('RGBA', (1, 1), color=self.color)
        
                img_data = img.tobytes("raw", "RGBA", 0, -1)
                self.texture_id = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.texture_id)

                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

                glGenerateMipmap(GL_TEXTURE_2D)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

                # Enable texture wrapping
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

                glBindTexture(GL_TEXTURE_2D, 0)
            except Exception as e:
                self.texture_id = None
                print("ERROR: Failed to load or set texture or color.")
                print("Make sure that the texture file exists and/or color is a 4-number tuple (R G B and Transparency)")
                print("Error code: "+str(e))

        def draw(self):
            """
            Renders the STL model with texture or plain color.
            """
            glPushMatrix()
            glTranslatef(*self.position)
            glScalef(self.scale, self.scale, self.scale)
            glRotatef(self.rotation[0], 1, 0, 0)
            glRotatef(self.rotation[1], 0, 1, 0)
            glRotatef(self.rotation[2], 0, 0, 1)

            if self.texture_id:
                glColor4f(1, 1, 1, 1)
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.texture_id)

            self.vertex_vbo.bind()
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

            glVertexPointer(3, GL_FLOAT, 20, self.vertex_vbo)
            glTexCoordPointer(2, GL_FLOAT, 20, self.vertex_vbo + 12)

            self.index_vbo.bind()
            glDrawElements(GL_TRIANGLES, len(self.faces) * 3, GL_UNSIGNED_INT, None)

            self.vertex_vbo.unbind()
            self.index_vbo.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            if self.texture_id:
                glBindTexture(GL_TEXTURE_2D, 0)
                glDisable(GL_TEXTURE_2D)

            glPopMatrix()

        def translate(self, dx=0, dy=0, dz=0):
            """Translates the model by the specified deltas."""
            self.position[0] += dx
            self.position[1] += dy
            self.position[2] += dz

        def rotate(self, delta_pitch=0, delta_yaw=0, delta_roll=0):
            """Rotates the model by the specified angles."""
            self.rotation[0] += delta_pitch
            self.rotation[1] += delta_yaw
            self.rotation[2] += delta_roll

        def update_rotation(self):
            """Applies continuous rotation based on current rotation angles."""
            self.rotate()
            
        def check_collision(self, other):
            """
            Checks if the hitbox collides with something else using AABB.
            :param other: Another object with position, width, height, and depth attributes.
            :return: True if there is a collision, False otherwise.
            """
            if (abs(self.position[0] - other.position[0]) < (self.width / 2 + other.width / 2) and
                abs(self.position[1] - other.position[1]) < (self.height / 2 + other.height / 2) and
                abs(self.position[2] - other.position[2]) < (self.depth / 2 + other.depth / 2)):
                return True
            return False


    class TexturedRectangularPrism(RectangularPrism):
        def __init__(self, width, height, depth, position=(0, 0, 0), rotation=(0, 0, 0),
                     texture_front=None, texture_back=None, texture_left=None, texture_right=None, texture_top=None, texture_bottom=None):
            """
            Initialize a TexturedRectangularPrism.

            :param width: Width of the prism.
            :param height: Height of the prism.
            :param depth: Depth of the prism.
            :param position: 3D position of the prism.
            :param rotation: 3D rotation of the prism (pitch, yaw, roll).
            Another parameters are textures for each side, which can either be file paths, PIL image variables or tuples for plain colors.
            """
            self.width = width
            self.height = height
            self.depth = depth
            self.position = list(position)
            self.rotation = list(rotation)
            self.textures = self.create_texture_dict(texture_front, texture_back, texture_left, texture_right, texture_top, texture_bottom)
            self.texture_ids = {}
            self.load_textures()

        def create_texture_dict(self,texture_front=None, texture_back=None, texture_left=None, texture_right=None, texture_top=None, texture_bottom=None):
            '''
            This function creates a valid dictionary with textures for the rendered to use.
            '''
            list1 = [texture_front, texture_back, texture_left, texture_right, texture_top, texture_bottom]
            list2 = []
            for i in list1:
                if isinstance(i, str) and os.path.isfile(i):
                    img = Image.open(i)
                    imgc = img.convert('RGBA')
                    list2.append(imgc)
                elif isinstance(i, Image.Image):
                    list2.append(i)
                elif isinstance(i, tuple):
                    try:
                        list2.append(Image.new("RGBA", (1, 1), i))
                    except:
                        imgn = Image.new("RGB", (1, 1), i)
                        imgnc = imgn.convert('RGBA')
                        list2.append(imgnc)
                else:
                    list2.append(Image.new("RGBA", (1, 1), (0,0,0,0)))
            del list1
            textures = {
            'front': list2[0],
            'back': list2[1],
            'left': list2[2],
            'right': list2[3],
            'top': list2[4],
            'bottom': list2[5]
            }
            return textures

        def load_textures(self):
            """Load and bind textures for each side of the prism."""
            for side, image in self.textures.items():
                if image:
                    texture_id = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, texture_id)

                    image = image.convert("RGBA")
                    img_data = image.tobytes("raw", "RGBA", 0, -1)

                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

                    self.texture_ids[side] = texture_id

        def draw(self):
            """Render the textured rectangular prism."""
            half_width = self.width / 2
            half_height = self.height / 2
            half_depth = self.depth / 2

            # Define vertices for each face
            vertices = {
                'front': [(half_width, -half_height, -half_depth), (half_width, half_height, -half_depth),
                          (-half_width, half_height, -half_depth), (-half_width, -half_height, -half_depth)],
                'back': [(half_width, -half_height, half_depth), (half_width, half_height, half_depth),
                         (-half_width, half_height, half_depth), (-half_width, -half_height, half_depth)],
                'left': [(-half_width, -half_height, -half_depth), (-half_width, half_height, -half_depth),
                         (-half_width, half_height, half_depth), (-half_width, -half_height, half_depth)],
                'right': [(half_width, -half_height, -half_depth), (half_width, half_height, -half_depth),
                          (half_width, half_height, half_depth), (half_width, -half_height, half_depth)],
                'top': [(-half_width, half_height, -half_depth), (half_width, half_height, -half_depth),
                        (half_width, half_height, half_depth), (-half_width, half_height, half_depth)],
                'bottom': [(-half_width, -half_height, -half_depth), (half_width, -half_height, -half_depth),
                           (half_width, -half_height, half_depth), (-half_width, -half_height, half_depth)]
            }

            glPushMatrix()
            glTranslatef(*self.position)
            glRotatef(self.rotation[0], 1, 0, 0)
            glRotatef(self.rotation[1], 0, 1, 0)
            glRotatef(self.rotation[2], 0, 0, 1)

            for side, verts in vertices.items():
                texture_id = self.texture_ids.get(side)
                if texture_id:
                    glEnable(GL_TEXTURE_2D)
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    glColor4f(1, 1, 1, 1)
                else:
                    glDisable(GL_TEXTURE_2D)

                glBegin(GL_QUADS)
                tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]
                for tex_coord, vertex in zip(tex_coords, verts):
                    glTexCoord2f(*tex_coord)
                    glVertex3fv(vertex)
                glEnd()

                if texture_id:
                    glBindTexture(GL_TEXTURE_2D, 0)

            glDisable(GL_TEXTURE_2D)
            glPopMatrix()


    #2D Objects:
    
    class Rectangle_2D:
        """Represents a rectangle object for 2D rendering using OpenGL."""
        def __init__(self, x, y, width, height, fill_color, frame_color=None, frame_width=1):
            """
            Initialize the Rectangle with x, y coordinates, width, height, fill color,
            and optional frame color and width.

            :param x: X-coordinate of the top-left corner.
            :param y: Y-coordinate of the top-left corner.
            :param width: Width of the rectangle.
            :param height: Height of the rectangle.
            :param fill_color: Tuple representing RGBA color (0-1 range).
            :param frame_color: Tuple representing RGBA frame color (0-1 range), optional.
            :param frame_width: Width of the frame line, optional.
            """
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.fill_color = fill_color  # Expected to be a tuple with values in [0,1]
            self.frame_color = frame_color  # Expected to be a tuple with values in [0,1] or None
            self.frame_width = frame_width
            
        def move(self,x,y):
            self.x += x
            self.y += y
            
        def setlocation(self,x,y):
            self.x=x
            self.y=y
            
        def draw(self, app):
            """Draw the rectangle using OpenGL."""
            
            app.draw_rectangle_2d((self.x, self.y, self.width, self.height), self.fill_color)

            if self.frame_color and self.frame_width > 0:
                glLineWidth(self.frame_width)
                glColor4f(*self.frame_color)
                glBegin(GL_LINE_LOOP)
                glVertex2f(self.x, self.y)
                glVertex2f(self.x + self.width, self.y)
                glVertex2f(self.x + self.width, self.y + self.height)
                glVertex2f(self.x, self.y + self.height)
                glEnd()
                
        def is_mouse_above(self, mouse_x, mouse_y):
            """Check if the mouse (or other cursor) is above the object."""
            return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height
                

    
    class Circle_2D:
        """Represents a circle object for 2D rendering using OpenGL."""
        def __init__(self, x, y, radius, fill_color, frame_color=None, frame_width=1, segments=32):
            """
            Initialize the Circle with x, y coordinates, radius, fill color,
            and optional frame color and width.

            :param x: X-coordinate of the center.
            :param y: Y-coordinate of the center.
            :param radius: Radius of the circle.
            :param fill_color: Tuple representing RGBA color (0-1 range).
            :param frame_color: Tuple representing RGBA frame color (0-1 range), optional.
            :param frame_width: Width of the frame line, optional.
            :param segments: Number of segments to approximate the circle.
            """
            self.x = x
            self.y = y
            self.radius = radius
            self.fill_color = fill_color  # Expected to be a tuple with values in [0,1]
            self.frame_color = frame_color  # Expected to be a tuple with values in [0,1] or None
            self.frame_width = frame_width
            self.segments = segments
            
        def move(self,x,y):
            self.x += x
            self.y += y
            
        def setlocation(self,x,y):
            self.x=x
            self.y=y
            
        def draw(self, app):
            """Draw the circle using OpenGL."""
            
            app.draw_circle_2d(self, self.segments)

            if self.frame_color and self.frame_width > 0:
                glLineWidth(self.frame_width)
                glColor4f(*self.frame_color)
                glBegin(GL_LINE_LOOP)
                for i in range(self.segments):
                    angle = 2 * math.pi * i / self.segments
                    glVertex2f(self.x + math.cos(angle) * self.radius, self.y + math.sin(angle) * self.radius)
                glEnd()
                
        def is_mouse_above(self, mouse_x, mouse_y):
            """Check if the mouse (or other cursor) is above the object."""
            distance_squared = (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2
            return distance_squared <= self.radius ** 2
    
    
    class Image_2D:
        """Represents an image object for 2D rendering using OpenGL."""
        def __init__(self, image_path, x, y, width=None, height=None, rotation=0):
            """
            Initialize the Image with the image path, position, and optional dimensions.

            :param image_path: Path to the image file.
            :param x: X-coordinate of the top-left corner.
            :param y: Y-coordinate of the top-left corner.
            :param width: Width to scale the image to, optional.
            :param height: Height to scale the image to, optional.
            :param rotation: Rotate image within its rendering zone.
            """
            self.image_path = image_path
            self.x = x
            self.y = y

            try:
                image = pygame.image.load(image_path).convert_alpha()
            except pygame.error as e:
                #print(f"Failed to load image {image_path}: {e}")
                raise SystemExit(e)
            image = pygame.transform.rotate(image, 180 + rotation)
            image = pygame.transform.flip(image, True, False)
        
            if width and height:
                image = pygame.transform.scale(image, (width, height))
                self.width = width
                self.height = height
            else:
                self.width, self.height = image.get_size()

            image_data = pygame.image.tostring(image, "RGBA", True)

            # Generate an OpenGL texture ID
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # or GL_NEAREST
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # or GL_NEAREST

            # Upload the texture data to OpenGL
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                self.width,
                self.height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                image_data
            )

            glBindTexture(GL_TEXTURE_2D, 0)  # Unbind the texture
            
        def move(self,x,y):
            self.x += x
            self.y += y
            
        def setlocation(self,x,y):
            self.x=x
            self.y=y
            
        def draw(self, app):
            """Draw the image as a textured quad using OpenGL."""
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor4f(1, 1, 1, 1)  # Set color to white to display texture as-is

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(self.x, self.y)

            glTexCoord2f(1, 0)
            glVertex2f(self.x + self.width, self.y)

            glTexCoord2f(1, 1)
            glVertex2f(self.x + self.width, self.y + self.height)

            glTexCoord2f(0, 1)
            glVertex2f(self.x, self.y + self.height)
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)
            
        def is_mouse_above(self, mouse_x, mouse_y):
            """Check if the mouse (or other cursor) is above the object."""
            return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    class Image_2D_PIL:
        """Represents an image object for 2D rendering using OpenGL, but uses PIL image variable instead of file path."""
        def __init__(self, pil_image_variable, x, y, width=None, height=None, rotation=0):
            """
            Initialize the Image with the image path, position, and optional dimensions.

            :param pil_image_variable: PIL Image (not path to an image, but image saved into a PIL image variable).
            :param x: X-coordinate of the top-left corner.
            :param y: Y-coordinate of the top-left corner.
            :param width: Width to scale the image to, optional.
            :param height: Height to scale the image to, optional.
            :param rotation: Rotate image within its rendering zone.
            """
            self.pil_image = pil_image_variable
            self.x = x
            self.y = y
            self.rotation = rotation

            image = self.pil_image.convert("RGBA")
            image = image.rotate(180)
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            if width and height:
                image = image.resize((width, height))
                self.width = width
                self.height = height
            else:
                self.width, self.height = image.size

            self.image_data = image.tobytes("raw", "RGBA", 0, -1)

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            # Upload the texture data to OpenGL
            glTexImage2D(
                GL_TEXTURE_2D,
                0,
                GL_RGBA,
                self.width,
                self.height,
                0,
                GL_RGBA,
                GL_UNSIGNED_BYTE,
                self.image_data
            )

            glBindTexture(GL_TEXTURE_2D, 0)  # Unbind the texture

        def move(self, x, y):
            self.x += x
            self.y += y

        def setlocation(self, x, y):
            self.x = x
            self.y = y

        def draw(self, app):
            """Draw the image as a textured quad using OpenGL."""
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor4f(1, 1, 1, 1) 

            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(self.x, self.y)

            glTexCoord2f(1, 0)
            glVertex2f(self.x + self.width, self.y)

            glTexCoord2f(1, 1)
            glVertex2f(self.x + self.width, self.y + self.height)

            glTexCoord2f(0, 1)
            glVertex2f(self.x, self.y + self.height)
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)
            glDisable(GL_TEXTURE_2D)

        def is_mouse_above(self, mouse_x, mouse_y):
            """Check if the mouse (or other cursor) is above the object."""
            return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height



    #2D related methods
        
    def get_mouse_position(self):
        """Get current position of the mouse, return 2 variables - x and y."""
        x, y = pygame.mouse.get_pos()
        return x, y
            
    def set_perspective(self):
        """Set up the perspective projection for 3D rendering."""
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.camera.fov, (self.window_size_x / self.window_size_y), self.camera.min_render_distance, self.camera.max_render_distance)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.camera.setup_perspective()

    def set_orthographic(self):
        """Set up an orthographic projection for 2D rendering."""
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()  # Save current projection matrix
        glLoadIdentity()
        gluOrtho2D(0, self.window_size_x, self.window_size_y, 0)  # Top-left corner is (0,0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()  # Save current modelview matrix
        glLoadIdentity()

    def reset_projection(self):
        """Reset to the previous projection and modelview matrices."""
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def draw_rectangle_2d(self, rect, color):
        """
        Draw a 2D rectangle using OpenGL primitives.

        :param rect: Tuple (x, y, width, height).
        :param color: Tuple (r, g, b, a) with values in [0,1].
        """
        x, y, width, height = rect
        r, g, b, a = color
        glColor4f(r, g, b, a)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def draw_circle_2d(self, circle, segments=32):
        """
        Draw a filled 2D circle using OpenGL.

        :param circle: Instance of Circle_2D class.
        :param segments: Number of segments to approximate the circle.
        """
        glColor4f(*circle.fill_color)
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(circle.x, circle.y)  # Center of circle
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            glVertex2f(circle.x + math.cos(angle) * circle.radius, circle.y + math.sin(angle) * circle.radius)
        glEnd()

    def render_2d_objects(self, object_list, render_with_shading=False):
        """
        Render 2D objects using OpenGL. Should be called after rendering 3D objects.

        :param object_list: List of 2D objects (Rectangle_2D, Circle_2D, Image_2D, etc.).
        :param render_with_shading: Set to true to disable shading while rendering 2D objects. Default False.
        """
        if render_with_shading==False and self.enabled_shading==True:
            self.disable_shading()
            restore_shading = True
        else:
            restore_shading = False
            
        self.set_orthographic()  # Switch to orthographic projection

        # Disable depth testing to ensure 2D UI elements are rendered on top
        glDisable(GL_DEPTH_TEST)

        for obj in object_list:
            if hasattr(obj, 'draw'):
                obj.draw(self)  # Pass the app instance to the draw method
            else:
                print(f"Warning: Object {obj} does not have a 'draw' method.")

        # Re-enable depth testing if it was enabled
        if self.depth_testing_enabled:
            glEnable(GL_DEPTH_TEST)

        self.reset_projection()  # Switch back to perspective projection
        
        if restore_shading:
            self.enable_shading()

    
    #Audio:
       
    class SoundManager:
        """
        Allows to use and control audio in your program.
        Currently, it's just primitive audio playback, without support for audio within 3D space.
        """
        def __init__(self, channel_amount=8):
            """
            Initializes the Pygame mixer and creates dictionaries to store sounds, their playing status, and whether they should loop.
            :param channel_amount: Set how many PyGame audio channels to create, default 8.
            """
            pygame.mixer.init()
            self.sounds = {}
            self.is_playing = {}
            self.loop = {}
            self.channels = [pygame.mixer.Channel(i) for i in range(channel_amount)]
            self.channel_amount = channel_amount
        def add_sound_to_memory(self, name: str, file_path: str, loop=False):
            """
            Adds a new sound to the manager.
            
            
            :param name: The name of the sound, string. Any you want.
            :param file_path: The file path of the sound file, use whatever format PyGame and your system support.
            :param loop: Whether the sound should loop (for example background music) or not (for example sound effect), bool.
            """
            self.sounds[name] = pygame.mixer.Sound(file_path)
            self.is_playing[name] = False
            self.loop[name] = loop

        def play_sound(self, name: str):
            """
            Plays the specified sound.
            :param name: The name of the sound to play.
            """
            if not self.is_playing[name]:
                for channel in self.channels:
                    if not channel.get_busy():
                        channel.play(self.sounds[name], -1 if self.loop[name] else 0)
                        self.is_playing[name] = True
                        break

        def stop_sound(self, name:str):
            """
            Stops the specified sound.
            :param name (str): The name of the sound to stop.
            """
            for channel in self.channels:
                if channel.get_busy() and channel.get_sound() == self.sounds[name]:
                    channel.stop()
                    self.is_playing[name] = False
                    break

        def update(self):
            """
            Updates the playing status of the sounds.
            Checks if any of the sounds that are currently playing have finished playing, and if so, sets their playing status to False.
            """
            for name, is_playing in self.is_playing.items():
                if is_playing:
                    found_channel = False
                    for channel in self.channels:
                        if channel.get_busy() and channel.get_sound() == self.sounds[name]:
                            found_channel = True
                            break
                    if not found_channel:
                        self.is_playing[name] = False

    #3D rendering methods:
    def render_3d_objects(self, object_list):
        """
        Renders 3D objects by running draw() method for every object provided in object_list list.
        Returns the provided object list.
        """
        for i in object_list:
            if hasattr(i, 'draw'):
                i.draw()
                #print(str(time.time())+str(i))
        return object_list
                
    def render_visible_3d_objects(self,object_list,distance=20,angle=60):
        """
        Renders only 3D objects that are currently in the field of view, increasing rendering performance.
        :param object_list: List of objects to take into account then rendering, for example [cube1, cube2].
        :param distance: Rendering distance, default 20.
        :param angle: Angle in degrees between object and camera's forward vector. By default 60, which works good in default field of view of the camera, but increase it in case of problems. 
        Returns list of objects that were rendered.
        """
        visible_objects = self.camera.detect_objects_in_view(object_list,distance,angle)
        return self.render_3d_objects(visible_objects)
         
    #Asynchronous processing, functions and functionalities:
        
    class AsyncFunctionManager:
        def __init__(self):
            self.tasks = []
    
        async def start_async_function(self, async_function, *args):
            """
            Starts an asynchronous function and adds it to the list of tasks. Use the function itself and its arguments as arguments.
            """
            task = asyncio.create_task(async_function(*args))
            self.tasks.append(task)
            return task
    
        async def stop_async_function(self, task):
            """
            Cancels a specific running asynchronous function and waits for it to complete. Use the function itself as argument.
            """
            if task in self.tasks:
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
                self.tasks.remove(task)
    
        async def stop_all_async_functions(self):
            """
            Cancels all running asynchronous functions and waits for them to complete.
            """
            for task in self.tasks:
                task.cancel()
            await asyncio.gather(*self.tasks, return_exceptions=True)
            self.tasks.clear()
    
        async def get_async_function_result(self, task):
            """
            Checks if the given asynchronous function task has finished and returns its result, or None if it hasn't finished yet. Use the function itself as argument.
            """
            if task.done():
                try:
                    return task.result()
                except asyncio.CancelledError:
                    return None
            else:
                return None
            
    #Shading (light):
            
    def enable_shading(self):
        self.enabled_shading = True
        glEnable(GL_LIGHTING)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    def disable_shading(self):
        self.enabled_shading = False
        glDisable(GL_LIGHTING)
        glDisable(GL_COLOR_MATERIAL)
        
    def cache_current_material_settings(self):
        '''
        If you set a OpenGL material with set_material(), it will be used since calling that command for rendering objects.
        Use this to cache the current material setting, and then you can load it back with load_cached_material_settings().
        '''
        glPushAttrib(GL_LIGHTING_BIT)
        
    def load_cached_material_settings(self):
        '''
        If you set a OpenGL material with set_material(), it will be used since calling that command for rendering objects.
        With cache_current_material_settings() you can cache the current material setting, and with this command you can load it back.
        '''
        glPopAttrib()
        
    def use_default_material(self):
        '''
        Use default OpenGL material for rendering since calling this command.
        '''
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, [0.0])

    def set_material(self, ambient=[0.2, 0.2, 0.2, 1.0], diffuse=[0.8, 0.8, 0.8, 1.0], specular=[0.0, 0.0, 0.0, 1.0], shininess=[0.0]):
        '''
        Set OpenGL material to use since calling this command.
        All values in quadruples should be floats between 0 and 1. Only the last param, shininess must be a float between 0 and 128.
        :param ambient: A quadruple representing the ambient light color [R, G, B, A]. Default is [0.2, 0.2, 0.2, 1.0].
        :param diffuse: A quadruple representing the diffuse light color. Default is [0.8, 0.8, 0.8, 1.0].
        :param specular: A quadruple representing the specular light color. Default is [0.0, 0.0, 0.0, 1.0].
        :param shininess: A list with one float between 0 and 128 representing the shininess of the material. Default is [0.0].
        '''
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shininess)
        
    class LegacyLight:
        def __init__(self, light_id: int, position_tuple=(0.0, 0.0, 1.0), point_light=True,
                     ambient_quadruple=(0.0, 0.0, 0.0, 1.0), diffuse_quadruple=(1.0, 1.0, 1.0, 1.0),
                     specular_quadruple=(1.0, 1.0, 1.0, 1.0), spot_direction=(0.0, 0.0, -1.0), spot_exponent=0.0,
                     spot_cutoff=180.0, constant_attenuation=1.0, linear_attenuation=0.0,
                     quadratic_attenuation=0.0, enabled=True):
            '''
            Create a legacy OpenGL light.
            :param light_id: ID of the light source, int between 0 and 7 (legacy OpenGL supports up to 8 lights).
            :param position_tuple: (x, y, z) for point or directional light.
            :param point_light: If True, w=1.0 (point light). If False, w=0.0 (directional light).
            :param ambient_quadruple: (R, G, B, A) ambient color (dim fill light).
            :param diffuse_quadruple: (R, G, B, A) diffuse color (main light).
            :param specular_quadruple: (R, G, B, A) specular color (reflections).
            :param spot_direction: (x, y, z) spotlight direction (used if spot_cutoff < 180).
            :param spot_exponent: Spotlight exponent (0 = wide, 128 = very focused).
            :param spot_cutoff: Spotlight angle (in degrees). <180 for a cone, 180 for no cutoff.
            :param constant_attenuation: Constant attenuation factor (distance-based).
            :param linear_attenuation: Linear attenuation factor.
            :param quadratic_attenuation: Quadratic attenuation factor.
            :param enabled: Create the light already enabled.
            '''
            if light_id<0 or light_id>7:
                raise ValueError("Error: ID must be between 0 and 7. Only 8 legacy lights can exist.")
            match light_id:
                case 0:
                    self.gl_light = GL_LIGHT0
                case 1:
                    self.gl_light = GL_LIGHT1
                case 2:
                    self.gl_light = GL_LIGHT2
                case 3:
                    self.gl_light = GL_LIGHT3
                case 4:
                    self.gl_light = GL_LIGHT4
                case 5:
                    self.gl_light = GL_LIGHT5
                case 6:
                    self.gl_light = GL_LIGHT6
                case 7:
                    self.gl_light = GL_LIGHT7
                case _:
                    raise ValueError("Error: ID must be between 0 and 7. Only 8 legacy lights can exist.")
                
            if len(position_tuple) != 3:
                raise ValueError("position_tuple must have 3 elements (x, y, z).")
            if len(ambient_quadruple) != 4:
                raise ValueError("ambient_quadruple must have 4 elements (R, G, B, A).")
            if len(diffuse_quadruple) != 4:
                raise ValueError("diffuse_quadruple must have 4 elements (R, G, B, A).")
            if len(specular_quadruple) != 4:
                raise ValueError("specular_quadruple must have 4 elements (R, G, B, A).")
            if len(spot_direction) != 3:
                raise ValueError("spot_direction must have 3 elements (x, y, z).")
            
            if point_light:
                pl = 1.0
            else:
                pl = 0.0
            
            self.light_id = light_id
            self.position_quad = [position_tuple[0], position_tuple[1], position_tuple[2], pl]
            self.ambient_quad = ambient_quadruple
            self.diffuse_quad = diffuse_quadruple
            self.specular_quad = specular_quadruple
            self.spot_direction = spot_direction
            self.spot_exponent = spot_exponent
            self.spot_cutoff = spot_cutoff
            self.constant_attenuation = constant_attenuation
            self.linear_attenuation = linear_attenuation
            self.quadratic_attenuation = quadratic_attenuation
            
            self.apply_light_params_to_opengl()
            
            self.enabled = enabled
            if enabled:
                glEnable(self.gl_light)
            else:
                glDisable(self.gl_light)

        def apply_light_params_to_opengl(self):
            '''
            Applies all stored parameters to the OpenGL light.
            '''
            glLightfv(self.gl_light, GL_POSITION, self.position_quad)
            glLightfv(self.gl_light, GL_AMBIENT, self.ambient_quad)
            glLightfv(self.gl_light, GL_DIFFUSE, self.diffuse_quad)
            glLightfv(self.gl_light, GL_SPECULAR, self.specular_quad)
            glLightfv(self.gl_light, GL_SPOT_DIRECTION, self.spot_direction)
            glLightf(self.gl_light, GL_SPOT_EXPONENT, self.spot_exponent)
            glLightf(self.gl_light, GL_SPOT_CUTOFF, self.spot_cutoff)
            glLightf(self.gl_light, GL_CONSTANT_ATTENUATION, self.constant_attenuation)
            glLightf(self.gl_light, GL_LINEAR_ATTENUATION, self.linear_attenuation)
            glLightf(self.gl_light, GL_QUADRATIC_ATTENUATION, self.quadratic_attenuation)

        def enable(self):
            glEnable(self.gl_light)
            self.enabled = True

        def disable(self):
            glDisable(self.gl_light)
            self.enabled = False

        def update_params(self, ambient_quadruple=None, diffuse_quadruple=None, specular_quadruple=None, spot_direction=None,
                          spot_exponent=None, spot_cutoff=None, constant_attenuation=None, linear_attenuation=None,
                          quadratic_attenuation=None):
            '''
            Change any subset of the light parameters at runtime.
            Pass only the parameters you want to update, others will remain unchanged.
            '''
            if ambient_quadruple is not None:
                if len(ambient_quadruple) != 4:
                    raise ValueError("ambient_quadruple must have 4 elements (R, G, B, A).")
                self.ambient_quad = ambient_quadruple
                
            if diffuse_quadruple is not None:
                if len(diffuse_quadruple) != 4:
                    raise ValueError("diffuse_quadruple must have 4 elements (R, G, B, A).")
                self.diffuse_quad = diffuse_quadruple
                
            if specular_quadruple is not None:
                if len(specular_quadruple) != 4:
                    raise ValueError("specular_quadruple must have 4 elements (R, G, B, A).")
                self.specular_quad = specular_quadruple
                
            if spot_direction is not None:
                if len(spot_direction) != 3:
                    raise ValueError("spot_direction must have 3 elements (x, y, z).")
                self.spot_direction = spot_direction
                
            if spot_exponent is not None:
                self.spot_exponent = spot_exponent
            if spot_cutoff is not None:
                self.spot_cutoff = spot_cutoff
            if constant_attenuation is not None:
                self.constant_attenuation = constant_attenuation
            if linear_attenuation is not None:
                self.linear_attenuation = linear_attenuation
            if quadratic_attenuation is not None:
                self.quadratic_attenuation = quadratic_attenuation
            
            self.apply_light_params_to_opengl()

        def change_position(self, position_tuple, point_light: bool = None):
            '''
            Set new position of the light.
            :param position_tuple: Position tuple containing [X, Y, Z] position, or direction in case of directional light.
            :param point_light: If set to False, the light will be a directional light, otherwise a point one. Set None to keep original value.
            '''
            if len(position_tuple) != 3:
                raise ValueError("Error: Position must be a tuple of 3 elements.")
            
            if point_light == True:
                pl = 1.0
            elif point_light == False:
                pl = 0.0
            elif point_light == None:
                pl = self.position_quad[3]
            else:
                pl = self.position_quad[3]
                
            self.position_quad = [position_tuple[0], position_tuple[1], position_tuple[2], pl]
            glLightfv(self.gl_light, GL_POSITION, self.position_quad)

        def change_position_via_quadruple(self, position_quadruple):
            '''
            Change light's position by passing a tuple of 4 elements [X, Y, Z, TYPE]
            If TYPE is 1.0, then the light will be a point one. If 0.0 then directional light.
            If the light is directional, X Y and Z represent its direction.
            '''
            if len(position_quadruple)!=4:
                raise ValueError("Error: position_quadruple must be a tuple of 4 elements")
            self.position_quad = position_quadruple
            glLightfv(self.gl_light, GL_POSITION, self.position_quad)

        def change_light_type(self, point_light: bool):
            '''
            Changes type of light between point light and directional light.
            :param point_light: If set to False, the light will be a directional light, otherwise a point one.
            '''
            if point_light:
                pl = 1.0
            else:
                pl = 0.0
            self.position_quad[3] = pl
            glLightfv(self.gl_light, GL_POSITION, self.position_quad)

        def change_position_via_tuple(self, position_tuple):
            '''
            Change position by passing a tuple of 3 elements [X, Y, Z].
            If the light is directional, X Y and Z represent its direction.
            '''
            if len(position_tuple)!=3:
                raise ValueError("Error: position_tuple must be a tuple of 3 elements")
            a,b,c = position_tuple
            self.position_quad = [a,b,c,self.position_quad[3]]
            glLightfv(self.gl_light, GL_POSITION, self.position_quad)

        def translate(self, x: float, y: float, z: float):
            '''
            Move the light in 3D space.
            '''
            a, b, c, d = self.position_quad
            a += x
            b += y
            c += z
            self.position_quad = [a,b,c,d]
            #print(self.position_quad)
            glLightfv(self.gl_light, GL_POSITION, self.position_quad)