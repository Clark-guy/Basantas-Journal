import sys
import shutil
from datetime import date, datetime, timezone
import bs4
from pprint import pprint
from markdown_it import MarkdownIt
import xml.etree.ElementTree as ET
from PIL import Image
import pillow_heif
from pathlib import Path
from pymov2gif import convert

#This python file should take in a bunch of text and make it into a blog post
#for starters just going to have it piped in, but ultimately could use tkinter
#for a user interface

#to use this script in the future:

'''
1. Export the apple notes file into the 'input' folder in siteGenerator. It 
should create a folder with the name you specify, and a .md file with the same
name

2. run 'source .venv/bin/activate' from siteGenerator to activate the 
virtual environment

3. run 'python ./main.py "foldername"' to generate the new entry. Don't specify
the path to the folder, just its name. E.g. 'python ./main "IST"'

3.5 - for a dry run (no rss update, no linking to the /posts folder) add -d

4. manually move files to neocities. That means copy the new post, feed.xml,
blog.html. 


TODO:
1. would be a good idea to fix the figure elements so images can be minimized
for easier reading.

2. would also be a good idea to make images work with the simple newsletter -
this is just a matter of fixing the rss feed script to supply the correct url.

3. I could make it so that if dryRun is false, it automatically pushes to 
github. Or even have a separate flag to do that.
'''



def updateRSSFeed(todaysDate,title,summary):
    namespaces = {'atom': 'http://www.w3.org/2005/Atom'}
    dateTimeNow = datetime.now(timezone.utc).isoformat()
    ET.register_namespace("","http://www.w3.org/2005/Atom")
    et = ET.parse('../../feed.xml')

    root = et.getroot()
    updated = root.find('atom:updated', namespaces)
    if updated is not None:
        updated.text = str(dateTimeNow)



    newEntryTag = ET.Element('entry')
    titleTag = ET.SubElement(newEntryTag, 'title')
    linkTag = ET.SubElement(newEntryTag, 'link')
    idTag = ET.SubElement(newEntryTag, 'id')
    updatedTag = ET.SubElement(newEntryTag, 'updated')
    publishedTag = ET.SubElement(newEntryTag, 'published')
    summaryTag = ET.SubElement(newEntryTag, 'summary')


    titleTag.text = title
    linkTag.attrib['href'] = 'https://clarknado.neocities.org/pages/blog%20posts/'+todaysDate+'/post'
    idTag.text = 'https://clarknado.neocities.org/pages/blog%20posts/'+todaysDate+'/post'
    updatedTag.text = str(dateTimeNow)
    publishedTag.text = str(dateTimeNow)
    summaryTag.text = summary
    summaryTag.attrib['type'] = 'html'

    #index 5 - insert at top
    root.insert(5, newEntryTag)
    ET.indent(et.getroot(), space="  ")
    et.write('../../feed.xml', encoding='utf-8', xml_declaration=True)


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

def convertHeicToJpeg(filename):
    heif_file = pillow_heif.read_heif(filename)
    outputImage = Image.frombytes(
        heif_file.mode,
        heif_file.size,
        heif_file.data,
        "raw",
    )
    outputImage.save(filename.replace('.heic', '.jpeg'), format("jpeg"))
    #delete original heic file
    Path(filename).unlink(missing_ok=False)

