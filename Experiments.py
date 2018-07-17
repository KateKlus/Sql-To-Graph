import re


string = 'T1 inner join T2 on T1.K=T2.K'

tables_list = re.findall(r'\w+ join \w+ on', string)

print(tables_list)
