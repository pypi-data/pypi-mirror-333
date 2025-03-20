from typing import Any, get_origin, get_args, Type

from pydantic import Field, create_model, BaseModel
from pydantic.fields import FieldInfo

from core.tool.rpc.http import ApiDef

fields = {
    "name": (str, Field(..., description="The person's name")),
    "age": (int, Field(..., description="The person's age")),
    "is_student": (bool, Field(False, description="Whether the person is a student")),
    "kwargs": {
        "name": (str, Field(..., description="The person's name")),
        "age": (int, Field(..., description="The person's age")),
        "is_student": (bool, Field(False, description="Whether the person is a student")),
    }
}

api_def = ApiDef(url='http://221.229.0.177:9981/chat', method='post', name='llm_chat', description='通过大模型调用来回答问题', is_async=False, args={
             "model_uid": {'title': '选择模型id', 'description': '选择模型id，默认选择deepseek-chat^deepseek-chat^396@deepseek^18', 'required': True, 'type': 'string'},
             "q": {'title': '提问的问题描述', 'description': '提问的问题描述', 'required': False, 'type': 'string'},
             "prompt": {'title': '前置提示词', 'description': '前置提示词', 'required': False, 'type': 'string'},
            })

# fields = {
#     "name": (str, "The person's name"),
#     "age": (int, "The person's age"),
#     "address": {
#         "street": (str, "The street address"),
#         "city": (str, "The city of residence"),
#         "zip_code": (str, "The postal code")
#     },
#     "hobbies": (list[str], "A list of hobbies"),
#     "is_student": (bool, "Whether the person is a student")
# }


def create_nested_model(model_name: str, fields: dict[str, Any]) -> Type[BaseModel]:
    """
    递归生成嵌套的 BaseModel 类，并为每个字段添加 Field 描述。
    """
    nested_fields = {}
    for field_name, field_info in fields.items():
        if isinstance(field_info, dict):  # 如果字段是嵌套字典
            nested_model_name = f"{model_name}_{field_name.capitalize()}"
            nested_model = create_nested_model(nested_model_name, field_info)
            nested_fields[field_name] = (nested_model, ...)
        elif isinstance(field_info, tuple):  # 如果字段包含类型和描述
            field_type, field_description = field_info
            if get_origin(field_type) is list:  # 如果字段是列表
                list_type = get_args(field_type)[0]
                nested_fields[field_name] = (list[list_type], Field(..., description=field_description))
            else:  # 普通字段
                nested_fields[field_name] = (field_type, Field(..., description=field_description))
        else:  # 普通字段（无描述）
            nested_fields[field_name] = (field_info, ...)

    return create_model(model_name, **nested_fields)

# DynamicModel = create_nested_model("DynamicModel", fields=api_def.args)
# res = DynamicModel.model_json_schema()['properties']
# for k, v in res.items():
#     print(k)
#     # print(v.values())
#     print(v)
#     print({
#                 'title': v['description'].title,
#                 'description':  v['description'].description,
#                 'required': v['description'].is_required(),
#                 'type': v['type'],
#             })
# print(res)

f = Field(**{'title': '前置提示词', 'description': '前置提示词', 'required': True, 'type': 'string', 'default': '1'})
print(f)

#
# from pydantic import BaseModel, create_model, Field
# from typing import Any, get_origin, get_args
#
#
# def create_nested_model(model_name: str, fields: dict[str, Any]) -> type[BaseModel]:
#     nested_fields = {}
#     for field_name, field_type in fields.items():
#         if isinstance(field_type, dict):  # 嵌套字典
#             nested_model_name = f"{model_name}_{field_name.capitalize()}"
#             nested_model = create_nested_model(nested_model_name, field_type)
#             nested_fields[field_name] = (nested_model, ...)
#         elif get_origin(field_type) is list:  # 列表类型
#             list_type = get_args(field_type)[0]
#             nested_fields[field_name] = (list[list_type], ...)
#         else:  # 普通字段
#             nested_fields[field_name] = (field_type, ...)
#
#     return create_model(model_name, **nested_fields)
#
#
# # 定义嵌套字典
# nested_dict = {
#     "name": str,
#     "age": int,
#     "address": {
#         "street": str,
#         "city": str,
#         "zip_code": str
#     },
#     "hobbies": list[str],
#     "is_student": bool
# }
#
# # 生成嵌套模型
# NestedModel = create_nested_model("NestedModel", nested_dict)
#
# # 使用生成的模型
# instance = NestedModel(
#     name="Alice",
#     age=30,
#     address={
#         "street": "123 Main St",
#         "city": "Springfield",
#         "zip_code": "12345"
#     },
#     hobbies=["reading", "hiking"],
#     is_student=False
# )
#
# print(instance)
# print(instance.model_json_schema())
