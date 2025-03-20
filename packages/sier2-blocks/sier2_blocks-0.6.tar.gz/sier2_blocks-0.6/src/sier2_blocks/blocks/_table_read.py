import param
import pandas as pd
import panel as pn
from io import StringIO
from sier2 import Block, Connection
from sier2.panel import PanelDag

from sier2_blocks import TableDataInput, SimpleTable

if __name__ == '__main__':
    table_data = TableDataInput()
    table = SimpleTable()

    dag = PanelDag(doc='Example csv reader', title='TableDataInput')
    dag.connect(csv_data, table, Connection('out_data', 'in_df'))
    dag.show()