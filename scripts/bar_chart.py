import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select, Slider,HoverTool, LabelSet, Panel
from bokeh.palettes import Blues4
from bokeh.plotting import figure

# STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp', 'record_max_temp']
def bar_tab(covid_data):
    def get_dataset(src, option, min_year, max_year):
        df = src.copy()
        # df = df.set_index(['Date'])
        # df.sort_index(inplace=True)

        if (min_year <= max_year):
            df = df[df.Year >= min_year]
            df = df[df.Year <= max_year]

        total = df.groupby(by='Province')[option].max()
        total.sort_values(ascending=False, inplace=True)

        return ColumnDataSource(data=dict(name=total.index.to_list(), value=total.to_list()))

    def make_plot(source, title):
        
        plot = figure(width=1000, height=750, x_range = source.data["name"])
        plot.vbar(x='name', source=source, width=0.5, bottom=0, top='value', color="red")

        labels = LabelSet(x='name', y='value', text='value',x_offset=5, y_offset=5, source=source, render_mode='canvas')
        plot.add_layout(labels)

        plot.title.text = title

        # fixed attributes
        plot.xaxis.axis_label = None
        plot.yaxis.axis_label = "Cases"
        plot.axis.axis_label_text_font_style = "bold"
        # plot.x_range = DataRange1d(range_padding=0.0)
        plot.grid.grid_line_alpha = 0.6

        return plot

    def update_plot(attrname, old, new):
        option = option_select.value
        plot.title.text = option + ' Covid pada Provinsi di pulau Jawa'
        min_year = min_year_slider.value
        max_year = max_year_slider.value

        src = get_dataset(df, option, min_year, max_year)
        source.data.update(src.data)

    option = 'Total_Cases'
    min_year = 2020
    max_year = 2021

    options = ['Total_Cases', 'Total_Deaths', 'Total_Recovered']
    years = [2020, 2021]

    option_select = Select(value=option, title='Option', options=options)
    min_year_slider = Slider(title="Start Year", start=2020, end=2021, value=2020, step=1)
    max_year_slider = Slider(title="End Year", start=2020, end=2021, value=2021, step=1)
    #ini ganti ke slider tahun
    # year_select = Select(value=year, title='Year', options=years)

    # distribution_select = Select(value=distribution, title='Distribution', options=['Discrete', 'Smoothed'])

    df = covid_data.copy()
    df['Date'] = pd.to_datetime(df.Date)
    source = get_dataset(df, option, min_year, max_year)
    plot = make_plot(source, option + ' Covid pada Provinsi di pulau Jawa')

    option_select.on_change('value', update_plot)
    min_year_slider.on_change('value', update_plot)
    max_year_slider.on_change('value', update_plot)
    # year_select.on_change('value', update_plot)

    # controls = column(province_select, year_select)
    controls = column(option_select, min_year_slider, max_year_slider)

    layout = row(controls, plot)

    # Make a tab with the layout 
    tab = Panel(child=layout, title = 'Total report')

    return tab