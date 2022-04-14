import csv
import pandas as pd
import re


#the cleaner will probably be different for each org, but this is an idea of how to clean the data
data = open('data.csv', "r")
csvReader = csv.reader(data)
df = pd.DataFrame(csvReader, columns =['Name','LinkedIn link', 'Sub-titles', 'Bio', 'Major', 'SIC Roles'])
firstColumn = df.iloc[:,0]
listClean = []

for element in firstColumn:
    strippedElement= element.replace('\n','')
    strippedElement = strippedElement.replace('  ', '\t')
    splitedElement = re.split(r'\t+', strippedElement)
    if len(splitedElement) > 2:
        splitedElement[1] = splitedElement[1]+splitedElement[2]
        splitedElement.pop(2)
    listClean.append(splitedElement)

df.drop('Name', axis=1, inplace=True)
dfName = pd.DataFrame(listClean, columns=['Name', 'Pronouns'])
dfClean = pd.concat([dfName,df], axis=1)
dfClean.drop(index=df.index[0], axis=0, inplace=True)

majorList = []
for item in dfClean.iloc[:,5]:
    if item != 'N/A':
        item = item[:len(item) // 2]
    else:
        item = item
    majorList.append(item)

SICRolesList = []
for item in dfClean.iloc[:,6]:
    if item != 'N/A':
        item = item[:len(item) // 2]
    else:
        item = item
    SICRolesList.append(item)

SICRolesDirty = dfClean.columns[6]
dfClean.drop(SICRolesDirty, axis=1, inplace=True)
dfClean[SICRolesDirty]=SICRolesList

majorDirty = dfClean.columns[5]
dfClean.drop(majorDirty, axis=1, inplace=True)
dfClean[majorDirty]=majorList

print(dfClean)
dfClean.to_csv('data.csv', index=False)




