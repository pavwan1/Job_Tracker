from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Job


jobs = Blueprint('jobs', __name__)

    

@jobs.route('/add', methods=['POST'])
def add_job():
    data = request.get_json()
    company = data.get('company')
    position = data.get('position')
    status = data.get('status', 'pending')
    
    new_job = Job(company=company, position=position, status=status, user_id=current_user.id)
    db.session.add(new_job)
    db.session.commit()
    
    return jsonify({'message': "Job added successfully", "Job":new_job.to_dict()}), 201

@jobs.route('/jobs', methods=["GET"])
def get_all_jobs():
    
    jobs = Job.query.filter_by(user_id=current_user.id).all()
    
    jobs_list = [job.to_dict() for job in jobs]
    
    return jsonify(jobs_list), 200

@jobs.route('/jobs/<int:id>', methods=["POST", "PUT"])
def update_job(id):
    
    job = Job.query.filter_by(user_id=current_user.id).first()  
    
    if not job:
        return jsonify({"message": "Job not found"}), 404
    
    data = request.get_json()
    
    job.company = data.get('company', job.company)
    job.position = data.get('position', job.position)
    job.status = data.get('status', job.status)
    print("Incoming status:", data.get('status'))
    print("Current job status before commit:", job.status)
    
    db.session.commit()
    
    return jsonify({'message':'Job updated', "job":job.to_dict()}), 200

@jobs.route('/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    
    job = Job.query.get_or_404(id)
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({'message':f'Job with {id} deleted successfully'}), 200

    