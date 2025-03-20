from whisper_ai_zxs.agent_test import AgentTest
#from ..whisper_ai_zxs.agent_servicer_YD import Agent_YD
from whisper_ai_zxs.agent_servicer_Test import Agent_Test


Agent = Agent_Test("植想说天猫店:亮亮")

Test = AgentTest(Agent)

Test.test()
