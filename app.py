import json
from flask import Flask, jsonify, request
from routes.jobs_routes import job_routes  # Import init_routes from the routes module
from flask_cors import CORS

def init_routes(app):
    app.register_blueprint(job_routes)
    
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

JOB_DB_FILE = 'jobs.json'

# Function to read jobs from the JSON file
def read_jobs():
    with open('jobs.json', 'r') as f:
        return json.load(f)

# Function to write jobs to the JSON file
def write_jobs(jobs):
    with open('jobs.json', 'w') as f:
        json.dump(jobs, f, indent=4)

# Route to get all jobs
@app.route('/jobs', methods=['GET'])
def get_jobs():
    jobs = read_jobs()
    return jsonify(jobs)

# Route to add a new job
@app.route('/add-job', methods=['POST'])
def add_job():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    jobs = read_jobs()
    new_job = {
        'id': len(jobs) + 1,  # Simple ID assignment
        'jobName': data['jobName'],
        'dateposted': data['dateposted'],
        'company': data['company'],
        'description': data['description'],
        'responsibilities': data['responsibilities'],
        'location': data['location'],
        'positionType': data['positionType'],
        'requirements': data['requirements'],
        'salary': data['salary'],
    }
    jobs.append(new_job)
    write_jobs(jobs)
    
    return jsonify({'message': 'Job added successfully'}), 201

# Route to get a job by ID
@app.route('/job/<int:job_id>', methods=['GET'])
def get_job(job_id):
    jobs = read_jobs()
    job = next((job for job in jobs if job['id'] == job_id), None)
    
    if job is not None:
        return jsonify(job)
    return jsonify({'error': 'Job not found'}), 404

# Route to update a job
@app.route('/update-job/<int:job_id>', methods=['PUT'])
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
@app.route('/delete-job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    jobs = read_jobs()
    job = next((job for job in jobs if job['id'] == job_id), None)

    if job is not None:
        jobs.remove(job)
        write_jobs(jobs)
        return jsonify({'message': 'Job deleted successfully'})
    return jsonify({'error': 'Job not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)# Initialize the routes
    init_routes(app)

import sys
print(sys.path)
