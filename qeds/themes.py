COLOR_CYCLE = [
    "#165aa7",  # logo blue
    "#cb495c",  # logo red
    "#fec630",  # logo yellow
    "#bb60d5",  # pink
    "#f47915",  # orange
    "#06ab54",  # logo green
    "#002070",  # dark blue
    "#b27d12",  # dark yellow
    "#007030",  # dark green
]

TEXT_COLOR = "#444444"
BORDER_COLOR = "#e1e1e1"
PLOT_BGCOLOR = "#efefef"
PAPER_BGCOLOR = "#f7f7f7"


def mpl_style():
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    rcp = mpl.RcParams()
    rcp["axes.facecolor"] = PLOT_BGCOLOR
    rcp["figure.facecolor"] = PAPER_BGCOLOR

    # ticks
    for xy in ["x", "y"]:
        rcp[f'{xy}tick.color'] = TEXT_COLOR
        rcp[f'{xy}tick.direction'] = "out"
        rcp[f'{xy}tick.major.size'] = 10

    rcp["axes.spines.top"] = False
    rcp["axes.spines.right"] = False
    rcp["axes.grid"] = True
    rcp["grid.color"] = BORDER_COLOR
    rcp["grid.alpha"] = 0.9
    rcp["grid.linewidth"] = 1.0
    rcp["axes.linewidth"] = 2.0
    rcp["axes.edgecolor"] = BORDER_COLOR
    rcp["lines.color"] = BORDER_COLOR
    rcp['axes.prop_cycle'] = mpl.rcsetup.cycler('color', COLOR_CYCLE)

    # fonts and text
    rcp["font.family"] = ["Source Sans Pro", "DejaVu Sans"]
    rcp["font.size"] = 14
    rcp["text.color"] = TEXT_COLOR
    rcp['axes.labelcolor'] = TEXT_COLOR
    rcp['axes.titlesize'] = 'x-large'
    rcp['axes.labelsize'] = 'large'
    
    plt.style.library["qeds"] = rcp
    plt.style.reload_library()
    plt.style.use("qeds")

    return rcp


