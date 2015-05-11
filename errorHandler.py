# -*- coding: utf-8 -*-
###################################
#
#  Team:Tae Kim + Kevin Nguyen
#  Creator: Tae Kim 
#
#  errorHandler.py 
#  April 23,2015
#
#  Handles various errors from inputs of restaurant.py
#
###################################


import sys
import requests.exceptions

class errorHandlerClass():
    
  def __init__(self, thisError):  
       self.thisError = thisError
      
  def errorHandlerFunction(self):
    '''
    Checks various errors.   Error will terminate the program.  
    '''
    if self.thisError ==  IndexError:  #in case of IndexError
        print "*"*30
        print "You are too advance. Index is out of range."
        print "*"*30
        sys.exit(1)

    elif self.thisError ==  ValueError:  #in case of ValueError
        print "*"*30
        print "You are too advance. Please type in valid value or link next time"
        print "*"*30
        sys.exit(1)
        
    elif self.thisError ==  NameError:  #in case of NameError
        print "*"*30
        print "You are too advance. Please check and type in correct name"
        print "*"*30
        sys.exit(1)

    elif self.thisError ==  KeyboardInterrupt:   #in case of CTRL + C
        print "*"*30
        print "Keyboard interrupted. Shutting down the program."
        print "*"*30
        sys.exit(1)
    
    elif self.thisError ==  SyntaxError:   #without an input
        print "*"*30
        print "Please type in valid next time"
        print "*"*30
        sys.exit(1)
        
    elif self.thisError ==  requests.exceptions.MissingSchema:   #website error
        print "*"*30
        print "The website address is not correct. Please check again"
        print "*"*30
        sys.exit(1)
        
    elif self.thisError == SystemExit:
        sys.exit(1)
        
    else:
        print "I found an undefined error.  Please don't destroy the program. ----> ", self.thisError    
        sys.exit(1)
 #