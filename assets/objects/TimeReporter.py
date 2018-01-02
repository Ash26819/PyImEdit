import time

class TimeReporter():
    def __init__(self):
        self.start = time.time()

    def report(self, remaining_iters):
        end = time.time()
        iter_time = end-self.start
        etc = remaining_iters*iter_time
        print("Remaining Iterations: {} ETC: {:.2f} Previous Iteration: {:.2f}".format(
            remaining_iters, etc, iter_time))

