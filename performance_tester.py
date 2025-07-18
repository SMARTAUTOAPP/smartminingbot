import time
import psutil
import threading
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import logging

class PerformanceTester:
    def __init__(self):
        self.test_results = []
        self.monitoring_active = False
        self.performance_data = {
            'cpu_usage': [],
            'memory_usage': [],
            'network_io': [],
            'disk_io': [],
            'timestamps': []
        }
        
        # إعداد نظام السجلات
        logging.basicConfig(
            filename='performance_test.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self, duration=300):  # 5 minutes default
        """بدء مراقبة الأداء"""
        self.monitoring_active = True
        self.performance_data = {
            'cpu_usage': [],
            'memory_usage': [],
            'network_io': [],
            'disk_io': [],
            'timestamps': []
        }
        
        self.logger.info(f"Performance monitoring started for {duration} seconds")
        
        def monitor():
            start_time = time.time()
            while self.monitoring_active and (time.time() - start_time) < duration:
                # جمع بيانات الأداء
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                network = psutil.net_io_counters()
                disk = psutil.disk_io_counters()
                
                self.performance_data['cpu_usage'].append(cpu_percent)
                self.performance_data['memory_usage'].append(memory.percent)
                self.performance_data['network_io'].append(network.bytes_sent + network.bytes_recv)
                self.performance_data['disk_io'].append(disk.read_bytes + disk.write_bytes)
                self.performance_data['timestamps'].append(datetime.now())
                
                time.sleep(5)  # جمع البيانات كل 5 ثوان
        
        monitor_thread = threading.Thread(target=monitor)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return monitor_thread
    
    def stop_monitoring(self):
        """إيقاف مراقبة الأداء"""
        self.monitoring_active = False
        self.logger.info("Performance monitoring stopped")
    
    def test_mining_algorithm_performance(self, algorithm_func, test_data, iterations=100):
        """اختبار أداء خوارزمية التعدين"""
        self.logger.info(f"Testing algorithm performance with {iterations} iterations")
        
        execution_times = []
        memory_usage = []
        
        for i in range(iterations):
            # قياس استخدام الذاكرة قبل التنفيذ
            process = psutil.Process()
            memory_before = process.memory_info().rss / 1024 / 1024  # MB
            
            # قياس وقت التنفيذ
            start_time = time.time()
            try:
                result = algorithm_func(test_data)
                end_time = time.time()
                execution_time = end_time - start_time
                execution_times.append(execution_time)
                
                # قياس استخدام الذاكرة بعد التنفيذ
                memory_after = process.memory_info().rss / 1024 / 1024  # MB
                memory_usage.append(memory_after - memory_before)
                
            except Exception as e:
                self.logger.error(f"Algorithm test failed at iteration {i}: {e}")
                continue
        
        # حساب الإحصائيات
        if execution_times:
            avg_time = np.mean(execution_times)
            min_time = np.min(execution_times)
            max_time = np.max(execution_times)
            std_time = np.std(execution_times)
            
            avg_memory = np.mean(memory_usage)
            max_memory = np.max(memory_usage)
            
            test_result = {
                'test_name': 'Algorithm Performance Test',
                'timestamp': datetime.now().isoformat(),
                'iterations': len(execution_times),
                'execution_time': {
                    'average': avg_time,
                    'minimum': min_time,
                    'maximum': max_time,
                    'std_deviation': std_time
                },
                'memory_usage': {
                    'average_mb': avg_memory,
                    'maximum_mb': max_memory
                },
                'performance_score': self._calculate_performance_score(avg_time, avg_memory)
            }
            
            self.test_results.append(test_result)
            self.logger.info(f"Algorithm test completed. Average time: {avg_time:.4f}s")
            return test_result
        
        return None
    
    def test_data_collection_speed(self, data_collector, iterations=50):
        """اختبار سرعة جمع البيانات"""
        self.logger.info(f"Testing data collection speed with {iterations} iterations")
        
        collection_times = []
        data_sizes = []
        
        for i in range(iterations):
            start_time = time.time()
            try:
                data = data_collector.collect_all_data()
                end_time = time.time()
                
                collection_time = end_time - start_time
                collection_times.append(collection_time)
                
                # حساب حجم البيانات
                data_size = len(json.dumps(data).encode('utf-8'))
                data_sizes.append(data_size)
                
            except Exception as e:
                self.logger.error(f"Data collection test failed at iteration {i}: {e}")
                continue
            
            time.sleep(1)  # انتظار ثانية بين الاختبارات
        
        if collection_times:
            avg_time = np.mean(collection_times)
            avg_size = np.mean(data_sizes)
            throughput = avg_size / avg_time if avg_time > 0 else 0
            
            test_result = {
                'test_name': 'Data Collection Speed Test',
                'timestamp': datetime.now().isoformat(),
                'iterations': len(collection_times),
                'average_collection_time': avg_time,
                'average_data_size_bytes': avg_size,
                'throughput_bytes_per_second': throughput,
                'performance_rating': self._rate_data_collection_performance(avg_time)
            }
            
            self.test_results.append(test_result)
            self.logger.info(f"Data collection test completed. Average time: {avg_time:.4f}s")
            return test_result
        
        return None
    
    def test_security_module_performance(self, security_module, iterations=100):
        """اختبار أداء وحدة الأمان"""
        self.logger.info(f"Testing security module performance with {iterations} iterations")
        
        encryption_times = []
        decryption_times = []
        validation_times = []
        
        test_data = "This is a test string for encryption performance testing"
        
        for i in range(iterations):
            # اختبار التشفير
            start_time = time.time()
            encrypted_data = security_module.encrypt_sensitive_data(test_data)
            encryption_time = time.time() - start_time
            encryption_times.append(encryption_time)
            
            # اختبار فك التشفير
            if encrypted_data:
                start_time = time.time()
                decrypted_data = security_module.decrypt_sensitive_data(encrypted_data)
                decryption_time = time.time() - start_time
                decryption_times.append(decryption_time)
            
            # اختبار التحقق من API Key
            api_key = security_module.generate_api_key(f"test_user_{i}")
            start_time = time.time()
            is_valid = security_module.validate_api_key(f"test_user_{i}", api_key)
            validation_time = time.time() - start_time
            validation_times.append(validation_time)
        
        test_result = {
            'test_name': 'Security Module Performance Test',
            'timestamp': datetime.now().isoformat(),
            'iterations': iterations,
            'encryption': {
                'average_time': np.mean(encryption_times),
                'min_time': np.min(encryption_times),
                'max_time': np.max(encryption_times)
            },
            'decryption': {
                'average_time': np.mean(decryption_times),
                'min_time': np.min(decryption_times),
                'max_time': np.max(decryption_times)
            },
            'validation': {
                'average_time': np.mean(validation_times),
                'min_time': np.min(validation_times),
                'max_time': np.max(validation_times)
            }
        }
        
        self.test_results.append(test_result)
        self.logger.info("Security module test completed")
        return test_result
    
    def _calculate_performance_score(self, avg_time, avg_memory):
        """حساب نقاط الأداء"""
        # نقاط الأداء بناءً على الوقت والذاكرة
        time_score = max(0, 100 - (avg_time * 1000))  # كلما قل الوقت، زادت النقاط
        memory_score = max(0, 100 - avg_memory)  # كلما قلت الذاكرة، زادت النقاط
        
        return (time_score + memory_score) / 2
    
    def _rate_data_collection_performance(self, avg_time):
        """تقييم أداء جمع البيانات"""
        if avg_time < 1.0:
            return "Excellent"
        elif avg_time < 2.0:
            return "Good"
        elif avg_time < 5.0:
            return "Average"
        else:
            return "Poor"
    
    def generate_performance_report(self):
        """إنشاء تقرير الأداء"""
        if not self.test_results:
            return {"error": "No test results available"}
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'total_tests': len(self.test_results),
            'test_results': self.test_results,
            'system_info': {
                'cpu_count': psutil.cpu_count(),
                'memory_total_gb': psutil.virtual_memory().total / (1024**3),
                'disk_usage_percent': psutil.disk_usage('/').percent
            },
            'performance_summary': self._generate_performance_summary()
        }
        
        return report
    
    def _generate_performance_summary(self):
        """إنشاء ملخص الأداء"""
        summary = {
            'overall_rating': 'Good',
            'recommendations': [],
            'critical_issues': []
        }
        
        # تحليل نتائج الاختبارات
        for result in self.test_results:
            if 'performance_score' in result and result['performance_score'] < 50:
                summary['critical_issues'].append(f"Low performance score in {result['test_name']}")
            
            if 'average_collection_time' in result and result['average_collection_time'] > 5.0:
                summary['recommendations'].append("Consider optimizing data collection algorithms")
        
        # تحديد التقييم العام
        if summary['critical_issues']:
            summary['overall_rating'] = 'Needs Improvement'
        elif not summary['recommendations']:
            summary['overall_rating'] = 'Excellent'
        
        return summary
    
    def create_performance_charts(self):
        """إنشاء الرسوم البيانية للأداء"""
        if not self.performance_data['timestamps']:
            self.logger.warning("No performance data available for charting")
            return None
        
        # إعداد الخط العربي
        plt.rcParams['font.family'] = ['DejaVu Sans']
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Mining Bot Performance Analysis', fontsize=16)
        
        timestamps = self.performance_data['timestamps']
        
        # رسم استخدام المعالج
        ax1.plot(timestamps, self.performance_data['cpu_usage'], 'b-', linewidth=2)
        ax1.set_title('CPU Usage (%)')
        ax1.set_ylabel('Usage %')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # رسم استخدام الذاكرة
        ax2.plot(timestamps, self.performance_data['memory_usage'], 'r-', linewidth=2)
        ax2.set_title('Memory Usage (%)')
        ax2.set_ylabel('Usage %')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        
        # رسم I/O الشبكة
        if len(self.performance_data['network_io']) > 1:
            network_diff = np.diff(self.performance_data['network_io'])
            ax3.plot(timestamps[1:], network_diff, 'g-', linewidth=2)
        ax3.set_title('Network I/O (bytes/sec)')
        ax3.set_ylabel('Bytes/sec')
        ax3.grid(True, alpha=0.3)
        ax3.tick_params(axis='x', rotation=45)
        
        # رسم I/O القرص
        if len(self.performance_data['disk_io']) > 1:
            disk_diff = np.diff(self.performance_data['disk_io'])
            ax4.plot(timestamps[1:], disk_diff, 'm-', linewidth=2)
        ax4.set_title('Disk I/O (bytes/sec)')
        ax4.set_ylabel('Bytes/sec')
        ax4.grid(True, alpha=0.3)
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        chart_filename = f'performance_charts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        self.logger.info(f"Performance charts saved to {chart_filename}")
        return chart_filename
    
    def save_results(self, filename=None):
        """حفظ نتائج الاختبارات"""
        if filename is None:
            filename = f'performance_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        report = self.generate_performance_report()
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Performance results saved to {filename}")
            return filename
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            return None

if __name__ == "__main__":
    # اختبار وحدة اختبار الأداء
    tester = PerformanceTester()
    
    # بدء مراقبة الأداء لمدة دقيقة واحدة
    monitor_thread = tester.start_monitoring(duration=60)
    
    # محاكاة خوارزمية تعدين بسيطة للاختبار
    def simple_mining_algorithm(data):
        # محاكاة عملية حسابية
        result = 0
        for i in range(1000):
            result += i * i
        return result
    
    # اختبار أداء الخوارزمية
    test_data = {"test": "data"}
    algorithm_result = tester.test_mining_algorithm_performance(
        simple_mining_algorithm, 
        test_data, 
        iterations=50
    )
    
    print("Algorithm Performance Test Results:")
    print(json.dumps(algorithm_result, indent=2))
    
    # انتظار انتهاء المراقبة
    monitor_thread.join()
    
    # إنشاء الرسوم البيانية
    chart_file = tester.create_performance_charts()
    if chart_file:
        print(f"Performance charts created: {chart_file}")
    
    # حفظ النتائج
    results_file = tester.save_results()
    if results_file:
        print(f"Results saved to: {results_file}")

