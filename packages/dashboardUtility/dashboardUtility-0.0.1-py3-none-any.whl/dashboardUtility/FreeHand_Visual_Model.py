import json
import xml.etree.ElementTree as ET
import loggerutility as logger

class FreeHand_Visual_Model:
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

    def create_layout_data(self, input_data, visual_model):
        mapping = {}

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
                    "rows": [],
                    "columns": [{"uniqueName": "[Measures]"}] if visual_model.get("ID", "charts") != 'grid' else [],
                    "measures": []
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
        
        logger.log(f"""value :: {'chart' if visual_model.get("ID", "charts") in ['column', 'pie'] else 'charts' if visual_model.get("ID", "charts") not in ['grid','pivot'] else 'grid'}""")
        if visual_model.get("ID", "charts") != 'grid':
            if visual_model.get("ID", "charts") == 'pivot':            
                layout_data["layoutdata"]["options"]["showAggregationLabels"] = False
                layout_data["layoutdata"]["options"]['chart' if visual_model.get("ID", "charts") in ['column', 'pie'] else 'charts' if visual_model.get("ID", "charts") not in ['grid','pivot'] else 'grid']["showDataLabels"] = False
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
            if group_name.lower() == 'columns' or icon.lower() != 'grid':
                if columns or visual_json.get("Schema_Name").lower() == 'freehandsql':
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
                        "COLUMNS": []
                    }
                    visual_model["visualLayout"]["ColumnGroups"].append(group_data)

        layout_data = self.create_layout_data(visual_json, visual_model_copy)
        visual_model.update({"layoutdata": layout_data["layoutdata"]})
        
        visual_model.update({"moreOptions": {"toolbar": False}})
        return visual_model