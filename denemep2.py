import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash
import requests
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from plotly.validators.scatter.marker import SymbolValidator
import GetAssessmentData
raw_symbols = SymbolValidator().values

# app = dash.Dash(__name__)
app = dash.Dash(__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
# Enable server when deploying?
server = app.server

#For Config URL - ALWAYS put the &download=1 at the back of the URL!
config_url = "https://liveuclac-my.sharepoint.com/:x:/g/personal/ucnvlra_ucl_ac_uk/ER6KfG1ItOZHgmFYLAY0Rx0Bkzqy5hk_m5PpWh2jwEafFw?rtime=LS6CAdCX2kg&download=1"
#config_url = "https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EdQL2DOzuCtCl9oCZRZ7DnkB-qMKbGCO2yve-4mw234wrw?e=cJ9XgX&download=1"
#config_url = "https://liveuclac-my.sharepoint.com/:x:/g/personal/ucnvlra_ucl_ac_uk/ER6KfG1ItOZHgmFYLAY0Rx0Bkzqy5hk_m5PpWh2jwEafFw&download=1"
config_df = GetAssessmentData.Get_Config_Data(config_url)

db_url = str(config_df.iloc[0,1])+str("&download=1")
df = GetAssessmentData.Get_Assessments_Data(db_url)

mods_url = str(config_df.iloc[1,1])+str("&download=1")
mods_df = GetAssessmentData.Get_Module_Data(mods_url)

#Defning dictionary for optional modules (to be used in conjunction with external module listing csv) # Not used anymore
#Not used anymore
IEPMinorMods = {
    'APCH':"CENG0014",
    'BIOE':'MPHY0005',
    'CNNC':'ELEC0017',
}

#Defining some dictionaries for the app layout
# Use Dash Serve Layout https://dash.plotly.com/live-updates
def servelayout():

    layout = html.Div(
        children=[
            dbc.Row(id='topbanner', children=[
                html.H1("UCL Mecheng Heat Map (2022-23)"),
                html.Div('''Hello and Welcome'''),
                ]),
            dbc.Row(id='mainbodyarea', children=[
                dbc.Col(id="sidebar", children=[
                html.P(''),
                html.Div(children='Click the links below for the Excel version', style={'padding':5}),
                #dcc.Link(html.A('Year 1'), href='/Year1.xlsm', title="Year 1"),
                html.A(className='button1', children='Year 1',
                       href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EW3X6Dl4PAxLmoQgCrJvntoBge0SQ5dVbiunT4CqtYVTdQ?e=7dsdoi'
                       ),
                html.A(className='button1', children='Year 2',
                       href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/ETp_pNWIpnFEkMOJYE4PPcwBtksvrJcJPARYpxOxeUDUog?e=uO6yr7',
                       style={'margin': '15px'}),
                html.A(className='button1', children='Year 3',
                       href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EXyLW9Rdz35CgMXn_9kNPKkB3yf4hga7Of8QIWWd-p-VyQ?e=kkMRJM',
                       style={'margin': '15px'}),
                html.A(className='button1', children='Year 4',
                       href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/ERPCoSgqXydDip2Rnz_60hcBcTgqEM8h6T51AN-G6xjdAA?e=0Zdbe6',
                       style={'margin': '15px'}),

                html.P(''),
                html.A(className='button1', children='Download Master Assessment Spreadsheet',
                       href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EchRSDhblL5MtFUDLBiFIVcBlnk-wyaHjWwecrb8CYoPKg?e=qghjcs'
                        ),

                html.H2("1)"),
                dcc.Dropdown(id='dropdown-year', options=[
                    {'label': 'Year 1 Pure', 'value': 'Y1MECH'},
                    {'label': 'Year 1 with Business Finance', 'value': 'Y1WBF'},
                    {'label': 'Year 2 Pure', 'value': 'Y2MECH'},
                    {'label': 'Year 2 with Business Finance', 'value': 'Y2WBF'},
                    {'label': 'Year 3 Pure', 'value': 'Y3MECH'},
                    {'label': 'Year 3 with Business Finance', 'value': 'Y3WBF'},
                    {'label': 'Year 4', 'value': 'Y4MECH'}],
                             value="Y1MECH", multi=False, searchable=True,
                             placeholder='Please select your programme and year.',
                             clearable=True),

                html.Div(id='dd-output-container-1'),

                html.H2("2)"),
                dcc.Dropdown(id='minor-guide', options=[
                    {'label': 'Applied Chemistry & Molecular Engineering', 'value': 'APCH'},
                    {'label': 'Biomedical Engineering', 'value': 'BIOE'},
                    {'label': 'Connected Systems', 'value': 'CNNC'},
                    {'label': 'Crime & Security Engineering', 'value': 'CRIM'},
                    {'label': 'Engineering and Public Policy', 'value': 'ENPP'},
                    {'label': 'Entrepreneurship', 'value': 'ENTR'},
                    {'label': 'Environmental Engineering', 'value': 'ENVI'},
                    {'label': 'Finance & Accounting', 'value': 'FINA'},
                    {'label': 'Intelligent Systems', 'value': 'INTL'},
                    {'label': 'Intermediate Modern Foreign Language', 'value': 'INFL'},
                    {'label': 'Management', 'value': 'MGMT'},
                    {'label': 'Modern Applications of Engineering Mathematics', 'value': 'ENGM'},
                    {'label': 'Nanotechnology', 'value': 'NANO'},
                    {'label': 'Ocean Engineering', 'value': 'OCEA'},
                    {'label': 'Application Programming For Data Science', 'value': 'PRDS'},
                    {'label': 'Regenerative Medicine', 'value': 'REGM'},
                    {'label': 'Strategic Thinking in Engineering and Technology', 'value': 'STRT'},
                    {'label': 'Sustainable Building Design', 'value': 'SUST'},
                    {'label': 'Nil', 'value': 'Nil'}],
                    value = "Nil", multi = False, searchable = True, placeholder = 'Please select your minor.',
                    clearable = True),

                html.Div(id='dd-output-container'),

                html.H2("3)"),
                dcc.Dropdown(id='dropdown-choice', multi=True,
                             options=[{'label': x, 'value': x} for x in sorted(df["Module Code "].unique())],
                             value=sorted(df["Module Code "].unique())),
                ], width=3),
                dbc.Col(id="GraphPane",children=[
                html.H4("Please choose your programme from the 1st dropdown menu. Then, choose your minor from the 2nd dropdown menu to see the related modules."
                        " Finally, add the optional modules in the 3rd dropdown menu."),

                #https://dash.plotly.com/live-updates use this to update dropdown in intervals!!
                dcc.Graph(id='graph-output', figure={}),


                ])
            ])
        ]
    )
    return layout

app.layout = servelayout

# app.layout = html.Div(
#     children=[
#         dbc.Row(id='topbanner', children=[
#             html.H1("UCL Mecheng Heat Map (2022-23)"),
#             html.Div('''Hello and Welcome'''),
#             ]),
#         dbc.Row(id='mainbodyarea', children=[
#             dbc.Col(id="sidebar", children=[
#             html.P(''),
#             html.Div(children='Click the links below for the Excel version', style={'padding':5}),
#             #dcc.Link(html.A('Year 1'), href='/Year1.xlsm', title="Year 1"),
#             html.A(className='button1', children='Year 1',
#                    href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EW3X6Dl4PAxLmoQgCrJvntoBge0SQ5dVbiunT4CqtYVTdQ?e=7dsdoi'
#                    ),
#             html.A(className='button1', children='Year 2',
#                    href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/ETp_pNWIpnFEkMOJYE4PPcwBtksvrJcJPARYpxOxeUDUog?e=uO6yr7',
#                    style={'margin': '15px'}),
#             html.A(className='button1', children='Year 3',
#                    href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EXyLW9Rdz35CgMXn_9kNPKkB3yf4hga7Of8QIWWd-p-VyQ?e=kkMRJM',
#                    style={'margin': '15px'}),
#             html.A(className='button1', children='Year 4',
#                    href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/ERPCoSgqXydDip2Rnz_60hcBcTgqEM8h6T51AN-G6xjdAA?e=0Zdbe6',
#                    style={'margin': '15px'}),
#
#             html.P(''),
#             html.A(className='button1', children='Download Master Assessment Spreadsheet',
#                    href='https://liveuclac-my.sharepoint.com/:x:/g/personal/zcemyta_ucl_ac_uk/EchRSDhblL5MtFUDLBiFIVcBlnk-wyaHjWwecrb8CYoPKg?e=qghjcs'
#                     ),
#
#             html.H2("1)"),
#             dcc.Dropdown(id='dropdown-year', options=[
#                 {'label': 'Year 1 Pure', 'value': 'Y1MECH'},
#                 {'label': 'Year 1 with Business Finance', 'value': 'Y1WBF'},
#                 {'label': 'Year 2 Pure', 'value': 'Y2MECH'},
#                 {'label': 'Year 2 with Business Finance', 'value': 'Y2WBF'},
#                 {'label': 'Year 3 Pure', 'value': 'Y3MECH'},
#                 {'label': 'Year 3 with Business Finance', 'value': 'Y3WBF'},
#                 {'label': 'Year 4', 'value': 'Y4MECH'}],
#                          value="Y1MECH", multi=False, searchable=True,
#                          placeholder='Please select your programme and year.',
#                          clearable=True),
#
#             html.Div(id='dd-output-container-1'),
#
#             html.H2("2)"),
#             dcc.Dropdown(id='minor-guide', options=[
#                 {'label': 'Applied Chemistry & Molecular Engineering', 'value': 'APCH'},
#                 {'label': 'Biomedical Engineering', 'value': 'BIOE'},
#                 {'label': 'Connected Systems', 'value': 'CNNC'},
#                 {'label': 'Crime & Security Engineering', 'value': 'CRIM'},
#                 {'label': 'Engineering and Public Policy', 'value': 'ENPP'},
#                 {'label': 'Entrepreneurship', 'value': 'ENTR'},
#                 {'label': 'Environmental Engineering', 'value': 'ENVI'},
#                 {'label': 'Finance & Accounting', 'value': 'FINA'},
#                 {'label': 'Intelligent Systems', 'value': 'INTL'},
#                 {'label': 'Intermediate Modern Foreign Language', 'value': 'INFL'},
#                 {'label': 'Management', 'value': 'MGMT'},
#                 {'label': 'Modern Applications of Engineering Mathematics', 'value': 'ENGM'},
#                 {'label': 'Nanotechnology', 'value': 'NANO'},
#                 {'label': 'Ocean Engineering', 'value': 'OCEA'},
#                 {'label': 'Application Programming For Data Science', 'value': 'PRDS'},
#                 {'label': 'Regenerative Medicine', 'value': 'REGM'},
#                 {'label': 'Strategic Thinking in Engineering and Technology', 'value': 'STRT'},
#                 {'label': 'Sustainable Building Design', 'value': 'SUST'},
#                 {'label': 'Nil', 'value': 'Nil'}],
#                 value = "Nil", multi = False, searchable = True, placeholder = 'Please select your minor.',
#                 clearable = True),
#
#             html.Div(id='dd-output-container'),
#
#             html.H2("3)"),
#             dcc.Dropdown(id='dropdown-choice', multi=True,
#                          options=[{'label': x, 'value': x} for x in sorted(df["Module Code "].unique())],
#                          value=sorted(df["Module Code "].unique())),
#             ], width=3),
#             dbc.Col(id="GraphPane",children=[
#             html.H4("Please choose your programme from the 1st dropdown menu. Then, choose your minor from the 2nd dropdown menu to see the related modules."
#                     " Finally, add the optional modules in the 3rd dropdown menu."),
#
#             #https://dash.plotly.com/live-updates use this to update dropdown in intervals!!
#             dcc.Graph(id='graph-output', figure={}),
#
#
#             ])
#         ])
#     ]
# )

@app.callback(
    Output(component_id='graph-output', component_property='figure'),
    [Input(component_id='dropdown-choice', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(val_chosen):
    if len(val_chosen) > 0:
        print(f"value user chose: {val_chosen}")
        print(type(val_chosen))
        dff = df[df["Module Code "].isin(val_chosen)]
        fig = px.scatter(dff, x='Deadline Date', y="Module Code ", size="Assessment Weighting (%)", hover_name="Module Title"
                 , opacity=1,color="Module Title", hover_data=['Module Code ','Assessment Name','Deadline Date',
                                                               'Assessment Weighting (%)',"Assessment Type"])

        #This part is still waiting on us to confirm the overall assessment types before coding it up
        #implement formative code - the assessemtn weighting column is = zero

        #df_formative = dff[dff['Assessment Type'].str.contains('formative', na=False)]  # Assessment Type 1: Formative Assessment
        #Getting list of formative assessments
        df_formative = dff[dff["Assessment Weighting (%)"] == 0]
        # 2 = Diamond Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_formative["Deadline Date"], y=df_formative["Module Code "], marker_symbol=2,
                marker=dict(color='rgba(400,400,400, 0.5)', size=10, line=dict(color='Black', width=2)), showlegend=False,
                hoverinfo='skip'))

        df_quiz = dff[dff['Assessment Type'].str.contains('Quiz', na=False)]  # Assessment Type 2: Quiz
        # 23 = Diamond Tall Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_quiz["Deadline Date"], y=df_quiz["Module Code "], marker_symbol=23,
                marker=dict(size=df_quiz["Assessment Weighting (%)"]), showlegend=False, hoverinfo='skip'))

        df_exam = dff[dff['Assessment Type'].str.contains('Exam', na=False)]  # Assessment Type 3: Exam
        # 17 = Star Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_exam["Deadline Date"], y=df_exam["Module Code "], marker_symbol=17,
                marker=dict(size=20), showlegend=False, hoverinfo='skip'))

        df_peer = dff[dff['Assessment Type'].str.contains('Peer Review', na=False)]  # Assessment Type 4: Peer Review
        # 3 = Cross Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_peer["Deadline Date"], y=df_peer["Module Code "], marker_symbol=3,
                marker=dict(size=df_peer["Assessment Weighting (%)"]), showlegend=False, hoverinfo='skip'))

        df_gcw = dff[dff['Assessment Type'].str.contains('Group Coursework', na=False)]  # Assessment Type 5: Group Coursework
        # 200 = Circle_Dot Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_gcw["Deadline Date"], y=df_gcw["Module Code "], marker_symbol=200,
                marker=dict(size=df_gcw["Assessment Weighting (%)"]), showlegend=False, hoverinfo='skip'))

        df_lab = dff[dff['Assessment Type'].str.contains('Lab Report', na=False)]  # Assessment Type 6: Lab Report
        # 22 = Star Diamond Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_lab["Deadline Date"], y=df_lab["Module Code "], marker_symbol=22,
                marker=dict(size=df_lab["Assessment Weighting (%)"]), showlegend=False, hoverinfo='skip'))

        df_pres = dff[dff['Assessment Type'].str.contains('Presentation', na=False)]  # Assessment Type 7: Presentation
        # 18 = Hexagram Shape
        fig.add_trace(
            go.Scatter(
                mode='markers', x=df_pres["Deadline Date"], y=df_pres["Module Code "], marker_symbol=18,
                marker=dict(size=df_pres["Assessment Weighting (%)"]), showlegend=False, hoverinfo='skip'))

        return fig

    elif len(val_chosen) == 0:
        raise dash.exceptions.PreventUpdate


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('minor-guide', 'value'),
    dash.dependencies.Input('dropdown-year', 'value')
     ])

