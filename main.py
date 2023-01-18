import numpy as np

from gdshelpers.geometry.chip import Cell
from gdshelpers.parts.waveguide import Waveguide
from gdshelpers.parts.coupler import GratingCoupler
from gdshelpers.parts.resonator import RingResonator
from gdshelpers.parts.splitter import Splitter
from gdshelpers.parts.logo import KITLogo, WWULogo
from gdshelpers.parts.optical_codes import QRCode
from gdshelpers.parts.text import Text
from gdshelpers.parts.marker import CrossMarker

# Generate a coupler with parameters from the coupler database
coupler1 = GratingCoupler.make_traditional_coupler_from_database([0, 0], 1, 'sn330', 1550)
coupler2 = GratingCoupler.make_traditional_coupler_from_database([150, 0], 1, 'sn330', 1550)

coupler1_desc = coupler1.get_description_text(side='left')
coupler2_desc = coupler2.get_description_text(side='right')

# And add a simple waveguide to it
wg1 = Waveguide.make_at_port(coupler1.port)
wg1.add_straight_segment(10)
wg1.add_bend(-np.pi/2, 10, final_width=1.5)

res = RingResonator.make_at_port(wg1.current_port, gap=0.1, radius=20,
                                 race_length=10, res_wg_width=0.5)

wg2 = Waveguide.make_at_port(res.port)
wg2.add_straight_segment(30)
splitter = Splitter.make_at_root_port(wg2.current_port, total_length=20, sep=10, wg_width_branches=1.0)

wg3 = Waveguide.make_at_port(splitter.right_branch_port)
wg3.add_route_single_circle_to_port(coupler2.port)

# Add a marker just for fun
marker = CrossMarker.make_traditional_paddle_markers(res.center_coordinates)

# The fancy stuff
kit_logo = KITLogo([25, 0], 10)
wwu_logo = WWULogo([100, 30], 30, 2)
qr_code = QRCode([25, -40], 'https://www.uni-muenster.de/Physik.PI/Pernice', 1.0)
dev_label = Text([100, 0], 10, 'A0', alignment='center-top')

# Create a Cell to hold the objects
cell = Cell('EXAMPLE')

# Convert parts to gdsCAD polygons
cell.add_to_layer(1, coupler1, wg1, res, wg2, splitter, wg3, coupler2)
cell.add_to_layer(2, wwu_logo, kit_logo, qr_code, dev_label)
cell.add_to_layer(2, marker)
cell.add_to_layer(3, coupler1_desc, coupler2_desc)
cell.show()
