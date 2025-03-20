from zhanshop.app import App
from zhanshop.config import Config
from zhanshop.log import Log


class Help():
    title = "帮助"
    description = "显示命令的帮助"
    def execute(self, server):
        """
        echo PHP_EOL;
        echo "欢迎使用zhanshop控制台系统".PHP_EOL;

        echo PHP_EOL;
        echo "用法:   cmd 指令 --参数 参数信息".PHP_EOL;
        $output->output("");
        $output->output("可用命令：", 'info');
        $output->output("");
        @return:
        """
        print("\n欢迎使用zhanshop控制台系统\n")
        print("用法:   server.py 指令 --参数 参数信息")
        Log.echo("\n可用命令\n", 'info')
        console = App.make(Config).get("console")
        for name, value in console.items():
            Log.echo(name, 'success', False)
            Log.echo(" " * (36 - len(name)), 'success', False)
            description = '';
            obj = value()
            description += obj.title + " "+obj.description;
            Log.echo(description, 'info')

        print("")