def update_output(IEPMinor, ProgramYear):
    #Find the correct modules from Mods_df!
    return_mods = []
    my_chosen_prog = " "
    print("Programme Year:" , ProgramYear)
    print("Minor Chosen: ", IEPMinor)
    #my_chosen_prog = mods_df.loc[(mods_df['Minor Code'] == IEPMinor)]
    #my_chosen_prog = mods_df.get_locs([slice(None), [IEPMinor, ProgramYear]])
    try:
        my_chosen_prog = mods_df.loc[(ProgramYear, IEPMinor),:] #see stackoverflow: Select rows in pandas MultiIndex DataFrame
        print(my_chosen_prog)

        if ProgramYear == "Y2MECH":
            return_mods = my_chosen_prog.loc["Module 8"]
        elif ProgramYear == "Y3MECH":
            return_mods = [my_chosen_prog.loc["Module 5"],my_chosen_prog.loc["Module 6"]]
        else:
            print("Man's not on a pure course")

    except:
        print("Some problem when selecting optional modules and handling programmes")

    return 'The optional modules are "{}"'.format(return_mods)

@app.callback(
    dash.dependencies.Output('dropdown-choice', 'value'),
    [dash.dependencies.Input('dropdown-year', 'value')],
    dash.dependencies.Input('minor-guide', 'value')
    )

