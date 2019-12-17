"""
This file defines the appearance and functionality of the web app. It
has three main parts:
(1) imports from other modules
(2) defines and parses parameters (CAPITALIZED) that represent
	the 'static' aspects of the web page
(3) defines 'callback functions' which control the interactive aspects
	of the web page
"""

# imports backend and information from ../user_config

if __name__ == '__main__': # if using the local machine as the web server
	import sys
	from backend import DataSet
	sys.path.insert(1, '../user_config')
	from settings import (
		DATA_CSVFILEPATH, DATA_IDFIELD,
		INITIAL_GRAPHTYPE, INITIAL_DATAFIELDS, INITIAL_DATAFILTERS,
		INITIAL_HISTOGRAM_BINSIZE, MAX_HISTOGRAM_BINSIZE,
		HISTOGRAM_BINSIZE_INCREMENT,
		)
	CSVPATH_CACHE = DATA_CSVFILEPATH
	DATA_CSVFILEPATH = '../user_config/' + DATA_CSVFILEPATH
	import filter_functions as FILTER_FUNCTIONS

else: # if using gunicorn (../Procfile) + Heroku as the web server
	from src.backend import DataSet
	from user_config.settings import (
		DATA_CSVFILEPATH, DATA_IDFIELD,
		INITIAL_GRAPHTYPE, INITIAL_DATAFIELDS, INITIAL_DATAFILTERS,
		INITIAL_HISTOGRAM_BINSIZE, MAX_HISTOGRAM_BINSIZE,
		HISTOGRAM_BINSIZE_INCREMENT,
		)
	CSVPATH_CACHE = DATA_CSVFILEPATH
	DATA_CSVFILEPATH = 'user_config/' + DATA_CSVFILEPATH
	import user_config.filter_functions as FILTER_FUNCTIONS

# imports graphing and page layout libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.figure_factory as ff
from dash.dependencies import Input, Output

CSS_URL = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
WEBAPP_TITLE = CSVPATH_CACHE[:-4] # title of the webpages' tab

# unique string IDs for UI elements
GRAPH_ID = '0'
GRAPH_ID2 = '7'
GRAPHTYPESLIDER_ID = '1'
DATATYPEDROPDOWN_ID = '2'
# FILTERDROPDOWN_ID = '3'
HISTOGRAMBINSLIDER_ID = '4'
GROUPINGDROPDOWN_ID = '5'
FILTERCHECKBOX_ID = '6'

# names and ordering of available graph types
GRAPHTYPE_CHOICES = [
	'Histogram', # leftmost choice
	'Density Plot',
	'Violin Plot',
	'Box Plot',
	'Bar Plot',
	'Dot Plot', # rightmost choice
	]

FILTER_CHOICES = [
	'isMale',
	'analyticMajor',
	'nativeEnglish'
	]

# parses the parameters into helper variables
dataSet = DataSet()
dataSet.addCsv(DATA_CSVFILEPATH)
dataFields = [
	fieldName
	for fieldName in dataSet.getSchema(DATA_CSVFILEPATH)
	]
filterFunctions = {} # maps filter function names' to their function objects
def _negate(func):
	return (lambda x : not func(x))
for name, func in FILTER_FUNCTIONS.__dict__.items():
	if callable(func):
		filterFunctions[name] = func
		# adds a negated version of every filter
		# filterFunctions['not_' + name] = _negate(func)

