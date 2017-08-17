""" BlueSky: The open-source ATM simulator."""
# from bluesky import settings  #, stack, tools
from bluesky import settings
from bluesky.traf import traffic
import bluesky.navdb as _navdb

if settings.gui == 'pygame':
    import bluesky.ui.pygame.screen as _scr
    import bluesky.sim.pygame.simulation as _sim
else:
    import bluesky.sim.qtgl.screenio as _scr
    import bluesky.sim.qtgl.simulation as _sim

# Main singleton objects in BlueSky
traf = traffic.Traffic()
navdb = _navdb.navdb
sim = _sim.sim
scr = _scr.scr
