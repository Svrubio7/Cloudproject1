from flask import Flask, request, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

def control_valve(valve_id, action):
    print(f"Controlling {valve_id}: {action}")
    # Add hardware control logic here

# New function to parse time and add job to the scheduler
def schedule_valve_operation(valve_id, action, time_str):
    time = datetime.strptime(time_str, '%H:%M').time()
    scheduler.add_job(
        func=control_valve,
        trigger='cron',
        hour=time.hour,
        minute=time.minute,
        args=[valve_id, action],
        replace_existing=True
    )
    print(f"Scheduled {valve_id} to {action} at {time_str}")

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/api/set-time', methods=['POST'])
def set_time():
    data = request.json
    valve_id = data['deviceId']
    action = data['action']
    time = data['time']
    schedule_valve_operation(valve_id, action, time)
    return jsonify(success=True)

# New endpoint to handle immediate valve status changes
@app.route('/api/change-valve-status', methods=['POST'])
def change_valve_status():
    data = request.json
    valve_id = data['valveId']
    action = data['action']
    control_valve(valve_id, action)  # Call the control function directly
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
