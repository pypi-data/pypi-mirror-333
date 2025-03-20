import pandas
class Office():
    path = None
    def __init__(self, path):
        self.path = path

    def toArray(self):
        # 获取文件类型
        extension = self.path.split(".")[-1]
        if(extension == "csv"):
            dfs = pandas.read_csv(self.path, sheet_name=None)
            return {sheet_name: df.values for sheet_name, df in dfs.items()}
        elif (extension == "xls" or extension == "xlsx"):
            dfs = pandas.read_excel(self.path, sheet_name=None)
            return {sheet_name: df.values for sheet_name, df in dfs.items()}
        return None