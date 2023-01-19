import cadquery as cq

filter_width = 20
fan_width = 121
fan_holes = 105

fan_screw_d = 4.07  # M4 (4mm) with fudge room

fan_plate = (
    cq.Workplane("XY")
        .rect(fan_width, fan_width + filter_width*2)
        .extrude(4)
        .rect(fan_holes, fan_holes, forConstruction=True)
        .vertices().circle(fan_screw_d/2).cutThruAll()
)

topface = fan_plate.faces(">Z")
fan_plate = fan_plate.faces(">Z").edges("not (<X or >X or <Y or >Y)").chamfer(3)


rib_width = 4
rib_depth = 15
total_y = fan_width + filter_width*2
fan_plate = (
    topface
    .center(0, total_y/2)
    .rect(fan_width, rib_width).extrude(rib_depth)
    .center(0, -(filter_width+rib_width))
    .rect(fan_width-35, rib_width).extrude(rib_depth)
    .center(0, -(fan_width-rib_width*2))
    .rect(fan_width-35, rib_width).extrude(rib_depth)
    .center(0, -(filter_width+rib_width))
    .rect(fan_width, rib_width).extrude(rib_depth)
)


fan_plate = fan_plate.faces("<Z").edges("|X").fillet(1.5)
fan_plate = fan_plate.faces(">Z").edges("|X").fillet(1.5)

screw_holes = (
    fan_plate.faces("<Z")
    .rect(fan_holes, fan_holes, forConstruction=True)
    .vertices().circle(fan_screw_d/2).extrude(10, combine=False)
)

fan_plate = fan_plate.cut(screw_holes)

fan_plate = fan_plate.faces("<Z").circle(50).cutThruAll()


nofan_width = 100
nofan_plate = (
    cq.Workplane("XY")
        .rect(100, fan_width + filter_width*2)
        .extrude(3)
        .faces(">Z")
        .center(0, total_y/2)
        .rect(nofan_width, rib_width).extrude(rib_depth)
        .center(0, -(filter_width+rib_width))
        .rect(nofan_width-0, rib_width).extrude(rib_depth)
        .center(0, -(fan_width-rib_width*2))
        .rect(nofan_width-0, rib_width).extrude(rib_depth)
        .center(0, -(filter_width+rib_width))
        .rect(nofan_width, rib_width).extrude(rib_depth)
)
nofan_plate = nofan_plate.faces("<Z").edges("|X").fillet(1.5)
nofan_plate = nofan_plate.faces(">Z").edges("|X").fillet(1.5)

corner_width = 25 + 40
corner_plate = (
    cq.Workplane("XY")
        .rect(corner_width, fan_width + filter_width*2)
        .extrude(3)
        .faces(">Z")
        .center(0, total_y/2)
        .rect(corner_width, rib_width).extrude(rib_depth)
        .center(0, -(filter_width+rib_width))
        .rect(corner_width-0, rib_width).extrude(rib_depth)
        .center(0, -(fan_width-rib_width*2))
        .rect(corner_width-0, rib_width).extrude(rib_depth)
        .center(0, -(filter_width+rib_width))
        .rect(corner_width, rib_width).extrude(rib_depth)
)
corner_plate = corner_plate.faces("<Z").edges("|X").fillet(1.5)
corner_plate = corner_plate.faces(">Z").edges("|X").fillet(1.5)
corner_plate = corner_plate.faces("<X").edges("|Z").fillet(1.5)

corner = (
    corner_plate
    .mirror(mirrorPlane="YZ", basePointVector=(0, 0, 0))
    .rotate((0, 0, 0), (0, 1, 0), 90)
    .translate((-corner_width/2, 0, corner_width/2))
)
# corner = corner.edges("<Y and <Z").fillet(1.5)
corner_plate = corner_plate.union(corner)


cq.exporters.export(fan_plate, 'output/cr_fanplate.stl')
cq.exporters.export(nofan_plate, 'output/cr_nofanplate.stl')
cq.exporters.export(corner_plate, 'output/cr_corner.stl')

cq.exporters.export(fan_plate, 'output/cr_fanplate.step')
cq.exporters.export(nofan_plate, 'output/cr_nofanplate.step')
cq.exporters.export(corner_plate, 'output/cr_corner.step')