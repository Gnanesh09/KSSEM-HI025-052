# app/services/payment_service.py
import razorpay
import qrcode
import io
import base64
from datetime import datetime
from app.database.session import get_db
from app.models.payment import Payment
from app.config import settings

# Initialize Razorpay
try:
    import razorpay
    razorpay_client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
except:
    razorpay_client = None
    print("⚠️ Razorpay client not initialized (Demo Mode)")

class PaymentService:
    """Payment service for Razorpay, UPI, and Bank Transfer"""
    
    @staticmethod
    def create_razorpay_order(payment_id: str, amount: float, farmer_id: str):
        """Create Razorpay payment order"""
        
        if not razorpay_client or settings.DEMO_MODE:
            print("⚠️ Using DEMO Razorpay order")
            return {
                "razorpay_order_id": f"order_DEMO_{payment_id}",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "currency": "INR"
            }
        
        try:
            razorpay_order = razorpay_client.order.create(dict(
                amount=int(amount * 100),
                currency='INR',
                receipt=payment_id,
                payment_capture=1
            ))
            
            return {
                "razorpay_order_id": razorpay_order['id'],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "currency": "INR"
            }
        except Exception as e:
            print(f"Error creating Razorpay order: {str(e)}")
            return {
                "razorpay_order_id": f"order_DEMO_{payment_id}",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "currency": "INR"
            }
    
    @staticmethod
    def verify_razorpay_payment(razorpay_payment_id: str, razorpay_order_id: str, razorpay_signature: str):
        """Verify Razorpay payment signature"""
        
        if not razorpay_client or settings.DEMO_MODE:
            print("⚠️ Using DEMO payment verification")
            return True
        
        try:
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            razorpay_client.utility.verify_payment_signature(params_dict)
            return True
        except Exception as e:
            print(f"Payment verification failed: {str(e)}")
            return False
    
    @staticmethod
    def generate_upi_qr(payment_id: str, amount: float, farmer_id: str, farmer_name: str):
        """Generate UPI QR code - FIXED: Returns base64 encoded image"""
        try:
            # UPI string format
            upi_string = f"upi://pay?pa={settings.UPI_ID}&pn=GreenChain&tn=Claim-{payment_id}&am={amount}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(upi_string)
            qr.make(fit=True)
            
            # Create image in memory (NO FILES!)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Convert to base64
            img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
            
            return {
                "qr_code_base64": img_base64,  # Send as base64
                "upi_string": upi_string,
                "payment_id": payment_id
            }
        except Exception as e:
            print(f"Error generating UPI QR: {str(e)}")
            return None
    
    @staticmethod
    def generate_bank_transfer_details(payment_id: str, farmer_id: str, amount: float):
        """Generate bank transfer details"""
        return {
            "payment_id": payment_id,
            "amount": amount,
            "bank_name": "GreenChain Bank",
            "account_holder": "GreenChain Insurance",
            "account_number": "1234567890",
            "ifsc_code": "GCIN0000001",
            "reference": f"CLAIM-{payment_id}"
        }

payment_service = PaymentService()