# lays out the basic HTML along with the interactive components
INITIAL_LAYOUT = html.Div(children=[
	# TODO data filter checkbox
	html.Div(children=[
		html.Div(children=[
		dcc.Markdown('''
Select data filters:
			'''),
		# TODO Note: UI cannot be customized as Dash does not support all HTML tags
		html.Div(children=[
				dcc.Slider(
					id=FILTERCHECKBOX_ID,
					min=0,
					max=len(FILTER_CHOICES) - 1,
					marks={i: m for i, m in enumerate(FILTER_CHOICES)},
					included=False,
					step=None,
					vertical=True,
					value=0,
				),
				],
				style={'height': 100},
			),
		],
			style={'position': 'absolute', 'left': '40', 'top': '200'}
		),

		# displays the data, controlled by the callback function 'updateGraph'
		# defined below
		html.Div(children=[
			dcc.Graph(
				id=GRAPH_ID,
				config=dict(displayModeBar=False),
				# Full screen: config={ 'fillFrame':True},
			),
			html.Div(children=[
				dcc.Graph(
					id=GRAPH_ID2,
					config=dict(displayModeBar=False),
				),
				],
					style={'position': 'absolute', 'top':'0', 'left': '600'}
				),
		],
			style={'position':'absolute', 'left':'160'}
		),
	],
	),


	html.Div(children=[
		html.Div(children=[
			# graph type slider
			dcc.Slider(
				id=GRAPHTYPESLIDER_ID,
				min=0,
				max=len(GRAPHTYPE_CHOICES)-1,
				marks={i:m for i,m in enumerate(GRAPHTYPE_CHOICES)},
				included=False,
				step=None,
				value=GRAPHTYPE_CHOICES.index(INITIAL_GRAPHTYPE),
				),

			# two line breaks
			dcc.Markdown('''
&nbsp;
				'''),

			# data field selector
			dcc.Markdown('''
Select data fields:
				'''),
			dcc.Dropdown(
				id=DATATYPEDROPDOWN_ID,
				options=[{'label':e,'value':e} for e in dataFields],
				multi=True,
				value=INITIAL_DATAFIELDS,
				placeholder=''
				),

			],
			id='dropdown'
			),

			# line break
			dcc.Markdown('''
&nbsp;
				'''),

		# these controls are only shown when histogram is selected,
		# as controlled by the callback function 'showOrHideHistogramControls'
		# defined below
		html.Div(id='histogram controls', children=[

			# bin size slider
			dcc.Markdown('''
	Select bin size:
				'''),
			dcc.Slider(
				id=HISTOGRAMBINSLIDER_ID,
				min=1,
				max=MAX_HISTOGRAM_BINSIZE,
				marks=dict(
					{1:'1'}.items()
					| {i:str(i) for i in range(
						HISTOGRAM_BINSIZE_INCREMENT,
						MAX_HISTOGRAM_BINSIZE+1,
						HISTOGRAM_BINSIZE_INCREMENT
						)}.items()
					),
				included=False,
				step=1,
				value=INITIAL_HISTOGRAM_BINSIZE,
				),

			]
			),

		# prevents things from being cut off or the elements being
		# excessively wide on large screens
	],
		style={'position':'relative', 'top':'450'}
	),
	],
	style={
		'maxWidth':'1000px', 'padding-left':'110px', 'padding-right':'110px', 'font':'arial'
		}
	)

# creates the "app" helper variable
app = dash.Dash()
app.layout = INITIAL_LAYOUT
server = app.server
app.css.append_css(dict(external_url=CSS_URL))
app.title = WEBAPP_TITLE

@app.callback(
	Output('histogram controls', 'style'),
	[Input(GRAPHTYPESLIDER_ID, 'value')]
	)
def showOrHideHistogramControls(graphType:int):
	"""
	shows or hides the histogram controls depending on
	whether Histogram is currently selected
	"""

	if GRAPHTYPE_CHOICES[graphType] == 'Histogram':
		return {'display': 'block'}
	return {'display': 'none'}

@app.callback(
	Output(GRAPH_ID, 'figure'),
	[Input(DATATYPEDROPDOWN_ID, 'value'),
	 Input(FILTERCHECKBOX_ID, 'value'),
	 Input(GRAPHTYPESLIDER_ID, 'value'),
	 Input(HISTOGRAMBINSLIDER_ID, 'value'),
	 ]
	)
def updateGraph(dataFields:list, filterIndex:int, graphType:int,
				binSize:int):
	"""
	updates the graph based on the chosen data fields, data filters,
	graph type, and bin size (the latter if histogram is selected)
	"""

	# title of the graph, set to the filename for now
	title = CSVPATH_CACHE[:-4]

	if len(dataFields) == 0:
		return go.Figure(layout=dict(title=title)) # empty graph

	if filterIndex is 0:
		fList = ['isMale']
	elif filterIndex is 1:
		fList = ['analyticMajor']
	elif filterIndex is 2:
		fList = ['nativeEnglish']
	# function which filters a piece of data
	# depending on the filters the user selected
	def dataFilter(data:dict) -> bool:
		for name in fList:
			if not filterFunctions[name](data):
				return False
		return True

	filteredDataSet = tuple(filter(dataFilter, dataSet))

	if len(filteredDataSet) == 0:
		return go.Figure(layout=dict(title=title)) # empty graph

	# convert the data being plotted into numbers
	try:
		traceValues = [
			[ float(d[field]) for d in filteredDataSet ]
			for field in dataFields
			]
	except ValueError:
		return go.Figure(layout=dict(title="Error: Can't plot non-numeric data on a numeric axis."))

	# turn the position on the graph type slider into a graph type name
	graphType = GRAPHTYPE_CHOICES[graphType]

	if graphType == 'Histogram':

		out = ff.create_distplot(
			traceValues, dataFields,
			show_curve=False, show_rug=False, bin_size=binSize,
			)
		out.layout['title'] = title
		return out

	if graphType == 'Density Plot':

		out = ff.create_distplot(
			traceValues, dataFields,
			show_hist=False, show_rug=False,
			)
		out.layout['title'] = title
		return out

	layout = dict(title=title) # layout used by all of the graph types below

	if graphType == 'Violin Plot':

		traces = [
			dict(
				type='violin',
				name=field,
				y=values,
				)
			for field,values in zip(dataFields,traceValues)
			]

	elif graphType == 'Box Plot':

		traces = [
			go.Box(
				name=field,
				y=values,
				)
			for field,values in zip(dataFields,traceValues)
			]

	elif graphType == 'Dot Plot':

		traces = [
			dict(
				type='scatter',
				name=field,
				y=[d[field] for d in filteredDataSet],
				x=[d[DATA_IDFIELD] for d in filteredDataSet],
				mode='markers',
				)
			for field in dataFields
			]

		layout['xaxis'] = dict(
			title=DATA_IDFIELD,
			type='category',
			titlefont=dict(
				size=12,
				),
			)

	elif graphType == 'Bar Plot':

		traces = [
			go.Bar(
				name=field,
				y=[d[field] for d in filteredDataSet],
				x=[d[DATA_IDFIELD] for d in filteredDataSet],
				)
			for field in dataFields
			]

		layout['xaxis'] = dict(
			title=DATA_IDFIELD,
			type='category',
			titlefont=dict(
				size=12,
				),
			)

	return go.Figure(data=traces, layout=layout)

