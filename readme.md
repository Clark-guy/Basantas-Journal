#Basanta's Journal

This is the code for my blog, hosted on neocities.org. You can find my site at
https://www.clarknado.neocities.org/. The name is a play on Sharknado with my
Middle name, Clark.

TODO:
 * Make a dark mode stylesheet
 * revamp home page - compress site updates section, have a link to most recent blog post
 * consider GitHub actions to update neocities



##### CODING PRACTICES #####
* For text documents that will not be put on the site, 80 character limit (like
this readme for example)

##### STYLE #####
I think that it makes the most sense to have the backgrounds be scenery from nepal
Other motifs - yarn borders, paper backgrounds?
a lot of this can come later - for now focus on functionality

##### OTHER #####
Want to put more of those 80x31 tags on the page. those are cute

##### Static Site Generation #####
It's been a while since I've updated this readme, so I should go over it sometime soon. In the meantime, I want to write myself some quick notes on using the site generator
 * navigate to the site generator, activate environment with 'source ./venv/bin/activate'
 * move your exported note folder (including md file and attachments folder) into input folder
 * run [python main 'folder name']
 * copy the new files (feed.xml, blog.html, blog entry) to neocities. Ideally, this will be handled by a github action in the future.

If I fix it so my script uploads to github automatically, and then via a github action updates neocities, I could use a scheduled task on macos to watch the input folder for a new file, and have it scoop it up every so often instead of doing it by hand. Then every time I exported to that folder, it would run the script, upload to github, github would upload to neocities, and all I would need to do is verify it made it over a few minutes later. Might be over-engineering this slightly.

