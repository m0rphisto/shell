#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
fid='$Id: quizgame.py v0.3 2024-06-26 18:37:44 +0200 .m0rph $'
################################################################################
# Description:
# Found on github and licenced it.
# https://github.com/butterflyx/multichoice-quiz/blob/main/quizgame.py
#
# Used for the bsi-quiz: IT-Grundschutzpraktiker and IT-Sicherheitsbeauftragter
# https://github.com/butterflyx/GrundschutzQuiz/blob/main/bsi.json 
#
# ------------------------------------------------------------------------------
# Version history:
#
# v0.2: Unfortunately this Python Script was coded under Linux and had some
#       errors, so it didn't run under Windows.
#
# v0.3: Added direct result output.
#
# v0.4: Added result saving functionality for a better overview of the learning
#       process.
#
# ------------------------------------------------------------------------------
# This script is free software, licenced under GNU GPL v3.
################################################################################

import json
import time
import random
import glob
import os
import argparse
# import call method from subprocess module 
from subprocess import call 

# .m0rph: We need some cross platform stuff.
me = os.path.splitext(os.path.basename(__file__))[0]
SEP = os.path.sep # directory separator
cwd = os.getcwd() # current working directory


class Quiz:
   BANNER = r'''
              _ _   _     _         _                     _    
  _ __ ___  _   _| | |_(_) ___| |__   ___ (_) ___ ___      __ _ _   _(_)____
 | '_ ` _ \| | | | | __| |/ __| '_ \ / _ \| |/ __/ _ \_____ / _` | | | | |_  /
 | | | | | | |_| | | |_| | (__| | | | (_) | | (_|  __/_____| (_| | |_| | |/ / 
 |_| |_| |_|\__,_|_|\__|_|\___|_| |_|\___/|_|\___\___|     \__, |\__,_|_/___|
                                                |_|         
A quiz game for multiple choice tests
@author: butterflyx <info@butterflyx.com>
'''

   def __init__(self):
      # list available json files with quiz data
      self.gamesList = []
      # chosen game from gameslist
      self.topic = ""
      # the content of the loaded json file
      self.rawGame = None
      # list of chapters in game
      self.chapters = []

      # number of questions available (to calc eg pass limit)
      self.questionsTotal = 0
      # number of questions left in stack
      self.questionsLeft = 0      
      # list of shuffeled questions for the quiz itself
      self.questions = []
      # the actually asked question
      self.question = []
      # list of right answered questions
      # while learning depend on times answered right before pushed here
      # while simulating a test, instantly pushed here if correct
      self.questionsRightAnswered = []
      # list of wrong answered questions
      # if simulating a test to show a list of questions that should be repeated
      self.questionsWrongAnswered = []

      # limit of questions to ask
      self.limit = 0
      # threshold to pass the quiz; show banners only if set
      self.threshold = None

      # set to true if Strg+C to stop quiz
      self.breakFlag = False

      self.failedBanner = """
                                                   
         @@@@@@@@   @@@@@@   @@@  @@@       @@@@@@@@  @@@@@@@   
         @@@@@@@@  @@@@@@@@  @@@  @@@       @@@@@@@@  @@@@@@@@  
         @@!       @@!  @@@  @@!  @@!       @@!       @@!  @@@  
         !@!       !@!  @!@  !@!  !@!       !@!       !@!  @!@  
         @!!!:!    @!@!@!@!  !!@  @!!       @!!!:!    @!@  !@!  
         !!!!!:    !!!@!!!!  !!!  !!!       !!!!!:    !@!  !!!  
         !!:       !!:  !!!  !!:  !!:       !!:       !!:  !!!  
         :!:       :!:  !:!  :!:  :!:       :!:       :!:  !:!  
          ::       ::   :::   ::  :: ::::   :: ::::   :::: ::  
          :         :   : :   :   : :: : :  : :: ::   :: :  :   
                                                   
      """

      self.passedBanner = """
       :::::::::    :::     ::::::::  :::::::: :::::::::::::::::::  
       :+:    :+: :+: :+:  :+:    :+::+:    :+::+:       :+:    :+: 
       +:+    +:++:+   +:+ +:+       +:+       +:+       +:+    +:+ 
       +#++:++#++#++:++#++:+#++:++#+++#++:++#+++#++:++#  +#+    +:+ 
       +#+      +#+     +#+       +#+       +#++#+       +#+    +#+ 
       #+#      #+#     #+##+#    #+##+#    #+##+#       #+#    #+# 
       ###      ###     ### ########  ######## ###################  
      """

   def listGames(self) -> list:
      """ list all available quizzes in subfolder 'quizzes' """
      # .m0rph: We need cross platform stuff
      files = '%s%s%s%s%s' % (cwd, SEP, 'quizzes', SEP, '*.json')
      self.gamesList = glob.glob(files)
      return self.gamesList

   def setGame(self, topic, limit) -> bool:
      """ load the raw quiz data into memory and prepare quiz to play """
      # https://careerkarma.com/blog/python-check-if-file-exists/
      # .m0rph: We need cross platform stuff
      tpath = '%s%s%s'      % (cwd, SEP, topic)
      tfile = '%s%s%s%s%s%s' % (cwd, SEP, 'quizzes', SEP, topic, '.json')
      if os.path.exists(tpath) and (topic in self.gamesList):
         self.topic = topic   
      elif os.path.exists(tfile) and (tfile in self.gamesList):
         self.topic = tfile
      else:
         raise QuizNotFound()

      game = self.readGameFile()

      for chapter in game["quiz"]:
         self.chapters.append(chapter)
         #print(f"Chapter: {chapter}")
         for question in game["quiz"][chapter]:
            quizquestion = {}
            #print(f"Question-Nr: {question}")
            self.questionsTotal += 1
            quizquestion["chapter"] = chapter
            quizquestion["questionnr"] = question
            quizquestion["timesRightAnswered"] = 0
            quizquestion["userAnswers"] = []
            quizquestion["question"] = game["quiz"][chapter][question]["question"]
            # shuffle possible answers as well
            # https://stackoverflow.com/questions/19895028/randomly-shuffling-a-dictionary-in-python
            keys = list(game["quiz"][chapter][question]["answers"].keys())
            random.shuffle(keys)
            quizquestion["answers"] = [(key, game["quiz"][chapter][question]["answers"][key]) for key in keys]
            # quizquestion["answers"] = game[chapter][question]["answers"]
            quizquestion["right"] = game["quiz"][chapter][question]["right"]
            self.questions.append(quizquestion)
      # shuffle the questions
      random.shuffle(self.questions)
      print(Colors.blue(f"{self.questionsTotal} questions found in {self.topic}"))

      # pop questions above limit after shuffling
      if limit:
         self.limit = limit
         while self.limit > 0 and len(self.questions) > self.limit:
            self.questions.pop(0)
         self.questionsTotal = len(self.questions)
         print(Colors.blue(f"This quiz is limited to {self.questionsTotal} random questions."))

      # initially all questions are left as well
      self.questionsLeft = self.questionsTotal

      return True

   def readGameFile(self) -> list:
      """ open and read the file with the quiz """
      try:
         # .m0rph: Added character encoding
         with open(self.topic, "r", encoding = 'utf-8') as json_file:
            self.rawGame = json.load(json_file)
      except:
         print(f"unable to read {self.topic}")

      return self.rawGame

   def getQuestion(self) -> list:
      """ get one question out of the heap """
      # take the first question of the randomized array
      self.question = self.questions.pop(0)
      # update remaining questions
      self.getQuestionsLeft()
      return self.question

   def getQuestionsTotal(self) -> int:
      """ get total number of questions in quiz """
      return self.questionsTotal

   def getQuestionsLeft(self) -> int:
      """ get number of questions in quiz not yet asked """
      self.questionsLeft = len(self.questions)
      return self.questionsLeft

   def getProgress(self) -> int:
      """ calculates the percentage of answered questions """
      p = int(round(100-((self.getQuestionsLeft() / self.getQuestionsTotal()) * 100)))
      return p

   def printProgressbar(self, prog=None) -> None:
      """ visualize the percentage of answered questions """
      progress =  prog if prog != None else self.getProgress()
      barlevel = int(str(progress*0.1)[:1]) # get first digit
      blanks = (10-barlevel)
      if barlevel < 5:
         print("[ "+Colors.highlight_lightgreen(("  "*barlevel))+Colors.highlight_gray(("  "*blanks))+" ]")
      else:
         print("[ "+Colors.highlight_green(("  "*barlevel))+Colors.highlight_gray(("  "*blanks))+" ]")

   # define clear function ; from https://www.geeksforgeeks.org/clear-screen-python/
   def clear(self) -> None: 
      """ clears screen """
      # check and make call for specific operating system 
      # .m0rph: Added parantheses and shell condition
      _ = call(('clear' if os.name =='posix' else 'cls'), shell = True) 


   def askQuestion(self) -> list:
      """ prints the questions as well as possible answers and awaits input(s) """
      answers = []
      keys = []
      securityQuestion = False

      print("")
      print(f"Category: {self.question['chapter']}")
      print("")
      print(Colors.blue("Question:")+f" {self.question['question']}")
      print("")
      for key, answer in self.question['answers']:
         keys.append(key.upper())
         print(Colors.blue(f"({key}) ")+f"{answer}") 
      print("")
      print(f">> ")
      options = list(sorted(set(keys).difference(answers)))
      try:
         while(options != []):
            choice = input(f"Enter choice {options} or hit Enter to finish question: ")
            if choice.upper() in options:
               answers.append(choice.upper())
               print(Colors.blue("Any other answer you want to check?"))
               securityQuestion = False        
            elif choice.upper() in answers:
               print(Colors.yellow(f"you have already marked answer ({choice}) as true. Try again or press enter if no other answer is right."))
               securityQuestion = False
            elif choice == "" and securityQuestion == True:
               return answers
            elif choice == "" and securityQuestion == False:
               securityQuestion = True
               print(Colors.blue("Sure you have all answers marked? Press Enter again to finish this question."))
            else:
               print(Colors.red("Invalid choice. Try again"))
               securityQuestion = False
            options = list(sorted(set(keys).difference(answers)))
         return answers   
      except KeyboardInterrupt:
         choice = input(Colors.yellow("\n\nDo you want to interrupt the quiz? (y/n) : "))
         if choice.lower() == "y":
            self.breakFlag = True
            return False
         else:
            print("OK, then try again.")
            self.askQuestion()

   def validateAnswer(self, answers) -> bool:
      """ check if answer given was right """
      if sorted(answers) == sorted(self.question['right']):
         # .m0rph: Added direct result output (correct answer)
         print(Colors.green(f"Right! {answers} == {self.question['right']}"))
         input(Colors.yellow(f"Next [ENTER]: "))
         self.questionsRightAnswered.append(self.question)
         self.question = []
         return True
      # .m0rph: Added direct result output (wrong answer)
      print(Colors.red(f"Choice not correct! {answers} != {self.question['right']}"))
      input(Colors.yellow(f"Next [ENTER]: "))
      self.question["useranswers"] = answers
      self.questionsWrongAnswered.append(self.question)
      self.question = []
      return False

   def setThreshold(self, threshold) -> int:
      """ set the minimum amount of right answers to pass the quiz """
      self.threshold = threshold if threshold <= 100 else 100
      return self.threshold


   # m0rph: Added result saving functionality
   def printResults(self) -> None:
      """ print the results of the quiz """
      qleft = self.getQuestionsLeft()+1 if self.breakFlag else self.getQuestionsLeft() # +1 for current question
      questionsAnswered = self.getQuestionsTotal() - qleft
      print("")
      print(Colors.green("Your results:"))
      print("~~~~~~~~~~~~~")
      print(f"You have answered {questionsAnswered} questions out of {self.getQuestionsTotal()} questions.")
      if questionsAnswered > 0:
         percent = int(round(len(self.questionsRightAnswered)/questionsAnswered * 100))
         print(f"And you got {len(self.questionsRightAnswered)} of {questionsAnswered} right, which is a {percent}% percentage (minimum %: {self.threshold}).")
         if self.threshold != None:
            if percent >= self.threshold:
               print(Colors.green(self.passedBanner))
            else:
               print(Colors.red(self.failedBanner))
      print(f"")
      if self.questionsWrongAnswered != []:
         print(Colors.yellow("These questions should be reviewed:"))
         for question in self.questionsWrongAnswered:
            print("")
            print(f"{question['chapter']} - question {question['questionnr']} :")
            print(Colors.blue(question['question']))
            print("")
            print("possible answers:")
            for key, answer in sorted(question["answers"]):
               print("("+Colors.blue(key)+f") {answer}")
            print("")
            print(f"Your answers: "+Colors.red(question['useranswers'])+"")
            print(f"right answers: "+Colors.green(question['right'])+"")
            print("--------")
         print("")

      

      
   
   def playQuiz(self, args) -> None:
      """ take the quiz """
      #print(f"quizname: {args.quizname} ; l: {args.l} ; t: {args.t}")
      self.listGames()
      self.setGame(args.quizname, args.l)
      if args.t:
         self.setThreshold(args.t)
      print("")
      print(Colors.green("Starting the quiz in a moment..."))
      time.sleep(2)
      while (self.questionsLeft > 0):
         self.clear()
         print("--------")
         print(f"progress: {self.getProgress()} % ")
         self.printProgressbar()
         self.getQuestion()
         answer = self.askQuestion()
         if answer == False or answer == [] or type(answer) is not list:
            break
         else:
            self.validateAnswer(answer)
         self.clear()
      self.printResults()
      print(Colors.green("Thank you for taking the quiz!"))
      print("")
      print("~~~~~~~~~~")
      print(f"{self.rawGame['meta']['title']}")
      print("~~~~~~~~~~")
      print(f"brought to you by: {self.rawGame['meta']['author']}")
      print("")
      if self.rawGame["meta"]["contributors"] != []:
         print("with contributions by:")
         for supporter in self.rawGame["meta"]["contributors"]:
            print(f"{supporter}")
      # .m0rph: Added disclaimer output
      if self.rawGame['meta']['disclaimer'] != []:
         print("~~~~~~~~~~")
         print(f"disclaimer:\n{self.rawGame['meta']['disclaimer']}")
         print("~~~~~~~~~~")
      print("")
      print(f"licence: {self.rawGame['meta']['licence']}")
      print("")
      print(f"please visit {self.rawGame['meta']['homepage']} for more information.")
      print("")
      print("Bye.\n")
      exit(0)



