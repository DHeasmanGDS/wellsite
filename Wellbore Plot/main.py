"""
Author: Drew Heasman, heasman.drew@gmail.com for questions or suggestions

Description: A bokeh implimentation of the excel wellbore plot typically
used by oil companies drilling in Western Canada.

ToDo:  
    - Create a header
    - Allow for user input
    - Print a pdf, png,
    - Calculate a dip on structure.
    - move points freely, add inflections
    - check for uses on completions
"""

import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column
from bokeh.models import Range1d, LinearAxis, ColumnDataSource

# Importing Data
dhp = pd.read_csv('surveys.txt', sep='\t')
gamma = pd.read_csv('gamma.txt', sep='\t')
rop_gas = pd.read_csv('rop_gas.txt', sep='\t')
tops = pd.read_csv('tops.txt', sep='\t')
prev_well = pd.read_csv('Previous Well.txt', sep='\t')

# Adding and transforming feature data
gamma['rol20'] = gamma['Gamma'].rolling(window=20).mean()
rop_gas['gasrol30'] = rop_gas['Gas'].rolling(window=10).mean()
rop_gas['roprol30'] = rop_gas['ROP'].rolling(window=30).mean()
dhp['TVD'] = -dhp['TVD']
prev_well['TVD'] = -prev_well['TVD']
tops['TVDtop'] = -tops['TVDtop']
tops['TVDpath'] = -tops['TVDpath']
tops['TVDbtm'] = -tops['TVDbtm']

# Set variables
fig_width = 2000
fig_height = 350
kb_elev = 1224.70
y_btm, y_top = -2070,-2145
sub_top = kb_elev + y_top
sub_btm = kb_elev + y_btm
gasmax = 1500

# Set output file
output_file("wellbore.html")

dh_source = ColumnDataSource(dhp)

TOOLTIPS = [
    ("Measured Depth: ", "@{x}{0,0.00}"),
    ("Total Vertical Depth: ", "@{y}{0,0.00}"),
]

# Main wellbore plot
p1 = figure(title="Wellbore Plot",
           y_axis_label='Total Vertical Depth (m)',
           width=fig_width,
           plot_height=fig_height,
           toolbar_location="left",
           toolbar_sticky=False,
           y_range=[y_top,y_btm],
           tooltips=TOOLTIPS,
           tools=['pan,box_zoom,crosshair,hover,reset']
           )
p1.toolbar.logo = None

# Set subsea y-range on right side
p1.extra_y_ranges['Subsea'] = Range1d(start=sub_top, end=sub_btm)
p1.add_layout(LinearAxis(y_range_name='Subsea', axis_label='Subsea (m)'), 'right')

# Plot Drillhole path
p1.line(dhp['MD'], dhp['TVD'],
       legend_label="Drill hole path",
       line_width=2,
       )
p1.circle(dhp['MD'], dhp['TVD'],
         legend_label='Drill hole path',
         fill_color='black',
         size=5)

# Plot Previous wellpath
p1.line(prev_well['MD'], prev_well['TVD'],
        legend_label="Previous Well Path",
        line_width=2,
        alpha = 0.2,
        color='grey',
        )
p1.circle(prev_well['MD'], prev_well['TVD'],
          legend_label="Previous Well Path",
          fill_color="grey",
          size=5,
          alpha=0.2)

# Plot top, windowtop, and windowbottom
p1.line(tops['MD'], tops['TVDtop'],
        legend_label="CSs top",
        line_width=2,
        color='red')
p1.line(tops['MD'], tops['TVDpath'],
        legend_label="Window Top",
        line_width=2,
        color='purple')
p1.line(tops['MD'], tops['TVDbtm'],
        legend_label="Window Bottom",
        line_width=2,
        color='blue')

# Plot ROP and Gas figure
p2 = figure(title="ROP and Gas",
           y_axis_label='ROP',
           width=fig_width,
           plot_height=200,
           x_range=p1.x_range,
           tools = "xpan"
          )
p2.toolbar.logo = None
p2.toolbar_location = None

# Set ROP axis data
p2.yaxis.axis_label = 'ROP (min/m)'
p2.y_range = Range1d(start=0, end=15)

# Plot ROP
p2.line(rop_gas['Depth'], rop_gas['roprol30'],
       legend_label="",
       line_width=2,
       color='green'
       )

# Set Gas axis data
p2.extra_y_ranges['Gas'] = Range1d(start=0, end=gasmax)
p2.add_layout(LinearAxis(y_range_name='Gas', axis_label='Gas (units)'), 'right')

# Plot Gas
p2.line(rop_gas['Depth'], rop_gas['gasrol30'],
        legend_label="",
        line_width=2,
        color='red',
        y_range_name='Gas'
        )

# Plot Gamma figure
p3 = figure(title="Gamma",
           x_axis_label='Measured Depth (meters)',
           y_axis_label='Gamma (cps)',
           width=fig_width,
           plot_height=200,
           x_range=p1.x_range,
           y_range=[0,150],
           tools = "xpan"
           )
p3.toolbar.logo = None
p3.toolbar_location = None

# Plot gamma axis
p3.extra_y_ranges['Gamma'] = Range1d(start=0, end=150)
p3.add_layout(LinearAxis(y_range_name='Gamma', axis_label='Gamma (cps)'), 'right')

# Plot 75 gamma api line
p3.line(gamma['Depth'], 75,
        legend_label="",
        line_width=1,
        color='green'
        )

# Plot gamma
p3.line(gamma['Depth'], gamma['rol20'],
       legend_label="",
       line_width=2,
       color='blue'
       )

# Show html file
layout = column(p1,p2,p3)
show(layout)
