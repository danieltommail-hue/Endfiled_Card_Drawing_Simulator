import os
import pandas as pd

abs_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
write_path=os.path.join(abs_path,'data','standard','acquisition_center','default.csv')
read_path=os.path.join(abs_path,'data','standard','acquisition_center','content.csv')

reader=pd.read_csv(read_path)
reader=reader.fillna(0)

contents=reader.to_dict(orient='records')

reader=pd.read_csv(write_path)
reader=reader.fillna(0)

goods=reader.to_dict(orient='records')

for content,good in zip(contents,goods):
    temp={}
    for key,value in content.items():
        if key!='name':
            temp[key]=value
    good['content']=temp

writer=pd.DataFrame(goods,columns=['name','type','cost','cost_type','gained','limit','content','content_in_text','path'])
writer.to_csv(write_path,index=False)
print('finish')