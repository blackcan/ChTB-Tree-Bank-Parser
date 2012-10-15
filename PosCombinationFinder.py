# -*- coding:utf-8 -*-

#利用TreeBankParser解析完TreeBank後，統計所有片語的POS Tag組合

import os, json
from TreeBankParser import TreeBankParser


fileList = []
def VisitFiles(fileList, dirName, files):
    for file in files:
        if os.path.splitext(file)[-1] == '.fid':
            fileList.append(file)
os.path.walk('./Data/', VisitFiles, fileList)

finalList = {}

#使用遞迴找出所有child的pos tags
def findChild (sentenceTree, cid):
    result = []
    if type(sentenceTree[cid][3]) == list:
        for childID in sentenceTree[cid][3]:
            result.extend(findChild(sentenceTree, childID))
    else:
        result.extend([sentenceTree[cid][2]])
    return result

for file in fileList:
    readDoc = open('./Data/' + file, 'r')
    parseTree = TreeBankParser(readDoc.read().decode('utf-8', 'ignore'))
    for sID in parseTree.tree.keys():
        for cID in parseTree.tree[sID].keys():
            content = parseTree.tree[sID][cID]
            if type(content[3]) == list and content[2] != 'S':
                posListString = '|'.join(findChild(parseTree.tree[sID], cID))
                if not content[2] in finalList:
                    finalList[content[2]] = {posListString:1}
                else:
                    if posListString not in finalList[content[2]]:
                        finalList[content[2]][posListString] = 1 
                    else:
                        finalList[content[2]][posListString] += 1
    print file 

writeFile = open('result.txt', 'w')
writeFile.close()
writeFile = open('result.txt', 'a')
for phrase in finalList.keys():
    writeFile.write(phrase + '\n')
    for posString in finalList[phrase]:
        writeFile.write(posString + ': ' + str(finalList[phrase][posString]) + '\n')
    writeFile.write('\n')
    
writeFile.close()
writeFile = open('result_json.txt', 'w')
writeFile.write(json.dumps(finalList))
