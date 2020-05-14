# extract text from websites
#import urllib
import math
import numpy as np
import string
import urllib.request
from bs4 import BeautifulSoup

def createDic(wordls):
    word_dic = {}
    for i in wordls:
        if i in word_dic:
            word_dic[i] += 1
        else:
            word_dic[i] = 1
    return word_dic

def getSimilarities(dicA, dicB):
    sumAB = 0
    sumAA = 0
    sumBB = 0
    for i in dicA:
        if i in dicB:
            sumAB += dicA[i] * dicB[i]
            sumAA += dicA[i] ** 2
        else:
            sumAA += dicA[i] ** 2
    for j in dicB:
        sumBB += dicB[j] ** 2
    similarity = sumAB/((math.sqrt(sumAA))*(math.sqrt(sumBB)))
    return  similarity

def computeMatrix(dicls):
    sim_matrix = [0]*len(dicls)
    for i in range(len(dicls)):
        sim_matrix[i] = [0]*len(dicls)
        for j in range(len(dicls)):
            sim_matrix[i][j] = getSimilarities(dicls[i],dicls[j])
    return sim_matrix




# create word dictionaries for both websites
# compute similarity matrix

# output the most similar page of each individual page


if __name__ == "__main__":
    file = open("input.txt")
    urlls = file.readlines()
    file.close()
    urlls = [i.strip("\n") for i in urlls]
    totalwordls = []
    outfile = open("output.txt","a")
    dicls = []
    for i in urlls:
        html = urllib.request.urlopen(i).read()
        # soup = BeautifulSoup(html)
        soup = BeautifulSoup(html, "lxml")
        # remove all script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        # now retrieve text
        text = soup.get_text()
        text.replace("\n",' ')
        #print(text[:100])
        table = str.maketrans(' ',' ',string.punctuation)
        text.translate(table)
        print(text[:100])
        wordls = text.split()
        totalwordls+=wordls
        #wordls = [i.strip("\n") for i in wordls]
        worddic = createDic(wordls)
        print(worddic)
        dicls.append(worddic)
    # compute similarity matrix
    sim_matrix = computeMatrix(dicls)
    array_sim = np.array(sim_matrix)
    np_sim = np.matrix(array_sim)

    for line in np_sim:
        np.savetxt(outfile,line, fmt = "%.2f")

    #print out the url that has the highest similarity for each url
    for i in range(len(sim_matrix)):
        sorted_ls = sorted(sim_matrix[i])
        second_max = sorted_ls[-2]
        print(sim_matrix[i])
        index = sim_matrix[i].index(second_max)
        line = urlls[i] + ": " + urlls[index] +'\n'
        outfile.write(line)




