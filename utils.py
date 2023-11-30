from re import sub
from selenium import webdriver


def close_tabs(func):
    """closes all previous tabs except one"""
    def wrapper(self, *args, **kwargs):
        for handle in self.driver.window_handles[1:]:
            self.driver.switch_to.window(handle)
            self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        func(self, *args, **kwargs)

    return wrapper


def process_input(command):
    """removes the command from a message"""
    # FIXME hardcoded for /getitem command
    processed_message = sub(r'/getitem', '', command)
    return processed_message


def retry_on_error(func, wait=0.1, retry=0, *args, **kwargs):
    i = 0
    while True:
        try:
            return func(*args, **kwargs)
            break
        except telegram.error.NetworkError:
            logging.exception(f"Network Error. Retrying...{i}")
            i += 1
            time.sleep(wait)
            if retry != 0 and i == retry:
                break
