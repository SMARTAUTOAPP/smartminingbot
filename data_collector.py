import requests
import json
import time
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.crypto_api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.mining_pools = {
            "BTC": "https://api.slushpool.com/stats/json/btc",
            "ETH": "https://api.ethermine.org/poolStats"
        }
        
    def get_crypto_prices(self, coins=["bitcoin", "ethereum"]):
        """جمع أسعار العملات المشفرة من API"""
        try:
            params = {
                'ids': ','.join(coins),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true'
            }
            response = requests.get(self.crypto_api_url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching crypto prices: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception in get_crypto_prices: {e}")
            return None
    
    def get_mining_difficulty(self, coin="BTC"):
        """جمع بيانات صعوبة التعدين"""
        # هذه دالة وهمية - في التطبيق الحقيقي ستتصل بـ APIs حقيقية
        difficulty_data = {
            "BTC": {"difficulty": 62463471666286, "hash_rate": "400 EH/s"},
            "ETH": {"difficulty": 15500000000000000, "hash_rate": "900 TH/s"}
        }
        return difficulty_data.get(coin, {})
    
    def get_energy_costs(self):
        """جمع بيانات تكلفة الطاقة"""
        # في التطبيق الحقيقي، يمكن جمع هذه البيانات من مصادر محلية أو APIs
        return {
            "cost_per_kwh": 0.12,  # دولار لكل كيلوواط ساعة
            "timestamp": datetime.now().isoformat()
        }
    
    def get_hardware_status(self):
        """جمع بيانات حالة الأجهزة"""
        # محاكاة بيانات الأجهزة
        return {
            "gpu_temp": 65,  # درجة الحرارة بالسيليزيوس
            "gpu_usage": 95,  # نسبة الاستخدام
            "power_consumption": 250,  # واط
            "hash_rate": "50 MH/s",
            "fan_speed": 75  # نسبة سرعة المروحة
        }
    
    def collect_all_data(self):
        """جمع جميع البيانات المطلوبة"""
        print("جاري جمع البيانات...")
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "crypto_prices": self.get_crypto_prices(),
            "mining_difficulty": {
                "BTC": self.get_mining_difficulty("BTC"),
                "ETH": self.get_mining_difficulty("ETH")
            },
            "energy_costs": self.get_energy_costs(),
            "hardware_status": self.get_hardware_status()
        }
        
        print("تم جمع البيانات بنجاح")
        return data
    
    def save_data_to_file(self, data, filename="mining_data.json"):
        """حفظ البيانات في ملف"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"تم حفظ البيانات في {filename}")
        except Exception as e:
            print(f"خطأ في حفظ البيانات: {e}")

if __name__ == "__main__":
    collector = DataCollector()
    data = collector.collect_all_data()
    collector.save_data_to_file(data)
    print(json.dumps(data, indent=2, ensure_ascii=False))

