# To login to my SQL Database, use this command:
# $ mysql -u ian -p
# The password is: Delpenine1971~

# For SQL commands: https://www.cyberciti.biz/faq/mysql-command-to-show-list-of-databases-on-server/
# For SQL commands: https://www.a2hosting.com/kb/developer-corner/mysql/managing-mysql-databases-and-users-from-the-command-line

from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:5555/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app) 

id = db.engine.execute('select count(id) from blogs').scalar() + 1

print("--------------------------------")
print("This is the printed id:" + str(id))

class Blogs(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, name, body):
        self.name = name
        self.body = body

@app.route('/', methods=['GET'])
def index():

	tasks = Blogs.query.all()

	return render_template('blog.html',title="Build a Blog!", tasks=tasks)	 


@app.route('/blog', methods=['GET'])
def index2():
    tasks = Blogs.query.all()
    return render_template('blog.html', title="Build a Blog!", 
        tasks=tasks)



@app.route('/newpost', methods=['POST', 'GET'])
def index3():
    if request.method == 'POST':
        blogs_title = request.form['entry_title']
        blogs_body = request.form['body']

        title_error = ""
        body_error = ""
        
        if not blogs_title:
            title_error = "A title is required"
        if not blogs_body:
            body_error = "Blog content is required"
        if title_error or body_error:
            return render_template('newpost.html', entry_title = blogs_title, title_error_render = title_error,
            body = blogs_body, body_error_render = body_error)

        new_post = Blogs(blogs_title, blogs_body)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for('.index4', id = id))

    return render_template('newpost.html', title = "Add a new blog entry", entry_title = "", body = "")

@app.route('/blogs?id=<id>', methods=['GET'])
def index4(id):
    
    post = Blogs.query.filter_by(id=int(id))
    
    return render_template('entry.html', tasks=post)

if __name__ == '__main__':    
    app.run()