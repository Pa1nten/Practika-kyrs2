from flask import Flask, request, jsonify
import psycopg2
import config
import threading
import webbrowser

app = Flask(__name__)

class DBManager:
    def __init__(self, db_info):
        self.db_info = db_info
        self.connection = None

    def get_connection(self):
        if not self.connection:
            self.connection = psycopg2.connect(**self.db_info)
        return self.connection

    def retrieve_logs(self, ip=None, start_date=None, end_date=None, group_by=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        base_query = 'SELECT * FROM logs WHERE TRUE'
        params = []
        if ip:
            base_query += " AND ip = %s"
            params.append(ip)
        if start_date:
            base_query += " AND timestamp >= %s"
            params.append(start_date)
        if end_date:
            base_query += " AND timestamp <= %s"
            params.append(end_date)
        if group_by:
            base_query += f" GROUP BY {group_by}"

        cursor.execute(base_query, params)
        logs = cursor.fetchall()
        cursor.close()
        return logs

@app.route('/', methods=['GET'])
def fetch_logs():
    db_manager = DBManager(config.db_info)
    ip = request.args.get('ip')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    group_by = request.args.get('group_by')

    logs = db_manager.retrieve_logs(ip, start_date, end_date, group_by)
    columns = ['ip', 'timestamp', 'method', 'url', 'status', 'user_agent']
    json_logs = [dict(zip(columns, log)) for log in logs]

    return jsonify(json_logs)

def open_browser(url):
    webbrowser.open(url)

if __name__ == '__main__':
    port = 5000 
    url = f"http://127.0.0.1:{port}/"

    threading.Thread(target=open_browser, args=(url,)).start()

    app.run(port=port)