def plotly_template():
    import plotly.graph_objects as go
    import plotly.io as pio

    template = go.Layout.Template(
        {
            'data': {
                'bar': [
                    {
                        'error_x': {
                            'color': '#444444'
                        },
                        'error_y': {
                            'color': '#444444'
                        },
                        'marker': {
                            'line': {
                                'color': '#efefef',
                                'width': 0.5
                            }
                        },
                        'type': 'bar'
                    }
                ],
                'barpolar': [
                    {
                        'marker': {
                            'line': {
                                'color': '#efefef',
                                'width': 0.5
                            }
                        },
                        'type': 'barpolar'
                    }
                ],
                'carpet': [
                    {
                        'aaxis': {
                            'endlinecolor': '#444444',
                            'gridcolor': 'white',
                            'linecolor': 'white',
                            'minorgridcolor': 'white',
                            'startlinecolor': '#444444'
                        },
                        'baxis': {
                            'endlinecolor': '#444444',
                            'gridcolor': 'white',
                            'linecolor': 'white',
                            'minorgridcolor': 'white',
                            'startlinecolor': '#444444'
                        },
                        'type': 'carpet'
                    }
                ],
                'choropleth': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'type': 'choropleth'
                    }
                ],
                'contour': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'colorscale': [[0, '#035f2f'], [1, '#c7fde0']],
                        'type': 'contour'
                    }
                ],
                'contourcarpet': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'type': 'contourcarpet'
                    }
                ],
                'heatmap': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'colorscale': [[0, '#035f2f'], [1, '#c7fde0']],
                        'type': 'heatmap'
                    }
                ],
                'heatmapgl': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'colorscale': [[0, '#035f2f'], [1, '#c7fde0']],
                        'type': 'heatmapgl'
                    }
                ],
                'histogram': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'histogram'
                    }
                ],
                'histogram2d': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'colorscale': [[0, '#035f2f'], [1, '#c7fde0']],
                        'type': 'histogram2d'
                    }
                ],
                'histogram2dcontour': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'colorscale': [[0, '#035f2f'], [1, '#c7fde0']],
                        'type': 'histogram2dcontour'
                    }
                ],
                'mesh3d': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'type': 'mesh3d'
                    }
                ],
                'parcoords': [
                    {
                        'line': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'parcoords'
                    }
                ],
                'scatter': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scatter'
                    }
                ],
                'scatter3d': [
                    {
                        'line': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scatter3d'
                    }
                ],
                'scattercarpet': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scattercarpet'
                    }
                ],
                'scattergeo': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scattergeo'
                    }
                ],
                'scattergl': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scattergl'
                    }
                ],
                'scattermapbox': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scattermapbox'
                    }
                ],
                'scatterpolar': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scatterpolar'
                    }
                ],
                'scatterpolargl': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scatterpolargl'
                    }
                ],
                'scatterternary': [
                    {
                        'marker': {
                            'colorbar': {
                                'outlinewidth': 0,
                                'tickcolor': 'rgb(237,237,237)',
                                'ticklen': 6,
                                'ticks': 'inside'
                            }
                        },
                        'type': 'scatterternary'
                    }
                ],
                'surface': [
                    {
                        'colorbar': {
                            'outlinewidth': 0,
                            'tickcolor': 'rgb(237,237,237)',
                            'ticklen': 6,
                            'ticks': 'inside'
                        },
                        'colorscale': [[0, '#035f2f'], [1, '#c7fde0']],
                        'type': 'surface'
                    }
                ],
                'table': [
                    {
                        'cells': {
                            'fill': {
                                'color': '#efefef'
                            },
                            'line': {
                                'color': '#e1e1e1'
                            }
                        },
                        'header': {
                            'fill': {
                                'color': '#f7f7f7'
                            },
                            'line': {
                                'color': '#e1e1e1'
                            }
                        },
                        'type': 'table'
                    }
                ]
            },
            'layout': {
                'annotationdefaults': {
                    'arrowhead': 0,
                    'arrowwidth': 1
                },
                'colorscale': {
                    'sequential': [[0, '#035f2f'], [1, '#c7fde0']],
                    'sequentialminus': [[0, '#035f2f'], [1, '#c7fde0']]
                },
                'colorway': [
                    '#165aa7', '#cb495c', '#fec630', '#bb60d5', '#f47915',
                    '#06ab54', '#002070', '#b27d12', '#007030'
                ],
                'font': {
                    'color': '#444444'
                },
                'geo': {
                    'bgcolor': '#f7f7f7',
                    'lakecolor': '#f7f7f7',
                    'landcolor': '#efefef',
                    'showlakes': True,
                    'showland': True,
                    'subunitcolor': 'white'
                },
                'hoverlabel': {
                    'align': 'left'
                },
                'hovermode':
                'closest',
                'paper_bgcolor':
                '#f7f7f7',
                'plot_bgcolor':
                '#efefef',
                'polar': {
                    'angularaxis': {
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside'
                    },
                    'bgcolor': '#efefef',
                    'radialaxis': {
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside'
                    }
                },
                'scene': {
                    'xaxis': {
                        'backgroundcolor': '#efefef',
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showbackground': True,
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside',
                        'zerolinecolor': '#e1e1e1'
                    },
                    'yaxis': {
                        'backgroundcolor': '#efefef',
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showbackground': True,
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside',
                        'zerolinecolor': '#e1e1e1'
                    },
                    'zaxis': {
                        'backgroundcolor': '#efefef',
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showbackground': True,
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside',
                        'zerolinecolor': '#e1e1e1'
                    }
                },
                'shapedefaults': {
                    'fillcolor': 'black',
                    'line': {
                        'width': 0
                    },
                    'opacity': 0.3
                },
                'ternary': {
                    'aaxis': {
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside'
                    },
                    'baxis': {
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside'
                    },
                    'bgcolor': '#efefef',
                    'caxis': {
                        'gridcolor': '#e1e1e1',
                        'linecolor': '#e1e1e1',
                        'showgrid': True,
                        'tickcolor': '#e1e1e1',
                        'ticks': 'outside'
                    }
                },
                'xaxis': {
                    'automargin': True,
                    'gridcolor': '#e1e1e1',
                    'linecolor': '#e1e1e1',
                    'showgrid': True,
                    'tickcolor': '#e1e1e1',
                    'ticks': 'outside',
                    'zerolinecolor': '#e1e1e1'
                },
                'yaxis': {
                    'automargin': True,
                    'gridcolor': '#e1e1e1',
                    'linecolor': '#e1e1e1',
                    'showgrid': True,
                    'tickcolor': '#e1e1e1',
                    'ticks': 'outside',
                    'zerolinecolor': '#e1e1e1'
                }
            }
        }
    )
    pio.templates["qeds"] = template
    return template
    # template generated with the following code
    """
    colorscale = [[0, "#035f2f"], [1, "#c7fde0"]]
    colorway = COLOR_CYCLE

    # Set colorbar_common
    # Note the light inward ticks in
    # https://ggplot2.tidyverse.org/reference/scale_colour_continuous.html
    colorbar_common = dict(
        outlinewidth=0, tickcolor=colors["gray93"], ticks="inside", ticklen=6
    )

    # Common axis common properties
    axis_common = dict(
        showgrid=True,
        gridcolor=BORDER_COLOR,
        linecolor=BORDER_COLOR,
        tickcolor=BORDER_COLOR,
        ticks="outside",
    )

    # semi-transparent black and no outline
    shape_defaults = dict(fillcolor="black", line={"width": 0}, opacity=0.3)

        # Remove arrow head and make line thinner
    annotation_defaults = {"arrowhead": 0, "arrowwidth": 1}

    # initialize_template is found here:
    # https://github.com/plotly/plotly.py/blob/65625d49226632abcf932d530aa9c90ba1bc59c1/packages/python/plotly/templategen/utils/__init__.py
    template = initialize_template(
        paper_clr=PAPER_BGCOLOR,
        font_clr=TEXT_COLOR,
        panel_background_clr=PLOT_BGCOLOR,
        panel_grid_clr="white",
        axis_ticks_clr=TEXT_COLOR,
        zerolinecolor_clr=BORDER_COLOR,
        table_cell_clr=PLOT_BGCOLOR,
        table_header_clr=PAPER_BGCOLOR,
        table_line_clr=BORDER_COLOR,
        colorway=colorway,
        colorbar_common=colorbar_common,
        colorscale=colorscale,
        axis_common=axis_common,
        annotation_defaults=annotation_defaults,
        shape_defaults=shape_defaults,
    )
    """
