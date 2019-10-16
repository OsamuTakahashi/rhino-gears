from __future__ import division
import rhinoscriptsyntax as rs
from helpers import generate_gear_crv_with_outside, generate_pitch_circle_crv

__commandname__ = "InvoluteGearIn"


params = {
    "n":  30,
    "r":  10,
    "m":  1,
    "pa": 20,
    "pc": False
}


def RunCommand(is_interactive):
    global params

    center = rs.GetPoint(message="Select center point")

    n = rs.GetInteger(message="Number of teeth",
                      number=params["n"], minimum=4)

    r = rs.GetReal(message="Outside Diameter",
                      number=params["r"])

    m = rs.GetReal(message="Gear module",
                   number=params["m"])

    pa = rs.GetReal(message="Pressure angle",
                    number=params["pa"], minimum=0, maximum=45)

    bool_opts = rs.GetBoolean(message="Output options",
                              items=(("PitchCircle", "No", "Yes"),),
                              defaults=(params["pc"],))

    if None in [center, n, m, pa, bool_opts]:
        return 1  # Cancel

    pc = bool_opts[0]

    params["n"] = n
    params["m"] = m
    params["r"] = r
    params["pa"] = pa
    params["pc"] = pc

    cplane = rs.ViewCPlane()  # Get current CPlane
    cplane = rs.MovePlane(cplane, center)
    xform = rs.XformChangeBasis(cplane, rs.WorldXYPlane())

    rs.EnableRedraw(False)
    old_plane = rs.ViewCPlane(plane=rs.WorldXYPlane())

    gear = generate_gear_crv_with_outside(teeth=params["n"],
                             module=params["m"],
                             outside_diam=params["r"],
                             pressure_angle=params["pa"])

    rs.ViewCPlane(plane=old_plane)
    rs.TransformObjects(gear, xform)

    rs.EnableRedraw(True)

    if pc:
        circle = generate_pitch_circle_crv(teeth=params["n"],
                                           module=params["m"])
        rs.TransformObjects(circle, xform)
        rs.SelectObjects([gear, circle])
    else:
        rs.SelectObjects(gear)

    return 0  # Success


if __name__ == "__main__":
    RunCommand(True)
