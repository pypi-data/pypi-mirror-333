import os
import msvcrt
import platform
import random

goodbye = [
    "Catch you later, alligator!",
    "Don’t let the door hit you on the way out… unless you’re into that.",
    "See you in the funny papers!",
    "Until we meet again… or until you hit ‘Exit’ again.",
    "Bye now, or should I say… ‘adios amigo!’",
    "You came, you saw, you clicked ‘exit’.",
    "Take care, don’t break anything!",
    "Remember, this isn’t goodbye, it’s just ‘until the next update’!",
    "I’ll be here, but you won’t… oh well.",
    "Don’t go chasing any wild errors!",
    "Time’s up, but don’t worry, I’ll still be here when you come back.",
    "Alright, take a break and don’t do anything I wouldn’t do.",
    "Exit stage left. Cue dramatic music.",
    "Go on, leave! I’ll still be running in the background.",
    "Off you go, you little adventure!",
    "Leaving already? Well, it was nice knowing you… for the past 5 minutes.",
    "You're leaving? But we were just getting started!",
    "Alright, that’s enough of me for one day. Have a good one!",
    "Goodbye and good riddance! (Kidding, come back soon!)",
    "Time to close the program. It was a wild ride.",
    "Peace out! Don’t let your battery die on the way out.",
    "Goodbye! May your future be bug-free.",
    "Catch you on the flip side, or whenever you reopen the app.",
    "See you later, you magnificent coding genius.",
    "It’s been real. See you on the other side of the monitor.",
    "Exit? More like a well-deserved vacation for you.",
    "So long, and thanks for all the data!",
    "Don’t let the bugs bite… unless they’re part of your debugging process.",
    "Adieu, my digital friend!",
    "Goodbye, and remember: your code will always remember you.",
    "That’s all folks! For now...",
    "Go and enjoy the real world! It’s probably less buggy.",
    "You’ve been an awesome user! Now go live your best life!",
    "The program is over, but your journey isn’t!",
    "It’s not you, it’s me… okay, maybe it’s you.",
    "Well, that was fun. Let’s never do that again… unless you want to.",
    "Closing time! You don’t have to go home, but you can’t stay here.",
    "See you in the next release!",
    "Goodbye! May your hard drive always be spacious.",
    "Houston we have a problem!",
    "No more buttons to press! It's time for a break.",
    "You’ve earned yourself a logout! Enjoy it.",
    "Time’s up! But hey, you can always come back for more fun!",
    "You survived! Now go get a cookie.",
    "Take care, don't forget your session cookies!",
    "Goodbye, my friend. Until we meet again… hopefully with fewer errors.",
    "Hope you enjoyed the ride! Now get out of here!",
    "Time to peace out like a cool hacker.",
    "You clicked exit… but it’s not over. I’m always lurking.",
    "Don’t let the program crash while you’re gone!",
    "Closing the doors… but only for now. You’ll be back.",
    "That’s a wrap! See you next time.",
    "Your session has ended, but don’t worry, I’ll wait for your return!",
    "So long, and thanks for all the clicks!",
    "Exit button pressed… now go live your life!",
    "And just like that, you’re gone. See ya later, space cowboy.",
]

COLOR_RESET = "\033[0m"
COLOR_SELECTED = "\033[1;32m"  
COLOR_UNSELECTED = "\033[0;37m"  
COLOR_PROMPT = "\033[1;34m"  
COLOR_EXIT = "\033[1;31m"  
COLOR_MARKED = "\033[1;33m"  

def get_terminal_height():
    current_os = platform.system().lower()

    if current_os == 'windows':
        size = os.get_terminal_size()
        return size.lines
    elif current_os in ['linux', 'darwin']:
        try:
            size = os.popen('stty size', 'r').read().split()
            return int(size[0])
        except Exception as e:
            print(f"Error getting terminal size: {e}")
            return 20  
    else:
        print(f"Unsupported OS: {current_os}")
        return 20

def selecto(options, funny_exit_message=True, select_multiple=False, multi_index_jump=5):
    if not options:
        print("I don't know chief, that list be looking kinda empty.")
        return None

    multi_index_jump = max(1, min(multi_index_jump, len(options)//2))

    selected_items = set()

    def draw_menu(selected_idx, term_height):
        os.system('cls' if os.name == 'nt' else 'clear')

        max_visible_items = term_height - 6  

        if selected_idx < max_visible_items // 2:
            start_idx = 0
        else:
            start_idx = selected_idx - (max_visible_items // 2)

        end_idx = min(len(options), start_idx + max_visible_items)

        if end_idx == len(options):
            start_idx = max(0, len(options) - max_visible_items)

        for idx in range(start_idx, end_idx):

            if select_multiple:
                selected = "x" if idx in selected_items else " "

                if idx == selected_idx:

                    print(f"{COLOR_SELECTED}> [{COLOR_MARKED}{selected}{COLOR_RESET}{COLOR_SELECTED}] {options[idx]}{COLOR_RESET}")
                else:

                    print(f" {COLOR_MARKED if idx in selected_items else COLOR_UNSELECTED} [{selected}] {options[idx]}{COLOR_RESET}")
            else:

                if idx == selected_idx:
                    print(f"{COLOR_SELECTED}> {COLOR_RESET}{COLOR_SELECTED}{options[idx]}{COLOR_RESET}")
                else:
                    print(f"{COLOR_UNSELECTED}  {options[idx]}{COLOR_RESET}")

        print(f"\n{COLOR_PROMPT}Item {selected_idx + 1} of {len(options)}{COLOR_RESET}")

        if select_multiple:
            print(f"{COLOR_PROMPT}Press 'Q'  to exit, 'Space' to toggle selection, 'Enter' to confirm selection(s).{COLOR_RESET}")
        else:
            print(f"{COLOR_PROMPT}Press 'Q'  to exit, 'Enter' to confirm selection.{COLOR_RESET}")

    def menu():
        selected_idx = 0
        term_height = get_terminal_height()

        while True:
            draw_menu(selected_idx, term_height)
            key = msvcrt.getch()

            if key in (b'\xe0', b'\x0e'):  
                key = msvcrt.getch()
                if key == b'H' and selected_idx > 0:  
                    selected_idx -= 1
                elif key == b'P' and selected_idx < len(options) - 1:
                    selected_idx += 1
                elif key == b'K':  
                    selected_idx = max(0, selected_idx - multi_index_jump)  
                elif key == b'M':  
                    selected_idx = min(len(options) - 1, selected_idx + multi_index_jump)  

            elif key == b' ' and select_multiple:  
                if selected_idx in selected_items:
                    selected_items.remove(selected_idx)
                else:
                    selected_items.add(selected_idx)
            elif key == b'\r':  
                if select_multiple:
                    return sorted(list(selected_items))  
                else:
                    return selected_idx  
            elif key.lower() == b'q':  
                if funny_exit_message:
                    print(f"{COLOR_EXIT}{random.choice(goodbye)}{COLOR_RESET}")
                    return None
                else:
                    print(f"{COLOR_EXIT}Exiting...{COLOR_RESET}")
                    return None

    return menu()