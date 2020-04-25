######################################################
# Project: Project_3
# UIN: 659811790
# repl.it URL: https://repl.it/@egutie39/cs111project3
######################################################

#!/bin/python3

import urllib.request
import json
import csv
#this py file holds covid_data
from covid_data import covid_data


response = urllib.request.urlopen("https://raw.githubusercontent.com/pomber/covid19/master/docs/countries.json ")

contents = response.read()

data = json.loads(contents)


# Formating of 'data' --------------------------------------------------------
# data is dictionary that holds dictionaries..
# with the keys being the country
#length is 252
# print(data)
# Then that Country's dictionary looks like..
# {'flag': '🇺🇸', 'code': 'US'}

# ---- !!!!!!!! ----
# One of Countrys do not have the 'code' key
# "Cruise Ship" is the "Country" key with no 'code' key

# ctr=0
# for i in data:
#   if 'code' in data[i].keys():
#     print(data[i]['code'])
#   else:
#     ctr+=1
#     print(data[i])


################################################



# local 'country_codes.csv' file -----------------------------------------------

#'rt' will use the system default encoding, 
# ..which tends to be UTF8
f = open('country_codes.csv','rt')

content = csv.reader(f,skipinitialspace=True)

country_data = {}

#keys will hold the header of country_codes.csv file
keys = []
ctr = 0

for i in content:
  if ctr == 0:
    keys = i #keys will equal the headers
  else:
    country_dict = {} #a temp dict, will be overwritten..
    # every iteration
    for j in range(len(keys)):
      country_dict[keys[j]] = i[j] #One country's data set
      
    # we put the country's data in the main dict..
    # with country 'alpha-2 code' being the key of retrival
    country_data[country_dict['Alpha-2 code']] = country_dict

  ctr+=1

f.close()

################################################



# local population_data -------------------------------------------------------
g = open('population_data.csv','rt')
content = csv.reader(g, skipinitialspace=True)

pop_data = {}

keys = []
ctr = 0 

for i in content:
  if ctr == 0:
    keys = i
  else:
    pop_dict = {}
    for j in range(len(keys)):
      pop_dict[keys[j]] = i[j]
    
    #keys will be the 2 letter code mentioned csv file
    pop_data[pop_dict['Country Code']] = pop_dict

  ctr+=1
g.close()

################################################



# Formating of 'pop_2018' -----------------------------------------------------

# pop_2018 holds the countries that are both in 'covid_data' and 'population_data.csv'
# ... It is a list of tuples holding the country name and its population in 2018
# ... population number gotten from 'population_data.csv' 
# example: ('Australia', '24982688')

pop_2018 = []
for i in data:
  if 'code' in data[i].keys() and i in covid_data.keys():
    
    # print(i)
    two_code = data[i]['code']
      
    if two_code in country_data.keys() and i in covid_data.keys():
      
      # print(country_data[two]['Alpha-3 code'])
      three_code = country_data[two_code]['Alpha-3 code']

      if three_code in pop_data.keys() and i in covid_data.keys():
        # print(i)
        solo_tuple = (i,pop_data[three_code]['2018'])
        pop_2018.append(solo_tuple)

  else:
    continue

###########################################################



# function highPerCapital(date) ------------------------------------------------
# this function returns a tuple of the country name and it's per capita percentage

def highPerCapital(date):
  """ date is in YYYY-MM-DD format, date MUST mirror covid_data's own date entries, returns a tuple """

  high_capita = 0.0
  high_capita_con = ""

  for i in pop_2018:
    for j in range(len(covid_data[i[0]])):
      try:
        if covid_data[i[0]][j]['date'] == date and int(i[1]) >=100000:
          confirms = float(covid_data[i[0]][j]['confirmed'])
          pop = float(i[1])

          per = confirms / pop
          
          if high_capita <= per:
            high_capita = per
            high_capita_con = i[0]

      except ValueError:
        print('\nNo 2018 data for',i[0])


  percent_high_capita = high_capita * 100
  result = "{:.4f}".format(percent_high_capita)

  return high_capita_con,result

###########################################################





# main -----------------------------------------------------------
def main():

  #file holding answers
  my_file = open('project3_659811790.txt','w')


  #1 - 4. Which country took the fewest/highest days to go from 100 (or more) cases to 10,000 or more cases? How many days was that?

  days_100_to_10000 = []

  for c in covid_data:
    first_i_over_100 = 0
    first_i_over_10000 = 0

    # loop the dates
    for i in range(len(covid_data[c])):
      
      # first index over 100
      if first_i_over_100 == 0:
        if int(covid_data[c][i]['confirmed']) > 100:
          first_i_over_100 = i
      
      # first index over 10000
      if first_i_over_10000 == 0:
        if int(covid_data[c][i]['confirmed']) > 10000:
          first_i_over_10000 = i
      
      num_days = first_i_over_10000 - first_i_over_100
    
    if(num_days > 0):
      days_100_to_10000.append((c,num_days))
  
  lst_sorted = sorted(days_100_to_10000 , key=lambda item: item[1])

  #first index holds name and days of country with the fewest cases
  few_days = lst_sorted[0][1]
  country_few_days = lst_sorted[0][0]

  print(few_days)
  print(country_few_days)

  my_file.write(str(few_days))
  my_file.write('\n')
  my_file.write(country_few_days)
  my_file.write('\n')

  print()

  #last index holds name and days of the country with the most cases
  most_days = lst_sorted[-1][1]
  country_most_days = lst_sorted[-1][0]

  print(most_days)
  print(country_most_days)

  my_file.write(str(most_days))
  my_file.write('\n')
  my_file.write(country_most_days)
  my_file.write('\n')


  # ----------------------------------------------------- #

  #5.On February 10, 2020, which country had the highest per-capita infection percentage?

  #AND

  #6. What was that percentage?

  
  feb_10 = highPerCapital('2020-2-10')
  
  #country name
  print(feb_10[0])
  my_file.write(feb_10[0])
  my_file.write('\n')

  #percentage
  print(feb_10[1])
  my_file.write(feb_10[1])
  my_file.write('\n')
    

  # ----------------------------------------------------- #

  #7. On March 10, 2020, which country had the highest per-capita infection percentage?

  #AND

  #8. What was that percentage?

  mar_10 = (highPerCapital('2020-3-10'))

  #country name
  print(mar_10[0])
  my_file.write(mar_10[0])
  my_file.write('\n')

  #percentage
  print(mar_10[1])
  my_file.write(mar_10[1])
  my_file.write('\n')


  # ----------------------------------------------------- #

  #9. On April 10, 2020, which country had the highest per-capita infection percentage?

  #AND

  #10. What was that percentage?

  april_10 = (highPerCapital('2020-4-10'))

  #country name
  print(april_10[0])
  my_file.write(april_10[0])
  my_file.write('\n')

  #percentage
  print(april_10[1])
  my_file.write(april_10[1])
  my_file.write('\n')


  # ----------------------------------------------------- #

  
main()