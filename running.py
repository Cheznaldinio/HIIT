import time
import pyttsx3
import threading
import queue
import re
import pygame

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('volume', 0.8)

# Instructions and timings extracted from the image
instructions = [
    ("Instruction 1, speed 7.4", 0 * 60),
    ("Instruction 2, speed 3.8", 2.5 * 60),
    ("Instruction 3, speed 7.4", 3 * 60),
    ("Instruction 4, speed 3.8", 5 * 60),
    ("Instruction 5, speed 7.4", 5.5 * 60),
    ("Instruction 6, speed 3.8", 7.5 * 60),
    ("Instruction 7, speed 7.4", 8 * 60),
    ("Instruction 8, speed 3.8", 10 * 60),
    ("Instruction 9, speed 7.4", 10.5 * 60),
    ("Instruction 10, speed 3.8", 12.5 * 60),
    ("Instruction 11, speed 7.4", 13.5 * 60),
    ("Instruction 12, speed 3.8", 15.5 * 60),
    ("Instruction 13, speed 7.4", 16 * 60),
    ("Instruction 14, speed 3.8", 18 * 60),
    ("Instruction 15, speed 7.4", 18.5 * 60),
    ("Instruction 16, speed 3.8", 20.5 * 60),
    ("Instruction 17, speed 7.4", 21 * 60),
    ("Instruction 18, speed 3.8", 23 * 60),
    ("Instruction 19, speed 7.4", 23.5 * 60),
    ("Instruction 20, speed 3.8", 25.5 * 60),
    ("Instruction 21, speed 7.4", 26.5 * 60),
    ("Instruction 22, speed 3.8", 28.5 * 60),
    ("Instruction 23, speed 7.4", 29 * 60),
    ("Instruction 24, speed 3.8", 31 * 60),
    ("Instruction 25, speed 7.4", 31.5 * 60),
    ("Instruction 26, speed 3.8", 33.5 * 60),
    ("Instruction 27, speed 7.4", 34 * 60),
    ("Instruction 28, speed 3.8", 36 * 60),
    ("Instruction 29, speed 7.4", 36.5 * 60),
    ("Instruction 30, speed 3.8", 38.5 * 60),
    ("Instruction 31, speed 7.4", 39.5 * 60),
    ("Instruction 32, speed 3.8", 41.5 * 60),
    ("Instruction 33, speed 7.4", 42 * 60),
    ("Instruction 34, speed 3.8", 44 * 60),
    ("Instruction 35, speed 7.4", 44.5 * 60),
    ("Instruction 36, speed 3.8", 46.5 * 60),
    ("Instruction 37, speed 7.4", 47.5 * 60),
    ("Instruction 38, speed 3.8", 49.5 * 60),
    ("Instruction 39, speed 7.4", 50 * 60),
    ("Instruction 40, speed 3.8", 52 * 60),
    ("Instruction 41, speed 7.4", 52.5 * 60),
    ("Instruction 42, speed 0", 55 * 60)
]




# Command queue to handle user inputs
command_queue = queue.Queue()

def get_user_input():
    while True:
        command = input().strip().lower()
        command_queue.put(command)

# Start the thread to capture user inputs
input_thread = threading.Thread(target=get_user_input, daemon=True)
input_thread.start()

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1500, 1100))
pygame.display.set_caption("Speed Display")
font = pygame.font.Font(None, 120)

def update_speed_display(speed):
    screen.fill((0, 0, 0))
    pygame.display.flip()
    time.sleep(0.1)
    screen.fill((255, 0, 0))
    pygame.display.flip()
    time.sleep(0.1)
    screen.fill((0, 255, 0))
    pygame.display.flip()
    time.sleep(0.1)
    screen.fill((0, 0, 0))
    text = font.render(f"Speed: {speed}", True, (255, 255, 255))
    screen.blit(text, (600, 500))
    pygame.display.flip()

def extract_speed(instruction):
    match = re.search(r'speed ([\d\.]+)', instruction)
    if match:
        return float(match.group(1))
    return None

def execute_instructions(instructions):
    start_time = time.time()
    current_instruction = 0
    paused = False
    speed_factor = 1.0

    while current_instruction < len(instructions):
        if not paused:
            instruction, delay = instructions[current_instruction]
            adjusted_delay = delay / speed_factor
            time_to_wait = adjusted_delay - (time.time() - start_time)
            if time_to_wait > 0:
                time.sleep(time_to_wait)
            print(instruction)
            engine.say(instruction)
            engine.runAndWait()
            speed = extract_speed(instruction)
            if speed is not None:
                update_speed_display(speed)
            current_instruction += 1

        if not command_queue.empty():
            command = command_queue.get()
            if command == 'p':
                paused = True
                print("Paused.")
            elif command == 'r':
                current_instruction = 0
                start_time = time.time()
                print("Restarting.")
                paused = False
            elif command == 's':
                paused = False
                start_time = time.time() - (instructions[current_instruction][1] / speed_factor)
                print("Resuming.")
            elif command == 'b':
                if current_instruction > 1:
                    current_instruction -= 2
                    start_time = time.time() - (instructions[current_instruction][1] / speed_factor)
                    print("Going back one instruction.")
            elif re.match(r's\d+', command):
                instruction_number = int(command[1:])
                if 1 <= instruction_number <= len(instructions):
                    current_instruction = instruction_number - 1
                    start_time = time.time() - (instructions[current_instruction][1] / speed_factor)
                    print(f"Starting at instruction {instruction_number}.")
            elif re.match(r'speed\d+(\.\d+)?', command):
                speed_factor = float(command[5:])
                start_time = time.time() - (instructions[current_instruction][1] / speed_factor)
                print(f"Setting speed to {speed_factor}x.")

        # Check for Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Initial speed display
initial_speed = extract_speed(instructions[0][0])
if initial_speed is not None:
    update_speed_display(initial_speed)

execute_instructions(instructions)
print("All instructions have been printed and read aloud.")
pygame.quit()
