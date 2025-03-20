
class AgentTest:
    def __init__(self, reg):
        """ 初始化一个空字典用于存储函数 """
        self._agent_kf = reg

    def test(self):
        #初始化
        kf_name = self._agent_kf.get_kf_name()
        #self._agent_kf.call("stop", kf_name)
        #self._agent_kf.call("start", kf_name)
        user_list = self._agent_kf.call("get_customers_waiting")
        for user in user_list:
            chat_list = self._agent_kf.call("get_new_chats", user)
            print ("chat_list:", chat_list)
            self._agent_kf.call("reply", user, "This is a test!")
            self._agent_kf.call("transfer_to_customer_care", user, "人工客服", "test")
            self._agent_kf.call("get_recently_order", user)
            self._agent_kf.call("specify_logistic", user, "顺丰陆运")
            self._agent_kf.call("recommend_product", user, "大马士革玫瑰纯露")
            self._agent_kf.call("modify_notes", user, "test")
            self._agent_kf.call("recommend_product", user, "大马士革玫瑰纯露")
            self._agent_kf.call("modify_address", user, "大马士革玫瑰纯露")
            self._agent_kf.call("contact_old_user", user)
            self._agent_kf.call("activate", kf_name)

            self._agent_kf.call("close_chat", user)
            



        