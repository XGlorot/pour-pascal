import re
import numpy

filenames = {'ctyxcty_age_us.txt': 'StateFlow200610.txt', 'CtyxCty_ager_US.txt': 'StateFlow201116.txt'}

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
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
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}

for n in filenames:
  f = open(n)

  flow_in = {}
  flow_out = {}

  line = f.readline()
  while line:
    state_fips_in, county_fips_in, state_fips_out, county_fips_out = (
        line[0: 3], line[3: 6], line[6: 9], line[9: 12])
    age_group = line[13: 15]

    if age_group in ["01", "02"]:
      subline_in = line[15: 194]

      state_in = subline_in[:30]
      state_in = re.split(' *$', state_in)[0]
      county_in = subline_in[30:]
      county_in = re.split('[0-9 .]+$', county_in)[0]
      stats_in = [i for i in subline_in[30:][len(county_in):].split(' ')
                  if i != '']

      subline_out = line[195: 374]
      state_out = subline_out[:30]
      state_out = re.split(' *$', state_out)[0]
      county_out = subline_out[30:]
      county_out = re.split('[0-9 .]+$', county_out)[0]
      stats_out = [i for i in subline_out[30:][len(county_out):].split(' ')
                   if i != '']

      if county_fips_in.isdigit() and state_fips_in.isdigit():
        if (state_in, county_in, age_group) in flow_in:
          assert stats_in == flow_in[(state_in, county_in, age_group)]
        else:
          flow_in[(state_in, county_in, age_group)] = stats_in
      if county_fips_out.isdigit() and state_fips_out.isdigit():
        if (state_fips_out, county_fips_out, age_group) in flow_out:
          assert stats_out == flow_out[(state_out, county_out, age_group)]
        else:
          flow_out[(state_out, county_out, age_group)] = stats_out
    line = f.readline()

  tot_in = {}
  tot_out = {}
  tot_current = {}

  for key in flow_in:
    if not(key[0] in tot_in):
      tot_in[key[0]] = [0, 0, 0, 0]
      tot_current[key[0]] = [0, 0]
    for idx in range(4):
      tot_in[key[0]][idx] += int(flow_in[key][idx + 10]
                                 if flow_in[key][idx + 10] != '.' else 0)
    for idx in range(2):
      tot_current[key[0]][idx] += int(flow_in[key][idx])

  for key in flow_out:
    if not(key[0] in tot_out):
      tot_out[key[0]] = [0, 0]
    for idx in range(4):
      tot_out[key[0]][idx%2] += int(flow_out[key][idx + 10]
                                 if flow_out[key][idx + 10] != '.' else 0)

  f = open(filenames[n], 'w')
  f.write('Location,Population 1-17,Population 1-17 CI,'
          'State Flow In,State Flow In CI,Int. Flow In, Int. Flow In CI,'
          'State Flow Out,State Flow Out CI\n')
  for key in tot_current:
    f.write('%s,%d,%d,%d,%d,%d,%d,%d,%d\n'%(
        us_state_abbrev[key], tot_current[key][0], tot_current[key][1],
        tot_in[key][0],tot_in[key][1],tot_in[key][2],tot_in[key][3],
        tot_out[key][0],tot_out[key][1]))
