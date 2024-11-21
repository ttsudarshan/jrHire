from models import Job
from flask import render_template ,request , jsonify ,url_for
from sqlalchemy.sql import text
# import random
import stripe


def register_routes(app, db):
    app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51QMBs0CmDlczV4oJTM2Y89b0GegNKH6XxZpSS0sgzxac8JncG1IBEZkxjuHwv3sswXHN89iXtVVlpig7kZEzL28T000I3PrEC1'
    app.config['STRIPE_PRIVATE_KEY'] = 'sk_test_51QMBs0CmDlczV4oJV1syJcavkvvADgXlLJxKhj7pvJ2jqKrDwVz9N61UEyMq7C1s701kYl3JBIEueYOtM5kGoJ3d00Gk2eiRru'
        
    
    @app.route('/pineapple')
    def pineapple():
        jobs = Job.query.all()
        return str(jobs)
    
        
    # @app.route('/')
    # def landingpage():
    #     # Get all jobs
    #     jobs = Job.query.all()
        
        # tags = set()
        # for job in jobs:
        #     tags.update(tag.strip() for tag in job.tags.split(','))
        # tags = list(tags)
        # return render_template('index.html', jobs=jobs )
       
        # @app.template_filter('split_tags')
        # def split_tags(tags):
        #     tags = tags.split(',')
        #     return tags
        
    @app.route('/')
    def landingpage():
        per_page = 10  # Number of jobs per page
        page = 1
        jobs = Job.query.order_by(Job.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return render_template('index.html', jobs=jobs)
      
    @app.route('/load_more')
    def load_more():
        page = int(request.args.get('page', 1))
        per_page = 10
        jobs = Job.query.order_by(Job.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert each job to a dictionary
        job_data = [
            {
                'id': job.id,
                'company_name': job.company_name,
                'job_title': job.job_title,
                'job_type': job.job_type,
                'created_at': job.created_at.isoformat(),  # Convert datetime to string format
                'introduction': job.introduction,
                'time_period': job.time_period,
                'compensation_per_hour': job.compensation_per_hour,
                'description': job.description,
                'benefits': job.benefits,
                'requirements': job.requirements,
                'location': job.location,
                'tags': job.tags,
                'profile_colors': job.profile_colors,
                'is_remote': job.is_remote,
                'is_paid': job.is_paid,
                'is_worldwide': job.is_worldwide
            }
            for job in jobs
        ]
        return jsonify(job_data)

        
    @app.route('/api/search-jobs')
    def search_jobs():
        query = request.args.get('query', '').lower()
        if not query:
            jobs = Job.query.all()
        else:
            jobs = Job.query.filter(
                (Job.job_title.ilike(f'%{query}%')) |
                (Job.tags.ilike(f'%{query}%'))
            ).all()
        
        return jsonify([{
            'id': job.id,
            'job_title': job.job_title,
            'company_name': job.company_name,
            'location': job.location,
            'compensation_per_hour': job.compensation_per_hour,
            'tags': job.tags,
            'created_at': job.created_at,
            'profile_colors': job.profile_colors 
        } for job in jobs])
        
        
    @app.route('/post-job', methods=['GET', 'POST'])
    def jobpage():
        
            
        stripe.api_key = app.config['STRIPE_PRIVATE_KEY']
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price':'price_1QNCfJCmDlczV4oJ4jnb3Z0m',
                'quantity': 1,
            }],
            mode ='payment',
            success_url=url_for('landingpage' , _external=True),    
            cancel_url=url_for('landingpage' , _external=True)    
        )
              
        if request.method == 'POST':
            # Get data from form
            company_name = request.form['company_name']
            job_title = request.form['job_title']
            job_type = request.form['job_type']
            introduction = request.form['introduction']
            time_period = request.form['time_period']
            compensation_per_hour = request.form['compensation_per_hour']
            description = request.form['description']
            benefits = request.form['benefits']
            requirements = request.form['requirements']
            location = request.form['location']
            tags = request.form['tags']
            profile_colors = request.form['profile_colors']
            url_ats= request.form['url_ats']
        # Fix for radio button handling
            is_remote = request.form.get('is_remote') == 'yes'
            is_paid = request.form.get('is_paid') == 'yes'
            is_worldwide = request.form.get('is_worldwide') == '1'

        # Now these variables will be True if 'yes'/'1' is selected, False if 'no'/'0' is selected
        # Convert to integer for database if needed
            # is_remote_int = 1 if is_remote else 0
            # is_paid_int = 1 if is_paid else 0
            # is_worldwide_int = 1 if is_worldwide else 0

            # Create a new job entry
            new_job = Job(
                company_name=company_name,
                job_title=job_title,
                job_type=job_type,
                introduction=introduction,
                time_period=time_period,
                compensation_per_hour=compensation_per_hour,
                description=description,
                benefits=benefits,
                requirements=requirements,
                location=location,
                tags=tags,
                profile_colors=profile_colors,
                url_ats=url_ats,
                is_remote=is_remote,
                is_paid=is_paid,
                is_worldwide=is_worldwide
            )

            # Add and commit the new job to the database
            db.session.add(new_job)
            db.session.commit()
            return "Job added successfully!"
        else:
            return render_template('job_post.html' , checkout_session=session['id'] , checkout_public_key=app.config['STRIPE_PUBLIC_KEY'])
        
    @app.route('/jobs/<id>')
    def indie_job_page(id):
        jobs = Job.query.filter_by(id=id).first()     
        # benefits = list(Job.query.with_entities(Job.benefits).filter_by(id=id).first())
        # benefits = Job.query.with_entities(Job.benefits).filter_by(id=id).first().benefits.split(',')

        benefits = Job.query.with_entities(Job.benefits).filter_by(id=id).first()
        benefits = list(map(lambda x: x.strip().capitalize(), benefits.benefits.split(',')))

        tags = Job.query.with_entities(Job.tags).filter_by(id=id).first().tags.split(',')
        tags = list(map(lambda x: x.strip().capitalize(), tags))   
        
        return render_template('indie_job_page.html' , jobs=jobs , benefits=benefits , tags=tags )

    @app.route('/runs')
    def runs():
        # Create a new job entry
        new_job = Job(
            company_name="Google",
            job_title="Data Engineer",
            job_type="Intern",  # intern , traniee , associate , junior
            introduction="Join a team of experts working at the intersection of AI and data engineering.",  # Adding introduction
            time_period="3", # in months
            compensation_per_hour=50,  # Example hourly compensation
            description="Work with large data sets and machine learning models.",
            benefits="Health insurance, 401k, remote options",
            requirements="Experience in Python and SQL, knowledge of machine learning.",  # Adding requirements
            location="USA",  # Adding location
            tags="Python, Pytorch, Data Engineering",
            profile_colors="#0000FF",  # Example color
            is_remote=True,
            is_paid=True,
            is_worldwide=True
        )
            
        # Add and commit the new job to the database
        db.session.add(new_job)
        db.session.commit()
        
        return "Job added successfully!"

        
        