import json
from flask import Blueprint, jsonify, request

job_routes = Blueprint('jobs_routes', __name__)

#Function to read jobs from the JSON file
def read_jobs():
    with open('jobs.json', 'r') as f:
        return json.load(f)
    
#Function to write jobs to the JSON file
def write_jobs(jobs):
    with open('jobs.json', 'w') as f:
        json.dump(jobs, f, indent=4)

#Route to get all jobs
@job_routes.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = read_jobs
    return jsonify(jobs)

#Route to add a new job
@job_routes.route('/add-job', methods=['POST'])
def add_job():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    jobs = read_jobs()
    new_job = {
        'id': len(jobs) + 1, 
        'title': data['title'],
        'description': data['description'],
        'company': data['company']
    }
    jobs.append(new_job)
    write_jobs(jobs)

    return jsonify({'message': 'Job added successfully'}), 201

# Route to get a job by ID
@job_routes.route('/job/<int:job_id>', methods=['GET'])
def get_job(job_id):
    jobs = read_jobs()
    job = next((job for job in jobs if job['id'] == job_id), None)
    
    if job is not None:
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

# Route to update a job
@job_routes.route('/update-job/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    jobs = read_jobs()
    job = next((job for job in jobs if job['id'] == job_id), None)

    if job is not None:
        job['title'] = data.get('title', job['title'])
        job['description'] = data.get('description', job['description'])
        job['company'] = data.get('company', job['company'])
        write_jobs(jobs)
        return jsonify({'message': 'Job updated successfully'})
    return jsonify({'error': 'Job not found'}), 404

# Route to delete a job
@job_routes.route('/delete-job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    jobs = read_jobs()
    job = next((job for job in jobs if job['id'] == job_id), None)

    if job is not None:
        jobs.remove(job)
        write_jobs(jobs)
        return jsonify({'message': 'Job deleted successfully'})
    return jsonify({'error': 'Job not found'}), 404