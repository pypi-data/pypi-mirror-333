from pprint import pprint
from random import choice
from pistol_magazine import *
from flask import Flask, jsonify


# Create a custom provider
@provider
class MyProvider:
    def my_provider(self):
        return choice(["ACTIVE", "INACTIVE"])


"""
Define hook functions
pre_generate: Executes operations before generating all data. Suitable for tasks like logging or starting external services.
after_generate: Executes operations after generating each data entry but before final processing. Suitable for tasks like data validation or conditional modifications.
final_generate: Executes operations after generating and processing all data entries. Suitable for final data processing, sending data to message queues, or performing statistical analysis.
"""


@hook('pre_generate', order=1, hook_set='SET1')
def pre_generate_first_hook():
    print("Start Mocking User Data")


@hook('pre_generate', order=2, hook_set='SET1')
def pre_generate_second_hook():
    """
    Perform some preprocessing operations, such as starting external services.
    """


@hook('after_generate', order=1, hook_set="SET1")
def after_generate_first_hook(data):
    """
    :param data:
    :return:
    """
    # data['customized_param'] = 'ACTIVE' if data['int_param'] >= 18 else 'INACTIVE'
    # return data


@hook('final_generate', order=1, hook_set="SET1")
def final_generate_second_hook(data):
    """
    Suppose there is a function send_to_message_queue(data) to send data to the message queue
    Or use built-in data exporters to export data, like the code below⬇️.
    """
    # yaml_exporter = YAMLExporter()  # Also support csv, db, xml export
    # yaml_exporter.export(data, 'output.yaml')


class Temp(DataMocker):
    assetName: Str = Str()
    assetId: Str = Str(data_type="md5")
    heat: StrInt = StrInt(byte_nums=16, unsigned=True)
    impact: StrInt = StrInt(byte_nums=16, unsigned=True)
    profitability: StrInt = StrInt(byte_nums=16, unsigned=True)
    noOfContents: StrInt = StrInt(byte_nums=16, unsigned=True)
    totalViews: StrInt = StrInt(byte_nums=16, unsigned=True)
    totalDuration: ProviderField = ProviderField(RegexProvider(pattern=r"^\d{1,3}:[0-5]\d:[0-5]\d$").gen)
    totalEarning: StrFloat = StrFloat(left=6, right=2, unsigned=True)
    lastOnMonthEarning: StrFloat = StrFloat(left=4, right=2, unsigned=True)

    # list_param: List = List(
    #     [
    #         Datetime(Datetime.D_FORMAT_YMD_T, weeks=2),
    #         StrInt(byte_nums=6, unsigned=True),
    #         Dict(
    #             {
    #                 "a": Float(left=2, right=4, unsigned=True),
    #                 "b": Timestamp(Timestamp.D_TIMEE10, days=2),
    #                 "url": ProviderField(RegexProvider(
    #                     pattern=r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:watch\?v=|embed\/|v\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})").gen)
    #             }
    #         )
    #     ]
    # )

    def gen_data(self):
        return self.mock(single_item=True)


def test_fake_max_push_data():
    pprint(Temp().gen_data())


