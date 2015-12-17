# LinkedIn2Md  
  
Export **public** LinkedIn resume to markdown format.  
You can use this tool to generate a Markdown format resume from your LinkedIn profile.  
Edit the output Markdown file and transform it into PDF,  
so you can have the pure text resume (maybe put it on your personal website which support markdown format)  
and PDF resume at the same time.  
  
  
## Why create this project?  
  
1. Save to PDF function on LinkedIn doesn't support Chinese characters.  
2. [Resume Builder on LinkedIn](http://resume.linkedinlabs.com/) cannot import Honors&Awards section on your profile.  
3. LinkedIn profile cannot export to pure text format like Markdown or reSturcturedText.  
  
## Why not use LinkedIn API as a application so you can get the private info from the profile of user?  
  
Creating a application on LinkedIn is too troublesome for me,  
you have to fill the company name, commercial usage, ... and so on for registration.  
This is just a toy project for my personal usage to generate a resume in markdown format because I am too lazy to write one and I don't won't to maintain lots of different versions of my resume.  I just wanna write on LinkedIn and use it anywhere.  
Besides, all sections of my profile are public.  
So, that's why I get the profile from a browser and parse the html then output into markdown format.  
  
## Why Markdown instead of reStructedText?  
  
I am not familiar with reStructedText syntax and I think Markdown format is enough for this usage.  
Lots of tools can help you transform a Markdown file into a PDF.  
  
---  
  
## Installation  
  
`pip install git+https://github.com/M157q/linkedin2md.git`  
  
---  
  
## Usage  
  
```  
usage: linkedin2md [-h] linkedin_id  
  
Export public LinkedIn resume to markdown format  
  
positional arguments:  
  linkedin_id  The id of the target LinkedIn profile.  
  
optional arguments:  
  -h, --help   show this help message and exit  
```  
  
---  
  
## LICENSE  
  
GPLv3  
