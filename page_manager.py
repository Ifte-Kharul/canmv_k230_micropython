import lvgl as lv

history = []
current_page = None  # Global variable to track current page

def init(first_page):
    global current_page

    if current_page:
        lv.obj_del(current_page)  # Delete previous page if it exists
        history.clear()  # Clear navigation history

    current_page = first_page  # Set current page
    print("First page loaded:", first_page)
    lv.scr_load(first_page)  # Load first page

def load_page(new_page, animation=lv.SCR_LOAD_ANIM.MOVE_LEFT):
    global current_page

    if current_page:
        print(f"Switching from {current_page} to {new_page}")
        history.append(current_page)  # Save the current page in history
        print("Added to history:", history)

        lv.scr_load_anim(new_page, animation, 300, 0, False)
        current_page = new_page  # Update current page reference
    else:
        print("No current page, loading first page.")
        lv.scr_load_anim(new_page, animation, 300, 0, False)
        current_page = new_page

def go_back(animation=lv.SCR_LOAD_ANIM.MOVE_RIGHT):
    global current_page

    if history:
        previous_page = history.pop()  # Get the last page
        print(f"Going back from {current_page} to {previous_page}")

        lv.scr_load_anim(previous_page, animation, 300, 0, False)
        current_page = previous_page  # Update current page reference
    else:
        print("History is empty, cannot go back.")
