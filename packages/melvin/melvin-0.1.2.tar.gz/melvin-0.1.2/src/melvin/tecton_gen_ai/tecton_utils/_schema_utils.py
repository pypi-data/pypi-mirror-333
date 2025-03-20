import json

import jsonschema
from pydantic.v1.datetime_parse import parse_datetime
from tecton.types import Array, Bool, Field, Float64, Int64, String, Struct, Timestamp


def _get_type(schema_field, schema_dict):
    if "$ref" in schema_field:
        obj = _get_obj_from_ref(schema_field["$ref"], schema_dict)
        return _get_type(obj, schema_dict)

    if "type" not in schema_field:
        raise ValueError(f"Type not found: {schema_field}")

    dtype_str = schema_field["type"]
    if dtype_str == "string":
        if "format" in schema_field:
            if schema_field["format"] == "date-time":
                return Timestamp
            else:
                raise ValueError(f"Format {schema_field['format']} not supported")
        else:
            return String
    elif dtype_str == "number":
        return Float64
    elif dtype_str == "integer":
        return Int64
    elif dtype_str == "boolean":
        return Bool
    elif dtype_str == "array":
        item_type = _get_type(schema_field["items"], schema_dict)
        return Array(item_type)
    elif dtype_str == "object":
        struct_fields = _process_object(schema_field["properties"], schema_dict)
        return Struct(struct_fields)
    elif "$ref" in dtype_str:
        obj = _get_obj_from_ref(dtype_str["$ref"], schema_dict)
        return _get_type(obj, schema_dict)
    else:
        raise ValueError(f"Type {dtype_str} not supported")


def _get_obj_from_ref(ref, schema_dict):
    path = ref.split("/")[1:]
    obj = schema_dict
    for item in path:
        obj = obj[item]
    return obj


def _process_object(properties, schema_dict):
    fields = []
    for property_name, property_value in properties.items():
        if "$ref" in property_value:
            obj = _get_obj_from_ref(property_value["$ref"], schema_dict)

            if obj["type"] == "object":
                struct_fields = _process_object(obj["properties"], schema_dict)
                fields.append(Field(name=property_name, dtype=Struct(struct_fields)))
            else:
                fields.append(
                    Field(name=property_name, dtype=_get_type(obj, schema_dict))
                )
        else:
            fields.append(
                Field(name=property_name, dtype=_get_type(property_value, schema_dict))
            )
    return fields


def get_tecton_fields_from_json_schema(schema_dict):
    """Converts a JSON schema into a list of Tecton Field types"""
    struct = _get_type(schema_dict, schema_dict)
    return struct.fields


def _get_field_converter(schema, value):
    if schema.get("format") == "date-time" and isinstance(value, str):
        return parse_datetime
    return None


def _convert_string_format_recursive(obj, schema):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in schema.get("properties", {}):
                prop_schema = schema["properties"][key]
                if converter := _get_field_converter(prop_schema, value):
                    obj[key] = converter(value)
                elif isinstance(value, (dict, list)):
                    _convert_string_format_recursive(value, prop_schema)
    elif isinstance(obj, list) and schema.get("items"):
        item_schema = schema["items"]
        for i, item in enumerate(obj):
            if converter := _get_field_converter(item_schema, item):
                obj[i] = converter(item)
            elif isinstance(item, (dict, list)):
                _convert_string_format_recursive(item, item_schema)


def load_to_rich_dict(json_str: str, schema):
    output = json.loads(json_str)
    jsonschema.validate(output, schema)
    _convert_string_format_recursive(output, schema)
    return output
