from flask import Flask, request, jsonify
from flask_cors import CORS
import database

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Endpoint to handle deposits and return the updated balance
@app.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    wallet_address = data.get('wallet_address')
    amount = data.get('amount')
    status = data.get('status', 'pending')  # Default status is 'pending'
    
    if not wallet_address or not amount:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        # Insert the new deposit
        deposit_record = database.insert_deposit(wallet_address, amount, status)
        
        # Calculate the total deposited balance
        total_deposited = database.get_total_deposited(wallet_address)
        
        return jsonify({
            'message': 'Deposit recorded successfully',
            'deposit': deposit_record,
            'total_deposited': total_deposited
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)