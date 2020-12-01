import numpy
name = ['polio', 'dtap', 'polio', 'MMR', 'Hib', 'varicelle',
        'hepatB', 'hepatA','PCV', 'rotavirus']

for nn in name:
  sep = ";"
  offset = 2
  f = open(nn + '.csv')
  header = f.readline().split(sep)[:-1]
  header_idx = numpy.nonzero([(i != '')*1. for i in header])[0]
  age = f.readline().split(sep)[:-1]
  age_idx = numpy.nonzero([(i != '')*1. for i in age])[0]
  title = f.readline().split(sep)[:-1]
  dd = {}
  c = f.readline()
  while c:
    parsed = c.split(sep)[:-1]
    location = parsed[0].replace(',', ' ')
    idx = 1
    while idx < len(header):
      if (idx in header_idx):
        dose = header[idx][1:].replace(',', ' ')
      if (idx in age_idx):
        ag = age[idx].replace(',', ' ')
      if title[idx] == 'SAMPLE SIZE':
        idx += 2
      if idx >= len(header):
        break
      if title[idx] == 'DIFFERENCE TO PREVIOUS YEAR':
        idx += 1
      if idx >= len(header):
        break
      year = int(title[idx])
      if (parsed[idx] != '') and (parsed[idx] != 'NaN') and (parsed[idx] != 'NA') :
        value = float(parsed[idx])
        if title[idx+1] == 'LL':
          assert(title[idx+1] == 'LL')
          LL = float(parsed[idx+1])
          assert(title[idx+2] == 'UL')
          UL = float(parsed[idx+2])
          assert(title[idx+4] == 'SAMPLE SIZE')
          SIZE = float(parsed[idx+4])
          idx = idx + 6
        else:
          assert(title[idx+1] == 'CI')
          if parsed[idx+1] == 'NaN':
            LL = value - float(parsed[idx+1])
            UL = value + float(parsed[idx+1])
          else:
            LL = value - float(parsed[idx+1][offset:-1])
            UL = value + float(parsed[idx+1][offset:-1])
          assert(title[idx+2] == 'SAMPLE SIZE')
          SIZE = float(parsed[idx+2])
          idx = idx + 4
        dd[(dose, ag, location, year)] = (value, LL, UL, SIZE)
      else:
        idx = idx + 4
    c = f.readline()
  f.close()
  f = open(nn + '_row.txt', 'w')
  f.write('dose,category,location,year,coverage,low,high,size\n')
  for i in dd:
    f.write('%s,%s,%s,%d,%f,%f,%f,%f\n'%(i[0], i[1], i[2], i[3], dd[i][0], dd[i][1], dd[i][2], dd[i][3]))
  f.close()
