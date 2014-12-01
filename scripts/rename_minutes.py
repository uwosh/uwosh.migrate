#
# renames the titles of curriculum proposal minutes pdfs to something more
# readable:
#
# fapaminutes_122508.pdf -> "December 12, 2008"
#

from Products.PythonScripts.standard import html_quote
request = container.REQUEST
RESPONSE =  request.RESPONSE

months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

contents = context.contentItems()

for item in contents:
  title = item[0].split('.')[0]
  obj = item[1]

  if (title.find('minutes') != -1):
    date = title[(title.find('minutes') + 7): ]

    while date[0].isdigit() == False:
      date = date[1:]

    while date[-1].isdigit() == False:
      date = date[:-1] 

    year = "20" + date[-2:]
    day = date[-4:-2]
    month = int(date[:-4]) 

    title = months[month] + ' ' + day + ', ' + year
    print title
    obj.setTitle(title)
    obj.reindexObject()

return printed
