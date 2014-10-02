#!/usr/bin/env python
import web, os, sys

root = os.path.join(os.path.dirname(__file__)+"/")
sys.path.insert(0, root)
static = os.path.join(os.path.dirname(__file__)+"/static/")
templates = os.path.join(os.path.dirname(__file__)+"/templates/")
sys.path.insert(1, templates)
os.chdir(root)

urls = (
    '/', 'index',
    '/blog', 'blog',
    '/about', 'about',
    '/photography', 'photography',
    '/resume', 'resume',
    '%s/static/images/photos/.*'%(root), 'images'
)

application = web.application(urls, globals())
web.config.debug = True

render = web.template.render(templates, base='base')

class index:
    def GET(self):
        return render.index()        
class blog:
    def GET(self):
        return render.blog()
class about:
    def GET(self):
        bio = open('%s/bio/bio.txt'%(root), 'r')
        return render.about(bio)
class photography:
    def GET(self):
        import os

        total_con=os.listdir('%s/static/images/photos'%(root))

        files=[]

        for f_n in total_con:
            if f_n.split('.')[1] == 'jpg':
                files.append(f_n)
        
        return render.photography(files)
class resume:
    def GET(self):
        return render.resume()


if __name__ == '__main__':
	web.application(urls, globals()).run()
