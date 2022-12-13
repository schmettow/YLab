### 0

class Timer:
    def set():
        pass
    def start():
        pass
    def read():
        pass
    def alarm():
        pass

### 1


class Timer:
    def __init__(self, duration = 1):
        self.duration = duration
        self.started = False
    def start(self):
        pass
    def read(self):
        pass
    def alarm(self):
        pass

### 2

from time import monotonic as now

class Clock:
    def __init__(self):
        self.started = False
    def start(self):
        self.t_started = now()
        self.started = True
        return True
    def read(self):
        return now() - self.t_started

### 3

class Timer(Clock):
    def set(self, duration):
        self.duration = duration

    def alarm(self):
        return self.t_started + self.duration > now()

### 4

class Timer(Clock):
    def set(self, duration):
        self.duration = duration

    def alarm(self):
        return self.t_started + self.duration > now()

    def remaining(self):
        return now() - self.t_started + self.duration
        

### 5

class Timer(Clock):
    def __init__(self, duration):
        Clock.__init__(self)
        self.duration = duration

    def alarm(self):
        return self.t_started + self.duration > now()

    def remaining(self):
        return now() - self.t_started + self.duration

### 6

class Timer(Clock):
    def __init__(self, duration):
        Clock.__init__(self)
        self.duration = duration

    @property
    def alarm(self):
        return self.t_started + self.duration > now()
    
    @property
    def remaining(self):
        return now() - self.t_started + self.duration

### 6

class Timer(Clock):
    def __init__(self, duration):
        Clock.__init__(self)
        self.duration = duration

    @property
    def alarm(self):
        return self.t_started + self.duration > now()
    
    @property
    def remaining(self):
        return now() - self.t_started + self.duration