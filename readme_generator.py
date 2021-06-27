from os import error, read
from bs4 import BeautifulSoup
import urllib.request

class ReadmeGenerator:
    def __init__(self, level_num, path):
        self.level = level_num
        self.level_name = ""
        self.description_text = ""
        self.problem_number = []
        self.problem_name = []
        self.right_code_list = []
        self.number_of_problems = 0
        self.path = path

    def decode(self):
        right_code = open('right_code.txt', 'r')
        self.right_code_list = right_code.readlines()

        for i in range(0, len(self.right_code_list)):
            self.right_code_list[i] = self.right_code_list[i].rstrip('\n')
            self.right_code_list[i] = int(self.right_code_list[i])
    
        right_code.close()
    
    def crawl(self):
        url = "https://www.acmicpc.net/step"
        html = urllib.request.urlopen(url).read()
        bs = BeautifulSoup(html, 'html.parser')

        table = bs.select('body > div.wrapper > div.container.content > div:nth-child(5) > div > div > table > tbody >' + ('tr >' * self.level) + ' td:nth-child(5)')
        self.number_of_problems = int(table[0].get_text())

        description = bs.select('body > div.wrapper > div.container.content > div:nth-child(5) > div > div > table > tbody >' + ('tr >' * self.level) + ' td:nth-child(3)')
        self.description_text = description[0].get_text()

        url = "https://www.acmicpc.net/step/" + str(self.right_code_list[self.level - 1])
        html = urllib.request.urlopen(url).read()
        bs = BeautifulSoup(html, 'html.parser')

        problem_id_list = bs.select('#problemset > tbody > tr > td.list_problem_id')
        for problem_id in problem_id_list:
            self.problem_number.append(int(problem_id.get_text()))

        problem_name_list = bs.select('#problemset > tbody > tr > td:nth-child(3) > a')
        for problem_name in problem_name_list:
            self.problem_name.append(str(problem_name.get_text()))

    def writeReadme(self):
        f = open(self.path + "/README.md", 'w')

        f.write("#<b> [Level " + str(self.level) + "] " + self.level_name + "<b>\n")
        f.write(self.description_text + "\n")
        f.write("## [Problem List]\n")
        f.write("<ol>\n")

        for i in range(0, self.number_of_problems):
            f.write("<li> #" + str(self.problem_number[i]) + " : " + self.problem_name[i] + "\n")
        
        f.write("</ol>")

        f.close()


def main():
    print("enter a path to save README.md file : ")
    path = input()
    print("enter a level number (1~50) : ")
    level_number = int(input())
    readme_generator = ReadmeGenerator(level_number, path)
    readme_generator.decode()
    readme_generator.crawl()
    readme_generator.writeReadme()

if __name__ == "__main__":
    main()