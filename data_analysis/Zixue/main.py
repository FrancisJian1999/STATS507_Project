
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from sklearn.model_selection import train_test_split

app = dash.Dash(__name__)
server = app.server

df1 = pd.read_csv("AAO2b05c.csv", sep=",", header=0)

df1['Q'] = df1['YYYYQ'].astype(str).str[-1]

# Convert the 'Q' column to integers
df1['Q'] = df1['Q'].astype(int)

averages_by_yyyyq = df1.groupby('YYYYQ').mean()
columns_to_remove = [averages_by_yyyyq.columns[0], averages_by_yyyyq.columns[1], averages_by_yyyyq.columns[3]]
averages_by_yyyyq = averages_by_yyyyq.drop(columns_to_remove, axis=1)




data = pd.read_excel('gdp.xlsx', engine='openpyxl')

data = data.dropna(axis=1, how='all')

first_row_list = data.iloc[0].tolist()
gdp = first_row_list[1:]

averages_by_yyyyq = averages_by_yyyyq.iloc[:-1]

averages_by_yyyyq['GDP'] = gdp

# Compute the correlation matrix
correlation_matrix = averages_by_yyyyq.corr()

heatmap = go.Figure(go.Heatmap(z=correlation_matrix, x=correlation_matrix.columns, y=correlation_matrix.columns, colorscale='Viridis'))

# Update the layout to adjust the height, width, and title of the heatmap
heatmap.update_layout(
    height=600,
    width=800,
    title="Correlation plot of GDP and surveys of consumer variables"
)



# Create a line plot of GDP versus YYYYQ
gdp_line_plot = go.Figure(go.Scatter(x=list(range(len(averages_by_yyyyq.index))), y=averages_by_yyyyq['GDP'], mode='lines+markers'))

# Update the layout to adjust the title of the line plot
gdp_line_plot.update_layout(title="GDP vs Time")

# Set the x-axis to have equal distance between each value
gdp_line_plot.update_xaxes(tickmode='array', tickvals=list(range(len(averages_by_yyyyq.index))), ticktext=averages_by_yyyyq.index)

box_plot_except_two = go.Figure()

for column in averages_by_yyyyq.columns:
    if column not in ['HOMEAMT', 'INVAMT','GDP','YYYY','ICS','ICC','ICE','PAGOR1','NEWS1','NEWS2','PX1','PAGOR2','BUS5']:
        box_plot_except_two.add_trace(go.Box(y=averages_by_yyyyq[column], name=column, boxpoints='outliers', jitter=0.3, pointpos=-1.8))

# Update the layout to adjust the title of the box plot
box_plot_except_two.update_layout(title="Box Plots of Variables")

# Create a box plot for HOMEAMT and INVAMT
box_plot_two = go.Figure()

gdp_vs_invamt = go.Figure(go.Scatter(x=averages_by_yyyyq['GDP'], y=averages_by_yyyyq['INVAMT'], mode='markers'))

# Update the layout to adjust the title of the scatter plot
gdp_vs_invamt.update_layout(title="GDP vs INVAMT", xaxis_title="GDP", yaxis_title="INVAMT")

app.layout = html.Div([
    dcc.Graph(id='heatmap', figure=heatmap),
    dcc.Graph(id='gdp_line_plot', figure=gdp_line_plot),
    dcc.Graph(id='box_plot_except_two', figure=box_plot_except_two),  # Add the first box plot to the layout
    dcc.Graph(id='gdp_vs_invamt', figure=gdp_vs_invamt)  # Add the line plot of GDP vs INVAMT to the layout

])

if __name__ == '__main__':
    app.run_server(debug=True)

