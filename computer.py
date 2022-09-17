import pygame
import cpu
import ram

CHARZ = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '+', '-', '@', ',', '.', ':', ';', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '"', '£', '$', '%', '^', '&', '*', '(', ')']
# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Computer:
    def __init__(self, program="test_prog.l16"):
        self.ram = ram.Ram(65536)
        self.cpu = cpu.CPU(self.ram)
        self.program = program
        self.on = False

    def load_program(self, file_name):
        self.program = file_name
        self.prog_size = self.ram.load_program(self.program)

    def update(self, screen):
        return self.tick(screen)

    def tick(self, screen):
        return self.cpu.run(screen)


class TextRectException:
    def __init__(self, message=None):
            self.message = message

    def __str__(self):
        return self.message


def multiLineSurface(string: str, font: pygame.font.Font, rect: pygame.rect.Rect, fontColour: tuple, BGColour: tuple, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Parameters
    ----------
    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rect style giving the size of the surface requested.
    fontColour - a three-byte tuple of the rgb value of the
             text color. ex (0, 0, 0) = BLACK
    BGColour - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                1 horizontally centered
                2 right-justified

    Returns
    -------
    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    finalLines = []
    requestedLines = string.splitlines()
    # Create a series of lines that will fit on the provided
    # rectangle.
    for requestedLine in requestedLines:
        if font.size(requestedLine)[0] > rect.width:
            words = requestedLine.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulatedLine = ""
            for word in words:
                testLine = accumulatedLine + word + " "
                # Build the line while the words fit.
                if font.size(testLine)[0] < rect.width:
                    accumulatedLine = testLine
                else:
                    finalLines.append(accumulatedLine)
                    accumulatedLine = word + " "
            finalLines.append(accumulatedLine)
        else:
            finalLines.append(requestedLine)

    # Let's try to write the text out on the surface.
    surface = pygame.Surface(rect.size)
    surface.fill(BGColour)
    accumulatedHeight = 0
    for line in finalLines:
        if accumulatedHeight + font.size(line)[1] >= rect.height:
             raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempSurface = font.render(line, 1, fontColour)
        if justification == 0:
            surface.blit(tempSurface, (0, accumulatedHeight))
        elif justification == 1:
            surface.blit(tempSurface, ((rect.width - tempSurface.get_width()) / 2, accumulatedHeight))
        elif justification == 2:
            surface.blit(tempSurface, (rect.width - tempSurface.get_width(), accumulatedHeight))
        else:
            raise TextRectException("Invalid justification argument: " + str(justification))
        accumulatedHeight += font.size(line)[1]
    return surface


pygame.init()

screen = pygame.display.set_mode((640, 480))


bg_col = GRAY
computer = Computer()
computer.load_program("test_prog.l16")
pygame.display.set_caption(f"Computer Running: {computer.program}")
font = pygame.font.Font('freesansbold.ttf', 24)
screen_buffer = f"LS8/16 COMPUTER (V1.01A) -- {len(computer.ram.mem) - computer.prog_size - 16} Bytes Free\n"
screen_buffer += "READY. \n"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.unicode in CHARZ:
                screen_buffer += f"{event.unicode}"
    sb = computer.update(screen)
    if sb:            
        screen_buffer += f"{sb} \n"
    screen.fill(bg_col)
    textRect = multiLineSurface(screen_buffer, font, pygame.rect.Rect(0, 0, 640, 480), BLACK, bg_col)
    screen.blit(textRect, (0, 0))
    # pixels = pygame.PixelArray(screen)
    # for i in range(100):
    #     pixels[i, i] = 0xff0000
    # pixels.close()
    pygame.display.update()

pygame.quit()