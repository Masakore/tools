if __name__ == '__main__':
  import csv
  import argparse
  #from decimal import *
  from random import uniform
  from random import randrange
  import re

  import pandas as pd
  import jaconv

  parser = argparse.ArgumentParser(description='csv to anonymise')
  parser.add_argument('file', help='csv file to import', action='store')
  args = parser.parse_args()
  csv_file = args.file

  df = pd.read_csv(csv_file, header=None).fillna("")
  match = df[0]
  field_name = df[1]
  movement = df[2]
  type = df[3]
  category = df[4]

  f = open("dictionary_ja.json", 'w')
  f.write("{ \n")
  f.write("  \"docs\": [\n")

  for i, m in enumerate(match):
    # rule = "{{\"doc_type\":\"{dict_filter}\"}}\n".format(dict_filter=i)
    l = 0 if field_name[i] == "tekiyocd" else 1
    field = "custom" if (field_name[i] == "tekiyocd" or field_name[i] == "mtree-category") else "description"

    lc = "\n" if i == (len(match) - 1) else ",\n"
    m = re.sub('\s{3,}', '', m)


    

    if field == "custom":
      rule = "    {{\"doc_type\":\"dict_filter\",\"level\":{level},\"country\":\"\",\"bank\":\"\",\"movement\":\"{movement}\",\"field\":\"{field}\",\"field_name\":\"{field_name}\",\"type\":\"{type}\",\"match\":\"{match}\",\"category\":\"{cat}\"}}{lc}".format(level=l,movement=movement[i],field=field,field_name=field_name[i],type=type[i],match=jaconv.h2z(m, kana=True),cat=category[i],lc=lc)
    else:
      rule = "    {{\"doc_type\":\"dict_filter\",\"level\":{level},\"country\":\"\",\"bank\":\"\",\"movement\":\"{movement}\",\"field\":\"{field}\",\"type\":\"{type}\",\"match\":\"{match}\",\"category\":\"{cat}\"}}{lc}".format(level=l,movement=movement[i],field=field,type=type[i],match=jaconv.h2z(m, kana=True),cat=category[i],lc=lc)

    f.write(rule)	

  f.write("  ]\n")
  f.write("}")
  f.close()