import unittest
import openai_simple_chat


class TestJsonUtils(unittest.TestCase):
    def test_1(self):
        text = """{&quot;maxValue&quot;: 9.8}"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_2(self):
        text = """
<think>xxxx</think>
{&quot;maxValue&quot;: 9.8}
"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_3(self):
        text = """
<think>xxxx</think>
```json
{"maxValue": 9.8}
```
"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_4(self):
        text = """
<think>xxxx</think>
```
{"maxValue": 9.8}
```
"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_5(self):
        text = """
xxxx
```
{"maxValue": 9.8}
```json
"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_6(self):
        text = """
xxxx
```
{"maxValue": 9.8}
```
"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_7(self):
        text = """{"maxValue": 9.8}"""
        data = openai_simple_chat.parse_json_response(text)
        assert data["maxValue"] == 9.8

    def test_8(self):
        text = """<think>
好吧，用户让我用标准的JSON格式回复“1+1=?”并指定结果为result。我应该先确认自己是否正确理解了要求。

首先，JSON格式是特定的，每个对象必须包裹在双引号内，值之间用逗号分隔。这里是一个计算式，输出应该是字符串“2？”，然后用result字段表示这个值。

接下来，我要确保语法正确。如果用户需要一个字典而不是一个字符串，那么可能有误，但根据问题描述，我应该返回一个字符串结果，并且最终格式是JSON。

另外，检查是否有其他用户的指令或要求，比如是否需要自动生成代码块，但看来这里只需要简单的输出即可。

最后，确认自己没有遗漏任何细节，确保JSON结构正确，值与字段名称匹配，以及语法无误。
</think>

Here is the result in JSON format, using `result` as the field to represent the value:

```json
{
  "result": "2"
}
```

But since you specifically asked for the calculation of \(1 + 1 = ?\), the appropriate response would be:

```json
{"result": "2"}
```
"""
        data = openai_simple_chat.parse_json_response(text)
        assert data

    def test_9(self):
        text = """<think>\n嗯，用户让我用标准的JSON格式来返回1+1的结果，并且输出格式是{"result": xx}。首先，我需要确认JSON的标准结构是什么样的。一般来说，JSON是一个对象，里面包含键值对，每个键对应一个数组或单个值。\n\n接下来，我要处理的是计算结果。1加1等于2，所以结果应该是2。然后，按照JSON的格式来写，应该是一个对象，里面的键是“result”，对应的值就是2。\n\n我还要考虑一下是否有其他可能的错误情况，比如用户是否需要更复杂的结构或者不同的输出方式。但在这个问题中，看起来很简单，直接返回数值就可以了。\n\n最后，我要确保我的回答符合用户的指示，严格按照JSON格式来写，并且结果正确无误。\n</think>\n\n{"result": 2}"""
        data = openai_simple_chat.parse_json_response(text)
        assert data
