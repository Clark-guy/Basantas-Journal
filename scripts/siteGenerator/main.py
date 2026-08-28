import sys
import shutil
from datetime import date
import bs4

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


def main():
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

    



if __name__ == "__main__":
    main()