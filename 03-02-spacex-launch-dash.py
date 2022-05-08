# Build a Dashboard Application with Plotly Dash
# In this lab, you will be building a Plotly Dash application for users
# to perform interactive visual analytics on SpaceX launch data in real-time.
# 
# This dashboard application contains input components such as a dropdown list and
# a range slider to interact with a pie chart and a scatter point chart.
# You will be guided to build this dashboard application via the following tasks:
# 	TASK 1: Add a Launch Site Drop-down Input Component
# 	TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
# 	TASK 3: Add a Range Slider to Select Payload
# 	TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
# 
# Note:Please take screenshots of the Dashboard and save them. Further upload your notebook to github.
# The github url and the screenshots are later required in the presentation slides.

# Libraries
import os
import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output


# Prepare data
print('Preparing data...')
if os.path.isfile('spacex_launch_dash.csv'):
	pass
else:
	import wget
	data_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
	wget.download(data_url)

spacex_df = pd.read_csv('spacex_launch_dash.csv')
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

slider_marks = {}
for i in range(0, 10000 + 1, 1000):
	slider_marks[i] = str(i)


# Create a dash app
print('Creating an app...')
app = dash.Dash(__name__)

# Build the app's layout
app.layout = html.Div(
	children = [
		# app title
		html.H1('SpaceX Launch Records Dashboard', style = {'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

		# TASK 1: Add a dropdown list to enable Launch Site selection
		# The default select value is for ALL sites
		html.Div(
			dcc.Dropdown(
				id = 'site-dropdown',
				# value = 'ALL',
				options = [
					{'label': 'All Sites', 'value': 'ALL'},
					{'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
					{'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
					{'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
					{'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
				],
				placeholder = 'Select a Launch Site here',
				searchable = True,
				style = {'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
			)
		),
		html.Br(),

		# TASK 2: Add a pie chart to show the total successful launches count for all sites
		# If a specific launch site was selected, show the Success vs. Failed counts for the site
		html.Div(dcc.Graph(id='success-pie-chart')),
		html.Br(),

		# TASK 3: Add a slider to select payload range
		html.P("Payload range (Kg):"),
		html.Div(
			dcc.RangeSlider(
				id='payload-slider',
				min = 0,
				max = 10000,
				step = 1000,
				marks = slider_marks,
				value = [min_payload, max_payload]
			)
		),
		html.Br(),
		html.Div(dcc.Graph(id='success-payload-scatter-chart')),

		# TASK 4: Add a scatter chart to show the correlation between payload and launch success
	]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
	Output(component_id = 'success-pie-chart', component_property = 'figure'),
	Input(component_id = 'site-dropdown', component_property = 'value')
)
def get_pie_chart(entered_site):
	if entered_site == 'ALL':
		df = spacex_df
		fig = px.pie(
			df,
			values = 'class',
			names = 'Launch Site',
			title = 'Total Success Launches By Site'
		)
	else:
		df = spacex_df[spacex_df['Launch Site'] == entered_site]
		fig = px.pie(
			df,
			names = 'class',
			title = 'Total Success Launches for site {}'.format(entered_site)
		)

	return fig

@app.callback(
	Output(component_id = 'success-payload-scatter-chart', component_property = 'figure'),
	[
		Input(component_id = 'site-dropdown', component_property = 'value'),
		Input(component_id = 'payload-slider', component_property = 'value')
	]
)
def get_scatter_chart(entered_site, slider_range):
	if entered_site == 'ALL':
		df = spacex_df[spacex_df['Payload Mass (kg)'].between(left = slider_range[0], right = slider_range[1], inclusive = True)]
		title = 'Correlation between Payload and Success for all Sites'
	else:
		df = spacex_df[(spacex_df['Payload Mass (kg)'].between(left = slider_range[0], right = slider_range[1], inclusive = True)) & (spacex_df['Launch Site'] == entered_site)]
		title = 'Correlation between Payload and Success for site {}'.format(entered_site)
	fig = px.scatter(
		data_frame = df,
		x = 'Payload Mass (kg)',
		y = 'class',
		color = 'Booster Version Category',
		title = title
	)

	return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output




# Run the app
if __name__ == "__main__":
	app.run_server(
        port = 8050,
        host = '127.0.0.1',
        debug = True
    )


# Finding Insights Visually
# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data,
# and answer the following questions:
# 1. Which site has the largest successful launches?
# 2. Which site has the highest launch success rate?
# 3. Which payload range(s) has the highest launch success rate?
# 4. Which payload range(s) has the lowest launch success rate?
# 5. Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
# 
# Answer:
# 1. KSC LC-39A
# 2. KSC LC-39A
# 3. 2k-4k
# 4. 0-2k
# 5. B5