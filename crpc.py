import os
import cadquery as cq

# Width of the filter in mm. Despite being labeled 1" (25.4mm) thick they're
# really only 20mm thick
filter_width = 20
# Width of PC fan used in this build.  The fan plate will be built 1mm wider
# than this to leave a little bit of room for imperfectly sized fans.
fan_width = 80
fan_diameter = 75
fan_depth = 15
plate_width = fan_width

# Standard hole spacing for 80mm fans
fan_holes = 71.5

# Screw holes for mounting the fans to the plate
fan_screw_d = 5  # M4 (4mm) with fudge room

std_fillet = 0.8

# Thickness of the plate to build.  A 4mm one is very solid, 2mm works though
plate_depth = 4

# Begin building the plate that a fan can be mounted to.  Start with the
# basic rectangle and drill mounting holes to it.
rib_width = 4
inner_rib_depth = 18
outer_rib_depth = 10
fan_plate = (
    cq.Workplane("XY")
      .rect(plate_width, fan_width + filter_width*2 + rib_width*4)
      .extrude(plate_depth)
)

topface = fan_plate.faces(">Z")

total_y = fan_width + filter_width*2 + rib_width*4
fan_plate = (
    topface
    .center(0, total_y/2)
    .rect(plate_width, rib_width).extrude(plate_depth+outer_rib_depth)
    .center(0, -(filter_width+rib_width))
    .rect(plate_width, rib_width).extrude(plate_depth+inner_rib_depth)
    .center(0, -(fan_width+rib_width*2))
    .rect(plate_width, rib_width).extrude(plate_depth+inner_rib_depth)
    .center(0, -(filter_width+rib_width))
    .rect(plate_width, rib_width).extrude(plate_depth+outer_rib_depth)
)


fan_plate = fan_plate.faces("<Z").edges("|X").fillet(std_fillet*2)
fan_plate = (
    fan_plate
    .faces(">>Z[-2]")
    .edges("|X")
    .fillet(std_fillet)
)

fan_plate = fan_plate.faces("<Z").circle(fan_diameter/2).cutThruAll()

screw_detents = (
    cq.Workplane("XY")
    .workplane(offset=plate_depth)
    .rect(fan_holes, fan_holes, forConstruction=True)
    .vertices().sphere(fan_screw_d/3, combine=False)
)

fan_plate = fan_plate.union(screw_detents)

nub_width = 20
nub_length = 15
capture = (
    cq.Workplane("XY")
    .workplane(offset=plate_depth+fan_depth+1.0)
    .rect(fan_width-nub_length, fan_width-rib_width*2, forConstruction=True)
    .vertices()
    .rect(nub_length, nub_width).extrude(3)
)

capture = capture.edges("|Y and <Z").chamfer(1.5)

fan_plate = fan_plate.union(capture)

# Make protection plate for the fan blades
pro_depth = 2
fan_blade_protect = (
    cq.Workplane("XY")
    .circle(15).extrude(pro_depth)
)

for angle in [0, 45, 90, 135]:
    fan_blade_protect = fan_blade_protect.union(
        cq.Workplane("XY")
        .rect(fan_diameter, 3).extrude(pro_depth)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )

fan_blade_protect = fan_blade_protect.union(
    cq.Workplane("XY")
    .circle(30).extrude(pro_depth)
    .faces(">Z").circle(27).cutThruAll()
)

fan_blade_protect = fan_blade_protect.faces(">Z").edges().fillet(1.0)

fan_plate = fan_plate.union(fan_blade_protect)

# Now make a cut to lighten this up
fan_plate = fan_plate.cut(
    cq.Workplane("XY")
    .workplane(offset=plate_depth+5)
    .rect(fan_width-nub_length*2, fan_width+rib_width*4)
    .extrude(inner_rib_depth)
)

fan_plate = (
    fan_plate
    .faces(">Z")
    .edges("|X")
    .fillet(std_fillet)
)
cq.exporters.export(fan_plate, f'output/slim80_cr_fanplate_{fan_width}mm.stl')
# cq.exporters.export(fan_plate, f'output/slim80_cr_fanplate_{fan_width}mm.step')


# Create plates without a fan.  The 100mm one is easy to resize by percentage.
for nofan_width in [80, 100, 160]:
    nofan_plate = (
        cq.Workplane("XY")
          .rect(nofan_width, fan_width + filter_width*2 + rib_width*4)
          .extrude(plate_depth)
          .faces(">Z")
          .center(0, total_y/2)
          .rect(nofan_width, rib_width).extrude(plate_depth+outer_rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(nofan_width, rib_width).extrude(plate_depth+inner_rib_depth)
          .center(0, -(fan_width+rib_width*2))
          .rect(nofan_width, rib_width).extrude(plate_depth+inner_rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(nofan_width, rib_width).extrude(plate_depth+outer_rib_depth)
    )
    nofan_plate = nofan_plate.faces(">Z").edges("|X").fillet(std_fillet)
    cq.exporters.export(nofan_plate,
                        f'output/slim80_cr_nofanplate_{nofan_width}mm.stl')
    cq.exporters.export(nofan_plate,
                        f'output/slim80_cr_nofanplate_{nofan_width}mm.step')
    if nofan_width < 30:
        continue  # too small to put a hole in
    cord_hole_od = 18.5
    nut_max_od = 28
    nut_shave = (
        nofan_plate.faces("<Z")
                   .workplane(offset=2, invert=True,
                              centerOption='CenterOfMass')
                   .circle(nut_max_od/2)
                   .extrude(10, combine=False)
    )
    nofan_plate_with_hole = nofan_plate.cut(nut_shave)
    nofan_plate_with_hole = (
        nofan_plate_with_hole.faces("<Z")
                             .circle(cord_hole_od/2)
                             .cutThruAll()
    )
    cq.exporters.export(nofan_plate_with_hole,
                        f'output/slim80_cr_nofanplate_cord_hole_{nofan_width}mm.stl')
    cq.exporters.export(nofan_plate_with_hole,
                        f'output/slim80_cr_nofanplate_cord_hole_{nofan_width}mm.step')


for corner_width in [25, 30, 50, 65, 100]:
    corner_plate = (
        cq.Workplane("XY")
          .rect(corner_width, fan_width)
          .extrude(plate_depth)
          .faces(">Z")
          .center(0, total_y/2)
          .rect(corner_width, rib_width).extrude(inner_rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(corner_width-0, rib_width).extrude(inner_rib_depth)
          .center(0, -(fan_width-rib_width*2-filter_width*2))
          .rect(corner_width-0, rib_width).extrude(inner_rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(corner_width, rib_width).extrude(inner_rib_depth)
    )
    corner_plate = corner_plate.faces("<Z").edges("|X").fillet(std_fillet)
    corner_plate = corner_plate.faces(">Z").edges("|X").fillet(std_fillet)
    corner_plate = corner_plate.faces("<X").edges("|Z").fillet(std_fillet)

    corner = (
        corner_plate
        .mirror(mirrorPlane="YZ", basePointVector=(0, 0, 0))
        .rotate((0, 0, 0), (0, 1, 0), 90)
        .translate((-corner_width/2, 0, corner_width/2))
    )
    corner_plate = corner_plate.union(corner)
    cq.exporters.export(corner_plate,
                        f'output/slim80_cr_corner_{corner_width}mm.stl')
    cq.exporters.export(corner_plate,
                        f'output/slim80_cr_corner_{corner_width}mm.step')
