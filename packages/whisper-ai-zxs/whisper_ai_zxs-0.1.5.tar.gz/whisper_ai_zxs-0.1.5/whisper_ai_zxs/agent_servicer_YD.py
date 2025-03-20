# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块
"""
import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
"""

#from .resources.agent_servicer import AgentServicer
from .agent_servicer import AgentServicer

class Agent_YD(AgentServicer):
    def call(self, name, *args, **kwargs):
        """
        调用注册的函数
        :param name: 需要调用的函数名称
        :param args: 位置参数
        :param kwargs: 关键字参数
        :return: 返回调用结果
        """
        if name not in self._functions:
            raise KeyError(f"RPA流程 '{name}' 未注册")

        # 将 args 转换为字典
        arg_dict = {str(i): v for i, v in enumerate(args)}
        arg_dict.update(kwargs)  # 合并 kwargs
        p_arg = {
            "arg" : arg_dict,
            "result" : ""
        }
        self._functions[name].main(p_arg)
        #result = json.dumps(p_arg["result"])
        return p_arg["result"]
        #return self._functions[name](*args, **kwargs)
        #return run_module({ "module_path": self._functions[name] }, "main", SZEnv['rpa'], *args, **kwargs) 
