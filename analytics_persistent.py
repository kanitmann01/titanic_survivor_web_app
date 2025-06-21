import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import threading
import json

class PersistentTitanicAnalytics:
    def __init__(self, db_file='analytics.db'):
        self.db_file = db_file
        self.lock = threading.Lock()
        self._init_database()
        self._migrate_from_json()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            
            # Main analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY,
                    total_visits INTEGER DEFAULT 0,
                    total_predictions INTEGER DEFAULT 0,
                    app_launched TEXT,
                    last_updated TEXT
                )
            ''')
            
            # Predictions by result
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions_by_result (
                    result TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            # Predictions by class
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions_by_class (
                    class TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            # Predictions by gender
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions_by_gender (
                    gender TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            # Daily statistics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_stats (
                    date TEXT PRIMARY KEY,
                    visits INTEGER DEFAULT 0,
                    predictions INTEGER DEFAULT 0
                )
            ''')
            
            # Browser statistics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS browser_stats (
                    browser TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            # Device statistics
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS device_stats (
                    device TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            
            # Initialize main record if empty
            cursor.execute('SELECT COUNT(*) FROM analytics')
            if cursor.fetchone()[0] == 0:
                now = datetime.now().isoformat()
                cursor.execute('''
                    INSERT INTO analytics (total_visits, total_predictions, app_launched, last_updated)
                    VALUES (0, 0, ?, ?)
                ''', (now, now))
                
                # Initialize prediction results
                cursor.executemany('''
                    INSERT OR IGNORE INTO predictions_by_result (result, count) VALUES (?, 0)
                ''', [('survived',), ('died',)])
                
                # Initialize prediction classes
                cursor.executemany('''
                    INSERT OR IGNORE INTO predictions_by_class (class, count) VALUES (?, 0)
                ''', [('1',), ('2',), ('3',)])
                
                # Initialize prediction genders
                cursor.executemany('''
                    INSERT OR IGNORE INTO predictions_by_gender (gender, count) VALUES (?, 0)
                ''', [('male',), ('female',)])
            
            conn.commit()
    
    def _migrate_from_json(self):
        """Migrate existing JSON data to SQLite (one-time migration)"""
        json_file = 'analytics_data.json'
        
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                with sqlite3.connect(self.db_file) as conn:
                    cursor = conn.cursor()
                    
                    # Check if data already migrated
                    cursor.execute('SELECT total_visits FROM analytics WHERE id = 1')
                    current_visits = cursor.fetchone()[0]
                    
                    if current_visits == 0:  # Only migrate if no data exists
                        print("🔄 Migrating analytics data from JSON to SQLite...")
                        
                        # Update main analytics
                        cursor.execute('''
                            UPDATE analytics SET 
                            total_visits = ?, 
                            total_predictions = ?,
                            app_launched = ?,
                            last_updated = ?
                            WHERE id = 1
                        ''', (
                            data.get('total_visits', 0),
                            data.get('total_predictions', 0),
                            data.get('app_launched', datetime.now().isoformat()),
                            data.get('last_updated', datetime.now().isoformat())
                        ))
                        
                        # Migrate prediction results
                        results = data.get('predictions_by_result', {})
                        for result, count in results.items():
                            cursor.execute('''
                                UPDATE predictions_by_result SET count = ? WHERE result = ?
                            ''', (count, result))
                        
                        # Migrate prediction classes
                        classes = data.get('predictions_by_class', {})
                        for cls, count in classes.items():
                            cursor.execute('''
                                UPDATE predictions_by_class SET count = ? WHERE class = ?
                            ''', (count, cls))
                        
                        # Migrate prediction genders
                        genders = data.get('predictions_by_gender', {})
                        for gender, count in genders.items():
                            cursor.execute('''
                                UPDATE predictions_by_gender SET count = ? WHERE gender = ?
                            ''', (count, gender))
                        
                        # Migrate daily stats
                        daily_stats = data.get('daily_stats', {})
                        for date, stats in daily_stats.items():
                            cursor.execute('''
                                INSERT OR REPLACE INTO daily_stats (date, visits, predictions)
                                VALUES (?, ?, ?)
                            ''', (date, stats.get('visits', 0), stats.get('predictions', 0)))
                        
                        # Migrate browser stats
                        browser_stats = data.get('browser_stats', {})
                        for browser, count in browser_stats.items():
                            cursor.execute('''
                                INSERT OR REPLACE INTO browser_stats (browser, count)
                                VALUES (?, ?)
                            ''', (browser, count))
                        
                        # Migrate device stats
                        device_stats = data.get('device_stats', {})
                        for device, count in device_stats.items():
                            cursor.execute('''
                                INSERT OR REPLACE INTO device_stats (device, count)
                                VALUES (?, ?)
                            ''', (device, count))
                        
                        conn.commit()
                        print("✅ Analytics data successfully migrated to SQLite!")
                        
                        # Backup old JSON file
                        backup_file = f'analytics_data_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                        os.rename(json_file, backup_file)
                        print(f"📦 Old JSON data backed up as: {backup_file}")
                        
            except Exception as e:
                print(f"⚠️ Migration warning: {e}")
    
    def track_visit(self, user_agent: Optional[str] = None, ip_address: Optional[str] = None):
        """Track a page visit"""
        with self.lock:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Update total visits
                cursor.execute('''
                    UPDATE analytics SET 
                    total_visits = total_visits + 1,
                    last_updated = ?
                    WHERE id = 1
                ''', (datetime.now().isoformat(),))
                
                # Update daily stats
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_stats (date, visits, predictions)
                    VALUES (?, COALESCE((SELECT visits FROM daily_stats WHERE date = ?), 0) + 1,
                              COALESCE((SELECT predictions FROM daily_stats WHERE date = ?), 0))
                ''', (today, today, today))
                
                # Track browser
                if user_agent:
                    browser = self._parse_browser(user_agent)
                    cursor.execute('''
                        INSERT OR REPLACE INTO browser_stats (browser, count)
                        VALUES (?, COALESCE((SELECT count FROM browser_stats WHERE browser = ?), 0) + 1)
                    ''', (browser, browser))
                
                # Track device
                if user_agent:
                    device = self._parse_device(user_agent)
                    cursor.execute('''
                        INSERT OR REPLACE INTO device_stats (device, count)
                        VALUES (?, COALESCE((SELECT count FROM device_stats WHERE device = ?), 0) + 1)
                    ''', (device, device))
                
                conn.commit()
    
    def track_prediction(self, survived: bool, passenger_class: int, gender: str):
        """Track a prediction made by a user"""
        with self.lock:
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                
                # Update total predictions
                cursor.execute('''
                    UPDATE analytics SET 
                    total_predictions = total_predictions + 1,
                    last_updated = ?
                    WHERE id = 1
                ''', (datetime.now().isoformat(),))
                
                # Update prediction by result
                result = 'survived' if survived else 'died'
                cursor.execute('''
                    UPDATE predictions_by_result SET count = count + 1 WHERE result = ?
                ''', (result,))
                
                # Update prediction by class
                cursor.execute('''
                    UPDATE predictions_by_class SET count = count + 1 WHERE class = ?
                ''', (str(passenger_class),))
                
                # Update prediction by gender
                cursor.execute('''
                    UPDATE predictions_by_gender SET count = count + 1 WHERE gender = ?
                ''', (gender,))
                
                # Update daily predictions
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute('''
                    INSERT OR REPLACE INTO daily_stats (date, visits, predictions)
                    VALUES (?, COALESCE((SELECT visits FROM daily_stats WHERE date = ?), 0),
                              COALESCE((SELECT predictions FROM daily_stats WHERE date = ?), 0) + 1)
                ''', (today, today, today))
                
                conn.commit()
    
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
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Get main analytics
            cursor.execute('SELECT * FROM analytics WHERE id = 1')
            main_data = cursor.fetchone()
            
            # Get prediction results
            cursor.execute('SELECT * FROM predictions_by_result')
            predictions_by_result = {row['result']: row['count'] for row in cursor.fetchall()}
            
            # Get prediction classes
            cursor.execute('SELECT * FROM predictions_by_class')
            predictions_by_class = {row['class']: row['count'] for row in cursor.fetchall()}
            
            # Get prediction genders
            cursor.execute('SELECT * FROM predictions_by_gender')
            predictions_by_gender = {row['gender']: row['count'] for row in cursor.fetchall()}
            
            # Get browser stats
            cursor.execute('SELECT * FROM browser_stats WHERE count > 0')
            browser_stats = {row['browser']: row['count'] for row in cursor.fetchall()}
            
            # Get device stats
            cursor.execute('SELECT * FROM device_stats WHERE count > 0')
            device_stats = {row['device']: row['count'] for row in cursor.fetchall()}
            
            # Get recent 7 days activity
            cursor.execute('''
                SELECT * FROM daily_stats 
                ORDER BY date DESC 
                LIMIT 7
            ''')
            recent_activity = []
            daily_data = {row['date']: {'visits': row['visits'], 'predictions': row['predictions']} 
                         for row in cursor.fetchall()}
            
            # Ensure we have 7 days of data
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                day_data = daily_data.get(date, {'visits': 0, 'predictions': 0})
                recent_activity.append({
                    'date': date,
                    'visits': day_data['visits'],
                    'predictions': day_data['predictions']
                })
            recent_activity.reverse()
            
            # Calculate survival rate
            total_predictions = main_data['total_predictions']
            if total_predictions > 0:
                survival_rate = (predictions_by_result.get('survived', 0) / total_predictions) * 100
            else:
                survival_rate = 0
            
            # Calculate days running
            app_launched = datetime.fromisoformat(main_data['app_launched'])
            time_diff = datetime.now() - app_launched
            days_running = time_diff.days
            
            if days_running == 0:
                hours_running = int(time_diff.total_seconds() / 3600)
                if hours_running == 0:
                    days_running = "< 1 hour"
                else:
                    days_running = f"{hours_running} hours"
            
            return {
                'total_visits': main_data['total_visits'],
                'total_predictions': main_data['total_predictions'],
                'survival_rate': round(survival_rate, 1),
                'predictions_by_result': predictions_by_result,
                'predictions_by_class': predictions_by_class,
                'predictions_by_gender': predictions_by_gender,
                'browser_stats': browser_stats,
                'device_stats': device_stats,
                'recent_activity': recent_activity,
                'days_running': days_running,
                'last_updated': main_data['last_updated'],
                'app_launched': main_data['app_launched']
            }
    
    def backup_to_json(self, filename: Optional[str] = None) -> str:
        """Backup analytics data to JSON file"""
        if not filename:
            filename = f'analytics_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        stats = self.get_stats()
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2)
        
        return filename

# Global persistent analytics instance
analytics = PersistentTitanicAnalytics()