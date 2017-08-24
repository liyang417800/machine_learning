import re
regEx = re.compile('\\W*')


mySent='This book is the best book on Python or M.L. I have ever laid eyes upon'

listOfTokens = regEx.split(mySent)


[tok.lower() for tok in listOfTokens if len(tok)>0]

emailText = open('6.txt').read()

listOfTokens = regEx.split(emailText)

print listOfTokens

