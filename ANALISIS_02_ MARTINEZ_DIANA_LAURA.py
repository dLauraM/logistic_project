from collections import defaultdict
import csv
import pandas as pd

synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])

def openFile():
    file = open('synergy_logistics_database.csv', 'r', encoding='utf-8')
    csvreader = csv.reader(file)
    header = next(csvreader)
    # print(header)
    return file, csvreader


def createDirectionLists(csvreader):
    rows = []
    imports = []
    exports = []
    for index, row in enumerate(csvreader):
        # print(row[1])
        if row[1] == 'Exports':
            exports.append(row)
        else:
            imports.append(row)
        rows.append(row)
    return rows, imports, exports


def sortListByTotalValue(List):
    return (sorted(List, key=lambda x: x[9]))


def writeSortedLists(imports, exports):
    foutput = open("imports.txt", "w")
    sortedList = sortListByTotalValue(imports)
    for row in sortedList:
        foutput.write("%s\n" % row)
    foutput.close()

    foutput = open("exports.txt", "w")
    sortedList = sortListByTotalValue(exports)
    for row in sortedList:
        foutput.write("%s\n" % row)
    foutput.close()


def getTotalValuesByTrasportMode(list, message):
    print("\n\nValores totales de ", message, " por tipos de transporte \n")

    airData = []
    railData = []
    roadData = []
    seaData = []
    for row in list:
        if row[7] == 'Air':
            airData.append(row)
        elif row[7] == 'Rail':
            railData.append(row)
        elif row[7] == 'Road':
            roadData.append(row)
        elif row[7] == 'Sea':
            seaData.append(row)

    sumAirData = 0
    sumRailData = 0
    sumRoadData = 0
    sumSeaData = 0

    for row in airData:
        sumAirData = sumAirData + int(row[9])

    for row in railData:
        sumRailData = sumRailData + int(row[9])

    for row in roadData:
        sumRoadData = sumRoadData + int(row[9])

    for row in seaData:
        sumSeaData = sumSeaData + int(row[9])

    return {'Air': sumAirData, 'Rail': sumRailData, 'Road': sumRoadData, 'Sea': sumSeaData}


def printTotalValues(transport, totalValue, direction):
    if transport == 'Air':
        print("Valor total de ", direction, " por medio de transporte aereo \n", totalValue)
    elif transport == 'Rail':
        print("Valor total de ", direction, " por medio de transporte ferreo \n", totalValue)
    elif transport == 'Road':
        print("Valor total de ", direction, " por medio de transporte terrestre \n", totalValue)
    elif transport == 'Sea':
        print("Valor total de ", direction, " por medio de transporte maritimo \n", totalValue)


def importsAndExportsTotalValues(importsList, exportsList):
    totalValuesDict = getTotalValuesByTrasportMode(importsList, "importaciones")
    for transport in totalValuesDict:
        printTotalValues(transport, totalValuesDict[transport], "importaciones")

    max_key = max(totalValuesDict, key=totalValuesDict.get)
    print("El transporte con mayor valor total en importaciones fue: ", max_key, "con", totalValuesDict[max_key])

    totalValuesDict = getTotalValuesByTrasportMode(exportsList, "exportaciones")
    for transport in totalValuesDict:
        printTotalValues(transport, totalValuesDict[transport], "exportaciones")

    max_key = max(totalValuesDict, key=totalValuesDict.get)
    print("El transporte con mayor valor total en exportaciones fue: ", max_key, "con", totalValuesDict[max_key])

def createList(list, rowIndex):
    originList = []
    for row in list:
        originList.append(row[rowIndex])

    return originList


def removeDuplicatesFromList(list):
    keyList = []
    for origin in list:
        if origin not in keyList:
            keyList.append(origin)

    return keyList

def createDictionary(list):
    return dict(zip(list, ([] for _ in list)))

def createRouteDictionaries(list):
    originList = createList(list, 2)
    keyOriginList = removeDuplicatesFromList(originList)

    routeDictionary = createDictionary(keyOriginList)
    totalValueRouteDictionary = createDictionary(keyOriginList)
    for row in list:
        routeDictionary[row[2]].append(row[3])
    for row in list:
        totalValueRouteDictionary[row[2]].append(row[9])

    return routeDictionary, totalValueRouteDictionary

def Merge(dict1, dict2):
    return(dict2.update(dict1))

def calculateTotalValueRoutes(routeDictionary, totalValueRouteDictionary, direction):
    sumTotalValueDestination = 0
    for key in routeDictionary:
        print("\n\nOrigen: ", key)
        listWithoutDuplicates = removeDuplicatesFromList(routeDictionary[key])
        destinationDictionary = createDictionary(listWithoutDuplicates)
        for destination, totalValue in zip(routeDictionary[key], totalValueRouteDictionary[key]):
            destinationDictionary[destination].append(totalValue)
        for key in destinationDictionary:
        
            for totalValue in destinationDictionary[key]:
                sumTotalValueDestination = sumTotalValueDestination + int(totalValue)
            destinationDictionary[key] = sumTotalValueDestination
       
        max_key = max(destinationDictionary, key=destinationDictionary.get)
        print("La ruta con mayor valor total en ", direction," fue: ", max_key, "con", destinationDictionary[max_key])



def routeData(importRouteList, exportRouteList):
    print("\n\nValores totales de importaciones\n")
    routeDictionaryImports, totalValueRouteDictionaryImports = createRouteDictionaries(importRouteList)
    calculateTotalValueRoutes(routeDictionaryImports, totalValueRouteDictionaryImports, "importaciones")
    print("\n\nValores totales de exportaciones\n")
    routeDictionaryExports, totalValueRouteDictionaryExports = createRouteDictionaries(exportRouteList)
    calculateTotalValueRoutes(routeDictionaryExports, totalValueRouteDictionaryExports, "exportaciones")



def main():
    file, csvreader = openFile()
    data, importsList, exportsList = createDirectionLists(csvreader)
    # writeSortedLists
    importsAndExportsTotalValues(importsList, exportsList)
    routeData(importsList, exportsList)

    file.close()

if __name__ == '__main__':
    main()
    

exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']

def sol_3(df, p):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value'] / total_value_for_percent
    pais_total_value.sort_values(by='percent', ascending=False, inplace=True)
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_pequena = pais_total_value[pais_total_value['cumsum'] < p]
    
    return lista_pequena

res = sol_3(synergy_dataframe, 80)
print(res)

