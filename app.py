import web

urls = (
    '/', 'index',
    '/blog', 'blog',
    '/about', 'about',
    '/photography', 'photography',
    '/resume', 'resume',
    '/static/images/photos/.*' 'images'
)

application = web.application(urls, globals())
web.config.debug = True

render = web.template.render('templates/', base='base')

class index:
    def GET(self):
        return render.index()        
class blog:
    def GET(self):
        return render.blog()
class about:
    def GET(self):
        return render.about()
class photography:
    def GET(self):
        import os

        total_con=os.listdir('static/images/photos')

        files=[]

        for f_n in total_con:
            if f_n.split('.')[1] == 'jpg':
                files.append(f_n)
        
        return render.photography(files)
class resume:
    def GET(self):
        return render.resume()
        
if __name__ == "__main__": 
    app = web.application(urls, globals())
    app.run() 