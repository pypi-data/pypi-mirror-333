import os
import asyncio

from dataclasses import dataclass

from autogen_core import (
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    message_handler,
    type_subscription,
    AgentId,
)
from autogen_core.models import ChatCompletionClient, SystemMessage, UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogen_ext.models.cache import ChatCompletionCache, CHAT_CACHE_VALUE_TYPE
from autogen_ext.cache_store.diskcache import DiskCacheStore
from diskcache import Cache

from ..utils.tools import extract_code_blocks_with_type


@dataclass
class Message:
    content: str


schema_inference_agent_topic = "SchemaInferenceAgent"
schema_to_table_agent_topic = "SchemaToTableAgent"
field_summary_agent_topic = "FieldSummaryAgent"
analysis_recommendations_agent_topic = "AnalysisRecommendationsAgent"


@type_subscription(topic_type=schema_inference_agent_topic)
class SchemaInferenceAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A schema inference agent.")
        self._system_message = SystemMessage(
            content=(
                """please generate DDL based on input data which is a json object or list of json object seperated by comma
    here are the rules to follow
    * the DDL grammar follows ClickHouse style
    * the Table keyword MUST be replaced with Stream
    * all datatypes MUST be in lowercase, such uint32
    * all keywords MUST be in lowercase, such as nullable
    * all field names MUST keep same as in the json
    * composite types such as array, tuple cannot be nullable
    * should use composite types like array, tuple to represent complex structure in the json
    * from composite types, prefer tuple over map
    * if the data value is null, field type MUST be set as 'unknown'
    * return the result as a markdown sql code
    * Make sure the hierarchy is represented in the DDL match the input data


    here is a sample of output DDL:
    ```sql
    CREATE STREAM car_live_data
    (
      `cid` string,
      `gas_percent` float64,
      `in_use` bool
    ```

    here is a list of supported datatypes:
    * string
    * int, int32, int8, int64, smallint, bigint, uint16, uint32, uint64
    * float64, float32, double
    * decimal
    * bool
    * ipv4
    * ipv6
    * date
    * datetime
    * datetime64
    * uuid
    * tuple
    * array
    * map
"""
            )
        )
        self._model_client = model_client
        self._result = None

    @message_handler
    async def inference(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"{message.content}, please generate schema"
        llm_result = await self._model_client.create(
            messages=[
                self._system_message,
                UserMessage(content=prompt, source=self.id.key),
            ],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}\n{self.id.type}:\n{response}")
        self._result = response
        await self.publish_message(
            Message(response),
            topic_id=TopicId(schema_to_table_agent_topic, source=self.id.key),
        )


@type_subscription(topic_type=schema_to_table_agent_topic)
class SchemaToTableAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A agent turn schema to column table.")
        self._system_message = SystemMessage(
            content=(
                """based on generated DDL, please convert it into a json object
    Rules:
    * for type string, it MUST be a single line for string

    for example, if the input DDL is:
    CREATE STREAM car_live_data
    (
      `cid` string,
      `gas_percent` float64,
      `in_use` bool,
      `composite` tuple(
          'x' int
          ),
    )

    the output of the json description of the DDL should be:
    ```json

    [
        {
            "name" : "cid", "type" : "string"
        },
        {
            "name" : "gas_percent", "type" : "float64"
        },
        {
            "name" : "in_use", "type" : "bool"
        },
        {
            "name" : "composite", "type" : "tuple('x' int)"
        }
    ]
    ```
"""
            )
        )
        self._model_client = model_client
        self._result = None

    @message_handler
    async def convert(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"{message.content}, please convert to table"
        llm_result = await self._model_client.create(
            messages=[
                self._system_message,
                UserMessage(content=prompt, source=self.id.key),
            ],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}\n{self.id.type}:\n{response}")
        self._result = response


@type_subscription(topic_type=field_summary_agent_topic)
class FieldSummaryAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__("A agent provide field summary of a stream/table.")
        self._system_message = SystemMessage(
            content=(
                """please generate a report to explain each fields of the schema,
    turn the hierachy into flatten when generating this report for each field,
    use '.' to connect the parents and children names
    output the result into a json object
    here is a sample of the output:
    [
        {
            "name": "eventversion",
            "type": "uint32",
            "description": "The version of the current event."
        },
        {
            "name": "open_24h",
            "type": "string",
            "description": "The price of the asset at the beginning of the last 24-hour period."
        }
    ]
"""
            )
        )
        self._model_client = model_client
        self._result = None

    @message_handler
    async def summary(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"{message.content}, please generate field summary"
        llm_result = await self._model_client.create(
            messages=[
                self._system_message,
                UserMessage(content=prompt, source=self.id.key),
            ],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}\n{self.id.type}:\n{response}")
        self._result = response


@type_subscription(topic_type=analysis_recommendations_agent_topic)
class AnalysisRecommendationsAgent(RoutedAgent):
    def __init__(self, model_client: ChatCompletionClient) -> None:
        super().__init__(
            "A agent provide analysis recommendations base on schema and sample data."
        )

        self._system_message = SystemMessage(
            content=(
                """please generate 10 analysis SQL based on input schema and analysis recommendations
    output into a json object which is an array
    note, you need escape newlines if the output contains multiple lines string

    The generate SQL should follow these rules
    * the SQL follows the ClickHouse grammar
    * all method name MUST be in lower cases, following snake cases, for example : array_sum
    * no CROSS JOIN is supported

    As timeplus is a streaming processing platform, there are three different types of query regarding how to scan the data
    please randomly select one of these three patterns to generate SQL

    1 temperal window based analysis tumble window with 5 second window size
    following query return analysis result in a continously streaming query for every 5 second window
    select window_start, window_end, count(*) as count, max(c1) as max_c1
    from tumble(my_stream, 5s) group by window_start, window_end

    2 global aggregration which Global aggregation will start the aggregation for all incoming events since the query is submitted, and never ends.
    select count(*) as count, id as id
    from my_stream group by id

    3 historical aggreation, using table function, the query will just run traditional SQL that scan all historical data and return after query end
    select count(*) as count, id as id
    from table(my_stream) group by id


    #########
    here is a sample output:
    [
      {
        "sql": "select eventVersion, sum(videoSourceBandwidthBytesPerEvent + videoFecBandwidthBytesPerEvent + audioSourceBandwidthBytesPerEvent + audioFecBandwidthBytesPerEvent) as total_bandwidth_bytes from xray_stream group by eventVersion",
        "description": "Calculate the total bandwidth used per event version by summing up video, audio, and FEC bandwidths.",
        "name" : "Bandwidth Utilization Analysis"
      }
    ]"""
            )
        )
        self._model_client = model_client
        self._result = None

    @message_handler
    async def summary(self, message: Message, ctx: MessageContext) -> None:
        prompt = f"{message.content}, please generate field summary"
        llm_result = await self._model_client.create(
            messages=[
                self._system_message,
                UserMessage(content=prompt, source=self.id.key),
            ],
            cancellation_token=ctx.cancellation_token,
        )
        response = llm_result.content
        assert isinstance(response, str)
        print(f"{'-' * 80}\n{self.id.type}:\n{response}")
        self._result = response


class DataOnboardingAgent:
    def __init__(self):
        cache_dir = os.path.join(os.getcwd(), ".neutrino_cache")
        os.makedirs(cache_dir, exist_ok=True)  # Ensure the directory exists
        openai_model_client = OpenAIChatCompletionClient(
            model="gpt-4o-mini", temperature=0.0
        )
        cache_store = DiskCacheStore[CHAT_CACHE_VALUE_TYPE](Cache(cache_dir))
        self.client = ChatCompletionCache(openai_model_client, cache_store)
        self.runtime = SingleThreadedAgentRuntime()

    async def _inference(self, data, stream_name):
        await SchemaInferenceAgent.register(
            self.runtime,
            type=schema_inference_agent_topic,
            factory=lambda: SchemaInferenceAgent(model_client=self.client),
        )

        await SchemaToTableAgent.register(
            self.runtime,
            type=schema_to_table_agent_topic,
            factory=lambda: SchemaToTableAgent(model_client=self.client),
        )

        message = f"based on input data : {data}, and stream name : {stream_name}"
        self.runtime.start()

        await self.runtime.publish_message(
            Message(content=message),
            topic_id=TopicId(schema_inference_agent_topic, source="default"),
        )

        await self.runtime.stop_when_idle()
        inference_agent_id = AgentId(schema_inference_agent_topic, "default")
        inference_agent = await self.runtime.try_get_underlying_agent_instance(
            inference_agent_id
        )

        table_agent_id = AgentId(schema_to_table_agent_topic, "default")
        table_agent = await self.runtime.try_get_underlying_agent_instance(
            table_agent_id
        )

        inference_result = extract_code_blocks_with_type(inference_agent._result)
        table_result = extract_code_blocks_with_type(table_agent._result)

        # TODO: handle failed to extract case
        return inference_result[0][1], table_result[0][1]

    def inference(self, data, stream_name):
        return asyncio.run(self._inference(data, stream_name))

    async def _summary(self, data, columns):
        await FieldSummaryAgent.register(
            self.runtime,
            type=field_summary_agent_topic,
            factory=lambda: FieldSummaryAgent(model_client=self.client),
        )

        message = f"based on input data : {data}, and columns : {columns}"
        self.runtime.start()

        await self.runtime.publish_message(
            Message(content=message),
            topic_id=TopicId(field_summary_agent_topic, source="default"),
        )

        await self.runtime.stop_when_idle()
        agent_id = AgentId(field_summary_agent_topic, "default")
        agent = await self.runtime.try_get_underlying_agent_instance(agent_id)

        result = extract_code_blocks_with_type(agent._result)

        # TODO: handle failed to extract case
        return result[0][1]

    def summary(self, data, columns):
        return asyncio.run(self._summary(data, columns))

    async def _recommendations(self, data, columns, stream_name):
        await AnalysisRecommendationsAgent.register(
            self.runtime,
            type=analysis_recommendations_agent_topic,
            factory=lambda: AnalysisRecommendationsAgent(model_client=self.client),
        )

        message = f"based on input data : {data}, and columns : {columns} and stream name : {stream_name}"
        self.runtime.start()

        await self.runtime.publish_message(
            Message(content=message),
            topic_id=TopicId(analysis_recommendations_agent_topic, source="default"),
        )

        await self.runtime.stop_when_idle()
        agent_id = AgentId(analysis_recommendations_agent_topic, "default")
        agent = await self.runtime.try_get_underlying_agent_instance(agent_id)

        result = extract_code_blocks_with_type(agent._result)

        # TODO: handle failed to extract case
        return result[0][1]

    def recommendations(self, data, columns, stream_name):
        return asyncio.run(self._recommendations(data, columns, stream_name))
