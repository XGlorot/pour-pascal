race = {1: 'White', 2: 'Black', 3: 'Indian', 4: 'Asian'}
origin = {0: 'Non-hispanic', 1: 'Hispanic'}
sex = {1: "Male", 2: "Female"}

def parse_sensus(ll):
  dd = dict()
  dd['year'] = int(ll[0:4])
  dd['fips'] = str(ll[6:11])
  dd['race'] = race[int(ll[13])]
  dd['origin'] = origin[int(ll[14])]
  dd['sex'] = sex[int(ll[15])]
  dd['age'] = int(ll[16:18])
  dd['pop'] = int(ll[18:])
  return dd

f = open("us.1990_2018.singleages.adjusted.txt")

census_dict = {}
l = f.readline()
while l:
  curr = parse_sensus(l)
  if curr['year'] >= 2000 and curr['year'] < 2018:
    if curr['age'] > 18:
      curr['age'] = 18
    if (curr['year'], curr['fips'], curr['age']) in census_dict:
      census_dict[(curr['year'], curr['fips'], curr['age'])] = [
        census_dict[(curr['year'], curr['fips'], curr['age'])][0] + curr['pop'],
        census_dict[(curr['year'], curr['fips'], curr['age'])][1] + 1]
    else:
      census_dict[(curr['year'], curr['fips'], curr['age'])] = [curr['pop'], 0]
  l = f.readline()
                                      
f = open('census.txt', 'w')
f.write('Year,Fips,Age,Population\n' )
for i in census_dict:
  f.write(str(i[0]) + ',' + i[1] + ',' + str(i[2]) + 
          ',' + str(census_dict[i][0])+'\n')
f.close()
