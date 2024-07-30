import time
import threading
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
socketio = SocketIO(app)

DATABASE_URL = 'sqlite:///db.sqlite3'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class CounterResult(Base):
    __tablename__ = 'counter_results'
    id = Column(Integer, primary_key=True)
    counter_value = Column(Integer)
    elapsed_time = Column(Float)

Base.metadata.create_all(engine)

counter_value = 0
start_time = time.time()
interval = 2  # 72 сек (!)
max_counter_value = 400
reset_event = threading.Event()

def counter():
    global counter_value, start_time
    while True:
        reset_event.wait(interval)
        if reset_event.is_set():
            reset_event.clear()
            continue
        counter_value += 1
        elapsed_time = time.time() - start_time
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        socketio.emit('update_counter', {'counter_value': counter_value, 'hours': int(hours), 'minutes': int(minutes), 'seconds': int(seconds)})
        if counter_value > max_counter_value:
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    global counter_value, start_time
    elapsed_time = time.time() - start_time

    # Запись результата в БД
    session = Session()
    result = CounterResult(counter_value=counter_value, elapsed_time=elapsed_time)
    session.add(result)
    session.commit()
    session.close()

    # Сброс счетчика и времени
    counter_value = 0
    start_time = time.time()
    reset_event.set()
    return redirect(url_for('index'))

if __name__ == '__main__':
    threading.Thread(target=counter, daemon=True).start()
    socketio.run(app, debug=True)