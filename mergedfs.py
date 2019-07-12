import pandas as pd
import matplotlib.pyplot as plot

pop_df=pd.read_csv('population_state.csv')
pop_df.head()
ed_df=pd.read_csv('education_state.csv')
ed_df.head()
po_df=pd.read_csv('poverty_state.csv')
po_df.head()
unemp_df=pd.read_csv('umemp_state.csv')
unemp_df.head()


population_df=pd.DataFrame({'State':pop_df['State'], 'County':pop_df['Area_Name'],'population_2017':pop_df['POP_ESTIMATE_2017'],'Births_2017':pop_df['Births_2017'], 'Deaths_2017' : pop_df['Deaths_2017']})
population_df.head()
education_df=pd.DataFrame({'State':ed_df['Area name'], 'Uneducated':ed_df['Percent of adults with less than a high school diploma, 2012-2016']})
education_df.head()
poverty_df=pd.DataFrame({'State':po_df['Area_Name'], 'PovertyPercent_2017' : po_df['PCTPOVALL_2016']})
poverty_df.head()
unemployment_df=pd.DataFrame({'State':unemp_df['Area_name'], 'UnemploymentRate_2017' : unemp_df['Unemployment_rate_2017']})
unemployment_df.head()

df=pd.read_csv('notices_final.csv')

print(df.shape)
print(df.head())


notice_cnt=df.groupby(['county', 'category'],as_index=False).size()
##print(notice_cnt.head())
##notice_cnt.columns = notice_cnt.columns.get_level_values(0)
print(notice_cnt.head())

notice_unstacked=notice_cnt.unstack()

notice_unstacked=notice_unstacked.reset_index()

print(notice_unstacked.head())

counties = []
for index, row in notice_unstacked.iterrows():
    counties.append(row['county'])
print(counties)


population = []
births = []
deaths = []
for index1, row1 in population_df.iterrows():
        population.append(row1['population_2017'])
        births.append(row1['Births_2017'])
        deaths.append(row1['Deaths_2017'])

state_pop=pd.DataFrame(list(zip(counties, population)),
              columns=['county','population_2017'])
##state_pop
state_estimates=pd.DataFrame(list(zip(counties, population, births, deaths)),
              columns=['county','population_2017','Births_2017','Deaths_2017'])

total_estimates = pd.merge(state_estimates, notice_unstacked, on="state")
##print(total_estimates)


uneducated=[]
for index1, row1 in education_df.iterrows():
        uneducated.append(row1['Uneducated'])
state_estimates2=pd.DataFrame(list(zip(states, uneducated)),
              columns=['state','uneducated'])

total_estimates2 = pd.merge(state_estimates2, total_estimates, on="state")
print(total_estimates2)


pov=[]
for index1, row1 in poverty_df.iterrows():
        pov.append(row1['PovertyPercent_2017'])
state_estimates3=pd.DataFrame(list(zip(states, pov)),
              columns=['state','pov'])

total_estimates3 = pd.merge(state_estimates3, total_estimates2, on="state")
print(total_estimates3)

unemp=[]
for index1, row1 in unemployment_df.iterrows():
        unemp.append(row1['UnemploymentRate_2017'])
state_estimates4=pd.DataFrame(list(zip(states, unemp)),
              columns=['state','unemployment'])

total_estimates4 = pd.merge(state_estimates4, total_estimates3, on="state")
print(total_estimates4)
for col in total_estimates4.columns:
    print(col)

total_estimates4.to_csv('notice_data_with_variables.csv')