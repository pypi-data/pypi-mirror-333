import xml.etree.ElementTree as ET
import re
import loggerutility as logger

class FreeHand_SQL_Model:
    def __init__(self, visual_json, schema_xml_file_path):
        self.visual_json = visual_json
        self.schema_xml_file_path = schema_xml_file_path
        self.schema_json_data = self.parse_xml_to_json()

    def parse_xml_to_json(self):
        columns = {}
        try:
            tree = ET.parse(self.schema_xml_file_path)
            root = tree.getroot()
            for column in root.findall(".//COLUMN"):
                column_name = column.get("NAME")
                if column_name and column_name not in columns:
                    columns[column_name] = {attr: column.get(attr, "") for attr in column.keys()}
                    columns[column_name]["content"] = column.text or ""
        except Exception as e:
            logger.log(f"Error parsing XML: {e}")
        return columns
    
    def generate_sql_model(self):
        schema_name = self.visual_json.get("Schema_Name", "")
        visual_name = self.visual_json.get("Visual_Name", "")

        output = {
            "SQLModel": {
                "COLUMNS": [
                    {
                        "COLUMN": []
                    }
                ]
            },
            "CRITERIA": {"query": {"rules": []}},
            "VISUAL_NAME": 'Line' if visual_name == 'Scatter' else visual_name,
            "SCHEMA_NAME": schema_name,
            "SCHEMA_DESCR": self.format_name(schema_name),
            "SCHEMA_TYPE": "F",
            "OUTPUT_TYPE": "JSON",
            "DATABASE_TYPE": "1",
            "DATABASE_DETAIL": {
                "DATABASE_NAME": "Oracle",
                "TYPE": 1
            }
        }

        return output

    @staticmethod
    def format_name(name):
        if '_' in name:
            return ' '.join([word.capitalize() for word in name.split('_')])
        else:
            return name
