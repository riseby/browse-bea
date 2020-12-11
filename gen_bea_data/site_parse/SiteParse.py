import requests
import lxml.html
import re
import datetime
import PyPDF2

class SiteParse:
    status1 = "no valid data or complete data"

    def __init__(self,url,house):
        self.url = url
        self.house = house
        self.__fetchData()

    def __fetchData(self):
        self.data = ""
        self.status = ""

    def cleanString(self,str):
        cleanStr = re.sub("[\xa0\t\:]","",str)
        cleanStr = cleanStr.strip()
        return cleanStr

    def cleanOutputList(self, l):
        l = [self.cleanString(x) for x in l]
        l = list(filter(None,l))
        return l

    def getRegEx(self,date,regex):
        return regex[date.weekday()]

    def noDataFound(self):
        status = False
        for day, dayValue in self.data.items():
            if dayValue:
                status = True
        if not status:
            self.status = self.status1

    def getData(self):
        structuredData = {
            "house": self.house,
            "url": self.url,
            "status": self.status,
            "dishesPerDate": self.data
        }
        return structuredData

class Gastrogate(SiteParse):
    def __init__(self,savePath,url,house,dates):
        self.savePath = savePath
        self.url = url
        self.house = house
        self.status = ""
        self.data = {}
        self.html = ""
        if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
            self.__fetchData()
        if(self.status == 200):
            for d in dates:
                self.data[d.strftime("%Y-%m-%d")] = self.__getDishesByDate(d)
            self.noDataFound()

    def __validMenuDate(self,menuDateStr, date):
        d = date.day
        m = re.search(str(d),menuDateStr)
        m2 = re.search("dag",menuDateStr,re.IGNORECASE)
        return m != None and m2 != None

    def __fetchData(self):
        req = requests.get(self.url)
        self.status = req.status_code
        self.html = lxml.html.fromstring(req.text)

    def __getDishesByDate(self,date):

        menuDates = self.html.xpath(".//thead[@class='lunch-day-header']")
        menuDishes = self.html.xpath(".//tbody[@class='lunch-day-content']")
        i = 0
        for mdp in menuDates:
            md = mdp.xpath(".//th")[0]
            textDate = str(md.text_content())
            if(self.__validMenuDate(textDate,date)):
                lunchMenuDay = menuDishes[i]
                lunchDishes = lunchMenuDay.xpath(".//td[@class='td_title']")
                lunchDishesText = [str(x.text_content()) for x in lunchDishes]
                return self.cleanOutputList(lunchDishesText)

            i += 1
        return ""

class Styrman(SiteParse):
    def __init__(self,savePath,url,house,dates):
        self.savePath = savePath
        self.url = url
        self.house = house
        self.status = ""
        self.data = {}
        self.html = ""
        if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
            self.__fetchData()
        if(self.status == 200):
            for d in dates:
                self.data[d.strftime("%Y-%m-%d")] = self.__getDishesByDate(d)
            self.noDataFound()

    def __validMenuDate(self,menuDateStr, date):
        d = date.strftime("%-d/%-m")
        m = re.search(str(d),menuDateStr)
        return m != None

    def __fetchData(self):
        req = requests.get(self.url)
        self.status = req.status_code
        self.html = lxml.html.fromstring(req.text)

    def __getDishesByDate(self,date):
        lunchMenu = self.html.xpath("//div[@class='food-menu-item ']")
        for lunchMenuDay in lunchMenu:
            menuDate = lunchMenuDay.xpath(".//div[@class='food-menu-price']")[0]
            textDate = str(menuDate.text_content())
            if(self.__validMenuDate(textDate,date)):
                lunchDishes = lunchMenuDay.xpath(".//div[@class='food-menu-desc']//p")
                lunchDishesText = [str(x.text_content()) for x in lunchDishes]
                return self.cleanOutputList(lunchDishesText)

        return ""