def update_mods_taken(chosen_program, minorvalue):

    modlist = []
    print(chosen_program)
    print(minorvalue)
    try:
        selected_mods = mods_df.loc[[(chosen_program,minorvalue)]]
    except:
        print("There was an error filtering the module dataframe - jeny")
        modlist = []
        print(modlist)
        return modlist

    print(selected_mods)

    modlist = selected_mods.iloc[0]['ProgramMods'].split(',')
    print(modlist)
    return modlist
#     df_minor = df
#     df_minor = df[df['Course'].str.contains('Minor', na=False)]
#
#     df_core = df
#     df_core = df[df['Course'].str.contains('Core', na=False)]
#
#     df_y4_core = df_core[df_core['Year'].isin([4])]
#
#     df_y3_core = df_core[df_core['Year'].isin([3])]
#     df_y3_core_wbf = df_y3_core[df_y3_core['Combined'].str.contains('WBF', na=False)]
#     df_y3_core_mech = df_y3_core[df_y3_core['Combined'].str.contains('MECH', na=False)]
#
#     df_y2_core = df_core[df_core['Year'].isin([2])]
#     df_y2_core_wbf = df_y2_core[df_y2_core['Combined'].str.contains('WBF', na=False)]
#     df_y2_core_mech = df_y2_core[df_y2_core['Combined'].str.contains('MECH', na=False)]
#
#     df_y1_core = df_core[df_core['Year'].isin([1])]
#     df_y1_core_wbf = df_y1_core[df_y1_core['Combined'].str.contains('WBF', na=False)]
#     df_y1_core_mech = df_y1_core[df_y1_core['Combined'].str.contains('MECH', na=False)]
#
#     df_zero = df
# #Handle different Years
#     print(minorvalue)
#     if chosen_program == 'Y3WBF':
#         print("TRALALALALALA")
#         minors = ""
#         if minorvalue != None:
#             minors = minorvalue.split(", ")
#         print(minors)
#         modslist = np.ndarray.tolist(np.append(df_y3_core_wbf.ModuleCode.unique(), minors))
#         print(modslist)
#
#         return modslist
#     elif chosen_program == 'Y4MECH':
#         print("OOMPALOOMPA")
#         modslist = np.append(df_y4_core.ModuleCode.unique(), minorvalue)
#         print(modslist, type(modslist))
#         return sorted(df_y4_core.ModuleCode.unique())
#     elif chosen_program == 'Y3MECH':
#         return sorted(df_y3_core_mech.ModuleCode.unique())
#     elif chosen_program == 'Y2WBF':
#         return sorted(df_y2_core_wbf.ModuleCode.unique())
#     elif chosen_program == 'Y2MECH':
#         return sorted(df_y2_core_mech.ModuleCode.unique())
#     elif chosen_program == 'Y1WBF':
#         return sorted(df_y1_core_wbf.ModuleCode.unique())
#     elif chosen_program == 'Y1MECH':
#         return sorted(df_y1_core_mech.ModuleCode.unique())
#     else:
#         pass


if __name__ == '__main__':
    app.run_server(debug=True) #run_server might be depreciated
    #figure out dash update on page load
    #https://dash.plotly.com/live-updates