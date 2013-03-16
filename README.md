Motherly Instinct

Made during a 24 hour RPI Game Dev Club Game Jam, 10/27/2012 - 10/28/2012
Made under the themes of Surprise and Suspense
Polished over the next two weeks (added instruction screen, pausing, 
    curved webs, arcade cabinet controls, built into .exe)

Description
    An endless arcade game. Your goal is to defend your eggs from ravenous ants. 
    Last as long as possible by weaving webs and eating ants which they trap. 
    Ration your webs and venom for when the ants break through. 
    As part of the surprise and suspense themes, the timer displayed to you
        may not always be accurate.
    
Design Challenges
    Challenge
        - Design an Ant AI that led to interesting gameplay
    Resolution
        - Ants randomly choose between moving towards a target egg 
          (accelerate towards, not move directly towards) and wandering 
          towards a random point on the screen
        
    Challenge
        - Create feelings of surprise and suspense for the game jam themes
    Resolution
        - There is suspense in building up defenses and waiting for ants
          to arrive. There is surprise when ants break through webs or arrive
          before the timer indicates.
        
Technical Challenges
    Challenge
        - Link all nearby nodes with curves and detect when an ant collides 
          with any curve efficiently
    Resolution
        - Bezier curves built with points (number of points proportional 
          to the distance between the nodes) link nodes. Collision is tested
          by comparing the distance from an ant's center to the center of 
          any nearby points on such a curve.

To run on Windows 64 bit,
    run 'Motherly Instinct.exe'

To run from source, 
    install python 2.7 - 2.7.3 
        ( http://www.python.org/download/releases/2.7.3/ )
    install pygame 1.9.1 - 1.9.2 (be sure to install the py2.7 version)
        ( http://www.pygame.org/download.shtml )
    run with 'python main.py'

Controls
    Move with the arrow keys or WASD
    Place webs with Z
    Eat ants that are trapped in webs with X
    Enter your initials for the highscores with the arrow keys or WASD 
        and submit with ENTER
    Quit with ESC
    
Credits
    Scott Todd (todds@rpi.edu) - Lead programmer
    Brian Tam (tamb@rpi.edu) - Artist and HUD Programmer
    Ronald Sardarian (sardar@rpi.edu) - Programmer
    
    Bombadeer studios - Music
    http://www.freesfx.co.uk - Sound Effects
    