import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import threading

class TitanicAnalytics:
    def __init__(self, data_file='analytics_data.json'):
        self.data_file = data_file
        self.lock = threading.Lock()
        self._init_data_file()
    
    def _init_data_file(self):
        """Initialize analytics data file if it doesn't exist"""
        if not os.path.exists(self.data_file):
            initial_data = {
                'total_visits': 0,
                'total_predictions': 0,
                'predictions_by_result': {
                    'survived': 0,
                    'died': 0
                },
                'predictions_by_class': {
                    '1': 0,
                    '2': 0,
                    '3': 0
                },
                'predictions_by_gender': {
                    'male': 0,
                    'female': 0
                },
                'daily_stats': {},
                'browser_stats': {},
                'device_stats': {},
                'last_updated': datetime.now().isoformat(),
                'app_launched': datetime.now().isoformat()
            }
            self._save_data(initial_data)
    
    def _load_data(self) -> Dict[str, Any]:
        """Load analytics data from file"""
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._init_data_file()
            with open(self.data_file, 'r') as f:
                return json.load(f)
    
    def _save_data(self, data: Dict[str, Any]):
        """Save analytics data to file"""
        data['last_updated'] = datetime.now().isoformat()
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_visit(self, user_agent: Optional[str] = None, ip_address: Optional[str] = None):
        """Track a page visit"""
        with self.lock:
            data = self._load_data()
            data['total_visits'] += 1
            
            # Track daily visits
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in data['daily_stats']:
                data['daily_stats'][today] = {
                    'visits': 0,
                    'predictions': 0,
                    'unique_ips': set() if ip_address else []
                }
            data['daily_stats'][today]['visits'] += 1
            
            # Track browser info
            if user_agent:
                browser = self._parse_browser(user_agent)
                data['browser_stats'][browser] = data['browser_stats'].get(browser, 0) + 1
            
            # Track device info
            if user_agent:
                device = self._parse_device(user_agent)
                data['device_stats'][device] = data['device_stats'].get(device, 0) + 1
            
            # Convert sets to lists for JSON serialization
            for day_data in data['daily_stats'].values():
                if isinstance(day_data.get('unique_ips'), set):
                    day_data['unique_ips'] = list(day_data['unique_ips'])
            
            self._save_data(data)
    
    def track_prediction(self, survived: bool, passenger_class: int, gender: str):
        """Track a prediction made by a user"""
        with self.lock:
            data = self._load_data()
            data['total_predictions'] += 1
            
            # Track by result
            result = 'survived' if survived else 'died'
            data['predictions_by_result'][result] += 1
            
            # Track by class
            data['predictions_by_class'][str(passenger_class)] += 1
            
            # Track by gender
            data['predictions_by_gender'][gender] += 1
            
            # Track daily predictions
            today = datetime.now().strftime('%Y-%m-%d')
            if today not in data['daily_stats']:
                data['daily_stats'][today] = {
                    'visits': 0,
                    'predictions': 0,
                    'unique_ips': []
                }
            data['daily_stats'][today]['predictions'] += 1
            
            self._save_data(data)
    
    def _parse_browser(self, user_agent: Optional[str]) -> str:
        """Parse browser from user agent"""
        if not user_agent:
            return 'Unknown'
        
        user_agent = user_agent.lower()
        if 'chrome' in user_agent and 'edge' not in user_agent:
            return 'Chrome'
        elif 'firefox' in user_agent:
            return 'Firefox'
        elif 'safari' in user_agent and 'chrome' not in user_agent:
            return 'Safari'
        elif 'edge' in user_agent:
            return 'Edge'
        elif 'opera' in user_agent:
            return 'Opera'
        else:
            return 'Other'
    
    def _parse_device(self, user_agent: Optional[str]) -> str:
        """Parse device type from user agent"""
        if not user_agent:
            return 'Unknown'
        
        user_agent = user_agent.lower()
        if 'mobile' in user_agent or 'android' in user_agent:
            return 'Mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'Tablet'
        else:
            return 'Desktop'
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current analytics statistics"""
        data = self._load_data()
        
        # Calculate additional metrics
        total_predictions = data['total_predictions']
        if total_predictions > 0:
            survival_rate = (data['predictions_by_result']['survived'] / total_predictions) * 100
        else:
            survival_rate = 0
        
        # Get recent activity (last 7 days)
        recent_days = []
        for i in range(7):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            day_data = data['daily_stats'].get(date, {'visits': 0, 'predictions': 0})
            recent_days.append({
                'date': date,
                'visits': day_data['visits'],
                'predictions': day_data['predictions']
            })
        recent_days.reverse()
        
        app_launched = datetime.fromisoformat(data['app_launched'])
        days_running = (datetime.now() - app_launched).days
        
        return {
            'total_visits': data['total_visits'],
            'total_predictions': data['total_predictions'],
            'survival_rate': round(survival_rate, 1),
            'predictions_by_result': data['predictions_by_result'],
            'predictions_by_class': data['predictions_by_class'],
            'predictions_by_gender': data['predictions_by_gender'],
            'browser_stats': data['browser_stats'],
            'device_stats': data['device_stats'],
            'recent_activity': recent_days,
            'days_running': days_running,
            'last_updated': data['last_updated'],
            'app_launched': data['app_launched']
        }

# Global analytics instance
analytics = TitanicAnalytics()