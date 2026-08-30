I want to make a cool website. It should initially have a homepage, navigation, 
a link that takes you to the most recent post, and an archive of previous blog posts.

First thing's first - is there a better way to upload files to neocities? I guess I
can just duplicate the files that are there already locally and drag them over as I
update them. Is there a better way? FTP maybe?

Looks like I can upload to github and have it copy over as an action. That's okay,
I don't need to do all that. I'll stick to drag and drop.


In terms of building the site - I plan to cobble together something fairly 
simple to start, and then maybe look into static site generators (or even 
build one?) afterwards. Really just looking to do a home / blog / about page
to kick this off

At the moment this page does not need a backend - if I want to do that later
I can always save off the files and dump them into something self hosted.


##### Blog Plan #####
There's a lot of different ways to approach this. Obviously, at this point I
have already built the foundation of a site, so I won't be going the CMS route.
This leaves a few options still, between static site generators that can still
be used in tandem with my site, manual creation of html files and updating of
the index page, maybe even building my own tools.

If I were to build my own tool, I would probably use Python or similar to make
something that can take a series of basic html files, put them in order in a
list by date, update the index page, set up pagination for all the files, and
then update the RSS feed. I think that covers everything. I could make a 
new component for comments and have the tool throw one at the end of each
post. Maybe each post would need a folder which contained the html and a json
file for the comments, plus pictures for that post. 

That said, I probably should try to get this out sooner than later. I can begin
by just manually updating the index file and not having blog posts link to one
another. I can still use a folder for all blog posts, and a folder for each 
post to keep them separated.






##### CODING PRACTICES #####
* For text documents that will not be put on the site, 80 character limit (like
this readme for example)

##### STYLE #####
I think that it makes the most sense to have the backgrounds be scenery from nepal
Other motifs - yarn borders, paper backgrounds?
a lot of this can come later - for now focus on functionality

##### OTHER #####
Want to put more of those 80x31 tags on the page. those are cute

##### Note to Self #####
It's been a while since I've updated this readme, so I should go over it sometime soon. In the meantime, I want to write myself some quick notes on using the site generator
 * navigate to the site generator, activate environment with 'source ./venv/bin/activate'
 * move your exported note folder (including md file and attachments folder) into input folder
 * run [python main 'folder name']
 * copy the new files (feed.xml, blog.html, blog entry) to neocities. Ideally, this will be handled by a github action in the future.