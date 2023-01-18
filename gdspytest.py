import gdspy

lib = gdspy.GdsLibrary(infile="M1_55.gds")
# lib.write_gds('first.gds')

cells = lib.cells
top_cell = cells['top']

mystyle = {
    (3, 0): {'fill': 'none', 'stroke': 'rgb(0, 0, 255)', 'stroke-width': '0.1'},
    (56, 0): {'fill': 'none', 'stroke': 'rgb(255, 0, 0)', 'stroke-width': '0.1'},
    (205, 0): {'fill': 'none', 'stroke': 'rgb(0, 255, 0)', 'stroke-width': '0.1'},
}

top_cell.write_svg('first.svg', style=mystyle, background="white")
