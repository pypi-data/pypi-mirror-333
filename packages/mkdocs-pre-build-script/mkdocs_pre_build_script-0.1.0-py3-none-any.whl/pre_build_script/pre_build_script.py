import subprocess
import os
import logging
from mkdocs.plugins import BasePlugin
from mkdocs.config.config_options import Type


class MkdocsPreBuildScript(BasePlugin):
    config_scheme = (
        ('script', Type(list, default=[])),
    )

    def __init__(self):
        self.logger = logging.getLogger('[mkdocs_pre_build_script]')
        self.logger.setLevel(logging.INFO)

    def on_pre_build(self, config):
        scripts = self.config.get('script', [])
        for script in scripts:
            if not os.path.exists(script):
                self.logger.warning(f"脚本 {script} 不存在，跳过执行")
                continue
            try:
                subprocess.run(['python', script], check=True)
                self.logger.info(f"脚本 {script} 执行成功")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"执行脚本 {script} 时出错: {e}")
        return config
