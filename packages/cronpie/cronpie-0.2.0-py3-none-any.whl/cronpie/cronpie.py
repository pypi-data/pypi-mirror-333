import schedule
import time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

class CronPie:
    def __init__(self):
        self.jobs = []
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        pass

    def schedule(self, time = None, unit = None, expr = None):
        def decorator(func, *args, **kwargs):
            if expr:
                trigger = CronTrigger.from_crontab(expr)
                job = self.scheduler.add_job(func, trigger)
            elif time and unit:
                match unit:
                    case 'seconds':
                        job = schedule.every(time).seconds.do(func, *args, **kwargs)
                    case 'minutes':
                        job = schedule.every(time).minutes.do(func, *args, **kwargs)
                    case 'hours':
                        job = schedule.every(time).hours.do(func, *args, **kwargs)
                    case 'days':
                        job = schedule.every(time).days.do(func, *args, **kwargs)
                    case 'weeks':
                        job = schedule.every(time).weeks.do(func, *args, **kwargs)
                    case 'months':
                        job = schedule.every(time).months.do(func, *args, **kwargs)
                    case 'years':
                        job = schedule.every(time).years.do(func, *args, **kwargs)
                    case _:
                        raise ValueError('Invalid unit of time')

            self.jobs.append(job)
            return func
        return decorator
    
    def run(self):
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()
        

if __name__ == '__main__':
    app = CronPie()

    @app.schedule(time=5, unit='seconds')
    def my_func():
        print('Hello World')

    @app.schedule(time=1, unit='minutes')
    def my_func2():
        print('Hello World 2')

    @app.schedule(expr='*/5 * * * *')
    def my_func3():
        print('Hello World 3')

    app.run()