class QuizNotFound(Exception):
   pass     


class Colors:

   # https://godoc.org/github.com/whitedevops/colors
   Reset = "\033[0m"

   Bold      = "\033[1m"
   Dim      = "\033[2m"
   Underlined = "\033[4m"
   Blink     = "\033[5m"
   Reverse   = "\033[7m"
   Hidden    = "\033[8m"

   ResetBold      = "\033[21m"
   ResetDim      = "\033[22m"
   ResetUnderlined = "\033[24m"
   ResetBlink     = "\033[25m"
   ResetReverse   = "\033[27m"
   ResetHidden    = "\033[28m"

   Default     = "\033[39m"
   Black      = "\033[30m"
   Red        = "\033[31m"
   Green      = "\033[32m"
   Yellow      = "\033[33m"
   Blue       = "\033[34m"
   Magenta     = "\033[35m"
   Cyan       = "\033[36m"
   LightGray   = "\033[37m"
   DarkGray    = "\033[90m"
   LightRed    = "\033[91m"
   LightGreen   = "\033[92m"
   LightYellow  = "\033[93m"
   LightBlue   = "\033[94m"
   LightMagenta = "\033[95m"
   LightCyan   = "\033[96m"
   White      = "\033[97m"

   BackgroundDefault     = "\033[49m"
   BackgroundBlack      = "\033[40m"
   BackgroundRed        = "\033[41m"
   BackgroundGreen      = "\033[42m"
   BackgroundYellow      = "\033[43m"
   BackgroundBlue       = "\033[44m"
   BackgroundMagenta     = "\033[45m"
   BackgroundCyan       = "\033[46m"
   BackgroundLightGray   = "\033[47m"
   BackgroundDarkGray    = "\033[100m"
   BackgroundLightRed    = "\033[101m"
   BackgroundLightGreen   = "\033[102m"
   BackgroundLightYellow  = "\033[103m"
   BackgroundLightBlue   = "\033[104m"
   BackgroundLightMagenta = "\033[105m"
   BackgroundLightCyan   = "\033[106m"
   BackgroundWhite      = "\033[107m"

   @staticmethod
   def blue(string) -> str:
      return Colors.LightBlue+str(string)+Colors.Reset

   @staticmethod
   def green(string) -> str:
      return Colors.Green+str(string)+Colors.Reset

   @staticmethod
   def yellow(string) -> str:
      return Colors.Yellow+str(string)+Colors.Reset

   @staticmethod
   def red(string) -> str:
      return Colors.Red+str(string)+Colors.Reset

   @staticmethod
   def bold(string) -> str:
      return Colors.Bold+str(string)+Colors.Reset
   
   @staticmethod
   def highlight_green(string) -> str:
      return Colors.BackgroundGreen+str(string)+Colors.Reset

   @staticmethod
   def highlight_lightgreen(string) -> str:
      return Colors.BackgroundLightGreen+str(string)+Colors.Reset

   @staticmethod
   def highlight_gray(string) -> str:
      return Colors.BackgroundDarkGray+str(string)+Colors.Reset



if __name__ == "__main__":
   myquiz = Quiz()
   myquiz.clear()
   print(Colors.blue(myquiz.BANNER))
   print("")
   parser = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
   parser.add_argument('quizname', type=str, help='name of the quiz you want to play')
   parser.add_argument('--t', nargs='?', type=int, help='THRESHOLD for passing the quiz in percent (rounded). Show success or failure message at the end.')
   parser.add_argument('--l', nargs='?', type=int, help='LIMIT the number of questions in a quiz. No effect if number of available question less then limit.')
   parser.add_argument('-i', action='store_true', help='print available quizzes and exit')
   #parser.print_help()
   args = parser.parse_args()
   if args.i:
      print(myquiz.listGames())
      exit()
   else:
      myquiz.playQuiz(args)
