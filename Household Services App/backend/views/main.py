from flask import Blueprint, request, jsonify, send_from_directory, abort, current_app
from models import db, Admin, Customer, Professional, Service, ServiceRequest
from extensions import cache, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy import String, func
from flask_login import current_user, login_user, logout_user
import os
import uuid
import pytz
from werkzeug.utils import secure_filename

main_blueprint = Blueprint('main', __name__)

@login_manager.user_loader
def load_user(user_id):
    user_type, id = user_id.split('-')
    if user_type == 'customer':
        return Customer.query.get(int(id))
    elif user_type == 'professional':
        return Professional.query.get(int(id))
    elif user_type == 'admin':
        return Admin.query.get(int(id))
    else:
        return None
    
IST = pytz.timezone('Asia/Kolkata')

def format_date_to_ist(date):
    if date:
        return date.astimezone(IST).strftime('%d-%m-%Y %I:%M %p')
    return None

@main_blueprint.route('/customer_signup', methods=['POST'])
def customer_signup():
    data = request.get_json()
    if Customer.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    customer = Customer(
        email=data['email'],
        password=hashed_password,
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        address=data['address'],
        pin_code=data['pin_code']
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "Customer registered successfully", "user_id": customer.id}), 201

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'cv_files')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_blueprint.route('/professional_signup', methods=['POST'])
def professional_signup():
    data = request.form
    file = request.files.get('cv_file')

    if Professional.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400

    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        cv_filename = unique_filename
    else:
        cv_filename = None

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    professional = Professional(
        email=data['email'],
        password=hashed_password,
        full_name=data['full_name'],
        phone_number=data['phone_number'],
        address=data['address'],
        pin_code=data['pin_code'],
        service_name=data['service_name'],
        experience=data['experience'],
        status='pending',
        cv_file=cv_filename
    )
    db.session.add(professional)
    db.session.commit()
    return jsonify({"message": "Professional registered successfully", "user_id": professional.id}), 201

@main_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    admin = Admin.query.filter_by(email=email).first()
    if admin and check_password_hash(admin.password, password):
        login_user(admin)
        return jsonify({"message": "Admin login successful", "user_id": admin.id, "role": "admin", "full_name": admin.full_name}), 200

    customer = Customer.query.filter_by(email=email).first()
    if customer and check_password_hash(customer.password, password):
        login_user(customer)
        return jsonify({"message": "Login successful", "user_id": customer.id, "role": "customer", "full_name": customer.full_name}), 200

    professional = Professional.query.filter_by(email=email).first()
    if professional and check_password_hash(professional.password, password):
        login_user(professional)
        return jsonify({"message": "Login successful", "user_id": professional.id, "role": "professional", "full_name": professional.full_name}), 200

    return jsonify({"error": "Invalid email or password"}), 401

# Logout
@main_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

