# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 13:05:10 2016

@author: home
"""

import numpy as np
import json
import re
import timeit
from pprint import pprint

bTestMode = False

if(bTestMode):
    productsFileName = 'products.txt';#'test.json'
    listingFileName = 'listings_Test.txt';
else:
    productsFileName = 'products.txt';
    listingFileName = 'listings.txt';

products = []
prodStr = []
prodBrands = []
prodModels = []
prodListings = []
    
def GetProduct(searchStr):
    maxCount = 0;
    maxIndex = 0;
    ind = 0;
    
    title = searchStr["title"].lower();
    
    # Ignore 'for' for now
    if('for' in title):
        index = title.index('for');
        title = title[0:index-1];
        
    titleSplit = re.split("-|_| ", title);
    manufac = re.split("-|_| ", searchStr["manufacturer"].lower());  
    
    for productStr in prodStr:
        ind += 1;
        cnt = 0;

        # split the brand string, as it contains country, etc. sometimes
        #brandStr = re.split("-|_| ", str(products[ind-1]['manufacturer']).lower());   
        if(manufac[0] != prodBrands[ind-1][0]):
            continue;

        #modelStr = str(products[ind-1]['model']).lower()
        mAll = prodModels[ind-1]
        model = mAll[0];#re.split("-|_| ", modelStr);
        
#        if(ind == 466):
#            xy = ind;
        
        m1 = mAll[1]#" ".join(model);
        m2 = mAll[2]#"_".join(model);
        m3 = mAll[3]#"-".join(model);
        m4 = mAll[4]#"".join(model);
        #modelAll = [m1, m2, m3]
        bModelPresent = (m1 in title) or (m2 in title) or (m3 in title) or (m4 in title)
        
       
        if(not bModelPresent):     #all the model strings must be present in listing
            continue;        

        mIndex = title.index(model[0]);
        if(title[mIndex-1] != ' '):
            continue;               # this means model id is not present as separate word
        
        for s in productStr:
            if(s in title):
                cnt+=1;
        
        # Since long product titles will have more count, normalize it
        cnt = cnt/float(len(productStr))
        #print cnt
        if(maxCount < cnt):
            maxCount = cnt;
            maxIndex = ind;
            
    return maxIndex;

with open(productsFileName) as data_file:
    
    for ln in data_file:
        prData = json.loads(ln);
        products.append(prData);
        
        st = prData['product_name'].lower()
        prodStr.append(re.split("-|_|,", st));

        brandStr = re.split("-|_| ", str(prData['manufacturer']).lower());
        prodBrands.append(brandStr);
        
        modelStr = str(prData['model']).lower()
        model = re.split("-|_| ", modelStr);

        m1 = " ".join(model);
        m2 = "_".join(model);
        m3 = "-".join(model);
        m4 = "".join(model);        
        mAll = [model, m1, m2, m3, m4]
        prodModels.append(mAll);
        
        prodListings.append({'product_name': prData['product_name'], 'listings' : []})
        
    #products = [json.loads(p) for p in data_file]
    #prodListings = [{'product_name': p['product_name']} for p in products]

if bTestMode:
    testOpFile = open('TestOutput.txt', 'wb');

with open(listingFileName) as testFile:
    testIndex = 0;    
    
    for ln in testFile:
        testIndex += 1
        dat = json.loads(ln);
        
        T1 = timeit.default_timer()
        prId = GetProduct(dat);
        T2 = timeit.default_timer()
        
        if(prId > 0):
            prodListings[prId-1]['listings'].append(dat);
        if bTestMode:
            testOpFile.write(str(prId) + "\n")
        
        if(testIndex % 1000 == 0):
            print testIndex, 'T(ms):', (T2-T1)*1e3

if bTestMode:   
    testOpFile.close()

with open('OutputData.txt', 'wb') as opFile:
    #json.dump(prodListings, opFile)
    bFirstTime = True;
    for prod in prodListings:
        s = json.dumps(prod);
        if(not bFirstTime):
            opFile.write("\n")
        opFile.write(s)
        bFirstTime = False;
        
print 'Output is stored in file: OutputData.txt'
    