def resizeImage(filename):
    #resize image to like a reasonable size
    img = Image.open(filename.replace('.heic', '.jpeg'))
    baseWidth = 600
    wpercent = (baseWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((baseWidth, hsize), Image.Resampling.LANCZOS)
    img.save(filename.replace('.heic', '.jpeg'))

def movToGif(filename):
    print(filename)
    convert(filename, resolution='800x450', framerate=20, output_file=f'{filename[:-4]}.gif')

def processAttachments(filename):
    #print(filename)
    ext = Path(filename).suffix.lower()

    match ext:
        case '.heic':
            convertHeicToJpeg(filename)
            resizeImage(filename.replace('.heic', '.jpeg'))
        case '.jpeg':
            resizeImage(filename)
        case '.mov':
            movToGif(filename)

        

    


def fixMarkdownItalics(inputMarkDownString):
    #This is such a shitty way to fix this. I should come up with
    #something better, but unfortunately it works as is.
    #It just replaces the markdown stars with <i> tags since the
    #converter seems to fail to do that itself.

    inputMarkDownStringFixedItalics = ''
    openTag = True
    for char in inputMarkDownString:
        if char == '*':
            #print('found a star')
            if openTag:
                inputMarkDownStringFixedItalics += '<i>'
                openTag = False
            else:
                inputMarkDownStringFixedItalics += '</i>'
                openTag = True
        else:
            inputMarkDownStringFixedItalics += char
    return inputMarkDownStringFixedItalics



#this function fixes video tags with beautiful soup.
#since neocities does not support video files on free accounts,
#i won't be using this right now. I may in the future.
def fixVideoTags(html):
    soup = bs4.BeautifulSoup(html, features="html.parser")
    #print(str(soup.prettify()))
    #print('\n\nbefore:')
    #for tag in soup.find_all("img", alt="Movie"):
    #    print(tag)

    #print('--\nafter:')
    for oldtag in soup.find_all("img", alt="Movie"):
        tag = soup.new_tag("video")
        tag.attrs = oldtag.attrs.copy()
        oldtag.replace_with(tag)
        #tag.name='video'
        tag['controls'] = ''
        tag.parent.name= 'details'
        summary = soup.new_tag("summary")
        summary.string="video"
        tag.parent.append(summary)
        tag.wrap(soup.new_tag("figure"))

        details = tag.parent.parent
        #details.br.extract()

        details.contents[2].wrap(soup.new_tag("figcaption"))

        
        #print(details.figcaption)
        #print(details.figure)
        #print("VIDEO: ")
        #print(details.figure.video)
        details.figure.append(details.figcaption.extract())
        details.contents[1].extract()
        #print(details.figcaption)
        #print(details.figure)'''

        
        #for item in (tag.parent.parent.contents):
        #    print(f'item: {item}')
        #    print('movie)')
    
    #print(str(soup.prettify()))
    return (str(soup.prettify()))


def main():
    #take post from input (given name)
    if (len(sys.argv) >= 2):
        
        dryRun = False
        if (len(sys.argv) >2):
            dryRun = True if (sys.argv[2] == "-d") else False
        print(f"dry run: {dryRun}")

        postTitle = sys.argv[1]
        todaysDate = date.today().strftime('%m-%d-%y')

        #make a copy of the template to posts folder with new name
        outputPath = '../../pages/blog posts/' + todaysDate
        shutil.copytree('./input/template',outputPath, dirs_exist_ok=True)
        
        #read in markdown, convert to html, replace in template
        with open('./input/'+postTitle+'/'+postTitle+'.md') as inputMarkDown:
            inputMarkDownString = inputMarkDown.read().replace('.heic','.jpeg').replace('.mov','.gif')

            inputMarkDownStringFixedItalics = fixMarkdownItalics(inputMarkDownString)
            #print(inputMarkDownStringFixedItalics)

            md = MarkdownIt()
            # md.enable('emphasis') # TODO: it's possible this would fix the "fixMarkdownItalics" thing 
            if not dryRun:
                updateRSSFeed(todaysDate, postTitle, md.render(inputMarkDownStringFixedItalics))

            template = open('../../pages/blog posts/'+todaysDate+'/post.html', 'r')
            templateText = template.read()
            template.close()

            #print(md.render(inputMarkDownStringFixedItalics))
            

            with open('../../pages/blog posts/'+todaysDate+'/post.html', 'w') as newPost:
                newPostText = templateText.replace('<p>TEMPLATE</p>',md.render(inputMarkDownStringFixedItalics))
                newPost.write(newPostText)

                

        #Convert all images to jpeg and resize
        attachmentFolder = Path('./input/'+sys.argv[1]+'/Attachments')
        for image in attachmentFolder.iterdir():
            processAttachments('./input/'+sys.argv[1]+'/Attachments'+'/'+image.name)
        
        #copy Attachments folder into new folder
        shutil.copytree('./input/'+sys.argv[1]+'/Attachments',outputPath+'/Attachments', dirs_exist_ok=True)

        if not dryRun:
            linkBlogPage(todaysDate,postTitle)


    else:
        print("Wrong number of inputs")
        print("script must be called in one of the following formats:")
        print("python main.py \"Title of Entry\"")
        print("python main.py \"Title of Entry\" -d")


if __name__ == "__main__":
    main()