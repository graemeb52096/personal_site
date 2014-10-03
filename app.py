#!/usr/bin/env python
import web, os, sys, json
import model

root = os.path.join(os.path.dirname(__file__)+"/")
sys.path.insert(0, root)
static = os.path.join(os.path.dirname(__file__)+"/static/")
templates = os.path.join(os.path.dirname(__file__)+"/templates/")
sys.path.insert(1, templates)
os.chdir(root)

t_globals = {
    'datestr': web.datestr
}

urls = (
    '/', 'index',
    #blog sites
    '/blog', 'blog',
    '/view/(.*)', 'View',
    '/new', 'New',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    #end of blog sites
    '/about', 'about',
    '/photography', 'photography',
    '/resume', 'resume',
    '%s/static/images/photos/.*'%(root), 'images'
)

application = web.application(urls, globals())
web.config.debug = True

render = web.template.render(templates, base='base', globals=t_globals)

class index:
    def GET(self):
        return render.index()    
#blog classes    
class blog:
    def GET(self):
        posts = model.get_posts()
        return render.blog(posts)
class View:

    def GET(self, id):
        """ View single post """
        post = model.get_post(int(id))
        time = post.posted_on
        time_str = str(time)
        time_split = time_str.split(' ')
        date = time_split[0]
        time = time_split[1]
        return render.view(post,date)


class New:

    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, 
            description="Post title:"),
        web.form.Textarea('content', web.form.notnull, 
            description="Post content:"),
        web.form.Textbox('link', web.form.notnull,
            description="Link: "),
        web.form.Textbox('link_name', web.form.notnull,
            description="Link Name: "),
        web.form.Password('password', web.form.notnull,
            description="Super Secret Password:"),
        web.form.Button('Post entry'),
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        if str(form.d.password) == '123':
            model.new_post(form.d.title, form.d.content, form.d.link, form.d.link_name)
            raise web.seeother('/')
        else:
            return render.new(form)

class Delete:

    def POST(self, id):
        form = web.input()
        password = form.password
        if str(password) == '123':
            model.del_post(int(id))
            raise web.seeother('/')
        else:
            return render.base('<br><br><br><br><br>Youre Evil')


class Edit:

    def GET(self, id):
        post = model.get_post(int(id))
        form = New.form()
        form.fill(post)
        return render.edit(post, form)


    def POST(self, id):
        form = New.form()
        post = model.get_post(int(id))
        if not form.validates():
            return render.edit(post, form)
        if str(form.d.password) == '123':
            model.update_post(int(id), form.d.title, form.d.content, form.d.link, form.d.link_name)
            raise web.seeother('/')
        else:
            return render.edit(post, form)
#end blog classes

class about:
    def GET(self):
        bio = open('%s/bio/bio.txt'%(root), 'r')
        return render.about(bio)
class photography:
    def GET(self):

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
