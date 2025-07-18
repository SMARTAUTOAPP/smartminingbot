import numpy as np
import json
from datetime import datetime, timedelta
import math

class IntelligentAnalyzer:
    def __init__(self):
        self.historical_data = []
        self.profitability_threshold = 0.1  # 10% ربح أدنى
        self.risk_tolerance = 0.2  # 20% تحمل للمخاطر
        
    def calculate_profitability(self, coin_data, hardware_data, energy_cost):
        """حساب الربحية المتوقعة للعملة"""
        try:
            # استخراج البيانات الأساسية
            if coin_data == "BTC":
                price = 60000  # سعر وهمي
                hash_rate = 50  # TH/s
                difficulty = 62463471666286
                block_reward = 6.25
            elif coin_data == "ETH":
                price = 3000  # سعر وهمي
                hash_rate = 50  # MH/s
                difficulty = 15500000000000000
                block_reward = 2.0
            else:
                return 0
            
            # حساب الإيرادات المتوقعة يومياً
            daily_blocks = 144 if coin_data == "BTC" else 6400  # عدد البلوكات يومياً
            network_hash_rate = difficulty / (2**32) if coin_data == "BTC" else difficulty / (2**13)
            
            # نسبة الهاش ريت الخاص بنا من إجمالي الشبكة
            our_share = hash_rate / network_hash_rate
            
            # الإيرادات اليومية
            daily_revenue = our_share * daily_blocks * block_reward * price
            
            # التكاليف اليومية (الطاقة)
            power_consumption = hardware_data.get('power_consumption', 250)  # واط
            daily_energy_cost = (power_consumption / 1000) * 24 * energy_cost
            
            # الربح الصافي
            daily_profit = daily_revenue - daily_energy_cost
            
            # نسبة الربح
            profit_margin = (daily_profit / daily_revenue) * 100 if daily_revenue > 0 else 0
            
            return {
                'coin': coin_data,
                'daily_revenue': daily_revenue,
                'daily_cost': daily_energy_cost,
                'daily_profit': daily_profit,
                'profit_margin': profit_margin,
                'roi_days': daily_energy_cost / daily_profit if daily_profit > 0 else float('inf')
            }
            
        except Exception as e:
            print(f"خطأ في حساب الربحية: {e}")
            return None
    
    def predict_price_trend(self, historical_prices):
        """التنبؤ باتجاه السعر باستخدام المتوسط المتحرك البسيط"""
        if len(historical_prices) < 5:
            return "stable"
        
        # حساب المتوسط المتحرك لآخر 5 نقاط
        recent_avg = sum(historical_prices[-5:]) / 5
        older_avg = sum(historical_prices[-10:-5]) / 5 if len(historical_prices) >= 10 else recent_avg
        
        change_percent = ((recent_avg - older_avg) / older_avg) * 100 if older_avg > 0 else 0
        
        if change_percent > 5:
            return "bullish"
        elif change_percent < -5:
            return "bearish"
        else:
            return "stable"
    
    def calculate_risk_score(self, coin_data):
        """حساب درجة المخاطر للعملة"""
        # عوامل المخاطر
        volatility_score = 0.3  # تقلبات السعر
        difficulty_change_score = 0.2  # تغير الصعوبة
        market_cap_score = 0.1  # القيمة السوقية
        
        # حساب المخاطر الإجمالية (0-1)
        total_risk = volatility_score + difficulty_change_score + market_cap_score
        
        return min(total_risk, 1.0)
    
    def analyze_market_conditions(self, data):
        """تحليل ظروف السوق العامة"""
        analysis = {
            'market_sentiment': 'neutral',
            'recommended_action': 'hold',
            'confidence_level': 0.5
        }
        
        try:
            # تحليل أسعار العملات
            crypto_prices = data.get('crypto_prices', {})
            
            if crypto_prices:
                # حساب متوسط التغيير في 24 ساعة
                total_change = 0
                coin_count = 0
                
                for coin, price_data in crypto_prices.items():
                    if isinstance(price_data, dict) and 'usd_24h_change' in price_data:
                        total_change += price_data['usd_24h_change']
                        coin_count += 1
                
                if coin_count > 0:
                    avg_change = total_change / coin_count
                    
                    if avg_change > 5:
                        analysis['market_sentiment'] = 'bullish'
                        analysis['recommended_action'] = 'buy'
                        analysis['confidence_level'] = 0.8
                    elif avg_change < -5:
                        analysis['market_sentiment'] = 'bearish'
                        analysis['recommended_action'] = 'sell'
                        analysis['confidence_level'] = 0.7
        
        except Exception as e:
            print(f"خطأ في تحليل السوق: {e}")
        
        return analysis
    
    def recommend_mining_strategy(self, data):
        """اقتراح استراتيجية التعدين المثلى"""
        try:
            energy_cost = data.get('energy_costs', {}).get('cost_per_kwh', 0.12)
            hardware_data = data.get('hardware_status', {})
            
            # تحليل ربحية العملات المختلفة
            btc_profit = self.calculate_profitability('BTC', hardware_data, energy_cost)
            eth_profit = self.calculate_profitability('ETH', hardware_data, energy_cost)
            
            # تحليل السوق
            market_analysis = self.analyze_market_conditions(data)
            
            # اختيار أفضل عملة للتعدين
            best_coin = None
            max_profit = 0
            
            for profit_data in [btc_profit, eth_profit]:
                if profit_data and profit_data['daily_profit'] > max_profit:
                    max_profit = profit_data['daily_profit']
                    best_coin = profit_data['coin']
            
            # إنشاء التوصية
            recommendation = {
                'recommended_coin': best_coin,
                'expected_daily_profit': max_profit,
                'market_conditions': market_analysis,
                'risk_level': self.calculate_risk_score(best_coin) if best_coin else 0.5,
                'confidence': 0.8 if max_profit > 0 else 0.3,
                'timestamp': datetime.now().isoformat()
            }
            
            return recommendation
            
        except Exception as e:
            print(f"خطأ في إنشاء التوصية: {e}")
            return None
    
    def save_analysis(self, analysis, filename="analysis_results.json"):
        """حفظ نتائج التحليل"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, ensure_ascii=False, indent=2)
            print(f"تم حفظ التحليل في {filename}")
        except Exception as e:
            print(f"خطأ في حفظ التحليل: {e}")

if __name__ == "__main__":
    analyzer = IntelligentAnalyzer()
    
    # بيانات وهمية للاختبار
    test_data = {
        'crypto_prices': {
            'bitcoin': {'usd': 60000, 'usd_24h_change': 2.5},
            'ethereum': {'usd': 3000, 'usd_24h_change': -1.2}
        },
        'energy_costs': {'cost_per_kwh': 0.12},
        'hardware_status': {'power_consumption': 250}
    }
    
    recommendation = analyzer.recommend_mining_strategy(test_data)
    if recommendation:
        analyzer.save_analysis(recommendation)
        print(json.dumps(recommendation, indent=2, ensure_ascii=False))

