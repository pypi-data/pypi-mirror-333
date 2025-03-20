"""环境准备"""
import os
import shutil
import jinja2
import configparser
from string import Template
from lbkit.tasks.config import Config
from lbkit.tasks.task import Task
from lbkit.log import Logger
from lbkit.misc import DownloadFlag

log = Logger("product_prepare")


class ManifestValidateError(OSError):
    """Raised when validation manifest.yml failed."""

src_cwd = os.path.split(os.path.realpath(__file__))[0]

class TaskClass(Task):
    def decompress_toolchain(self):
        toolchain = self.config.get_product_config("toolchain")
        if not toolchain:
            # todo：toolchain成为强制配置项
            return
        file = toolchain.get("file")
        strip = toolchain.get("strip_components", 0)
        self.waitfile(file, 10)
        compiler_file = os.path.join(self.config.compiler_path, "lbkit_cache")
        _, hash = DownloadFlag.read(compiler_file)
        if hash:
            return
        # 可能标记不匹配，所以尝试删除目录后重新创建
        shutil.rmtree(self.config.compiler_path)
        os.makedirs(self.config.compiler_path)
        cmd = f"tar -xf {file} -C {self.config.compiler_path}"
        if strip:
            cmd += f" --strip-components={strip}"
        self.exec(cmd)
        sha256 = self.tools.file_digest_sha256(file)
        DownloadFlag.create(compiler_file, file, sha256)

    def get_conan_profile(self):
        profile = self.config.get_product_config("toolchain/profile")
        if profile:
            file = profile.get("file")
            name = profile.get("name")
        else:
            file = self.get_manifest_config("metadata/profile")
            name = "litebmc"
        self.waitfile(file)
        return file, name


    def load_conan_profile(self):
        profile, name = self.get_conan_profile()
        log.info("Copy profile %s", profile)
        profiles_dir = os.path.expanduser("~/.conan2/profiles")
        if not os.path.isdir(profiles_dir):
            cmd = "conan profile detect -f"
            self.exec(cmd, ignore_error=True)
        dst_profile = os.path.join(profiles_dir, name)
        with open(dst_profile, "w+") as dst_fp:
            src_fd = open(profile, "r")
            template = Template(src_fd.read())
            src_fd.close()
            content = template.safe_substitute(compiler_path=self.config.compiler_path)
            dst_fp.write(content)

        with open(dst_profile, "r") as fp:
            profile_data = jinja2.Template(fp.read()).render()
            parser = configparser.ConfigParser()
            parser.read_string(profile_data)
            strip = "strip"
            if parser.has_option("buildenv", "STRIP"):
                strip = parser.get("buildenv", "STRIP")
            path = ""
            if parser.has_option("buildenv", "PATH+"):
                path = parser.get("buildenv", "PATH+")
                if path.startswith("(path)"):
                    path = path[6:]
            elif parser.has_option("buildenv", "PATH"):
                path = parser.get("buildenv", "PATH")
                if path.startswith("(path)"):
                    path = path[6:]
            self.config.strip = os.path.join(path, strip)

    def run(self):
        """任务入口"""
        self.decompress_toolchain()
        """检查manifest文件是否满足schema格式描述"""
        self.config.load_manifest()
        self.load_conan_profile()

if __name__ == "__main__":
    config = Config()
    build = TaskClass(config, "test")
    build.run()