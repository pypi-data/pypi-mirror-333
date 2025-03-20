import time
from .agent_trainer import AgentTrainer
from datetime import datetime
from .whisper_tools import WhisperTools_Qywx

#from xbot import print

class WhisperAI:
    def __init__(self):
        """ 初始化一个空字典用于存储函数 """
        self._agent_kf = []
        self._agent_trainer = AgentTrainer()
        #self.daily_report = datetime.now().date()
        self.daily_report = ""

    def add_agent(self, reg):
        """ 初始化一个空字典用于存储函数 """
        self._agent_kf.append(reg)

    def run(self):
        #初始化
        for agent in self._agent_kf:
            agent.register_all_function()
            agent.call("stop", agent.get_kf_name())
            agent.set_kf_status(0)
            time.sleep(3)

        while True:
            errorTimes = 0
            try:

                count = 0

                if (count % 10 == 0):
                    for agent in self._agent_kf:
                        self.auto_start(agent)
                for agent in self._agent_kf:
                    if (agent.get_kf_status_now() == 1):
                        agent.call("activate", agent.get_kf_name())
                        agent.listening_user()
                        agent.listening_manage()
                        agent.heart_bit()
                    time.sleep(1)
                count = count + 1
                if (count >= 10000):
                    count = 0

                #判断时间，如果是凌晨4点，则发送日报：
                if (datetime.now().date() != self.daily_report and datetime.now().hour == 4):
                    for agent in self._agent_kf:
                        #self._agent_trainer.daily_report(agent)
                        self.daily_report = datetime.now().date()

            except Exception as e:
                errorTimes = errorTimes + 1
                print(f"主体循环出现异常{e}！")
                WhisperTools_Qywx.send_to_error_robot(f"主体循环出现异常：第{errorTimes}次。")
                if (errorTimes > 5):
                    break

    def auto_start(self, agent): 
        """
        启动AI，依据 kfStatus 调用 start 或 stop
        """
        kfStatus = agent.get_kf_status()
        # print(f"Auto Start {agent.get_kf_name()}-Status:{kfStatus}")
        if kfStatus:
            # 如果获取到状态信息，进行处理
            if kfStatus["manage_status"] == 0:
                result = agent.call("activate", agent.get_kf_name())
                # print ("activate result", result)
                if (result == True) :
                    agent.call("stop", agent.get_kf_name())
                agent.set_kf_status(0)
            elif kfStatus["status_now"] == 0:
                agent.call("start", agent.get_kf_name())
                agent.set_kf_status(1)
        else:
            # 如果没有找到对应的 kfStatus，可以记录错误或执行默认行为
            print(f"Error: kfStatus for {agent.get_kf_name()} not found")



        