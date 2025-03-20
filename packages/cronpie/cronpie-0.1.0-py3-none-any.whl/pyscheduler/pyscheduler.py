import schedule
import time

class PyScheduler:
    def __init__(self):
        self.jobs = []
        pass

    def schedule(self, time, unit):
        def decorator(func):
            print(time, unit)
            match unit:
                case 'seconds':
                    job = schedule.every(time).seconds.do(func)
                case 'minutes':
                    job = schedule.every(time).minutes.do(func)
                case 'hours':
                    job = schedule.every(time).hours.do(func)
                case 'days':
                    job = schedule.every(time).days.do(func)
                case 'weeks':
                    job = schedule.every(time).weeks.do(func)
                case 'months':
                    job = schedule.every(time).months.do(func)
                case 'years':
                    job = schedule.every(time).years.do(func)
                case _:
                    raise ValueError('Invalid unit of time')

            self.jobs.append(job)
            return func
        return decorator
    
    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
        

if __name__ == '__main__':
    app = PyScheduler()

    @app.schedule(time=5, unit='seconds')
    def my_func():
        print('Hello World')

    @app.schedule(time=1, unit='minutes')
    def my_func2():
        print('Hello World 2')

    app.run()
