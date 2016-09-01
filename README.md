# wired_parser

Provided class Wired can be used to collect articles from The Wired, using parse() method.
Recommended usage:
Always collects only the first 4 pages for a given category:

wired=Wired(4) 

Collects articles from the first 4 pages from all categories ad puts them into its attributes:

wired.parse() 

Collects articles from the science category only:

wired.parse("science") 

Prints the title of the first article from the first page of the science category:

print(wired.science[0][0].title)  

Prints the content of the article:

print(wired.science[0][0].content) 

