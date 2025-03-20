from neutrino.onboard.agent import DataOnboardingAgent
from neutrino.utils.tools import extract_code_blocks_with_type

data = """{
		"customer_id": 9,
		"name": "Johnathan Rodriguez",
		"email": "thomasramirez@example.org",
		"phone": "001-845-290-8721x77863",
		"address": "743 Cervantes Causeway Apt. 762\nPort Lauren, NY 12698",
		"ip": "127.0.0.1",
		"time": "2023-01-01 00:00:00",
		"event_time": "2023-01-01 00:00:00",
		"uid": "2a02:aa08:e000:3100::2",
		"uid2":"1f71acbf-59fc-427d-a634-1679b48029a9"
}"""

columns = [
    {
        "name": "customer_id",
        "type": "uint32"
    },
    {
        "name": "name",
        "type": "string"
    },
    {
        "name": "email",
        "type": "string"
    },
    {
        "name": "phone",
        "type": "string"
    },
    {
        "name": "address",
        "type": "string"
    },
    {
        "name": "ip",
        "type": "ipv4"
    },
    {
        "name": "time",
        "type": "datetime"
    },
    {
        "name": "event_time",
        "type": "datetime"
    },
    {
        "name": "uid",
        "type": "ipv6"
    },
    {
        "name": "uid2",
        "type": "uuid"
    }
]


agent = DataOnboardingAgent()

recommendation_result = agent.recommendations(data, columns, 'test_customer')
print(f"recommendations : {recommendation_result}")
