from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time

def send_message():
    print(f"Message sent at {datetime.now()}")

# Create a background scheduler
scheduler = BackgroundScheduler()

# Add the job
scheduler.add_job(
    send_message,
    'cron',
    day_of_week='mon',
    hour=8,
    minute=0
)

# Start the scheduler
scheduler.start()

# Your main application continues running here
print("Main application is running while scheduler works in background...")
try:
    while True:
        # Your main application logic
        time.sleep(5)
        print("Main app doing other work...")
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler properly
    scheduler.shutdown()