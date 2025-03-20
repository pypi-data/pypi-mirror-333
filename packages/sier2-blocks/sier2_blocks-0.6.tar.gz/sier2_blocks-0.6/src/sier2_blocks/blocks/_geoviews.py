from sier2 import Block
import param

import panel as pn
import numpy as np

import geoviews as gv
import holoviews as hv
import geoviews.tile_sources as gvts

gv.extension('bokeh', inline=True)

def guess_lon_col(cols):
    """
    Given a list of columns, guess what is an acceptable longitude column name.
    """
    guess = [c for c in cols if 'lon' in c.lower()]
    if guess:
        return guess[0]

    guess = [c for c in cols if 'x' in c.lower()]
    if guess:
        return guess[0]

    return cols[0]

def guess_lat_col(cols):
    """
    Given a list of columns, guess what is an acceptable latitude column name.
    """
    guess = [c for c in cols if 'lat' in c.lower()]
    if guess:
        return guess[0]

    guess = [c for c in cols if 'y' in c.lower()]
    if guess:
        return guess[0]

    # Assume we also didn't find a longitude, so default to the second column to avoid clashes.
    #
    return cols[1]

class GeoPoints(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.map = gvts.CartoMidnight()
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')#'scale_both')
        self.hv_pane.object=self._produce_plot

    x_sel = param.ObjectSelector()
    y_sel = param.ObjectSelector()
    
    @param.depends('in_df', 'x_sel', 'y_sel')
    def _produce_plot(self):
        if self.in_df is not None and self.x_sel is not None and self.y_sel is not None:
            return self.map * gv.Points(self.in_df, kdims=[self.x_sel, self.y_sel])

        else:
            return self.map

    def execute(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        
        self.param['x_sel'].objects = plottable_cols
        self.param['y_sel'].objects = plottable_cols

        self.x_sel = guess_lon_col(plottable_cols)
        self.y_sel = guess_lat_col(plottable_cols)

        self.out_df = self.in_df

    def __panel__(self):
        # return self.hv_pane
        return pn.Column(
            pn.Row(
                self.param['x_sel'],
                self.param['y_sel']
            ),
            self.hv_pane
        )

class GeoPointsSelect(Block):
    """The Points element visualizes as markers placed in a space of two independent variables."""

    in_df = param.DataFrame(doc='A pandas dataframe containing x,y values')
    out_df = param.DataFrame(doc='Output pandas dataframe')

    def __init__(self, *args, block_pause_execution=True, **kwargs):
        super().__init__(*args, block_pause_execution=block_pause_execution, **kwargs)

        self.map = gvts.CartoMidnight()
        
        self.hv_pane = pn.pane.HoloViews(sizing_mode='stretch_width')#'scale_both')
        self.selection = hv.streams.Selection1D()
        self.hv_pane.object=self._produce_plot

    x_sel = param.ObjectSelector()
    y_sel = param.ObjectSelector()
    
    @param.depends('in_df', 'x_sel', 'y_sel')
    def _produce_plot(self):
        if self.in_df is not None and self.x_sel is not None and self.y_sel is not None:
            scatter = self.map * gv.Points(self.in_df, kdims=[self.x_sel, self.y_sel])

        else:
            scatter = self.map

        scatter = scatter.opts(tools=['box_select'])
        self.selection.source = scatter
        return scatter

    def prepare(self):
        plottable_cols = [c for c in self.in_df.columns if self.in_df[c].dtype.kind in 'iuf']
        
        self.param['x_sel'].objects = plottable_cols
        self.param['y_sel'].objects = plottable_cols
        
        self.x_sel = guess_lon_col(plottable_cols)
        self.y_sel = guess_lat_col(plottable_cols)

    def execute(self):
        self.out_df = self.in_df.loc[self.selection.index]

    def __panel__(self):
        # return self.hv_pane
        return pn.Column(
            pn.Row(
                self.param['x_sel'],
                self.param['y_sel']
            ),
            self.hv_pane
        )