from flask import Blueprint, request, jsonify
from app.services.reconciliation import reconcile_contact

reconciliation = Blueprint('reconciliation', __name__)


@reconciliation.route('/identify', methods=['POST'])
def reconcile():
    data = request.json

    phone_number = data.get('phone_number')
    email = data.get('email')

    if not phone_number and email:
        return jsonify({'error': 'Phone number or email must be provided'}), 400

    contact = reconcile_contact(phone_number, email)

    return jsonify(contact), 201
