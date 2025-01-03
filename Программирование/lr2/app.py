from multiprocessing import Process
from converter import app as converter_app
from analytics import app as analytics_app

if __name__ == '__main__':
    converter_process = Process(target=converter_app.run, kwargs={'port': 5000, 'host': '0.0.0.0'})
    analytics_process = Process(target=analytics_app.run, kwargs={'port': 5001, 'host': '0.0.0.0'})

    converter_process.start()
    analytics_process.start()

    try:
        converter_process.join()
        analytics_process.join()
    except KeyboardInterrupt:
        converter_process.terminate()
        analytics_process.terminate()
