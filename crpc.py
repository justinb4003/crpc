import cadquery as cq

# Width of the filter in mm. Despite being labeled 1" (25.4mm) thick they're
# really only 20mm thick
filter_width = 20
# Width of PC fan used in this build.  The fan plate will be built 1mm wider
# than this to leave a little bit of room for imperfectly sized fans.
fan_width = 120
plate_width = fan_width + 25
# Standard hole spacing for 120mm fans
fan_holes = 105
# Screw holes for mounting the fans to the plate
fan_screw_d = 5  # M4 (4mm) with fudge room

std_fillet = 1.2

# Thickness of the plate to build.  A 4mm one is very solid, 2mm works though
plate_depth = 4

# Begin building the plate that a fan can be mounted to.  Start with the
# basic rectangle and drill mounting holes to it.
fan_plate = (
    cq.Workplane("XY")
      .rect(plate_width, fan_width)
      .extrude(plate_depth)
      .rect(fan_holes, fan_holes, forConstruction=True)
      .vertices().circle(fan_screw_d/2).cutThruAll()
)

topface = fan_plate.faces(">Z")
fan_plate = (
    fan_plate
    .faces(">Z")
    .edges("not (<X or >X or <Y or >Y)")
    .chamfer(1.5)
)

rib_width = 4
rib_depth = 15
total_y = fan_width
fan_plate = (
    topface
    .center(0, total_y/2)
    .rect(plate_width, rib_width).extrude(rib_depth)
    .center(0, -(filter_width+rib_width))
    .rect(plate_width, rib_width).extrude(rib_depth)
    .center(0, -(fan_width-(filter_width+rib_width)))
    .rect(plate_width, rib_width).extrude(rib_depth)
    .center(0, (filter_width+rib_width))
    .rect(plate_width, rib_width).extrude(rib_depth)
)


fan_plate = fan_plate.faces("<Z").edges("|X").fillet(std_fillet)
fan_plate = fan_plate.faces(">Z").edges("|X").fillet(std_fillet)

screw_holes = (
    fan_plate.faces("<Z")
    .rect(fan_holes, fan_holes, forConstruction=True)
    .vertices().circle(fan_screw_d/2).extrude(10, combine=False)
)

fan_plate = fan_plate.cut(screw_holes)

fan_plate = fan_plate.faces("<Z").circle(58).cutThruAll()
cq.exporters.export(fan_plate, f'output/slim_cr_fanplate_{fan_width}mm.stl')
cq.exporters.export(fan_plate, f'output/slim_cr_fanplate_{fan_width}mm.step')


# Create plates without a fan.  The 100mm one is easy to resize by percentage.
for nofan_width in [20]:
    nofan_plate = (
        cq.Workplane("XY")
          .rect(nofan_width, fan_width)
          .extrude(plate_depth)
          .faces(">Z")
          .center(0, total_y/2)
          .rect(nofan_width, rib_width).extrude(rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(nofan_width-0, rib_width).extrude(rib_depth)
          .center(0, -(fan_width-(filter_width+rib_width)))
          .rect(nofan_width-0, rib_width).extrude(rib_depth)
          .center(0, (filter_width+rib_width))
          .rect(nofan_width, rib_width).extrude(rib_depth)
    )
    nofan_plate = nofan_plate.faces("<Z").edges("|X").fillet(std_fillet)
    nofan_plate = nofan_plate.faces(">Z").edges("|X").fillet(std_fillet)
    cq.exporters.export(nofan_plate,
                        f'output/slim_cr_nofanplate_{nofan_width}mm.stl')
    cq.exporters.export(nofan_plate,
                        f'output/slim_cr_nofanplate_{nofan_width}mm.step')
    """
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
                        f'output/slim_cr_nofanplate_cord_hole_{nofan_width}mm.stl')
    cq.exporters.export(nofan_plate_with_hole,
                        f'output/slim_cr_nofanplate_cord_hole_{nofan_width}mm.step')
    """


for corner_width in [25, 37, 50, 65, 100]:
    corner_plate = (
        cq.Workplane("XY")
          .rect(corner_width, fan_width)
          .extrude(plate_depth)
          .faces(">Z")
          .center(0, total_y/2)
          .rect(corner_width, rib_width).extrude(rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(corner_width-0, rib_width).extrude(rib_depth)
          .center(0, -(fan_width-rib_width*2-filter_width*2))
          .rect(corner_width-0, rib_width).extrude(rib_depth)
          .center(0, -(filter_width+rib_width))
          .rect(corner_width, rib_width).extrude(rib_depth)
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
                        f'output/slim_cr_corner_{corner_width}mm.stl')
    cq.exporters.export(corner_plate,
                        f'output/slim_cr_corner_{corner_width}mm.step')
