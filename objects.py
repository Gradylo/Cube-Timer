class Set:
    def __init__(self):
        self.count = 0
        self.totaltime = 0.0
        self.times = []
        self.best = 0.0
        self.worst = 0.0
        self.mean = 0.0
        self.average = 0.0
        self.curr_avgs = {
            5 : 0,
            12 : 0,
            100: 0,
        }
        self.best_avgs = {
            5 : 0,
            12 : 0,
            100: 0,
        }

    def update_mean(self):
        self.mean = self.totaltime / self.count

    def add_time(self, t):

        # update vars
        self.count += 1
        self.totaltime += t
        if t < self.best or self.best == 0.0:
            self.best = t
        if t > self.worst or self.worst == 0.0:
            self.worst = t
        self.times.append(t)
        self.mean = self.totaltime / self.count

        # update averages
        for key in self.curr_avgs:
            self.update_avg(key)

        #update overall average
        if self.count > 2:
            self.average = (self.totaltime - self.best - self.worst) * 1.0 / (self.count - 2)


    def update_avg(self, n):
        if n < 3 or n > self.count:
            return

        #extract last n items from self.times
        worst = 0.0
        best = 0.0
        sum_ = 0.0
        index = self.count - 1
        for i in range(n):
            curr_time = self.times[index]
            sum_ += curr_time
            if best == 0.0 or curr_time < best:
                best = curr_time
            if worst == 0.0 or curr_time > worst:
                worst = curr_time
            index -= 1

        sum_ -= best + worst
        result = sum_ / (n - 2)
        if result < self.best_avgs[n] or self.best_avgs[n] == 0:
            self.best_avgs[n] = result
        self.curr_avgs[n] = result

    def get_average(self):
        return self.average

    def get_mean(self):
        return self.mean

    def get_count(self):
        return self.count

    def best_avg5(self):
        return self.best_avgs[5]

    def curr_avg5(self):
        return self.curr_avgs[5]

    def best_avg12(self):
        return self.best_avgs[12]

    def curr_avg12(self):
        return self.curr_avgs[12]

    def best_avg100(self):
        return self.best_avgs[100]

    def curr_avg100(self):
        return self.curr_avgs[100]

    def __str__(self):
        return self.times.__str__()
