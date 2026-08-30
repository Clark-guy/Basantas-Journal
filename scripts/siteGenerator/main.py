import sys
import shutil
from datetime import date, datetime, timezone
import bs4
from pprint import pprint
from markdown_it import MarkdownIt
import xml.etree.ElementTree as ET

#This python file should take in a bunch of text and make it into a blog post
#for starters just going to have it piped in, but ultimately could use tkinter
#for a user interface

#currently to run this (subject to change):
#cat testPost.txt | python main.py 'title'
#post will be dumped into output folder

'''
I have some issues with having a title in front. Maybe I should make it take two args
first arg is title, then post. I can add more args for more shit if necessary
Eventually I could replace this with a dict when i made a gui - then not all fields
would be totally mandatory. But for now, 2 args title / post will suffice
'''


def main1():
    print(len(sys.argv))
    if (len(sys.argv) == 2):
        title = '<h1>' + sys.argv[1] + '</h1>'
        postText = sys.stdin.read()
        postText = '<p>\n' + postText.replace('\n\n', '\n</p>\n\n<p>\n') + '\n</p>'
        #print("title is: " + title)
        #print("post is: " + postText)

        #testOutputPath = './output/' + date.today().strftime('%m-%d-%y')
        outputPath = '../../pages/blog posts/' + date.today().strftime('%m-%d-%y')
        shutil.copytree('./input/template',outputPath, dirs_exist_ok=True)

        #open new file and replace title, then content
        post = open(outputPath+'/post.html')
        postString = post.read()
        postString = postString.replace('<h1>TEMPLATE</h1>', title)
        postString = postString.replace('<p>TEMPLATE</p>', postText)
        post.close()

        newpost = open(outputPath+'/post.html', 'w')
        #print(postString)
        newpost.write(postString)

        post.close()
        #TODO RSS feed

        #TODO link from blog.html page
        with open("../../pages/blog.html") as bloghtml:
            soup = bs4.BeautifulSoup(bloghtml.read(), features="html.parser")
            #get element by id "postList"
        
        linkString = '/pages/blog posts/'+date.today().strftime('%m-%d-%y')+'/post.html'
        newLink = soup.new_tag("a", href=linkString, string=date.today().strftime('%m/%d/%y')+' - ' + sys.argv[1])
        listItem = soup.new_tag("li")
        listItem.append(newLink)
        print(str(listItem))
        soup.find(id="postList").insert(0, listItem)
        #add new list item of format <a href="/pages/blog posts/DATE/post.html">DATE - TITLE</a>
        with open("../../pages/blog.html", 'w') as bloghtmlOut:
            bloghtmlOut.write(str(soup.prettify()))

        print('successfully written to ' + outputPath)



    else:
        print("no input given")


def updateRSSFeed(todaysDate,title,summary):
    namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
    dateTimeNow = datetime.now(timezone.utc).isoformat()
    ET.register_namespace("","http://www.w3.org/2005/Atom")
    et = ET.parse('../../feed.xml')

    root = et.getroot()
    print(root)
    updated = root.find('atom:updated', namespaces)
    if updated is not None:
        updated.text = str(dateTimeNow)
        print('here')
        print(updated)
        print(updated.text)


    newEntryTag = ET.SubElement(et.getroot(), 'entry')
    titleTag = ET.SubElement(newEntryTag, 'title')
    linkTag = ET.SubElement(newEntryTag, 'link')
    idTag = ET.SubElement(newEntryTag, 'id')
    updatedTag = ET.SubElement(newEntryTag, 'updated')
    summaryTag = ET.SubElement(newEntryTag, 'summary')


    titleTag.text = title
    linkTag.attrib['href'] = 'https://clarknado.neocities.org/pages/blog%20posts/'+todaysDate+'/post'
    idTag.text = 'https://clarknado.neocities.org/pages/blog%20posts/'+todaysDate+'/post'
    updatedTag.text = str(dateTimeNow)
    summaryTag.text = summary
    summaryTag.attrib['type'] = 'html'

    ET.indent(et.getroot(), space="  ")
    et.write('../../feed.xml', encoding='utf-8', xml_declaration=True)

    pass

def linkBlogPage(date, title):
    with open("../../pages/blog.html") as bloghtml:
        soup = bs4.BeautifulSoup(bloghtml.read(), features="html.parser")

    link = soup.new_tag("a", href='/pages/blog posts/'+date+'/post.html', 
                        string=date.replace('-','/') +' - ' + title)
    listItem = soup.new_tag("li")
    listItem.append(link)
    soup.find(id="postList").insert(0, listItem)
    #add new list item of format <a href="/pages/blog posts/DATE/post.html">DATE - TITLE</a>
    with open("../../pages/blog.html", 'w') as bloghtmlOut:
        bloghtmlOut.write(str(soup.prettify()))



def main():
    #take post from input (given name)
    if (len(sys.argv) == 2):
        postTitle = sys.argv[1]
        todaysDate = date.today().strftime('%m-%d-%y')

        #make a copy of the template to posts folder with new name
        outputPath = '../../pages/blog posts/' + todaysDate
        shutil.copytree('./input/template',outputPath, dirs_exist_ok=True)
        
        #read in markdown, convert to html, replace in template
        with open('./input/'+postTitle+'/'+postTitle+'.md') as inputMarkDown:
            inputMarkDownString = inputMarkDown.read()
            md = MarkdownIt()
            #print(md.render(inputMarkDownString))
            #TODO Fix RSS Feed
            updateRSSFeed(todaysDate, postTitle, md.render(inputMarkDownString))

            template = open('../../pages/blog posts/'+todaysDate+'/post.html', 'r')
            templateText = template.read()
            template.close()

            with open('../../pages/blog posts/'+todaysDate+'/post.html', 'w') as newPost:
                newPostText = templateText.replace('<p>TEMPLATE</p>',md.render(inputMarkDownString))
                newPost.write(newPostText)

                

        #copy Attachments folder into new folder
        shutil.copytree('./input/'+sys.argv[1]+'/Attachments',outputPath+'/Attachments', dirs_exist_ok=True)

        linkBlogPage(todaysDate,postTitle)

        #TODO fix RSS updated for whole thing

        #TODO Fix figures to be in a figure element

        #TODO Shit I just thought of something..

        #TODO automatically push to github? Maybe not. Would be convenient but
        #then publishing would ALWAYS push to prod

        #TODO Need to figure out how I can add images to notes on my phone. I'm
        #confident I can do this, but just need to figure out how exactly.

    else:
        print("no input given")
        print("script must be called in the following format:")
        print("python main.py \"Title of Entry\"")



        #copy over pictures





if __name__ == "__main__":
    main()