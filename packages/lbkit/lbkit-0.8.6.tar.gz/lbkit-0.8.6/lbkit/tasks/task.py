"""任务基础类"""
import importlib
import os
import time
import shutil

from multiprocessing import Process
from lbkit.log import Logger
from lbkit.tools import Tools
from lbkit.misc import load_yml_with_json_schema_validate, DownloadFlag

from lbkit.tasks.config import Config

class ManifestValidateError(OSError):
    """Raised when validation manifest.yml failed."""

class Task(Process):
    """任务基础类，提供run和install默认实现以及其它基础该当"""
    def __init__(self, config: Config, name: str):
        super().__init__()
        self.log: Logger = Logger("task")
        self.tools: Tools = Tools(name)
        self.config: Config = config
        self.name = name

    def install(self):
        """安装任务"""
        self.log.info("install...........")

    def exec(self, cmd: str, verbose=False, ignore_error = False, sensitive=False, log_prefix="", **kwargs):
        kwargs["uptrace"] = kwargs.get("uptrace", 0) + 1
        return self.tools.exec(cmd, verbose, ignore_error, sensitive, log_prefix, **kwargs)

    def pipe(self, cmds: list[str], ignore_error=False, out_file = None, **kwargs):
        kwargs["uptrace"] = kwargs.get("uptrace", 0) + 1
        self.tools.pipe(cmds, ignore_error, out_file, **kwargs)

    def exec_easy(self, cmd, ignore_error=False, **kwargs):
        kwargs["uptrace"] = kwargs.get("uptrace", 0) + 1
        return self.tools.run(cmd, ignore_error, **kwargs)

    def do_hook(self, path):
        """执行任务钓子，用于定制化"""
        try:
            module = importlib.import_module(path)
        except TypeError:
            self.log.info("Load module(%s) failed, skip", path, uptrace=2)
            return
        self.log.info(f"load hook: {path}", uptrace=2)
        hook = module.TaskHook(self.config, "do_hook")
        hook.run()

    def get_manifest_config(self, key: str, default=None):
        return self.config.get_manifest_config(key, default)

    def load_manifest(self):
        """加载manifest.yml并验证schema文件"""
        return self.config.load_manifest()

    def waitfile(self, src, timeout=1):
        src = os.path.realpath(src)
        if os.path.islink(src):
            raise FileNotFoundError(f"Source file {src} is a symlink, copying failed")
        if not os.path.isfile(src):
            if timeout:
                # 如果有timeout的，可能是正在下载的文件，需要等待超时时间再检查一次
                time.sleep(timeout)
                if not os.path.isfile(src):
                    raise FileNotFoundError(f"Source file {src} does not exist, copying failed")
            else:
                raise FileNotFoundError(f"Source file {src} does not exist, copying failed")

        # 检查是否由download下载器下载，如果是，需要检查是否下载完成
        if src.startswith(self.config.download_path):
            timeout_cnt = 0
            timeout_sec = 0
            while True:
                _, hash = DownloadFlag.read(src)
                if hash:
                    filehash = self.tools.file_digest_sha256(src)
                    if hash != filehash:
                        DownloadFlag.clean(src)
                        raise Exception(f"The hash of file {src} is {filehash}, not equal to {hash}")
                    break
                else:
                    time.sleep(0.1)
                    timeout_sec += 0.1
                    timeout_cnt += 0.1
                # 每10秒打印一次等等日志
                if timeout_sec == 10:
                    self.log.info(f"Wait file {src} download success")
                    timeout_sec = 0
                # 60秒未创建文件的，判定文件不存在，中止构建
                if timeout_cnt == 60 and not os.path.isfile(src):
                    raise Exception(f"Check file {src} failed because source file does not exist")
                if timeout_cnt == 300:
                    raise Exception(f"Check file {src} failed because file was not downloaded within 300 seconds")

    def copyfile(self, src, dst):
        try:
            self.waitfile(src)
        except Exception as e:
            raise Exception(f"Copy file {src} to {dst} failed because source file not ready") from e

        dst = os.path.realpath(dst)
        if not dst.startswith(self.config.temp_path):
            raise FileNotFoundError(f"Destination file {dst} is not a subpath of {self.config.temp_path}")

        if os.path.isfile(dst):
            os.unlink(dst)
        dst_dir = os.path.dirname(dst)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        if os.path.isfile(dst) or os.path.islink(dst):
            os.unlink(dst)
        self.log.debug(f"copy {src} to {dst}")
        shutil.copyfile(src, dst)

    def deal_conf(self, config_dict):
        """
        处理每个Task的私有配置"work_config"
        当work类有set_xxx类方法时，则可以在target文件中配置xxx
        """
        if not config_dict:
            return
        for conf in config_dict:
            try:
                exist = getattr(self, f"set_{conf}")
                val = config_dict.get(conf)
                exist(val)
            except Exception as e:
                raise Exception(f"无效配置: {conf}, {e}") from e