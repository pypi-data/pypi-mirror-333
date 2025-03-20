"""测试任务"""
import time

from lbkit.tasks.config import Config
from lbkit.tasks.task import Task

class TaskClass(Task):
    def run(self):
        print(f"task {self.name} start....")
        time.sleep(2)
        print(f"task {self.name} stop")

    # def set_key1(self, val):
    #     print(f"Object {self.name} set key1: {val}")
    # def set_key2(self, val):
    #     print(f"Object {self.name} set key2: {val}")
    # def set_key3(self, val):
    #     print(f"Object {self.name} set key3: {val}")
    # def set_key4(self, val):
    #     print(f"Object {self.name} set key4: {val}")
    # def set_key5(self, val):
    #     print(f"Object {self.name} set key5: {val}")
    # def set_key6(self, val):
    #     print(f"Object {self.name} set key6: {val}")

if __name__ == "__main__":
    config = Config()
    build = TaskClass(config)
    build.run()
