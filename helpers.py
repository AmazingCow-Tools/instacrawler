import random;
import time;

from log import *;

def helper_wait_random_delay(delay):
    real_delay = random.uniform(delay * 0.5, delay * 1.5);
    log.D("[HELPER] Sleeping: {0}", real_delay);
    time.sleep(real_delay);
