from ..blocks._io import LoadDataFrame, StaticDataFrame, SaveDataFrame
from ..blocks._view import SimpleTable, SimpleTableSelect
from ..blocks._holoviews import HvPoints, HvPointsSelect, HvHist
from ..blocks._geoviews import GeoPoints, GeoPointsSelect

from sier2 import Connection
from sier2.panel import PanelDag

DOC = '''# Points chart

Load a dataframe from a file and display a Points chart.
'''

def geo_points_dag():
    sdf = StaticDataFrame(name='Load DataFrame')
    gps = GeoPointsSelect(name='Plot Points')
    gp = GeoPoints(name='View Selection')

    DOC = '''# Geo points chart
    
    Load an example dataframe and display a Geo points chart, allowing for a subset to be plotted.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Geo Points')
    dag.connect(sdf, gps,
        Connection('out_df', 'in_df'),
    )
    dag.connect(gps, gp,
        Connection('out_df', 'in_df'),
    )

    return dag

def hv_points_dag():
    """Load a dataframe from a file and display a Points chart."""

    ldf = LoadDataFrame(name='Load DataFrame')
    hps = HvPointsSelect(name='Plot Points')
    st = SimpleTable(name='View Selection')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Points')
    dag.connect(ldf, hps,
        Connection('out_df', 'in_df'),
    )
    dag.connect(hps, st,
        Connection('out_df', 'in_df'),
    )

    return dag

def hv_hist_dag():
    """Load a dataframe from a file and display a Histogram."""

    ldf = LoadDataFrame(name='Load DataFrame')
    hh = HvHist(name='Plot Histogram')

    DOC = '''# Points chart
    
    Load a dataframe from a file and display a Points chart.
    '''

    dag = PanelDag(doc=DOC, site='Chart', title='Histogram')
    dag.connect(ldf, hh,
        Connection('out_df', 'in_df'),
    )

    return dag

def table_view_dag():
    """Load a dataframe from file and display in a panel table."""

    ldf = LoadDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    sel_st = SimpleTable(name='Selection')

    DOC = '''# Table viewer

    Load a dataframe from a file and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(ldf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag

def static_view_dag():
    """Load a dataframe from file and display in a panel table."""

    sdf = StaticDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    sel_st = SimpleTable(name='Selection')

    DOC = '''# Table viewer

    Load a dataframe from a file and display the data as a table.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(sdf, st, Connection('out_df', 'in_df'))
    dag.connect(st, sel_st, Connection('out_df', 'in_df'))

    return dag

def save_csv_dag():
    """Load a dataframe from file and download."""
    sdf = StaticDataFrame(name='Load DataFrame')
    st = SimpleTableSelect(name='View Table')
    edf = SaveDataFrame(name='Export')

    DOC = '''# Table viewer

    Load a dataframe from file and download.
    '''

    dag = PanelDag(doc=DOC, title='Table')
    dag.connect(sdf, st, Connection('out_df', 'in_df'))
    dag.connect(st, edf, Connection('out_df', 'in_df'))

    return dag