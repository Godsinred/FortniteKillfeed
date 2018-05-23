class PriorityQueue:

    def __init__(self):
        self.high_queue = [] # names that haven't been looked up yet
        self.med_queue = [] # couldn't find in PC, need to check XBOX/PS4
        self.low_queue = [] # cound't find anywhere recheck name

    def push_high(self, username):
        self.high_queue.append(username)

    def push_med(self, username):
        self.med_queue.append(username)

    def push_low(self, username):
        self.low_queue.append(username)

    def check_high_queue(self):
        pass

    def check_med_queue(self):
        pass

    def check_low_queue(self):
        pass
