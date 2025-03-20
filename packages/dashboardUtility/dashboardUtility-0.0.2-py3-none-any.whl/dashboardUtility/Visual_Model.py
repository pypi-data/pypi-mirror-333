import json
import xml.etree.ElementTree as ET
import loggerutility as logger

class Visual_Model:
    def __init__(self, schema_xml_file_path):
        self.schema_xml_data = self._read_xml_file(schema_xml_file_path)

    def _read_xml_file(self, file_path):
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            columns_mapping = {}

            for column in root.findall('.//COLUMN'):
                name = column.attrib.get('NAME')
                if name and name not in columns_mapping:
                    column_data = column.attrib.copy()
                    column_data['TEXT'] = column.text.strip() if column.text else ""
                    columns_mapping[name] = column_data
            return columns_mapping
        except Exception as e:
            raise RuntimeError(f"Failed to read XML file: {e}")

    def load_visuals_json(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                visuals = data.get("Visuals", [])
                return visuals
        except Exception as e:
            raise RuntimeError(f"Failed to load visuals from file: {e}")

    def create_column_data(self, group_name, columns):
        column_list = []
        logger.log(f"group_name:: {group_name}")
        for idx, column in enumerate(columns, start=1):
            col_data = self.schema_xml_data.get(column, {})

            dbsize = col_data.get("DBSIZE", "")
            if isinstance(dbsize, str) and dbsize.isdigit():
                dbsize = int(dbsize)
            col_type = col_data.get("JAVATYPE", "java.lang.String")

            column_metadata = {
                "ITALIC": int(col_data.get("ITALIC", 0)),
                "BGCOLOR": col_data.get("BGCOLOR", ""),
                "EXPRESSIONTYPE": col_data.get("EXPRESSIONTYPE", "C"),
                "WIDTH": int(col_data.get("WIDTH", 100)),
                "HIDDEN": col_data.get("HIDDEN", ""),
                "DBSIZE": dbsize,
                "UNDERLINE": int(col_data.get("UNDERLINE", 0)),
                "COLID": int(col_data.get("COLID", idx)),
                "FONT": col_data.get("FONT", "TIMES NEW ROMAN"),
                "content": col_data.get("TEXT", ""),
                "NAME": column,
                "NATIVETYPE": col_data.get("NATIVETYPE", "AN"),
                "FONTSIZE": int(col_data.get("FONTSIZE", 12)),
                "FGCOLOR": col_data.get("FGCOLOR", "#000000"),
                "JAVATYPE": col_type,
                "ALIGNMENT": int(col_data.get("ALIGNMENT", 1)),
                "DBTABLE": col_data.get("DBTABLE", ""),
                "DBNAME": col_data.get("DBNAME", ""),
                "BOLD": int(col_data.get("BOLD", 0)),
                "DEFAULTFUNCTION": col_data.get("DEFAULTFUNCTION", ""),
                "COLTYPE": col_data.get("COLTYPE", "CHAR"),
                "KEY": col_data.get("KEY", "false").lower() == "true",
                "CAPS": col_data.get("CAPS", "false").lower() == "true",
                "FEILD_TYPE": "TEXTBOX",
                "value": "",
                "name": col_data.get("TEXT", ""),
                "type": "string" if col_data.get("COLTYPE", "") in ["VARCHAR2", "CHAR", "NUMBREAKAGE_RETURN_QTYBER"] else "date" if col_data.get("COLTYPE", "") in ["DATE"] else "number",
                "descr": f'{col_data.get("TEXT", "")} description',
                "expression": "",
                "tableName": col_data.get("DBTABLE", ""),
                "tableDisplayName": col_data.get("DBTABLE", "").title(),
                "FUNCTION": col_data.get("DEFAULTFUNCTION", ""),
                "ADV_FORMAT": "",
                "alignment": "",
                "groupName": group_name,
                "checked": True,
                "StandardName": group_name
            }

            if col_data.get("COLTYPE", "") in ["DATE"]:
                column_metadata["PATTERN"] = "dd-MMM-yy"
                
            column_list.append(column_metadata)
        return column_list

    def create_layout_data(self, input_data, visual_model):
        mapping = {}
        for group, columns in input_data.get("Groups", {}).items():
            for column in columns:
                column_lower = column.lower()
                col_data = self.schema_xml_data.get(column, {})
                col_type = col_data.get("JAVATYPE", "java.lang.String")
                content = col_data.get("TEXT", "")

                mapping[column_lower] = {
                    "type": None if col_data.get("COLTYPE", "") in ["VARCHAR2", "CHAR", "NUMBREAKAGE_RETURN_QTYBER"] else "date string" if col_data.get("COLTYPE", "") in ["DATE"] else "number",
                    "caption": content
                }

                if col_data.get("COLTYPE", "") in ["DATE"]:
                    mapping[column_lower]["format"] = "dd-MMM-yy"
                
                if mapping[column_lower]["type"] is None:
                    del mapping[column_lower]["type"]

        values = None
        layout_data = {
            "layoutdata": {
                "dataSource": {
                    "reportName": "data_model_explore",
                    "data": "",
                    "mapping": mapping,
                    "dataSourceType": "json",
                    "filename": values
                },
                "options": {
                    "viewType": 'charts' if visual_model.get("ID", "charts") not in ['grid','pivot'] else 'grid',
                    'chart' if visual_model.get("ID", "charts") in ['column', 'pie'] else 'charts' if visual_model.get("ID", "charts") not in ['grid','pivot'] else 'grid': {
                        "type": "bar_h" if input_data.get("Visual_Name", "column").lower() == 'bar' else 'compact' if input_data.get("Visual_Name", "column").lower() == 'pivot' else input_data.get("Visual_Name", "column").lower() if input_data.get("Visual_Name", "column").lower() != 'grid' else 'flat',
                        "showGrandTotals": "off" if input_data.get("Visual_Name", "column").lower() == 'pivot' else "off",
                        "showTotals": "on" if input_data.get("Visual_Name", "column").lower() == 'pivot' else "off",
                        "showFilter": False,
                        "multipleMeasures": True
                    },
                    "configuratorButton": False
                },
                "slice": {
                    "rows": [{"uniqueName": col.lower()} for col in input_data.get("Groups", {}).get("Rows", [])],
                    "columns": [{"uniqueName": col.lower()} for col in input_data.get("Groups", {}).get("Columns", [])] + 
                              [{"uniqueName": "[Measures]"}] if visual_model.get("ID", "charts") != 'grid' 
                              else [{"uniqueName": col.upper(),
                                     "caption": " ".join([i.title() for i in col.split("_")])} for col in input_data.get("Groups", {}).get("Columns", [])],
                    "measures": [
                        {
                            "uniqueName": measure.lower(),
                            "aggregation": "SUM" if self.schema_xml_data.get(measure, {}).get("JAVATYPE", "java.lang.String") != "java.lang.String" else "",
                            "format": measure.lower()
                        }
                        for measure in input_data.get("Groups", {}).get("Values", [])
                    ] 
                    if visual_model.get("ID", "charts") != 'grid' 
                    else [
                        {
                            "uniqueName": col.lower(),
                            "aggregation": "SUM" if self.schema_xml_data.get(col, {}).get("COLTYPE", "") in ["NUMBER", "NUMBREAKAGE_RETURN_QTYBER"] else "",
                            **(
                                {"format": col.lower()} if self.schema_xml_data.get(col, {}).get("COLTYPE", "") == "NUMBER" else {}
                            )
                        }
                        for col in input_data.get("Groups", {}).get("Columns", [])
                    ] + [
                        {
                            "uniqueName": col.upper(),
                            "aggFunction": ""
                        }
                        for col in input_data.get("Groups", {}).get("Columns", [])
                    ]
                },
                "formats": [{
                    "name": "",
                    "decimalPlaces": 3,
                    "maxDecimalPlaces": 3,
                    "decimalSeparator": "."
                }]
            }
        }

        if visual_model.get("ID", "charts") in ['grid','pivot']:
            layout_data["layoutdata"]["localization"] = {
                "grid": {
                    "blankMember": "",
                    "dateInvalidCaption": ""
                }
            }
        
        logger.log(f"""value :: {'chart' if visual_model.get("ID", "chart") != 'grid' else 'grid'}""")
        if visual_model.get("ID", "charts") != 'grid':
            if visual_model.get("ID", "charts") == 'pivot':            
                layout_data["layoutdata"]["options"]["showAggregationLabels"] = False
            else:
                layout_data["layoutdata"]["options"]["showAggregationLabels"] = False
                layout_data["layoutdata"]["options"]['chart' if visual_model.get("ID", "charts") in ['column', 'pie'] else 'charts' if visual_model.get("ID", "charts") not in ['grid','pivot'] else 'grid']["showMeasures"] = False
        else:
            layout_data["layoutdata"]["options"]['chart' if visual_model.get("ID", "charts") in ['column', 'pie'] else 'charts' if visual_model.get("ID", "charts") not in ['grid','pivot'] else 'grid']["showHeaders"] = True
                    
        return layout_data

    def generate_visual_model(self, visual_json, visual_json_list):
        visual_name = visual_json.get("Visual_Name", "Column")
        selected_visual_json = next((v for v in visual_json_list if v.get("VisualName") == visual_name), None)
        visual_model_copy = selected_visual_json

        if not selected_visual_json:
            raise ValueError(f"Data for {visual_name} is not found in file.")

        visual_model = {
            "visualLayout": {
                "ID": selected_visual_json.get("ID", "").lower(),
                "VisualName": selected_visual_json.get("VisualName"),
                "VisualType": selected_visual_json.get("VisualType"),
                "DisplayOrder": selected_visual_json.get("DisplayOrder"),
                "VisualIcon": selected_visual_json.get("VisualIcon"),
                "className": selected_visual_json.get("className"),
                "OutputType": selected_visual_json.get("OutputType"),
                "options": selected_visual_json.get("options", []),
                "ColumnGroups": []
            }
        }

        if visual_model.get("visualLayout").get("VisualName") in ['Column']:
            visual_model["visualLayout"]["linkOptions"] = visual_model.get("linkOptions", "")

        for group_name, columns in visual_json.get("Groups", {}).items():
            icon = visual_json.get("Visual_Name", "")
            if columns:
                logger.log(f"columns::  {columns}")

                group_data = {
                    "GroupID": len(visual_model["visualLayout"]["ColumnGroups"]) + 1,
                    "GroupName": group_name,
                    "GroupDescription": f"GroupDescription{len(visual_model['visualLayout']['ColumnGroups']) + 1}",
                    "GroupIcon": f"{icon}.svg",
                    "AllowedColumnTypes": "ANY",
                    "MinColumns": 0,
                    "MaxColumns": 0,
                    "StandardName": group_name,
                    "COLUMNS": self.create_column_data(group_name, columns)
                }
                visual_model["visualLayout"]["ColumnGroups"].append(group_data)

        layout_data = self.create_layout_data(visual_json, visual_model_copy)
        visual_model.update({"layoutdata": layout_data["layoutdata"]})
        
        visual_model.update({"moreOptions": {"toolbar": False}})
        return visual_model