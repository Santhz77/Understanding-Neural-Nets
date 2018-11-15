from pynput import keyboard

# This function keeps listening for any keyboard input and takes actions defined in on_press/on_releast functions
def listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# This function gets called when user presses any keyboard key
def on_press(key):
    global isEscape, sp, counter1, counter2
    # Pressing 'UP arrow key' will initiate saving provided capture region images
    if key == keyboard.Key.up:
        img = sp.capture()
        counter1 = sp.saveROIImg("jump", img, counter1)

    # Pressing 'Right arrow key' will initiate saving provided capture region images
    if key == keyboard.Key.right:
        img = sp.capture()
        counter2 = sp.saveROIImg("nojump", img, counter2)

# This function gets called when user releases the keyboard key previously pressed
def on_release(key):
    global isEscape, sp, counter1
    if key == keyboard.Key.esc:
        isEscape = True
        # Stop listener
        return False

# Object that is used to capture the screenshot
class ScreenCapture(object):
    numOfSamples = 300

    @classmethod
    def capture(self):
        # The Snapshot Region size is hard coded, please change it
        # based on the setting of your display window.
        # It actually took a bit of trial and error t arrive the bbox # in my case - should be a way to automate
        X1 = 380
        Y1 = 150
        X2 = 800
        Y2 = 300

        im=ImageGrab.grab(bbox=(X1,Y1,X2,Y2))
        if im.width % 2 > 0:
            # Capture region should be even sized else # you will see wrongly strided images i.e corrupted
            emsg = "Capture region width should be even (was %s)" % (region.size.width)
            raise ValueError(emsg)

        # Get width/height of image
        self.width = im.width
        self.height = im.height
        return im


    @classmethod
    def saveROIImg(self, name, img, counter):
        if counter <= self.numOfSamples:
            counter = counter + 1
            name = name + str(counter)

            print(counter, name)
            print("Saving img:",name)
            img.save("imgages-folder/"+name + ".png")
            return counter


import pyscreenshot as ImageGrab

if __name__ == "__main__":
    global isEscape, sp, counter1, counter2
    sp = ScreenCapture()
    counter1 = 0
    counter2 = 0
    listen()
