# from flask import Flask , render_template
# app = Flask(__name__)

# @app.route('/')
# def landingpage():
#     return render_template('index.html')

# @app.route('/post-job')
# def jobpage():
#     return render_template('job_post.html')
    
# @app.route('/jobs/<post_name>')
# def indie_job_page(post_name):    
#     content = {'post_name': post_name,
#                'names': 'simangka'
#                }              
#     return render_template('indie_job_page.html', **content)


# if __name__ == '__main__':
#     app.run(debug=True)