@app.callback(
	Output(GRAPH_ID2, 'figure'),
	[Input(DATATYPEDROPDOWN_ID, 'value'),
	 Input(FILTERCHECKBOX_ID, 'value'),
	 Input(GRAPHTYPESLIDER_ID, 'value'),
	 Input(HISTOGRAMBINSLIDER_ID, 'value'),
	 ]
	)
def updateGraph(dataFields:list, filterIndex:int, graphType:int,
				binSize:int):
	"""
	updates the graph based on the chosen data fields, data filters,
	graph type, and bin size (the latter if histogram is selected)
	"""

	# title of the graph, set to the filename for now
	title = 'Without filter'

	if len(dataFields) == 0:
		return go.Figure(layout=dict(title=title)) # empty graph

	if filterIndex is 0:
		fList = ['isMale']
	elif filterIndex is 1:
		fList = ['analyticMajor']
	elif filterIndex is 2:
		fList = ['nativeEnglish']
	# function which filters a piece of data
	# depending on the filters the user selected
	def dataFilter(data:dict) -> bool:
		for name in fList:
			return True

	filteredDataSet = tuple(filter(dataFilter, dataSet))

	if len(filteredDataSet) == 0:
		return go.Figure(layout=dict(title=title)) # empty graph

	# convert the data being plotted into numbers
	try:
		traceValues = [
			[ float(d[field]) for d in filteredDataSet ]
			for field in dataFields
			]
	except ValueError:
		return go.Figure(layout=dict(title="Error: Can't plot non-numeric data on a numeric axis."))

	# turn the position on the graph type slider into a graph type name
	graphType = GRAPHTYPE_CHOICES[graphType]

	if graphType == 'Histogram':

		out = ff.create_distplot(
			traceValues, dataFields,
			show_curve=False, show_rug=False, bin_size=binSize,
			)
		out.layout['title'] = title
		return out

	if graphType == 'Density Plot':

		out = ff.create_distplot(
			traceValues, dataFields,
			show_hist=False, show_rug=False,
			)
		out.layout['title'] = title
		return out

	layout = dict(title=title) # layout used by all of the graph types below

	if graphType == 'Violin Plot':

		traces = [
			dict(
				type='violin',
				name=field,
				y=values,
				)
			for field,values in zip(dataFields,traceValues)
			]

	elif graphType == 'Box Plot':

		traces = [
			go.Box(
				name=field,
				y=values,
				)
			for field,values in zip(dataFields,traceValues)
			]

	elif graphType == 'Dot Plot':

		traces = [
			dict(
				type='scatter',
				name=field,
				y=[d[field] for d in filteredDataSet],
				x=[d[DATA_IDFIELD] for d in filteredDataSet],
				mode='markers',
				)
			for field in dataFields
			]

		layout['xaxis'] = dict(
			title=DATA_IDFIELD,
			type='category',
			titlefont=dict(
				size=12,
				),
			)

	elif graphType == 'Bar Plot':

		traces = [
			go.Bar(
				name=field,
				y=[d[field] for d in filteredDataSet],
				x=[d[DATA_IDFIELD] for d in filteredDataSet],
				)
			for field in dataFields
			]

		layout['xaxis'] = dict(
			title=DATA_IDFIELD,
			type='category',
			titlefont=dict(
				size=12,
				),
			)

	return go.Figure(data=traces, layout=layout)

if __name__ == '__main__': # if using the local machine as the web server

	app.run_server(debug=True)