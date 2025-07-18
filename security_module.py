import hashlib
import hmac
import secrets
import time
import json
import logging
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os

class SecurityModule:
    def __init__(self):
        self.api_keys = {}
        self.session_tokens = {}
        self.failed_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 minutes
        self.encryption_key = self._generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # إعداد نظام السجلات
        logging.basicConfig(
            filename='mining_bot_security.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _generate_encryption_key(self):
        """توليد مفتاح التشفير"""
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def generate_api_key(self, user_id):
        """توليد مفتاح API آمن للمستخدم"""
        api_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        self.api_keys[user_id] = {
            'key_hash': key_hash,
            'created_at': datetime.now().isoformat(),
            'last_used': None,
            'usage_count': 0
        }
        
        self.logger.info(f"API key generated for user: {user_id}")
        return api_key
    
    def validate_api_key(self, user_id, provided_key):
        """التحقق من صحة مفتاح API"""
        if user_id not in self.api_keys:
            self.logger.warning(f"Invalid user ID attempted: {user_id}")
            return False
        
        provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()
        stored_hash = self.api_keys[user_id]['key_hash']
        
        if hmac.compare_digest(provided_hash, stored_hash):
            # تحديث معلومات الاستخدام
            self.api_keys[user_id]['last_used'] = datetime.now().isoformat()
            self.api_keys[user_id]['usage_count'] += 1
            self.logger.info(f"Valid API key used by user: {user_id}")
            return True
        else:
            self._record_failed_attempt(user_id)
            self.logger.warning(f"Invalid API key attempt by user: {user_id}")
            return False
    
    def _record_failed_attempt(self, user_id):
        """تسجيل محاولة دخول فاشلة"""
        current_time = time.time()
        
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = []
        
        # إزالة المحاولات القديمة
        self.failed_attempts[user_id] = [
            attempt for attempt in self.failed_attempts[user_id]
            if current_time - attempt < self.lockout_duration
        ]
        
        self.failed_attempts[user_id].append(current_time)
    
    def is_user_locked(self, user_id):
        """التحقق من حالة قفل المستخدم"""
        if user_id not in self.failed_attempts:
            return False
        
        current_time = time.time()
        recent_attempts = [
            attempt for attempt in self.failed_attempts[user_id]
            if current_time - attempt < self.lockout_duration
        ]
        
        return len(recent_attempts) >= self.max_attempts
    
    def encrypt_sensitive_data(self, data):
        """تشفير البيانات الحساسة"""
        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            elif not isinstance(data, str):
                data = str(data)
            
            encrypted_data = self.cipher_suite.encrypt(data.encode())
            self.logger.info("Data encrypted successfully")
            return encrypted_data
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            return None
    
    def decrypt_sensitive_data(self, encrypted_data):
        """فك تشفير البيانات الحساسة"""
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            self.logger.info("Data decrypted successfully")
            return decrypted_data.decode()
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            return None
    
    def generate_session_token(self, user_id):
        """توليد رمز جلسة آمن"""
        if self.is_user_locked(user_id):
            self.logger.warning(f"Session token request denied for locked user: {user_id}")
            return None
        
        token = secrets.token_urlsafe(32)
        expiry_time = datetime.now() + timedelta(hours=24)
        
        self.session_tokens[token] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': expiry_time.isoformat(),
            'is_active': True
        }
        
        self.logger.info(f"Session token generated for user: {user_id}")
        return token
    
    def validate_session_token(self, token):
        """التحقق من صحة رمز الجلسة"""
        if token not in self.session_tokens:
            self.logger.warning("Invalid session token attempted")
            return False
        
        session = self.session_tokens[token]
        expiry_time = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expiry_time or not session['is_active']:
            self.logger.info(f"Expired or inactive session token: {token[:8]}...")
            return False
        
        self.logger.info(f"Valid session token used by user: {session['user_id']}")
        return True
    
    def revoke_session_token(self, token):
        """إلغاء رمز الجلسة"""
        if token in self.session_tokens:
            self.session_tokens[token]['is_active'] = False
            user_id = self.session_tokens[token]['user_id']
            self.logger.info(f"Session token revoked for user: {user_id}")
            return True
        return False
    
    def validate_mining_parameters(self, params):
        """التحقق من صحة معاملات التعدين"""
        required_fields = ['coin', 'hash_rate', 'power_limit']
        
        # التحقق من وجود الحقول المطلوبة
        for field in required_fields:
            if field not in params:
                self.logger.warning(f"Missing required field: {field}")
                return False, f"Missing required field: {field}"
        
        # التحقق من صحة العملة
        valid_coins = ['BTC', 'ETH', 'LTC', 'XMR']
        if params['coin'] not in valid_coins:
            self.logger.warning(f"Invalid coin specified: {params['coin']}")
            return False, "Invalid coin specified"
        
        # التحقق من حدود الطاقة
        if not isinstance(params['power_limit'], (int, float)) or params['power_limit'] <= 0:
            self.logger.warning("Invalid power limit specified")
            return False, "Invalid power limit"
        
        # التحقق من معدل الهاش
        if not isinstance(params['hash_rate'], (int, float)) or params['hash_rate'] <= 0:
            self.logger.warning("Invalid hash rate specified")
            return False, "Invalid hash rate"
        
        self.logger.info("Mining parameters validated successfully")
        return True, "Parameters valid"
    
    def detect_suspicious_activity(self, activity_data):
        """كشف النشاط المشبوه"""
        suspicious_indicators = []
        
        # فحص استهلاك الطاقة غير الطبيعي
        if activity_data.get('power_consumption', 0) > 500:  # واط
            suspicious_indicators.append("High power consumption detected")
        
        # فحص درجة الحرارة العالية
        if activity_data.get('temperature', 0) > 85:  # درجة مئوية
            suspicious_indicators.append("High temperature detected")
        
        # فحص معدل الهاش غير المتوقع
        expected_hash_rate = activity_data.get('expected_hash_rate', 0)
        actual_hash_rate = activity_data.get('actual_hash_rate', 0)
        
        if expected_hash_rate > 0:
            deviation = abs(actual_hash_rate - expected_hash_rate) / expected_hash_rate
            if deviation > 0.3:  # انحراف أكثر من 30%
                suspicious_indicators.append("Unusual hash rate deviation")
        
        # فحص محاولات الاتصال المشبوهة
        if activity_data.get('failed_connections', 0) > 10:
            suspicious_indicators.append("Multiple failed connection attempts")
        
        if suspicious_indicators:
            self.logger.warning(f"Suspicious activity detected: {suspicious_indicators}")
            return True, suspicious_indicators
        
        return False, []
    
    def secure_wallet_connection(self, wallet_address):
        """تأمين اتصال المحفظة"""
        # التحقق من صحة عنوان المحفظة
        if not self._validate_wallet_address(wallet_address):
            self.logger.error(f"Invalid wallet address: {wallet_address}")
            return False, "Invalid wallet address"
        
        # تشفير عنوان المحفظة
        encrypted_address = self.encrypt_sensitive_data(wallet_address)
        if encrypted_address is None:
            return False, "Failed to encrypt wallet address"
        
        self.logger.info("Wallet connection secured successfully")
        return True, encrypted_address
    
    def _validate_wallet_address(self, address):
        """التحقق من صحة عنوان المحفظة"""
        # فحص أساسي لطول العنوان
        if len(address) < 26 or len(address) > 62:
            return False
        
        # فحص الأحرف المسموحة
        allowed_chars = set('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')
        if not all(c in allowed_chars for c in address):
            return False
        
        return True
    
    def generate_security_report(self):
        """إنشاء تقرير أمني"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_api_keys': len(self.api_keys),
            'active_sessions': sum(1 for s in self.session_tokens.values() if s['is_active']),
            'locked_users': len([u for u in self.failed_attempts.keys() if self.is_user_locked(u)]),
            'total_failed_attempts': sum(len(attempts) for attempts in self.failed_attempts.values()),
            'security_status': 'SECURE'
        }
        
        # تحديد حالة الأمان
        if report['locked_users'] > 0 or report['total_failed_attempts'] > 20:
            report['security_status'] = 'WARNING'
        
        if report['total_failed_attempts'] > 50:
            report['security_status'] = 'CRITICAL'
        
        self.logger.info(f"Security report generated: {report['security_status']}")
        return report

if __name__ == "__main__":
    # اختبار وحدة الأمان
    security = SecurityModule()
    
    # اختبار توليد مفتاح API
    api_key = security.generate_api_key("user123")
    print(f"Generated API Key: {api_key}")
    
    # اختبار التحقق من مفتاح API
    is_valid = security.validate_api_key("user123", api_key)
    print(f"API Key Valid: {is_valid}")
    
    # اختبار تشفير البيانات
    sensitive_data = {"wallet": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa", "private_key": "secret123"}
    encrypted = security.encrypt_sensitive_data(sensitive_data)
    print(f"Data Encrypted: {encrypted is not None}")
    
    # إنشاء تقرير أمني
    report = security.generate_security_report()
    print(f"Security Report: {json.dumps(report, indent=2)}")

