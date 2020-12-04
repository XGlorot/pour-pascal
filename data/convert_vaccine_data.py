import numpy
import re

name = ['DTaP', 'Polio', 'MMR', 'Hib', 'Varicelle',
        'HepatB', 'HepatA','PCV', 'Rotavirus']

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

for nn in name:
  sep = ";"
  offset = 2
  f = open(nn + '.csv')
  header = f.readline().split(sep)[: -1]
  header_idx = numpy.nonzero([(i != '') * 1. for i in header])[0]
  age = f.readline().split(sep)[: -1]
  age_idx = numpy.nonzero([(i != '') * 1. for i in age])[0]
  title = f.readline().split(sep)[: -1]
  dd = {}
  c = f.readline()
  while c:
    parsed = c.split(sep)[: -1]
    location = parsed[0].replace(',', ' ')
    idx = 1
    while idx < len(header):
      if title[idx] == 'SAMPLE SIZE':
        idx += 2
      if idx >= len(header):
        break
      if title[idx] == 'DIFFERENCE TO PREVIOUS YEAR':
        idx += 1
      if idx >= len(header):
        break
      if (idx in header_idx):
        dose = re.sub('\W+','', header[idx]).replace(',', ' ')
        if dose[0] == ' ':
            dose = dose[1:]
      if (idx in age_idx):
        ag = age[idx].replace(',', ' ')
      year = int(title[idx])
      if (parsed[idx] != '') and (parsed[idx] != 'NaN') and (parsed[idx] != 'NA') :
        value = float(parsed[idx])
        if title[idx + 1] == 'LL':
          assert(title[idx + 1] == 'LL')
          LL = float(parsed[idx + 1])
          assert(title[idx + 2] == 'UL')
          UL = float(parsed[idx + 2])
          assert(title[idx + 4] == 'SAMPLE SIZE')
          SIZE = float(parsed[idx + 4])
          idx = idx + 6
        else:
          assert(title[idx + 1] == 'CI')
          if parsed[idx + 1] == 'NaN':
            LL = value - float(parsed[idx + 1])
            UL = value + float(parsed[idx + 1])
          else:
            LL = value - float(parsed[idx + 1][offset: -1])
            UL = value + float(parsed[idx + 1][offset: -1])
          if LL < 0.:
                LL = 0.
          if UL > 100.:
                UL = 100.
          assert(title[idx + 2] == 'SAMPLE SIZE')
          SIZE = float(parsed[idx + 2])
          idx = idx + 4
        if location in us_state_abbrev:
            dd[(dose, ag, us_state_abbrev[location], year)] = (value, LL, UL, SIZE)
      else:
        idx = idx + 4
    c = f.readline()
  f.close()
  f = open(nn + '_row.txt', 'w')
  f.write('Dose,Category,Location,Denominator,Coverage,Lower CI,Higher CI,Year\n')
  for i in dd:
    f.write('%s,%s,%s,%f,%f,%f,%f,%d\n'%(i[0], i[1], i[2], dd[i][3], dd[i][0], dd[i][1], dd[i][2], i[3]))
  f.close()
