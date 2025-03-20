import xml.etree.ElementTree as ET
import re
import loggerutility as logger

class SQL_Model:
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

    def generate_sqlmodel_columns(self):
        columns = []
        groups = self.visual_json.get("Groups", {})

        for group_name, fields in groups.items():
            for field in fields:
                column_data = self.schema_json_data.get(field, {})
                checks = column_data.get("DBTABLE", field.split('_')[0])

                checks_value = column_data.get("DBTABLE")

                if isinstance(checks_value, list):
                    formatted_checks = [
                        '_'.join(word.capitalize() for word in value.split('_')) for value in checks_value
                    ]
                else:
                    formatted_checks = ['_'.join(word.capitalize() for word in checks_value.split('_'))]

                for formatted_check in formatted_checks:
                    logger.log(f"formatted_check:: {formatted_check}")

                column_name = column_data.get("content", self.format_name(field))

                column = {
                    "ITALIC": int(column_data.get("ITALIC", 0)),
                    "BGCOLOR": column_data.get("BGCOLOR", ""),
                    "EXPRESSIONTYPE": column_data.get("EXPRESSIONTYPE", "C"),
                    "WIDTH": int(column_data.get("WIDTH", 100)),
                    "HIDDEN": column_data.get("HIDDEN", ""),
                    "DBSIZE": int(column_data["DBSIZE"]) if column_data.get("DBSIZE", "").isdigit() else column_data.get("DBSIZE", ""),
                    "UNDERLINE": int(column_data.get("UNDERLINE", 0)),
                    "COLID": int(column_data.get("COLID", 0)),
                    "FONT": column_data.get("FONT", "TIMES NEW ROMAN"),
                    "content": column_data.get("content", self.format_name(field)),
                    "NAME": field,
                    "NATIVETYPE": column_data.get("NATIVETYPE", "AN"),
                    "FONTSIZE": int(column_data.get("FONTSIZE", 12)),
                    "FGCOLOR": column_data.get("FGCOLOR", "#000000"),
                    "JAVATYPE": column_data.get("JAVATYPE", "java.lang.String"),
                    "ALIGNMENT": int(column_data.get("ALIGNMENT", 1)),
                    "DBTABLE": column_data.get("DBTABLE", field.split('_')[0]),
                    "DBNAME": column_data.get("DBNAME", '_'.join(field.split('_')[2:])),
                    "BOLD": int(column_data.get("BOLD", 0)),
                    "DEFAULTFUNCTION": column_data.get("DEFAULTFUNCTION", ""),
                    "COLTYPE": column_data.get("COLTYPE", "CHAR" if len(field) <= 10 else "VARCHAR2"),
                    "KEY": column_data.get("KEY", "false").lower() == "true",
                    "CAPS": column_data.get("CAPS", "false").lower() == "true",
                    "FEILD_TYPE": "TEXTBOX",
                    "value": "",
                    "name": column_name,
                    "type": "string" if column_data.get("COLTYPE", "") in ["VARCHAR2", "CHAR", "NUMBREAKAGE_RETURN_QTYBER"] else "date" if column_data.get("COLTYPE", "") in ["DATE"] else "number",
                    "descr": f"{column_name} description",
                    "expression": "",
                    "tableName": column_data.get("DBTABLE", field.split('_')[0]),
                    "tableDisplayName": formatted_check,
                    "FUNCTION": column_data.get("DEFAULTFUNCTION", ""),
                    "ADV_FORMAT": "",
                    "alignment": "",
                    "groupName": group_name,
                    "checked": True,
                    "StandardName": group_name
                }

                if column_data.get("COLTYPE", "") in ["DATE"]:
                    column["PATTERN"] = "dd-MMM-yy"
                columns.append(column)

        return columns
    
    def get_column_details(self, table_name, table_field_name):
        logger.log(f"table_name ::: {table_name}")
        logger.log(f"table_field_name ::: {table_field_name}")

        field_name_without_table = table_field_name.replace(f"{table_name}_", "", 1).strip()

        logger.log(f"Field Name without Table Name ::: {field_name_without_table}")

        for column_name, column_data in self.schema_json_data.items():
            if column_data.get("NAME") == table_field_name:
                return (table_name, field_name_without_table, table_field_name.replace("_", " "), column_data.get("COLTYPE", ""))

    def generate_criteria(self):
        condition = self.visual_json.get("Condition", [])
        rules = []
        operators = ["=", "!=", ">", ">=", "<", "<="]
        conditions = []
        condition_operator = ""
        try:
            if "AND" in condition:
                conditions = condition.split("AND")
                condition_operator = "and"
            elif "OR" in condition:
                conditions = condition.split("OR")
                condition_operator = "or"

            for idx, cond in enumerate(conditions, start=1):
                operators = re.findall(r'[=<>!]+', cond)
                split_text = re.split(r'[=<>!]+', cond)
                # logger.log("Operators found:", operators)
                # logger.log("Split text:", split_text)

                if not operators:
                    raise Exception(f"No valid operator selected in : {cond}")
                
                field_value_parts = split_text
                field_part = field_value_parts[0].strip()
                value = field_value_parts[1].strip().replace("''", "").replace("'", "")

                logger.log(f"field_part ::: {field_part}")
                if '.' in field_part:
                    _, field_name = field_part.split('.')
                else:
                    field_name = field_part
                logger.log(f"field_name ::: {field_name}")
                dbtable, dbname, name, coltype = self.get_column_details(_.upper(), field_name.upper().replace(" ", "_"))
                logger.log(f"dbtable::  {dbtable}")
                logger.log(f"dbname::  {dbname}")
                logger.log(f"name :: {name}")

                rule = {
                    "id": f"Criteria_{idx}",
                    "customValue": "FixedValue",
                    "field": f"{dbtable}.{dbname}",
                    "COLTYPE": "string" if coltype.upper() in ["VARCHAR2", "CHAR", "NUMBREAKAGE_RETURN_QTYBER"] else "date" if coltype.upper() in ["DATE"] else "number",
                    "DBNAME": dbname,
                    "tableName": dbtable,
                    "queryOption": "F",
                    "operator": operators[0],
                    "currentFieldType": "string" if coltype.upper() in ["VARCHAR2", "CHAR", "NUMBREAKAGE_RETURN_QTYBER"] else "date" if coltype.upper() in ["DATE"] else "number",
                    "promptLabel": self.format_name(name).title(),
                    "chipValue": [],
                    "prevOption": "",
                    "columnTableName": "",
                    "columnDBNAME": "",
                    "value": int(value) if coltype.lower() == 'number' else value
                }
                rules.append(rule)
        except IndexError as e:
            logger.log(f"Error processing condition: {e}")

        result = {"query": {"rules": rules}}
        if condition_operator:
            result["query"]["condition"] = condition_operator

        return result

    def generate_sql_model(self):
        schema_name = self.visual_json.get("Schema_Name", "")
        visual_name = self.visual_json.get("Visual_Name", "")

        output = {
            "SQLModel": {
                "COLUMNS": [
                    {
                        "COLUMN": self.generate_sqlmodel_columns()
                    }
                ]
            },
            "CRITERIA": self.generate_criteria(),
            "VISUAL_NAME": 'Line' if visual_name == 'Scatter' else visual_name,
            "SCHEMA_NAME": schema_name,
            "SCHEMA_DESCR": self.format_name(schema_name),
            "SCHEMA_TYPE": "S",
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
        return ' '.join([word.capitalize() for word in name.split('_')])