class Filmhuset(SiteParse):
    def __init__(self,savePath,url,house,dates):
        self.savePath = savePath
        self.url = url
        self.house = house
        self.status = ""
        self.data = {}
        self.regEx = regEx = {0: 'ndag(.*)tisdag', 1: 'tisdag(.*)onsdag', 2: 'onsdag(.*)torsdag', 3: 'torsdag(.*)fredag[^a-z]', 4:'fredag(.*?)(\n\n|\n\s\n)', 5:'', 6:''}
        if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
            self.__fetchData()
        if(self.status == 200):
            for d in dates:
                self.data[d.strftime("%Y-%m-%d")] = self.__getDishesByDate(d)
            self.noDataFound()

    def __validMenuWeek(self,menuDateStr):
        weekNum = datetime.datetime.now().isocalendar()[1]
        m = re.search(".*vecka\:?\s+(\d{,2})",menuDateStr,re.IGNORECASE)
        if m:
            return int(m.group(1)) == weekNum
        else:
            return False

    def __fetchData(self):
        req = requests.get(self.url)
        self.status = req.status_code
        self.html = lxml.html.fromstring(req.text)
        for br in self.html.xpath("*//br"):
            br.tail = "\n" + br.tail if br.tail else "\n"

    def __getDishesByDate(self,date):
        lunchMenu =  self.html.xpath("//div[@class='day']")[0]
        textMenu = str(lunchMenu.text_content())

        dateToValidate =  self.html.xpath("//div[@class='divider-full']")[0]
        textDateToValidate = str(dateToValidate.text_content())

        dayRegEx=self.getRegEx(date,self.regEx)
        if dayRegEx and self.__validMenuWeek(textDateToValidate):
            p = re.compile(dayRegEx,re.S | re.I)
            m = p.search(textMenu)
            if m:
                dayMenu = m.group(1)
                return self.cleanOutputList(re.split('\n',dayMenu))
        return ""


class Sidahuset(SiteParse):
    def __init__(self,savePath,url,house,dates):
        self.savePath = savePath
        self.url = url
        self.house = house
        self.status = ""
        self.data = {}
        self.divDayDict = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4:'friday', 5:'', 6:''}
        self.__fetchData()
        if(self.status == 200):
            for d in dates:
                self.data[d.strftime("%Y-%m-%d")] = self.__getDishesByDate(d)
            self.noDataFound()

    def __validMenuWeek(self,menuDateStr):
        print(menuDateStr)
        weekNum = datetime.datetime.now().isocalendar()[1]
        m = re.search("(\d{1,2})",menuDateStr,re.IGNORECASE)
        if m:
            return int(m.group(1)) == weekNum
        else:
            return False

    def __fetchData(self):
        req = requests.get(self.url)
        self.status = req.status_code
        self.html = lxml.html.fromstring(req.text)

    def __getDishesByDate(self,date):
        lunchMenu = self.html.xpath("//div[@class='menu-content']")[0]
        menuHeader = lunchMenu.xpath("//div[@class='menu-heading']")[0]
        textMenu = str(lunchMenu.text_content())
        dayDivClass=self.getRegEx(date,self.divDayDict)
        if dayDivClass and self.__validMenuWeek(str(menuHeader.text_content())):
            path = "//div[@class='menu-item " + dayDivClass + "']//p"
            lunchMenuDay = lunchMenu.xpath(path)
            return self.cleanOutputList([dish.text_content() for dish in lunchMenuDay])
        else:
            return ""

class Eriksbakficka(SiteParse):
    def __init__(self,savePath,url,house,dates):
        self.savePath = savePath
        self.url = url
        self.house = house
        self.status = ""
        self.data = {}
        self.regEx = {0: 'ndag(.*)tisdag', 1: 'tisdag(.*)onsdag', 2: 'onsdag(.*)torsdag', 3: 'torsdag(.*)fredag[^a-z]', 4:'fredag(.*?)(veckans)', 5:'', 6:''}

        if datetime.date.today().weekday() != 5 and datetime.date.today().weekday() != 6:
            self.__fetchData()
        if(self.status == 200):
            for d in dates:
                self.data[d.strftime("%Y-%m-%d")] = self.__getDishesByDate(d)
            self.noDataFound()

    def __validMenuWeek(self,menuDateStr):
        weekNum = datetime.datetime.now().isocalendar()[1]
        m = re.search(".*vecka\:?\s+(\d{,2})",menuDateStr,re.IGNORECASE)
        if m:
            return int(m.group(1)) == weekNum
        else:
            return False

    def __fetchData(self):
        req = requests.get(self.url)
        self.status = req.status_code
        with open(self.savePath + "temp.pdf", "wb") as handle:
                handle.write(req.content)
        file = open(self.savePath + "temp.pdf", "rb")
        fileReader = PyPDF2.PdfFileReader(file)
        page = fileReader.getPage(0)
        self.pdfContent = page.extractText()

    def __getDishesByDate(self,date):
        textMenu =  self.pdfContent
        textDateToValidate = textMenu

        dayRegEx=self.getRegEx(date,self.regEx)
        if dayRegEx and self.__validMenuWeek(textDateToValidate):
            p = re.compile(dayRegEx,re.S | re.I)
            m = p.search(textMenu)
            if m:
                dayMenu = m.group(1)
                return self.cleanOutputList(re.split('\n',dayMenu))
        return ""

## TODO:
