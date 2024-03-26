from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd

st.set_page_config(
    page_title='Inventory tracker',
    page_icon=':shopping_bags:', 
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

def connect_db():
    '''Connects to the sqlite database.'''

    DB_FILENAME = Path(__file__).parent/'inventory.db'
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    '''Initializes the inventory table with some data.'''
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            price REAL,
            units_sold INTEGER,
            units_left INTEGER,
            cost_price REAL,
            reorder_point INTEGER,
            description TEXT
        )
        '''
    )

    cursor.execute(
        '''
        INSERT INTO 'inventory' ('id','item_name','price','units_sold','units_left','cost_price','reorder_point','description') VALUES 
         ('1','HP CRUISE 15W-40','150','12','12','100','18','Engine'), 
         ('2','HP CRUISE PREMIUM S 20W-50','175','5','19','85','18','Engine'), 
         ('3','HP EXTRA SUPER MOTOR OIL','200','3','21','120','18','Engine'), 
         ('4','HP DIESELINO 15W-40T','170','6','18','100','18','Engine (D)'), 
         ('5','HP HDX+ 15W-40 CF-4','350','4','20','155','18','Lubricant'), 
         ('6','HP HYLUBE LL 15W-40','180','7','17','100','18','Lubricant'), 
         ('7','HP SUPER DUTY BRAKE FLUID DOT 4','230','6','18','110','18','Brake'), 
         ('8','HP KISAN SHAKTI','145','9','15','75','18','Engine (Agri)'), 
         ('9','HP WET BRAKE OIL','170','4','16','65','18','Brake');        '''
    )
    conn.commit()


def load_data(conn):
    '''Loads the inventory data from the database.'''
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT * FROM inventory')
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(data,
        columns=[
            'id',
            'item_name',
            'price',
            'units_sold',
            'units_left',
            'cost_price',
            'reorder_point',
            'description',
        ])

    return df


def update_data(conn, df, changes):
    '''Updates the inventory data in the database.'''
    cursor = conn.cursor()

    if changes['edited_rows']:
        deltas = st.session_state.inventory_table['edited_rows']
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            '''
            UPDATE inventory
            SET
                item_name = :item_name,
                price = :price,
                units_sold = :units_sold,
                units_left = :units_left,
                cost_price = :cost_price,
                reorder_point = :reorder_point,
                description = :description
            WHERE id = :id
            ''',
            rows,
        )

    if changes['added_rows']:
        cursor.executemany(
            '''
            INSERT INTO inventory
                (id, item_name, price, units_sold, units_left, cost_price, reorder_point, description)
            VALUES
                (:id, :item_name, :price, :units_sold, :units_left, :cost_price, :reorder_point, :description)
            ''',
            (defaultdict(lambda: None, row) for row in changes['added_rows']),
        )

    if changes['deleted_rows']:
        cursor.executemany(
            'DELETE FROM inventory WHERE id = :id',
            ({'id': int(df.loc[i, 'id'])} for i in changes['deleted_rows'])
        )

    conn.commit()

'''
# Inventory tracker

**This is a managerial side only application.**
This page reads and writes directly from/to the inventory database.
'''

st.subheader('Inventory Database', divider='red')

conn, db_was_just_created = connect_db()

if db_was_just_created:
    initialize_data(conn)
    st.toast('Database initialized with some sample data.')

df = load_data(conn)

edited_df = st.data_editor(
    df,
    disabled=['id'], 
    num_rows='dynamic', 
    column_config={
        "price": st.column_config.NumberColumn(format="₹%.2f"),
        "cost_price": st.column_config.NumberColumn(format="₹%.2f"),
    },
    key='inventory_table')

has_uncommitted_changes = any(len(v) for v in st.session_state.inventory_table.values())

st.button(
    'Commit changes',
    type='primary',
    disabled=not has_uncommitted_changes,
    on_click=update_data,
    args=(conn, df, st.session_state.inventory_table))


''
''
''

st.subheader('Units left', divider='red')

need_to_reorder = df[df['units_left'] < df['reorder_point']].loc[:, 'item_name']

if len(need_to_reorder) > 0:
    items = '\n'.join(f'* {name}' for name in need_to_reorder)

    st.warning(f"Low Stock Items below:\n {items}")

''
''

st.altair_chart(
    alt.Chart(df)
        .mark_bar(
            orient='horizontal',
        )
        .encode(
            x='units_left',
            y='item_name',
        )
    + alt.Chart(df)
        .mark_point(
            shape='diamond',
            filled=True,
            size=50,
            color='salmon',
            opacity=1,
        )
        .encode(
            x='reorder_point',
            y='item_name',
        )
    ,
    use_container_width=True)

st.caption('NOTE: :diamonds: - reorder points')

''
''
''

st.subheader('Best sellers', divider='green')

''
''

st.altair_chart(alt.Chart(df)
    .mark_bar(orient='horizontal')
    .encode(
        x='units_sold',
        y=alt.Y('item_name').sort('-x'),
    ),
    use_container_width=True)
