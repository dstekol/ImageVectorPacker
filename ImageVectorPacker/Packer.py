
import csv
import os
import json
import pickle
from PIL import Image
import urllib
import shutil

#prompt for native words, foreign words, foreign language


#nativewords = []

features = {}
numImages = 10
#foreignword = ""
#foreignlanguage = ""
#foreignlanguageabbrev = ""
#demoname = "experiment"
imgBasePath = "/scratch-shared/users/bcal/packages/"
featureBasePath = "/nlp/data/bcal/features/alexnet/"
currentDir = ""
demoname="demofiles"
foreign_lang=""




#main function
def transfer():
    global foreign_lang

    #creates or clears destination folder
    if(demoname in os.listdir(os.getcwd())):
        shutil.rmtree(demoname)
    os.mkdir(demoname)

    #reads in language name and retrieves abbreviation
    foreign_abbrev = None
    while(foreign_abbrev==None):
        foreign_lang = raw_input("Enter foreign language: ")
        foreign_lang, foreign_abbrev = getLanguageAbbrev(foreign_lang)
        print(foreign_lang)
        print(foreign_abbrev)
        if(foreign_abbrev==None):
            print("Cant find language. Please try again.")
    
        

    #reads in foreign word and compiles images and features
    success = False
    while(not success):
        foreign_word = raw_input("Enter foreign word: ")
        success = getForeignWord(foreign_word, foreign_lang, foreign_abbrev)
        if(not success):
            print("Couldn't find foreign word. Please try again")
            
    #reads in native words and compiles images and features
    success = False
    remainingWords = numImages
    while(not success):
        nat_words = inputNativeWords(remainingWords)
        fetchedWords = set(getNativeWords(nat_words))
        remainingWords = len(nat_words) - len(fetchedWords)
        if(remainingWords > 0):
            print("Failed to fetch following native words: ")
            print(str(nat_words - fetchedWords))
        else:
            success = True

    
    #writes features file to destination folder
    with open(demoname+"/"+demoname+".js", 'w') as fjson:
        json.dump(features, fjson, ensure_ascii=False, sort_keys=True, indent=4)
    with open(demoname+"/"+demoname+".js", 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("var data = ".rstrip('\r\n') + '\n' + content)

    print("Finished")

#copies over data for native words
def getNativeWords(nativewords):
    with open("/nlp/data/bcal/features/word_absolute_paths.tsv") as pathmap:
        extractedNativeWords = []
        tsvin = csv.reader(pathmap, delimiter='\t')
        for row in tsvin:
            if row[0] in nativewords:
                #creates new folder for images
                print(demoname+"/"+row[0])
                os.mkdir(demoname+"/"+row[0])
                #gets the last part of the path (to tack on to the already known path)
                pathEnd = extractPathEnd(row[1])
                #gets the first 10 images that have a valid extension
                files = getFirst10(imgBasePath + pathEnd)
                tempFeatureArray = []
                filecounter = 0
                for f in files:
                    filecounter += 1
                    #shrinks and saves image file
                    downsize(pathEnd + f, demoname + "/" + row[0]+"/", filecounter)
                    #saves feature vector for image
                    tempFeatureArray.append(convertFromPickle(featureBasePath+pathEnd + f+".pkl"))
                
                features[row[0]] = {}
                features[row[0]]["vectors"] = tempFeatureArray
                features[row[0]]["files"] = os.listdir(demoname + "/" + row[0]+"/")
                extractedNativeWords.append(row[0])
        return extractedNativeWords

#gets abbreviated language code for provided language (ex. "french" -> "fr")
def getLanguageAbbrev(foreignlanguage):
    dat = urllib.urlopen("https://raw.githubusercontent.com/brendandc/multilingual-google-image-scraper/master/google-languages.json").read().decode('utf-8')
    allLangAbbrev = json.loads(dat)
    for lang in allLangAbbrev:
        if lang.upper() == foreignlanguage.upper():
            return lang, str(allLangAbbrev[lang]['hl'])
    return None, None



#copies over data from foreign word (features and images)
def getForeignWord(foreignword, foreignlanguage, foreignlanguageabbrev):
    dat = urllib.urlopen("https://raw.githubusercontent.com/brendandc/multilingual-google-image-scraper/master/dictionaries/dict."+foreignlanguageabbrev).read().decode('utf-8')
    results = []
    rowcounter = 0
    for row in dat.split("\n"):
        results.append(row.split("\t"))
        currentrow = results[len(results) - 1]
        if currentrow[0] == foreignword:
            os.mkdir(demoname+"/f_"+foreignword)
            pathEnd = foreignlanguage + "/" + str(rowcounter)+"/"
            files = getFirst10(imgBasePath + pathEnd)
            tempFeatureArray = []
            filecounter = 0
            for f in files:
                filecounter += 1
                downsize(pathEnd + f, demoname +"/f_" + foreignword + "/", filecounter)
                tempFeatureArray.append(convertFromPickle(featureBasePath + pathEnd +f+".pkl"))
                
            features["foreignword"] = {}
            features["foreignword"]["vectors"] = tempFeatureArray
            features["foreignword"]["files"] = os.listdir(demoname +"/f_" + foreignword + "/")
            features["foreignword"]["word"] = foreignword
            return True
        rowcounter += 1
    return False






#returns first 10 image filenames in given folder with acceptable formats
def getFirst10(path):
    validExtensions = [".png", ".PNG", ".jpg", "JPG", ".jpeg", ".JPEG"]
    filesFound = []
    for filename in os.listdir(path):
        valid = True
        try:
            Image.open(path+filename)
        except:
            valid = False
        name, ext = os.path.splitext(filename)
        if (ext in validExtensions) and valid:
            filesFound.append(filename)
            if len(filesFound)==numImages:
                return filesFound
    return filesFound


#returns string representation of pickle file
def convertFromPickle(src):
    with open(src, 'rb') as fpkl:
        data = pickle.load(fpkl)
        data = list(data)
        data = list(float(x) for x in data)
        return data

#takes image (specified by filename f) and creates a smaller version, which is saved in folder (specified by dest)
   #with a numerical name (specified by counter)
def downsize(f, dest, counter):
    image = Image.open(imgBasePath + f)
    name, ext = os.path.splitext(f)
    print(name)
    width, height = image.size
    newHeight = 100
    newWidth = int(width * newHeight / height)
    thumb = image.resize((newWidth, newHeight), Image.ANTIALIAS)
    print(dest + getZeroPrefix(counter) + ext)
    thumb.save(dest + getZeroPrefix(counter) + ext)

#adds a "0" prefix to any single digit numerical filenames (to make them consistent with how they are currently stored)
def getZeroPrefix(num):
    if num<numImages:
        return "0"+str(num)
    else:
        return str(num)



def inputNativeWords(num):
    valid = False
    while(not valid):
        natwords = raw_input("Enter "+str(num)+" native words, separated by commas: ").split(",")
        counter = 0
        for elt in natwords:
            natwords[counter] = elt.strip()
            counter += 1
        if(len(set(natwords))==num):
            valid = True
    return set(natwords)

def extractPathEnd(path):
    splicespot = path.find("alexnet/")+8;
    return path[splicespot:]
    
transfer()


