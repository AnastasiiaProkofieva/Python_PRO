import time
import logging


class TimerContext:
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        stop_time = time.perf_counter()
        period = stop_time - self.start_time
        logging.info(f"Execution time: {period:.2f} seconds")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    with TimerContext():
        time.sleep(2)


main()