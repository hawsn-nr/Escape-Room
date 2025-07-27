from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(vsync=False)
ground = Entity(model='plane', scale=(50, 1, 50), texture='grass', collider='box', texture_scale=(50, 50))
player = FirstPersonController(collider='box', position=(5, 1, 1))
#                                                   Room1
#---Walls Room 1---
room1_wall1 = Entity(model='cube', scale=(.5,10,10), position=(0,1,0), texture='white_cube', collider='box', color=color.brown, texture_scale=(10,10))
room1_wall2 = Entity(model='cube', scale=(.5,10,10), position=(10,1,0), texture='white_cube', collider='box', texture_scale=(10,10), color=color.brown)
room1_wall3 = Entity(model='cube', scale=(10,10,.5), position=(5,1,4.75), texture='white_cube', collider='box', texture_scale=(10,10), color=color.brown)
room1_wall4 = Entity(model='cube', scale=(4, 10, .5), position=(2.24, 1, -4.75), texture='white_cube', collider='box', color=color.brown, texture_scale=(4,10))
room1_wall5 = Entity(model='cube', scale=(4, 10, .5), position=(7.76, 1, -4.75), texture='white_cube', collider='box', color=color.brown, texture_scale=(4,10))
room1_wall6 = Entity(model='cube', scale=(1.5, 3.5, .5), position=(5, 4.25, -4.75), texture='white_cube', collider='box', color=color.brown, texture_scale=(1.5,3.5))

#---Doors---
door = Entity(model='cube', texture='brick', scale=(1.5, 2.5, 0.5), position=(5, 1.25, -5), collider='box')
final_exit_door = Entity(model='cube', texture='brick', position=(5, 1, -19.8), scale=(1.5, 2.5, 0.5), color=color.dark_gray, collider='box')
door_lock = True
final_door_lock = True
door.open_time = 0
final_exit_door.open_time = 0

#---Tiles---
blue = Entity(model='cube', position=(2, 0, 4), color=color.blue, collider='box', identifier='blue')
green = Entity(model='cube', position=(9.3, 0, 0), color=color.green, collider='box', identifier='green')
yellow = Entity(model='cube', position=(6, 0, 4), color=color.yellow, collider='box', identifier='yellow')
red = Entity(model='cube', position=(9.3, 0, 4), color=color.red, collider='box', identifier='red')
purple = Entity(model='cube', position=(1, 0, -4), color=rgb(128, 0, 128), collider='box', identifier='purple')

#                                                  Room2
#---Walls Room 2---
room2_wall1 = Entity(model='cube', scale=(.5, 10, 16), position=(0, 1, -12), texture='white_cube', collider='box', color=color.brown , texture_scale=(10,10))
room2_wall2 = Entity(model='cube', scale=(.5, 10, 16), position=(10, 1, -12), texture='white_cube', collider='box', color=color.brown , texture_scale=(10,10))
room2_wall3 = Entity(model='cube', scale=(4.5, 10, .5), position=(8, 1, -20), texture='white_cube', collider='box', color=color.brown, texture_scale=(4.5, 10))
room2_wall4 = Entity(model='cube', scale=(4.5, 10, .5), position=(2, 1, -20), texture='white_cube', collider='box', color=color.brown, texture_scale=(4.5, 10))
room2_wall5 = Entity(model='cube', scale=(1.5, 3.8, .5), position=(5, 4.1, -20), texture='white_cube', collider='box', color=color.brown, texture_scale=(1.5, 3.8))

#---Computer---
computer = Entity(position=(3, 0.85, -19.5), rotation=(0, 180, 0))
monitor = Entity(parent=computer, model='cube', scale=(1, 0.6, 0.1), color=color.dark_gray, texture='white_cube')
screen = Entity(parent=monitor, model='quad', scale=(0.9, 0.8), color=color.black, position=(0, 0, -0.06))

#---Cabinet---
cabinet = Entity(position=(7, 1, -19.5), rotation=(0, 180, 0), model='cube', texture='white_cube', scale=(1.5, 2, 0.8), color=color.rgba(150, 150, 150, 128), collider='box')
keycard_model = Entity(parent=cabinet, model='quad', scale=(0.3, 0.2), color=color.azure, position=(0, 0, -0.41), rotation=(-90, 0, 0), texture='white_cube', double_sided=True)
cabinet.keycard_model = keycard_model

#---Texts---
text = Text(text='Press Enter to start room 1!', wordwrap=20, color=color.black)
hint_1_text = 'Try stepping on the tiles and\nstarting with the cool colors before the warm ones.\nPress "o" to continue.'
try_again_text = 'Try Again!\nPress "o" to continue.'
congratulation_text = 'Congrats! The door is unlock now.\nGo to door and press "f".\nPress "o" to continue.'
room2_text = 'You are in the Lab. Find a way to open the final door.\nMaybe the computer can help.\nGo to the computer and press "e"\nthen type the password\nPress "o" to continue.'
congratulation_text_2 = 'Congrats! You Escaped!'
need_key_text = 'This door needs a rusty key!\nPress "o" to continue.'
key_collected_text = 'Key has been collected!\nGo to final door and escape!\nPress "o" to continue.'
password_success_text = 'Password correct!\nGo to the cabinet and collect Key, use "e"\nPress "o" to continue.'
password_fail_text = 'Incorrect password.\nPress "o" to continue.'