# Create a New Service
@main_blueprint.route('/create_service', methods=['POST'])
def create_service():
    data = request.get_json()
    service = Service(
        name=data['name'],
        price=data['price'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({"message": "Service created successfully"}), 201

# Update Service
@main_blueprint.route('/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    data = request.get_json()
    service.name = data.get('name', service.name)
    service.price = data.get('price', service.price)
    service.category= data.get('category', service.category)
    service.description = data.get('description', service.description)

    db.session.commit()
    return jsonify({"message": "Service updated successfully"}), 200

# DELETE Service
@main_blueprint.route('/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200

@main_blueprint.route('/services/category/<string:category>', methods=['GET'])
#@cache.cached(timeout=300)
def get_services_by_category(category):
    services = Service.query.filter_by(category=category).all()
    services_list = [
        {"id": s.id, "name": s.name, "price": s.price, "description": s.description}
        for s in services
    ]
    return jsonify(services_list), 200

# Get all unique categories
@main_blueprint.route('/services/categories', methods=['GET'])
#@cache.cached(timeout=300)
def get_service_categories():
    categories = db.session.query(Service.category).distinct().all()
    category_list = [category[0] for category in categories]
    return jsonify(category_list), 200

# View All Services
@main_blueprint.route('/services', methods=['GET'])
#@cache.cached(timeout=300)
def get_services():
    services = Service.query.all()
    services_list = [{"id": s.id, "name": s.name, "price": s.price, "category":s.category , "description": s.description} for s in services]
    return jsonify(services_list)

@main_blueprint.route('/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    return jsonify({
        "id": service.id,
        "name": service.name,
        "price": service.price,
        "description": service.description,
        "category": service.category
    }), 200

# View All Professionals
@main_blueprint.route('/professionals', methods=['GET'])
def get_professionals():
    professionals = Professional.query.all()
    professionals_list = []
    for p in professionals:
        average_rating = (
            db.session.query(db.func.avg(ServiceRequest.rating))
            .filter(ServiceRequest.professional_id == p.id, ServiceRequest.rating.isnot(None))
            .scalar()
        )
        
        average_rating = round(average_rating, 2) if average_rating else "N/A"
        
        professionals_list.append({
            "id": p.id,
            "username": p.full_name,
            "experience": p.experience,
            "service_name": p.service_name,
            "status": p.status,
            "average_rating": average_rating,
            "cv_file": p.cv_file
        })
    
    return jsonify(professionals_list), 200

@main_blueprint.route('/download_cv/<filename>', methods=['GET'])
def download_cv(filename):
    filename = secure_filename(filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        abort(404)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

# View All Approved Professionals
@main_blueprint.route('/professionals/approved', methods=['GET'])
#@cache.cached(timeout=300)
def get_approved_professionals():
    approved_professionals = Professional.query.filter_by(status='approved').all()
    approved_list = [
        {
            "id": p.id,
            "username": p.full_name,
            "experience": p.experience,
            "service_name": p.service_name
        }
        for p in approved_professionals
    ]
    return jsonify(approved_list), 200

# Approve Professional
@main_blueprint.route('/professionals/<int:professional_id>/approve', methods=['PATCH'])
def approve_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    professional.status = 'approved'
    db.session.commit()
    return jsonify({"message": "Professional approved successfully"}), 200

# Reject Professional
@main_blueprint.route('/professionals/<int:professional_id>/reject', methods=['PATCH'])
def reject_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    professional.status = 'rejected'
    db.session.commit()
    return jsonify({"message": "Professional rejected successfully"}), 200

# Delete Professional
@main_blueprint.route('/professionals/<int:professional_id>', methods=['DELETE'])
def delete_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    db.session.delete(professional)
    db.session.commit()
    return jsonify({"message": "Professional deleted successfully"}), 200

# Get Customer Profile
@main_blueprint.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    return jsonify({
        "full_name": customer.full_name,
        "address": customer.address,
        "pin_code": customer.pin_code,
        "phone_number": customer.phone_number
    }), 200

# Update Customer Profile
@main_blueprint.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.get_json()
    customer.full_name = data.get("full_name", customer.full_name)
    customer.address = data.get("address", customer.address)
    customer.pin_code = data.get("pin_code", customer.pin_code)
    customer.phone_number = data.get("phone_number", customer.phone_number)

    db.session.commit()
    return jsonify({"message": "Customer profile updated successfully"}), 200

# Get Professional Profile
@main_blueprint.route('/professionals/<int:professional_id>', methods=['GET'])
def get_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    return jsonify({
        "full_name": professional.full_name,
        "address": professional.address,
        "pin_code": professional.pin_code,
        "phone_number": professional.phone_number
    }), 200

# Update Professional Profile
@main_blueprint.route('/professionals/<int:professional_id>', methods=['PUT'])
def update_professional(professional_id):
    professional = Professional.query.get(professional_id)
    if not professional:
        return jsonify({"error": "Professional not found"}), 404

    data = request.get_json()
    professional.full_name = data.get("full_name", professional.full_name)
    professional.address = data.get("address", professional.address)
    professional.pin_code = data.get("pin_code", professional.pin_code)
    professional.phone_number = data.get("phone_number", professional.phone_number)

    db.session.commit()
    return jsonify({"message": "Professional profile updated successfully"}), 200

# Create Service Request
@main_blueprint.route('/create_request', methods=['POST'])
def create_request():
    data = request.get_json()
    customer_id = data.get('customer_id')
    
    if not customer_id:
        return jsonify({"error": "Customer ID is required"}), 400

    service_request = ServiceRequest(
        service_id=data['service_id'],
        customer_id=customer_id,
        professional_id=data.get('professional_id'),
        status='requested',
        remarks=data.get('remarks', ''),
        request_date=datetime.now()
    )
    db.session.add(service_request)
    db.session.commit()
    return jsonify({"message": "Service request created successfully", "request_id": service_request.id}), 201

# Close Service Request (Change status to 'completed')
@main_blueprint.route('/service_requests/<int:request_id>/close', methods=['PATCH'])
def close_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    if service_request.status != 'accepted':
        return jsonify({"error": "Service can only be closed if accepted"}), 400

    service_request.status = 'completed'
    service_request.completion_date = datetime.now()
    db.session.commit()

    return jsonify({"message": "Service closed successfully"}), 200

@main_blueprint.route('/service_requests/<int:request_id>/payment_details', methods=['GET'])
def get_payment_details(request_id):
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    # Fetch the associated service details
    service = service_request.related_service
    
    if not service:
        return jsonify({"error": "Service not found"}), 404

    # Return the service name and price
    response_data = {
        "service_name": service.name,
        "service_price": service.price  # return raw price for frontend formatting
    }
    
    return jsonify(response_data), 200

@main_blueprint.route('/assign_professional/<int:request_id>', methods=['PATCH'])
def assign_professional(request_id):
    data = request.get_json()
    service_request = ServiceRequest.query.get(request_id)
    
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    professional_id = data.get('professional_id')
    if not professional_id:
        return jsonify({"error": "Professional ID is required"}), 400

    professional = Professional.query.get(professional_id)
    
    if not professional or professional.status != 'approved':
        return jsonify({"error": "Professional not approved or does not exist"}), 400

    service = Service.query.get(service_request.service_id)
    if not service:
        return jsonify({"error": "Associated service not found."}), 404

    if (service.category or "").strip().lower() != (professional.service_name or "").strip().lower():
        return jsonify({"error": "Professional's service does not match the service category."}), 400

    service_request.professional_id = professional_id
    service_request.status = 'assigned'

    db.session.commit()

    return jsonify({"message": "Professional assigned successfully"}), 200

@main_blueprint.route('/customer_history', methods=['GET'])
def customer_service_history():
    customer_id = request.args.get('customer_id')
    service_requests = ServiceRequest.query.filter_by(customer_id=customer_id).all()
    
    history_list = [req.to_dict() for req in service_requests]
    
    return jsonify(history_list), 200

# Fetch service request details by ID
@main_blueprint.route('/service_requests/<int:request_id>', methods=['GET'])
def get_service_request(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404
    
    response_data = service_request.to_dict()

    return jsonify(response_data), 200

# Update Service Request Status (Accept/Reject)
@main_blueprint.route('/service_requests/<int:request_id>/status', methods=['PATCH'])
def update_service_request_status(request_id):
    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['accepted', 'rejected']:
        return jsonify({"error": "Invalid status"}), 400

    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    service_request.status = new_status
    db.session.commit()

    return jsonify({
        "message": f"Service request {new_status} successfully.",
        "service_request": {
            "id": service_request.id,
            "status": service_request.status,
            "customer_id": service_request.customer_id,
            "professional_id": service_request.professional_id,
            "request_date": service_request.request_date.isoformat() if service_request.request_date else None,
            "completion_date": service_request.completion_date.isoformat() if service_request.completion_date else None
        }
    }), 200

# Update Service Requests (Filtered by Assigned or Accepted)
@main_blueprint.route('/service_requests', methods=['GET'])
def get_service_requests():
    service_requests = ServiceRequest.query.options(
        joinedload(ServiceRequest.professional),
        joinedload(ServiceRequest.customer)
    ).all()

    requests_list = []
    for req in service_requests:
        professional_name = req.professional.full_name if req.professional else None
        customer_name = req.customer.full_name if req.customer else None
        customer_phone = req.customer.phone_number if req.customer else None
        customer_location = req.customer.address if req.customer else None
        request_data = {
            "id": req.id,
            "service_id": req.service_id,
            "customer_id": req.customer_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_location": customer_location,
            "professional_id": req.professional_id,
            "professional_name": professional_name,
            "status": req.status,
            "rating": req.rating,
            "remarks": req.remarks,
            "request_date": format_date_to_ist(req.request_date) if req.request_date else None,
            "completion_date": format_date_to_ist(req.completion_date) if req.completion_date else None,
        }
        requests_list.append(request_data)
    return jsonify(requests_list), 200

# Review Service Request
@main_blueprint.route('/review_request/<int:request_id>', methods=['POST'])
def submit_service_review(request_id):
    service_request = ServiceRequest.query.get(request_id)
    if not service_request:
        return jsonify({"error": "Service request not found"}), 404

    if service_request.rating:
        return jsonify({"error": "Rating already submitted for this service request"}), 400

    data = request.get_json()
    rating = data.get('rating')
    remarks = data.get('remarks')

    if not rating or not (1 <= rating <= 5):
        return jsonify({"error": "Invalid rating. Rating must be between 1 and 5"}), 400

    service_request.rating = rating
    service_request.remarks = remarks
    service_request.status = 'rated'
    db.session.commit()

    return jsonify({"message": "Rating and remarks submitted successfully"}), 200

@main_blueprint.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '')
    search_type = request.args.get('type', '')

    if not search_query or not search_type:
        return jsonify({"error": "Both query and type are required."}), 400

    search_results = []

    if search_type == 'service':
        search_results = Service.query.filter(
            (Service.id.ilike(f'%{search_query}%')) |
            (Service.name.ilike(f'%{search_query}%')) |
            (Service.price.ilike(f'%{search_query}%')) |
            (Service.description.ilike(f'%{search_query}%')) |
            (Service.category.ilike(f'%{search_query}%'))
        ).all()

    elif search_type == 'customer':
        search_results = Customer.query.filter(
            (Customer.id.ilike(f'%{search_query}%')) |
            (Customer.full_name.ilike(f'%{search_query}%')) |
            (Customer.email.ilike(f'%{search_query}%')) |
            (Customer.phone_number.ilike(f'%{search_query}%')) |
            (Customer.address.ilike(f'%{search_query}%')) |
            (Customer.pin_code.ilike(f'%{search_query}%'))
        ).all()

    elif search_type == 'professional':
        search_results = Professional.query.filter(
            (Professional.id.ilike(f'%{search_query}%')) |
            (Professional.full_name.ilike(f'%{search_query}%')) |
            (Professional.email.ilike(f'%{search_query}%')) |
            (Professional.phone_number.ilike(f'%{search_query}%')) |
            (Professional.address.ilike(f'%{search_query}%')) |
            (Professional.service_name.ilike(f'%{search_query}%')) |
            (Professional.experience.ilike(f'%{search_query}%')) |
            (Professional.status.ilike(f'%{search_query}%'))
        ).all()

    elif search_type == 'service_request':
        search_results = ServiceRequest.query.filter(
            (ServiceRequest.id.ilike(f'%{search_query}%')) |
            (ServiceRequest.status.ilike(f'%{search_query}%')) |
            (ServiceRequest.remarks.ilike(f'%{search_query}%')) |
            (ServiceRequest.rating.ilike(f'%{search_query}%')) |
            (ServiceRequest.request_date.ilike(f'%{search_query}%')) |
            (ServiceRequest.completion_date.ilike(f'%{search_query}%'))
        ).all()

    return jsonify([result.to_dict() for result in search_results]), 200

@main_blueprint.route('/professional/search', methods=['GET'])
def professional_search():
    search_query = request.args.get('query', '')
    professional_id = request.args.get('professional_id', '')

    if not search_query or not professional_id:
        return jsonify({"error": "Missing query or professional_id."}), 400

    search_results = ServiceRequest.query.join(Customer, ServiceRequest.customer_id == Customer.id) \
        .filter(ServiceRequest.professional_id == professional_id) \
        .filter(
            (ServiceRequest.id.ilike(f'%{search_query}%')) |
            (Customer.full_name.ilike(f'%{search_query}%')) |
            (Customer.phone_number.ilike(f'%{search_query}%')) |
            (Customer.address.ilike(f'%{search_query}%')) |
            (Customer.pin_code.ilike(f'%{search_query}%')) |
            (ServiceRequest.rating.ilike(f'%{search_query}%')) |
            (ServiceRequest.request_date.ilike(f'%{search_query}%'))
        )

    search_results = search_results.all()
    return jsonify([result.to_dict() for result in search_results]), 200

@main_blueprint.route('/customer/search/services', methods=['GET'])
def search_services():
    query = request.args.get('query', '')
    services = Service.query.filter(
        (Service.name.ilike(f'%{query}%')) |
        (Service.id.ilike(f'%{query}%')) |
        (Service.description.ilike(f'%{query}%')) |
        (Service.category.ilike(f'%{query}%'))
    ).all()
    return jsonify([service.to_dict() for service in services])

@main_blueprint.route('/customer/search/service-requests', methods=['GET'])
def search_service_requests():
    query = request.args.get('query', '')
    customer_id = request.args.get('customer_id')
    
    service_requests = ServiceRequest.query.join(Customer, ServiceRequest.customer_id == Customer.id)\
        .join(Professional, ServiceRequest.professional_id == Professional.id)\
        .filter(
            ServiceRequest.customer_id == customer_id,
            (
                ServiceRequest.status.ilike(f'%{query}%') |
                Customer.full_name.ilike(f'%{query}%') |
                Professional.full_name.ilike(f'%{query}%') |
                Professional.phone_number.ilike(f'%{query}%')
            )
        ).all()
        
    return jsonify([
        {
            "id": req.id,
            "service_name": req.related_service.name,
            "professional_name": req.professional.full_name,
            "phone_no": req.professional.phone_number,
            "status": req.status
        } for req in service_requests
    ])

@main_blueprint.route('/customer/summary', methods=['GET'])
def customer_summary():
    customer_id = request.args.get("customer_id")

    if not customer_id:
        return jsonify({"error": "Customer ID is required."}), 400

    status_counts = (
        db.session.query(ServiceRequest.status, db.func.count(ServiceRequest.id))
        .filter(ServiceRequest.customer_id == customer_id)
        .group_by(ServiceRequest.status)
        .all()
    )

    status_summary = {status: count for status, count in status_counts}

    all_statuses = ["requested", "assigned", "accepted", "rejected", "completed", "rated"]
    for status in all_statuses:
        if status not in status_summary:
            status_summary[status] = 0

    return jsonify(status_summary), 200

@main_blueprint.route('/professional/summary', methods=['GET'])
def professional_summary():
    professional_id = request.args.get("professional_id")

    if not professional_id:
        return jsonify({"error": "Professional ID is required."}), 400

    status_counts = (
        db.session.query(ServiceRequest.status, db.func.count(ServiceRequest.id))
        .filter(ServiceRequest.professional_id == professional_id)
        .group_by(ServiceRequest.status)
        .all()
    )

    status_summary = {status: count for status, count in status_counts}
    all_statuses = ["assigned", "closed", "rejected", "accepted", "completed", "rated"]
    for status in all_statuses:
        if status not in status_summary:
            status_summary[status] = 0

    assigned_count = status_summary.get('assigned', 0)
    status_summary['assigned'] = assigned_count

    rating_counts = (
        db.session.query(ServiceRequest.rating, db.func.count(ServiceRequest.id))
        .filter(ServiceRequest.professional_id == professional_id, ServiceRequest.rating.isnot(None))
        .group_by(ServiceRequest.rating)
        .all()
    )
    ratings_summary = {rating: count for rating, count in rating_counts}

    return jsonify({"status_summary": status_summary, "ratings_summary": ratings_summary}), 200

@main_blueprint.route('/admin/summary', methods=['GET'])
def admin_summary():
    status_counts = (
        db.session.query(ServiceRequest.status, db.func.count(ServiceRequest.id))
        .group_by(ServiceRequest.status)
        .all()
    )
    
    status_summary = {status: count for status, count in status_counts}
    
    all_statuses = ["requested", "assigned", "accepted", "rejected", "completed", "rated"]
    for status in all_statuses:
        if status not in status_summary:
            status_summary[status] = 0

    rating_counts = (
        db.session.query(ServiceRequest.rating, db.func.count(ServiceRequest.id))
        .filter(ServiceRequest.rating.isnot(None))
        .group_by(ServiceRequest.rating)
        .all()
    )
    
    ratings_summary = {rating: count for rating, count in rating_counts}

    return jsonify({
        "status_summary": status_summary,
        "ratings_summary": ratings_summary
    }), 200

@main_blueprint.route('/admin/export', methods=['POST'])
def trigger_export():
    from tasks.exports import export_closed_service_requests
    data = request.get_json()
    admin_email = data.get('email')

    if not hasattr(current_user, 'email') or not current_user.get_id().startswith('admin-'):
        return jsonify({"error": "Unauthorized access"}), 403

    export_closed_service_requests.delay(admin_email)
    return jsonify({'message': 'Export started. You will receive an email once it is complete.'}), 202
