import unittest
import openai_simple_chat


# 要求提供ollama本地大模型服务，并设置相应的环境变量
class TestChat(unittest.TestCase):
    def test_1(self):
        llm = openai_simple_chat.OllamaChatService()
        response, response_info = llm.chat(prompt="你好！")
        assert response
        assert response_info
        assert isinstance(response, str)
        assert isinstance(response_info, dict)

    def test_2(self):
        llm = openai_simple_chat.OllamaChatService()
        response, response_info = llm.jsonchat(
            """以标准json返回以下计算结果数值【输出格式为：{"result": xx}】：1+1"""
        )
        assert response
        assert response_info
        assert isinstance(response, dict)
        assert isinstance(response_info, dict)
        assert "result" in response
        assert response["result"] == 2

    def test_3(self):
        llm = openai_simple_chat.OllamaChatService()
        for delta, chunk in llm.streaming_chat(prompt="你好！"):
            assert isinstance(delta, str)
            assert isinstance(chunk, dict)

    def test_4(self):
        llm = openai_simple_chat.OllamaChatService(
            template_engine=openai_simple_chat.get_template_prompt_by_jinjia2,
            template_root="test_templates",
        )
        response, response_info = llm.jsonchat(template="calc.txt", expression="1+1")
        assert response
        assert response_info
        assert isinstance(response, dict)
        assert isinstance(response_info, dict)
        assert "result" in response
        assert response["result"] == 2