room_1_running = True
solution = [blue, green, yellow, red, purple]
stepped = []

room_2_running = False
cabinet_locked = True
player_has_key = False
is_typing_on_terminal = False
computer_on = True
correct_pass = 'RUSTY'
scrambled_pass = 'YUSRT'
terminal_ui_elements = []


def check_password():
    global cabinet_locked, terminal_ui_elements, computer_on
    player_answer = terminal_ui_elements[2].text
    if player_answer == correct_pass:
        text.text = password_success_text
        cabinet_locked = False
        computer_on = False
    else:
        text.text = password_fail_text
    exit_terminal_mode()
        
def open_door():
    door.animate_rotation((0, 0, 90), duration=1)
    door.animate_scale((0, 0, 0), duration=1)
    
def close_door():
    door.animate_rotation((0, 0, 0), duration=1)
    door.animate_scale((1.5, 2.5, 0.5), duration=1)

def open_door2():
    final_exit_door.animate_rotation((0, 0, 90), duration=1)
    final_exit_door.animate_scale((0, 0, 0), duration=1)
    
def close_door2():
    final_exit_door.animate_rotation((0, 0, 0), duration=1)    
    final_exit_door.animate_scale((1.5, 2.5, 0.5), duration=1)    
    
def start_terminal_interaction():
    global is_typing_on_terminal, terminal_ui_elements
    if is_typing_on_terminal or not room_2_running or not computer_on: return
    is_typing_on_terminal = True
    player.enabled = False
    panel = Entity(parent=camera.ui, model='quad', scale=(0.8, 0.6), color=color.black)
    prompt = Text(parent=panel, text=f"Unscramble: {scrambled_pass}\n> ", position=(-0.45, 0.1), origin=(-.5, 0), scale=1.5)
    input_text = Text(parent=panel, text="", position=(-0.3, 0.0), origin=(-.5, 0), scale=1.5)
    cursor = Entity(parent=panel, model='quad', color=color.lime, scale=(.01, .05), position=(-0.3, 0.0), origin=(-.5, 0))
    cursor.blink(duration=0.8)

    terminal_ui_elements = [panel, prompt, input_text, cursor]

def exit_terminal_mode():
    global is_typing_on_terminal, terminal_ui_elements
    if not is_typing_on_terminal: return
    
    is_typing_on_terminal = False
    player.enabled = True
    
    for element in terminal_ui_elements:
        destroy(element)
    terminal_ui_elements.clear()
    
def input(key):
    if is_typing_on_terminal:
        input_text = terminal_ui_elements[2]
        cursor = terminal_ui_elements[3]
        if key == 'escape':
            exit_terminal_mode()
        elif key == 'enter' or key == 'return':
            check_password()
        elif key == 'backspace':
            input_text.text = input_text.text[:-1]
        elif len(key) == 1:
            input_text.text += key.upper()
        return 
    if key == 'enter' and room_1_running:
        text.text = hint_1_text
    elif key == 'o':
        text.text = ''
    elif key == 'f':
        if abs(player.position.x - door.position.x) < 2 and abs(player.position.z - door.position.z) < 2 and not door_lock:
            open_door()
            door.open_time = time.time()
            if room_2_running:
                text.text = room2_text
        if distance(player, final_exit_door) < 2 and player_has_key:
            open_door2()
            final_exit_door.open_time = time.time()
            text.text = congratulation_text_2
                
def update():
    global stepped, door_lock, room_1_running, player_has_key, room_2_running, final_exit_door, key_collected_text
    if room_1_running:
        if (door.scale == Vec3(0.001, 0.001, 0.001)) and time.time() - door.open_time > 5 :
            close_door()
        for cube in solution:
            if player.intersects(cube) and cube.identifier not in stepped and room_1_running:
                if solution[len(stepped)].identifier == cube.identifier:
                    stepped.append(cube.identifier)
                else :
                    stepped = []
                    text.text = try_again_text
        if len(stepped) == 5:
            door_lock = False
            text.text = congratulation_text
            room_1_running = False
            room_2_running = True
            stepped = []
    if room_2_running:
        if not is_typing_on_terminal and distance(player, computer) < 2 and held_keys['e']:
            start_terminal_interaction()
        if not cabinet_locked and not player_has_key:
            if distance(player, cabinet) < 2 and held_keys['e']:
                text.text = key_collected_text
                player_has_key = True
        if (door.scale == Vec3(0.001, 0.001, 0.001)) and time.time() - final_exit_door.open_time > 5:
            close_door2()
        
sky = Sky()
app.run()