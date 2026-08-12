import importlib.util
import threading
import time
import unittest
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "custom_tool" / "pipeline_llm.py"
SPEC = importlib.util.spec_from_file_location("pipeline_llm_under_test", PATH)
pipeline = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(pipeline)


class FakeDelegate:
    def __init__(self, block=None, calls=None):
        self.block = block
        self.calls = calls if calls is not None else []

    def chatbot(self, **kwargs):
        value = str(kwargs["user_prompt"])
        self.calls.append(kwargs)
        if self.block and value == "one":
            self.block[0].set()
            self.block[1].wait(1.0)
        return ("generated:" + value, "history:" + value, "tools", None, "reasoning")


class PipelineTests(unittest.TestCase):
    def setUp(self):
        with pipeline._LOCK:
            pipeline._STATES.clear()

    def tearDown(self):
        self.wait_idle()
        with pipeline._LOCK:
            pipeline._STATES.clear()

    def wait_idle(self):
        deadline = time.time() + 2
        while time.time() < deadline:
            with pipeline._LOCK:
                if all(not state["running"] for state in pipeline._STATES.values()):
                    return
            time.sleep(0.01)
        self.fail("worker did not stop")

    def test_has_all_general_link_inputs_and_outputs(self):
        inputs = pipeline.LLMPartyPipeline.INPUT_TYPES()
        required = {
            "system_prompt", "user_prompt", "model", "temperature", "is_memory",
            "is_tools_in_sys_prompt", "is_locked", "main_brain", "max_length",
        }
        optional = {
            "system_prompt_input", "user_prompt_input", "tools", "file_content",
            "images", "imgbb_api_key", "conversation_rounds", "historical_record",
            "is_enable", "extra_parameters", "user_history", "img_URL", "stream",
        }
        self.assertTrue(required.issubset(inputs["required"]))
        self.assertTrue(optional.issubset(inputs["optional"]))
        self.assertEqual(pipeline.LLMPartyPipeline.RETURN_NAMES[:5], (
            "assistant_response", "history", "tool", "image", "reasoning_content"
        ))

    def test_next_run_uses_previous_full_result(self):
        delegate = FakeDelegate()
        pipeline._create_delegate = lambda _model: delegate
        node = pipeline.LLMPartyPipeline()
        first = node.chatbot("first", "enable", "sys", object(), 0.7, "disable", "disable", "disable", 1920, unique_id="1")
        self.assertEqual(first[0], "first")
        self.wait_idle()
        second = node.chatbot("second", "enable", "sys", object(), 0.7, "disable", "disable", "disable", 1920, unique_id="1")
        self.assertEqual(second[:5], ("generated:first", "history:first", "tools", None, "reasoning"))

    def test_only_latest_pending_input_is_kept(self):
        started, release = threading.Event(), threading.Event()
        calls = []
        delegate = FakeDelegate((started, release), calls)
        pipeline._create_delegate = lambda _model: delegate
        node = pipeline.LLMPartyPipeline()
        args = ("enable", "sys", object(), 0.7, "disable", "disable", "disable", 1920)
        node.chatbot("one", *args, unique_id="2")
        self.assertTrue(started.wait(1.0))
        node.chatbot("two", *args, unique_id="2")
        node.chatbot("three", *args, unique_id="2")
        release.set()
        self.wait_idle()
        self.assertEqual([call["user_prompt"] for call in calls], ["one", "three"])

    def test_empty_final_answer_keeps_previous_result(self):
        good = FakeDelegate()
        pipeline._create_delegate = lambda _model: good
        node = pipeline.LLMPartyPipeline()
        args = ("enable", "sys", object(), 0.7, "disable", "disable", "disable", 1920)
        node.chatbot("good", *args, unique_id="3")
        self.wait_idle()

        good.chatbot = lambda **_kwargs: ("", "new history", "tools", None, "reasoning only")
        output = node.chatbot("bad", *args, unique_id="3")
        self.assertEqual(output[0], "generated:good")
        self.wait_idle()
        with pipeline._LOCK:
            self.assertEqual(pipeline._STATES["default:3"]["ready"][0], "generated:good")


if __name__ == "__main__":
    unittest.main()
