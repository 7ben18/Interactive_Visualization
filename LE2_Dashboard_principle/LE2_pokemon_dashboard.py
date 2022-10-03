#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Import modules
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# In[4]:


# reading pokemon_data.csv
df = pd.read_csv("pokemon_data.csv")

# print df head and tail
display(df.head(), df.tail())


# In[5]:


# print df info
display(df.info())


# In[6]:


# create total stats column
df['Total'] = df['HP'] + df['Attack'] + df['Defense'] + df['Sp. Atk'] + df['Sp. Def'] + df['Speed']

# print df head
display(df.head())

# display datatyp of total
display(df['Total'].dtypes)


# In[7]:


# create coloumn if pokemon is dual type
df['Dual Type'] = df['Type 2'].notnull()

# print df head
display(df.head())


# In[8]:


# create scatterplot attack vs defense, size = total stats, shape = dual type, color = type 1
sns.scatterplot(x = 'Attack', y = 'Defense', size = 'Total', hue = 'Type 1', style = 'Dual Type', data = df)

# adjust size of plot
plt.gcf().set_size_inches(10, 10)

# add labels
plt.xlabel('Attack', fontsize = 15)
plt.ylabel('Defense', fontsize = 15)
plt.title('Attack vs Defense', fontsize = 20)

# legend not on plot
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# add mean attack and defense lines
plt.axvline(df['Attack'].mean(), color = 'black')
plt.axhline(df['Defense'].mean(), color = 'black')

# show plot
plt.show()


# In[9]:


# create multiple scatterplots, split by legendary and generation
sns.relplot(x = 'Attack', y = 'Defense', size = 'Total', hue = 'Type 1', style = 'Dual Type', col = 'Legendary', row = 'Generation', data = df)

# adjust size of plot
plt.gcf().set_size_inches(10, 10)


# legend not on plot
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# add mean attack and defense thin lines in every subplot
for ax in plt.gcf().axes:
    ax.axvline(df['Attack'].mean(), color = 'black', alpha = 0.5)
    ax.axhline(df['Defense'].mean(), color = 'black', alpha = 0.5)

# label generation and legendary show once
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# show plot
plt.show()


# In[10]:


# rename coloumn name type 1 to primary type
df.rename(columns = {'Type 1': 'Primary Type'}, inplace = True)

# print df head
display(df.head())


# In[11]:


# make that plot interactive
from turtle import shape
import plotly.express as px

# create interactive scatterplot
fig = px.scatter(df, x = 'Attack', y = 'Defense', 
                 size = 'Total', color = 'Primary Type',
                 hover_name = 'Name', facet_col = 'Generation', facet_row = 'Legendary')

# add legend out of plot
fig.update_layout(legend=dict(x=1, y=1))

# adjust size of plot
fig.update_layout(width = 2000, height = 2000)

# show plot
fig.show()

# export plot to dashboard html
fig.write_html("LE2_pokemon_dashboard.html")


# In[12]:


# interactive scatterplot with plotly express
import plotly.express as px

# create interactive scatterplot, x = #, y = total, size = total, color = type 1, symbol = dual type, hover name = name
fig = px.scatter(df, x = '#', y = 'Total',
                    size = 'Total', color = 'Primary Type',
                    hover_name = 'Name')

# add legend out of plot
fig.update_layout(legend=dict(x=1, y=1))

# adjust size of plot
fig.update_layout(width = 2000, height = 1000)

# show plot
fig.show()

# export plot to dashboard html
fig.write_html("LE2_pokemon_total_id.html")


# In[13]:


# using dash and plotly express to make a pokemon dashboard
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# create dash app
app = dash.Dash(__name__)

# create layout
app.layout = html.Div([
    html.H1('Pokemon Dashboard'),
    html.H2('Pokemon Attack vs Defense'),
    dcc.Graph(figure = px.scatter(df, x = 'Attack', y = 'Defense',
                    size = 'Total', color = 'Primary Type',
                    hover_name = 'Name')),
    html.H2('Pokemon Attack vs Defense by Generation and Legendary'),
    dcc.Graph(figure = px.scatter(df, x = 'Attack', y = 'Defense',
                    size = 'Total', color = 'Primary Type',
                    hover_name = 'Name', facet_col = 'Generation', facet_row = 'Legendary')),
    html.H2('Pokemon Total Stats by ID'),
    dcc.Graph(figure = px.scatter(df, x = '#', y = 'Total',
                    size = 'Total', color = 'Primary Type',
                    hover_name = 'Name'))
])

# run app
if __name__ == '__main__':
    app.run_server(debug = False)

