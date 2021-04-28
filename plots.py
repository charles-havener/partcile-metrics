from datetime import timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


#colors
blue_100_color = 'rgba(0,101,159,1)'
yellow_100_color = 'rgba(255,149,43,1)'

green_10_color = 'rgba(0,162,53,0.1)'
green_50_color = 'rgba(0,162,53,0.5)'
green_65_color = 'rgba(0,162,53,.65)'

red_50_color = 'rgba(181,44,56,0.5)'
red_65_color = 'rgba(181,44,56,0.75)'

axis_color = 'rgba(204,204,204,1)'
axis_grid_color = 'rgba(204,204,204,0.5)'
text_color = 'rgba(119,119,119,1)'
background_color = 'rgba(255,255,255,1)'


def setComboMarker(x, y, x_target, y_target):
    marker_size = 20
    line_width=1

    def getLineColor(x,y):
        if x > x_target or y > y_target:
            return red_65_color
        return green_65_color
    
    def getMarkerColor(x,y):
        if x > x_target or y > y_target:
            return red_50_color
        return green_50_color

    return dict(
        size=marker_size,
        color = list(map(getMarkerColor,x,y)),
        line=dict(
            color=list(map(getLineColor,x,y)),
            width=line_width,
        ),
    )


def setSingleMarker(y, y_target):
    marker_size = 20
    line_width=1

    def getLineColor(y):
        if y > y_target:
            return red_65_color
        return green_65_color
    
    def getMarkerColor(y):
        if y > y_target:
            return red_50_color
        return green_50_color

    return dict(
        size=marker_size,
        color = list(map(getMarkerColor,y)),
        line=dict(
            color=list(map(getLineColor,y)),
            width=line_width,
        ),
    )


def getTargets(group):
    if group in ["PCB"]:
        return 100000, 700
    else:
        return 10000,70


def CreateComboBubbleChart(df, output_name, data_name_1, data_name_2, group, days=30):
    """Creates a scatter plot with points colored differently for in spec and out of spec for their areas 
        for large and small particle counts.

    Args:
        df (dataframe): a pandas dataframe that contains the data to use
        output_name (str): the name of the file to be output along with it's path inside the images folder
        data_name_1 (str): the first header for the dataframe column to pull data points from
        data_name_2 (str): the second header for the dataframe column to pull data points from
        group (str): the functional area from which the measurements were taken
        days (int, optional): the number of recent days to pull data from. Defaults to 30.
    """

    # Filter df to include only most recent 'days' days
    in_days = df['DATE'] >= df['DATE'].max()-timedelta(days)
    df = df[in_days]

    # Generate Title
    title_data = {'0.5 MICRONS': '0.5\u03BC', '5.0 MICRONS': '5.0\u03BC'}
    title = f"Distribution of {title_data[data_name_1]}, {title_data[data_name_2]} readings ({days} days) -- {group}"

    # Set spec limits based on group
    small_target, large_target = getTargets(group)

    # Create Chart
    fig = go.Figure()

    # Add measurements to chart
    fig.add_trace(
        go.Scatter(
            mode='markers',
            x=df[data_name_2],
            y=df[data_name_1],
            name="data points",
            marker=setComboMarker(df[data_name_2],df[data_name_1], large_target, small_target),
        ),
    )

    # Create target box
    fig.add_trace(
        go.Scatter(
            name="target",
            y = [0,small_target,small_target,0,0],
            x = [0,0,large_target,large_target,0],
            fill="toself",
            fillcolor = green_10_color,
            marker=dict(
                color='rgba(1,1,1,0)', # Only care that opacity is 0
            ),
            line=dict(
                color=green_50_color,
                width=1
            )
        )
    )
    fig.update_xaxes(
        gridcolor = axis_grid_color,
        linecolor = axis_color,
        linewidth=2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 21,
                color = text_color,
            ),
            standoff = 4,
            text = "5.0\u03BC count",
        ),
        type='log',
    )
    fig.update_yaxes(
        gridcolor = axis_grid_color,
        linecolor = axis_color,
        linewidth=2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 21,
                color = text_color,
            ),
            standoff = 4,
            text = "0.5\u03BC count",
        ),
        type='log',
    )
    fig.update_layout(
        height = 1080,
        width = 1920,
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 28,
                color = text_color,
            ),
            text = title,
            x = 0.5,
            xanchor = 'center',
        ),
    )

    # Save the image
    fig.write_image(output_name + ".png")


def CreateSingleBubbleChart(df, output_name, data_name, group, days=30):

    """Creates a scatter plot with points colored differently for in spec and out of spec for their areas 
        for either large or small particle count.

    Args:
        df (dataframe): a pandas dataframe that contains the data to use
        output_name (str): the name of the file to be output along with it's path inside the images folder
        data_name (str): the header for the dataframe column to pull data points from
        days (int, optional): the number of recent days to pull data from. Defaults to 30.
    """

    # Filter df to include only most recent 'days' days
    in_days = df['DATE'] >= df['DATE'].max()-timedelta(days)
    df = df[in_days]

    # Generate Title
    title_data = {'0.5 MICRONS': '0.5\u03BC', '5.0 MICRONS': '5.0\u03BC'}
    title = f"Distribution of {title_data[data_name]} readings ({days} days) -- {group}"

    # Set spec limits based on group
    large_target, small_target = getTargets(group)
    if data_name == '0.5 MICRONS':
        target = large_target
    else:
        target = small_target

    # Create Chart
    fig = go.Figure()

    # Add measurements to chart
    fig.add_trace(
        go.Scatter(
            mode='markers',
            y=df[data_name],
            name="data points",
            marker=setSingleMarker(df[data_name], target),
        ),
    )

    # Create target box
    fig.add_trace(
        go.Scatter(
            name="target",
            y = [0,target,target,0,0],
            x = [0,0,len(df[data_name]),len(df[data_name]),0],
            fill="toself",
            fillcolor = green_10_color,
            marker=dict(
                color='rgba(1,1,1,0)', # Only care that opacity is 0
            ),
            line=dict(
                color=green_50_color,
                width=1
            )
        )
    )
    fig.update_xaxes(
        #gridcolor = axis_grid_color,
        linecolor = axis_color,
        linewidth=2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        type='linear',
    )
    fig.update_yaxes(
        gridcolor = axis_grid_color,
        linecolor = axis_color,
        linewidth=2,
        tickfont = dict(
            family = 'Open Sans, Arial, Helvetica, sans-serif',
            size = 14,
            color = text_color,
        ),
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 21,
                color = text_color,
            ),
            standoff = 4,
            text = f"{title_data[data_name]} Count",
        ),
        type='log',
    )
    fig.update_layout(
        height = 1080,
        width = 1920,
        paper_bgcolor = background_color,
        plot_bgcolor = background_color,
        title = dict(
            font = dict(
                family = 'Open Sans, Arial, Helvetica, sans-serif',
                size = 28,
                color = text_color,
            ),
            text = title,
            x = 0.5,
            xanchor = 'center',
        ),
    )

    # Save the image
    fig.write_image(output_name + ".png")

if __name__ == "__main__":
    pass