import subprocess


class System():
    @staticmethod
    def exec(cmd):
        """
        执行一条 shell 指令
        :param cmd:
        :return:
        """
        cmds = cmd.split(" ")
        cmds = list(filter(None, cmds))
        result = subprocess.run(cmds, capture_output=True, text=True)
        return {
            "code": result.returncode,
            "output": result.stdout
        }