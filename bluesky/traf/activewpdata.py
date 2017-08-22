import numpy as np
import bluesky as bs
from bluesky.tools.dynamicarrays import DynamicArrays, \
    RegisterElementParameters
from bluesky.tools.aero import nm, g0
from bluesky.tools.misc import degto180


class ActiveWaypoint(DynamicArrays):
    def __init__(self):
        with RegisterElementParameters(self):
            # Active WP latitude
            self.lat = np.array([])
            # Active WP longitude
            self.lon = np.array([])
            # Active WP altitude to arrive at
            self.alt = np.array([])
            # Active WP speed
            self.spd = np.array([])
            # Active vertical speed to use
            self.vs = np.array([])
            # Distance when to turn to next waypoint
            self.turndist = np.array([])
            # Distance when to turn to next waypoint
            self.flyby = np.array([])
            # Bearing next leg
            self.next_qdr = np.array([])

    def create(self, n=1):
        super(ActiveWaypoint, self).create(n)
        # LNAV route navigation

        # Active WP latitude
        self.lat[-n:] = 89.99
        # Active WP speed
        self.spd[-n:] = -999.
        # Distance to active waypoint where to turn
        self.turndist[-n:] = 1.0
        # Flyby/fly-over switch
        self.flyby[-n:] = 1.0
        # bearing next leg
        self.next_qdr[-n:] = -999.0

    def reached(self, qdr, dist, flyby):
        # Calculate distance before waypoint where to start the turn
        # Turn radius:      R = V2 / tan phi . g
        # Distance to turn: wpturn = R * tan (1/2 delhdg) but max 4 times
        # radius using default bank angle per flight phase

        # use .eps to avoid divide by zero
        # [nm]
        turnrad = bs.traf.tas * bs.traf.tas / \
                      np.maximum(bs.traf.eps, np.tan(bs.traf.bank) * g0 * nm)

        next_qdr = np.where(self.next_qdr < -900., qdr, self.next_qdr)

        # Avoid circling
        # away = np.abs(degto180(bs.traf.trk - next_qdr)+180.)>90.
        away = np.abs(degto180(bs.traf.trk - next_qdr)) > 90.
        incircle = dist < turnrad * 1.01
        circling = away * incircle

        # distance to turn initialisation point
        angle = np.abs(degto180(qdr % 360. - next_qdr % 360.))
        self.turndist = (flyby < 0.5) * \
            np.minimum(100., np.abs(turnrad * np.tan(np.radians(0.5 * angle))))

        # Check whether shift based dist [nm] is required, set closer
        # than WP turn distanc
        return np.where(bs.traf.swlnav * ((dist < self.turndist) + circling))[0]
