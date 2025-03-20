import json
import xml.etree.ElementTree as ET
import os
from typing import List, Dict
import json
import logging
from typing import List, Dict
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
import loggerutility as logger

from datetime import datetime

class ITMException(Exception):
    pass

class E12GenericUtility:
    @staticmethod
    def check_null(value):
        return "" if value is None else str(value)

    @staticmethod
    def get_stack_trace(exception):
        return str(exception)

class Source_SQL:
    def __init__(self):
        self.from_table_names: List[str] = []
        self.joins_table_names: List[str] = []
        self.function_list: List[str] = []
        self.selected_column_list: List[str] = []
        self.aggr_function: List[str] = []
        self.non_aggr_function: List[str] = []
        self.is_aggregate_func = False
        self.foreign_key_tables: List[str] = []
        self.main_table_name = ""

    def set_from_table_names(self, names: List[str]) -> None:
        """Set from table names."""
        self.from_table_names = names

    def get_from_table_names(self) -> List[str]:
        """Get from table names."""
        return self.from_table_names
    
    def is_object_function(self, hr_master_json, user_info):
        try:
            # logger.log(f"QueryBuilder.is_object() hr_master_json: {type(hr_master_json)}")
            join_predicates_json = hr_master_json.get("JOIN_PREDICATES")
            if isinstance(join_predicates_json, dict):  
                return True
            
            return False
        except Exception as e:
            # logger.log(f"QueryBuilder.is_object() Exception: {str(e)}")
            return True  
        
    def remove_at_from_keys(self, data):
        if isinstance(data, dict):
            return {
                key.lstrip('@#'): self.remove_at_from_keys(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.remove_at_from_keys(item) for item in data]
        else:
            return data

    def build_form_table_names_array(self, columns_array: List, user_info) -> None:
        """Build form table names array from JSON columns array."""
        table_name_array_list = []
        try:
            for column_obj in columns_array:
                selected_column_array = column_obj.get("COLUMN", [])
                for column in selected_column_array:
                    table_name = column.get("DBTABLE")
                    if table_name not in table_name_array_list:
                        table_name_array_list.append(table_name)
            
            self.set_from_table_names(table_name_array_list)
        except Exception as e:
            logging.error(f"Exception in build_select_part: {str(e)}")
            raise Exception(e)
        
    def _xml_to_json(self, xml_string):
        def parse_element(element):

            parsed = {}
            # Include element attributes
            if element.attrib:
                parsed.update({"@attributes": element.attrib})
            
            # Include child elements
            for child in element:
                child_parsed = parse_element(child)
                tag = child.tag
                if tag in parsed:
                    # Convert to list if multiple elements with the same tag
                    if not isinstance(parsed[tag], list):
                        parsed[tag] = [parsed[tag]]
                    parsed[tag].append(child_parsed)
                else:
                    parsed[tag] = child_parsed
            
            # Include text content
            if element.text and element.text.strip():
                text = element.text.strip()
                if parsed:
                    parsed["text"] = text
                else:
                    parsed = text
            
            return parsed

        try:
            root = ET.fromstring(xml_string)
            # Convert the parsed XML to JSON
            json_data = {root.tag: parse_element(root)}
            return json_data
        except ET.ParseError as e:
            return json.dumps({"error": str(e)})
          
    def _build_select_part(self, columns_array: List[dict], user_info: dict) -> str:
        select_parts = []
        
        for column_group in columns_array:
            for column in column_group.get("COLUMN", []):
                # logger.log(f"column ::: {column.get('COLUMN_TYPE')}")
                if 'COLUMN_TYPE' in column or 'COLTYPE' in column:
                    if column.get("COLUMN_TYPE") != "calc_column" or column.get("COLTYPE") != "calc_column":
                        expr_name = column.get("expression", "")
                        col_name = column.get("DBNAME")
                        table_name = column.get("DBTABLE")
                        function_name = column.get("FUNCTION", "")
                        as_name = column.get("NAME")

                        expression_value = self.expression_for_column(
                            table_name, col_name, expr_name, function_name, True)
                        
                        select_column = f"{expression_value} AS {as_name}"
                        select_parts.append(select_column)

                        if not function_name:
                            self.selected_column_list.append(f"{table_name}.{col_name}")

                        # logger.log(f"function_name ::: {function_name}")
                        # logger.log(f"selected_column_list ::: {self.selected_column_list}")
                        # logger.log(f"aggr_function ::: {self.aggr_function}")
                        if function_name in self.aggr_function:
                            self.is_aggregate_func = True

        return "SELECT " + ", ".join(select_parts)
    
    def build_from_part(self, columns_array, database_schema_name, schema_xml, user_info):
        from_part = None
        from_part_buff = []
        table_name_array_list = []
        
        try:

            all_table_data_configuration = {}
            schema_json = self._xml_to_json(schema_xml)
            hr_master_json = schema_json.get("HR_Master")
            is_object = self.is_object_function(hr_master_json, user_info)
            # logger.log(f"is_object ::: {is_object}")
            # logger.log(f"JOIN_PREDICATES ::: {'JOIN_PREDICATES' in hr_master_json}")

            if "JOIN_PREDICATES" in hr_master_json and is_object:
                join_predicate_json = hr_master_json["JOIN_PREDICATES"]
                json_array = []
                
                if isinstance(join_predicate_json.get("JOIN"), list):
                    json_array = join_predicate_json["JOIN"]
                elif isinstance(join_predicate_json.get("JOIN"), dict):
                    json_array.append(join_predicate_json["JOIN"])

                primary_key_value = ""
                previous_from_condition = ""
                
                for i in range(len(json_array)):
                    current_json = json_array[i]
                    current_json = self.remove_at_from_keys(current_json)
                    logger.log(f"current_json  after::: {current_json}")
                    id = ""
                    if "attributes" in current_json and "ID" in current_json["attributes"]:
                        id = current_json["attributes"]["ID"]
                    is_main_table = ""
                    if "attributes" in current_json and "MAIN_TABLE" in current_json["attributes"]:
                        is_main_table = current_json["attributes"]["MAIN_TABLE"]

                    if is_main_table.lower() == "yes":
                        main_table_name = id
                        foreign_key_array = current_json.get("FOREIGN_KEY", None)
                        primary_key_json = current_json["PRIMARY_KEY"]
                        # logger.log(f"primary_key_json ::: {primary_key_json}")
                        if "attributes" in primary_key_json and "text" in primary_key_json["attributes"]:
                            primary_key_value = primary_key_json["attributes"]["text"]
                        
                        if foreign_key_array:
                            # logger.log(f"foreign_key_array ::: {foreign_key_array}")
                            for j in range(len(foreign_key_array)):
                                foreign_key_json = foreign_key_array[j]
                                key_column = foreign_key_json["KEY_COLUMN"]
                                # logger.log(f"key_column ::: {key_column}")
                                join_table_name = ""
                                if "attributes" in foreign_key_json and "TABLE" in foreign_key_json["attributes"]:
                                    join_table_name = foreign_key_json["attributes"]["TABLE"]
                                if "text" in key_column:
                                    all_table_data_configuration[join_table_name] = key_column["text"]
                                # logger.log(f"all_table_data_configuration ::: {all_table_data_configuration}")
                                if join_table_name in self.from_table_names:
                                    logger.log(f"join_table_name ::: {join_table_name}")
                                    current_from_condition = ""
                                    join_type_val = ""
                                    join_type_name = " JOIN "
                                    logger.log(f"Line no ::: 216")
                                    logger.log(f"foreign_key_json ::: {foreign_key_json}")
                                    if "JOIN_TYPE" in foreign_key_json:
                                        join_type_val = E12GenericUtility.checkNull(foreign_key_json["JOIN_TYPE"])
                                        join_type_val = join_type_val.upper()
                                        if join_type_val == "EQUALS":
                                            join_type_name = " JOIN "
                                            logger.log(f"Line no ::: 223")
                                        if "_" in join_type_val:
                                            join_type_name = f" {join_type_val.replace('_', ' ')} JOIN "
                                    
                                    if main_table_name in self.from_table_names:
                                        logger.log(f"main_table_name ::: {main_table_name}")
                                        if database_schema_name != "":
                                            if previous_from_condition == "" or (previous_from_condition != "" and '"' + database_schema_name + '"' + "." + id not in previous_from_condition and '"' + database_schema_name + '"' + "." + join_table_name not in previous_from_condition):
                                                current_from_condition = f'"{database_schema_name}"."{id}" {join_type_name} "{database_schema_name}"."{join_table_name}" ON {id}.{key_column["content"]} = {join_table_name}.{key_column["content"]}\n'
                                            if previous_from_condition != "" and '"' + database_schema_name + '"' + "." + id not in previous_from_condition and '"' + database_schema_name + '"' + "." + join_table_name in previous_from_condition:
                                                current_from_condition = f"{join_type_name}\"{database_schema_name}\".\"{id}\" ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                            if previous_from_condition != "" and '"' + database_schema_name + '"' + "." + id in previous_from_condition and '"' + database_schema_name + '"' + "." + join_table_name not in previous_from_condition:
                                                current_from_condition = f"{join_type_name}\"{database_schema_name}\".\"{join_table_name}\" ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                            previous_from_condition += f" {current_from_condition}"
                                        else:
                                            if previous_from_condition == "" or (previous_from_condition != "" and id not in previous_from_condition and join_table_name not in previous_from_condition):
                                                current_from_condition = f"{id} {join_type_name} {join_table_name} ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                            if previous_from_condition != "" and id not in previous_from_condition and join_table_name in previous_from_condition:
                                                current_from_condition = f"{join_type_name}{id} ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                            if previous_from_condition != "" and id in previous_from_condition and join_table_name not in previous_from_condition:
                                                current_from_condition = f"{join_type_name}{join_table_name} ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                            previous_from_condition += f" {current_from_condition}"
                                        self.joins_table_names.append(id)
                                        self.joins_table_names.append(join_table_name)
                                    logger.log(f"current_from_condition ::: {current_from_condition}")
                                    from_part_buff.append(current_from_condition)
                        elif foreign_key_array is None:
                            foreign_key_json = current_json["FOREIGN_KEY"]
                            logger.log(f"foreign_key_json ::: {foreign_key_json}")
                            if foreign_key_json is not None:
                                key_column = foreign_key_json["KEY_COLUMN"]
                                join_table_name = foreign_key_json["TABLE"]
                                logger.log(f"join_table_name ::: {join_table_name}")
                                all_table_data_configuration[join_table_name] = key_column["content"]
                                if join_table_name in self.from_table_names:
                                    join_type_val = ""
                                    join_type_name = " JOIN "
                                    logger.log(f"Line no ::: 258")
                                    logger.log(f"JOIN_TYPE ::: {'JOIN_TYPE' in foreign_key_json}")
                                    if "JOIN_TYPE" in foreign_key_json:
                                        join_type_val = E12GenericUtility.checkNull(foreign_key_json["JOIN_TYPE"])
                                        join_type_val = join_type_val.upper()
                                        if join_type_val == "EQUALS":
                                            join_type_name = " JOIN "
                                            logger.log(f"Line no ::: 265")
                                        if "_" in join_type_val:
                                            join_type_name = f" {join_type_val.replace('_', ' ')} JOIN "
                                    
                                    current_from_condition = ""
                                    if database_schema_name != "":
                                        if previous_from_condition == "" or (previous_from_condition != "" and '"' + database_schema_name + '"' + "." + id not in previous_from_condition and '"' + database_schema_name + '"' + "." + join_table_name not in previous_from_condition):
                                            current_from_condition = f'"{database_schema_name}"."{id}" {join_type_name} "{database_schema_name}"."{join_table_name}" ON {id}.{key_column["content"]} = {join_table_name}.{key_column["content"]}, \n'
                                        if previous_from_condition != "" and '"' + database_schema_name + '"' + "." + id not in previous_from_condition and '"' + database_schema_name + '"' + "." + join_table_name in previous_from_condition:
                                            current_from_condition = f"{join_type_name}\"{database_schema_name}\".\"{id}\" ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                        if previous_from_condition != "" and '"' + database_schema_name + '"' + "." + id in previous_from_condition and '"' + database_schema_name + '"' + "." + join_table_name not in previous_from_condition:
                                            current_from_condition = f"{join_type_name}\"{database_schema_name}\".\"{join_table_name}\" ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                        previous_from_condition += f" {current_from_condition}"
                                    else:
                                        if previous_from_condition == "" or (previous_from_condition != "" and id not in previous_from_condition and join_table_name not in previous_from_condition):
                                            current_from_condition = f"{id} {join_type_name} {join_table_name} ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}, \n"
                                        if previous_from_condition != "" and id not in previous_from_condition and join_table_name in previous_from_condition:
                                            current_from_condition = f"{join_type_name}{id} ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                        if previous_from_condition != "" and id in previous_from_condition and join_table_name not in previous_from_condition:
                                            current_from_condition = f"{join_type_name}{join_table_name} ON {id}.{key_column['text']} = {join_table_name}.{key_column['text']}\n"
                                    previous_from_condition += f" {current_from_condition}"
                                    self.joins_table_names.append(id)
                                    self.joins_table_names.append(join_table_name)
                                    from_part_buff.append(current_from_condition)
                    else:
                        # logger.log(f"FOREIGN_KEY ::: {'FOREIGN_KEY' in current_json}")
                        if "FOREIGN_KEY" in current_json:
                            primaryKeyJson = current_json.get("PRIMARY_KEY")
                            foreignKeyJson = current_json.get("FOREIGN_KEY")
                            keyColumn = foreignKeyJson.get("KEY_COLUMN","")
                            foreignKeyTable = foreignKeyJson.get("attributes").get("TABLE")
                            logger.log(f'primaryKeyJson ::: {primaryKeyJson}')
                            logger.log(f'foreignKeyTable ::: {foreignKeyTable}')
                            logger.log(f'id ::: {id}')
                            logger.log(f'from_table_names ::: {self.from_table_names}')
                            logger.log(f'---------------------------------------------------------')
                            
                            if id in self.from_table_names:
                                joinTypeVal = ""
                                joinTypeName = " JOIN "
                                logger.log(f"Line no ::: 302")
                                logger.log(f"JOIN_TYPE ::: {'JOIN_TYPE' in foreignKeyJson}")
                                if "JOIN_TYPE" in foreignKeyJson:
                                    joinTypeVal = E12GenericUtility.checkNull(foreignKeyJson.get("JOIN_TYPE"))
                                    joinTypeVal = joinTypeVal.upper()
                                    if joinTypeVal == "EQUALS":
                                        joinTypeName = " JOIN "
                                        logger.log(f"Line no ::: 309")
                                    if "_" in joinTypeVal:
                                        joinTypeName = " " + joinTypeVal.replace("_", " ") + " JOIN "
                                        logger.log(f"Line no ::: 312")
                                
                                currentFromcondition = ""
                                if foreignKeyTable in all_table_data_configuration and main_table_name in self.from_table_names:
                                    if database_schema_name != "":
                                        if previous_from_condition == "" or (previous_from_condition != "" and database_schema_name + '.' + main_table_name not in previous_from_condition and database_schema_name + '.' + foreignKeyTable not in previous_from_condition):
                                            currentFromcondition = '"' + database_schema_name + '"' + "." + main_table_name + joinTypeName + '"' + database_schema_name + '"' + "." + foreignKeyTable + " ON " + main_table_name + "." + all_table_data_configuration[foreignKeyTable] + "=" + foreignKeyTable + "." + all_table_data_configuration[foreignKeyTable] + "\n"
                                        elif previous_from_condition != "" and database_schema_name + '.' + main_table_name not in previous_from_condition and database_schema_name + '.' + foreignKeyTable in previous_from_condition:
                                            currentFromcondition = joinTypeName + '"' + database_schema_name + '"' + "." + main_table_name + " ON " + main_table_name + "." + all_table_data_configuration[foreignKeyTable] + "=" + foreignKeyTable + "." + all_table_data_configuration[foreignKeyTable] + "\n"
                                        elif previous_from_condition != "" and database_schema_name + '.' + main_table_name in previous_from_condition and database_schema_name + '.' + foreignKeyTable not in previous_from_condition:
                                            currentFromcondition = joinTypeName + '"' + database_schema_name + '"' + "." + foreignKeyTable + " ON " + main_table_name + "." + all_table_data_configuration[foreignKeyTable] + "=" + foreignKeyTable + "." + all_table_data_configuration[foreignKeyTable] + "\n"
                                        previous_from_condition += " " + currentFromcondition
                                    else:
                                        if previous_from_condition == "" or (previous_from_condition != "" and main_table_name not in previous_from_condition and foreignKeyTable not in previous_from_condition):
                                            currentFromcondition = main_table_name + joinTypeName + foreignKeyTable + " ON " + main_table_name + "." + all_table_data_configuration[foreignKeyTable] + "=" + foreignKeyTable + "." + all_table_data_configuration[foreignKeyTable] + "\n"
                                        elif previous_from_condition != "" and main_table_name not in previous_from_condition and foreignKeyTable in previous_from_condition:
                                            currentFromcondition = joinTypeName + main_table_name + " ON " + main_table_name + "." + all_table_data_configuration[foreignKeyTable] + "=" + foreignKeyTable + "." + all_table_data_configuration[foreignKeyTable] + "\n"
                                        elif previous_from_condition != "" and main_table_name in previous_from_condition and foreignKeyTable not in previous_from_condition:
                                            currentFromcondition = joinTypeName + foreignKeyTable + " ON " + main_table_name + "." + all_table_data_configuration[foreignKeyTable] + "=" + foreignKeyTable + "." + all_table_data_configuration[foreignKeyTable] + "\n"
                                        previous_from_condition += " " + currentFromcondition

                                    self.joins_table_names.append(main_table_name)
                                    self.joins_table_names.append(foreignKeyTable)

                                currentFromcondition1 = ""
                                if database_schema_name != "":
                                    if previous_from_condition == "" or (previous_from_condition != "" and database_schema_name + '.' + id not in previous_from_condition and database_schema_name + '.' + foreignKeyTable not in previous_from_condition):
                                        currentFromcondition1 = '"' + database_schema_name + '"' + "." + id + joinTypeName + '"' + database_schema_name + '"' + "." + foreignKeyTable + " ON " + id + "." + primaryKeyJson.get("text") + "=" + foreignKeyTable + "." + keyColumn.get("text") + "\n"
                                    elif previous_from_condition != "" and database_schema_name + '.' + id not in previous_from_condition and database_schema_name + '.' + foreignKeyTable in previous_from_condition:
                                        currentFromcondition1 = joinTypeName + '"' + database_schema_name + '"' + "." + id + " ON " + id + "." + primaryKeyJson.get("text") + "=" + foreignKeyTable + "." + keyColumn.get("text") + "\n"
                                    elif previous_from_condition != "" and database_schema_name + '.' + id in previous_from_condition and database_schema_name + '.' + foreignKeyTable not in previous_from_condition:
                                        currentFromcondition1 = joinTypeName + '"' + database_schema_name + '"' + "." + foreignKeyTable + " ON " + id + "." + primaryKeyJson.get("text") + "=" + foreignKeyTable + "." + keyColumn.get("text") + "\n"
                                    previous_from_condition += " " + currentFromcondition1
                                else:
                                    if previous_from_condition == "" or (previous_from_condition != "" and id not in previous_from_condition and foreignKeyTable not in previous_from_condition):
                                        currentFromcondition1 = id + joinTypeName + foreignKeyTable + " ON " + id + "." + primaryKeyJson.get("text") + "=" + foreignKeyTable + "." + keyColumn.get("text") + "\n"
                                    elif previous_from_condition != "" and id not in previous_from_condition and foreignKeyTable in previous_from_condition:
                                        currentFromcondition1 = joinTypeName + id + " ON " + id + "." + primaryKeyJson.get("text") + "=" + foreignKeyTable + "." + keyColumn.get("text") + "\n"
                                    elif previous_from_condition != "" and id in previous_from_condition and foreignKeyTable not in previous_from_condition:
                                        currentFromcondition1 = joinTypeName + foreignKeyTable + " ON " + id + "." + primaryKeyJson.get("text") + "=" + foreignKeyTable + "." + keyColumn.get("text") + "\n"
                                    previous_from_condition += " " + currentFromcondition1

                                self.joins_table_names.append(id)
                                self.joins_table_names.append(foreignKeyTable)

                                checConditon = currentFromcondition1
                                if "and" in checConditon:
                                    checConditon = checConditon.replace("and", "")
                                    checConditon = checConditon.strip()

                                if checConditon not in from_part_buff:
                                    from_part_buff.append(currentFromcondition)

                                if currentFromcondition1.strip().endswith(joinTypeName):
                                    currentFromcondition1 = currentFromcondition1[:-1].strip()

                                from_part_buff.append(currentFromcondition1)
                                self.foreign_key_tables.append(foreignKeyTable)

            for i in range(len(columns_array)):
                json_object = columns_array[i]
                selected_column_array = json_object.get("COLUMN")
                for j in range(len(selected_column_array)):
                    column_json_object = selected_column_array[j]
                    col_type = ""

                    if "COLUMN_TYPE" in column_json_object or 'COLTYPE' in column_json_object:
                        col_type = column_json_object.get("COLUMN_TYPE") or column_json_object.get("COLTYPE")
                      
                    # logger.log(f"col_type ::: {col_type}")
                    if col_type.lower() != "calc_column":
                        table_name = column_json_object.get("DBTABLE")
                        if table_name not in table_name_array_list and table_name not in self.joins_table_names:
                            if len(from_part_buff) > 0:
                                last_char = from_part_buff[-1]
                                if last_char != ',':
                                    from_part_buff.append(", ")
                            if database_schema_name.strip() != "":
                                from_part_buff.append(f'"{database_schema_name}"."{table_name}", ')
                            else:
                                from_part_buff.append(f"{table_name}, ")
                            # logger.log(f"from_part_buff ::: {from_part_buff}")
                            table_name_array_list.append(table_name)
            
            if self.main_table_name not in self.joins_table_names:
                if self.main_table_name not in table_name_array_list and self.main_table_name != "":
                    if len(from_part_buff) > 0:
                        last_char = from_part_buff[-1]
                        if last_char != ',':
                            from_part_buff.append(", ")
                    if database_schema_name.strip() != "":
                        from_part_buff.append(f'"{database_schema_name}"."{self.main_table_name}", ')
                    else:
                        from_part_buff.append(f"{self.main_table_name}, ")
                    # logger.log(f"from_part_buff ::: {from_part_buff}")
                    table_name_array_list.append(self.main_table_name)
            
            # logger.log(f"from_part_buff ::: {from_part_buff}")
        
        except Exception as e:
            logger.log(f"Exception ::: {e}")
            raise ITMException(e)
        
        from_part = " FROM " + "".join(from_part_buff).strip()
        if from_part.endswith(","):
            from_part = from_part[:-1]
        
        return from_part

    def expression_for_column(self, table_name, col_name, expr_name, col_function, is_select_part):
        expression_value = ""
        if is_select_part:
            if not expr_name:
                if not col_function:
                    expression_value = f"{table_name}.{col_name}"
                else:
                    expression_value = f"{col_function}({table_name}.{col_name})"
            else:
                if not col_function:
                    expression_value = expr_name
                elif col_function and f"{col_function}(" in expr_name:
                    expression_value = expr_name
                    # Log statement can be added if necessary
                else:
                    expression_value = f"{col_function}({expr_name})"
        else:
            if not expr_name:
                expression_value = f"{table_name}.{col_name}"
            else:
                expression_value = expr_name

        return expression_value
        
    def build_where_part_conditions(self, where_part_buff, query_json_obj, main_condition, user_info, columns_array):
        try:
            rules_array = query_json_obj.get("rules", [])
            rule_set_condition = ""
            
            for i in range(len(rules_array)):
                column_json_object = rules_array[i]
                if "condition" in column_json_object:
                    rule_set_condition = column_json_object.get("condition", "")
                    rule_set_condition = " " + rule_set_condition + " "
                    if i == 0:
                        where_part_buff.append(" ( ")
                    else:
                        where_part_buff.append(" " + main_condition + " ( ")
                    
                    self.build_where_part_conditions(where_part_buff, column_json_object, rule_set_condition, user_info, columns_array)
                    where_part_buff.append(" ) ")
                else:
                    col_name = column_json_object.get("DBNAME", "")
                    table_name = column_json_object.get("tableName", "")
                    operator = column_json_object.get("operator", "")
                    where_str = where_part_buff[-1] if where_part_buff else ""
                    query_option = column_json_object.get("queryOption", "")
                    column_type = column_json_object.get("COLTYPE", "") or column_json_object.get("COLUMN_TYPE")
                    prompt_label = column_json_object.get("promptLabel", "")
                    value = ""
                    chip_value_arr = column_json_object.get("chipValue", [])
                    chip_value_a = []
                    custom_value = column_json_object.get("customValue", "")
                    column_name = ""
                    column_table = ""
                    expr_name = ""
                    col_function = ""

                    for column in columns_array:
                        selected_column_array = column.get("COLUMN", [])
                        for col_json_object in selected_column_array:
                            column_name = col_json_object.get("NAME", "")
                            column_table = col_json_object.get("DBTABLE", "")
                            if col_name.lower() == column_name.lower() and table_name.lower() == column_table.lower():
                                expr_name = col_json_object.get("expression", "")
                                col_function = col_json_object.get("FUNCTION", "")

                    if column_type.lower() == "number" and query_option.upper() != "P":
                        value = str(column_json_object.get("value", ""))
                    elif column_type.upper() in ["DATE", "DATETIME"] and query_option.upper() not in ["C", "P"]:
                        date_obj = datetime.strptime(column_json_object.get("value", ""), "%Y-%m-%dT%H:%M:%S.%fZ")
                        value = date_obj.strftime("%d-%b-%Y")
                    elif query_option.upper() != "P":
                        value = column_json_object.get("value", "")

                    if where_str and not where_str.endswith(" (") and i != 0:
                        if custom_value and custom_value != "FixedValue" and query_option.upper() == "F":
                            if operator.lower() in ["like", "in", "between"]:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} ?.@{custom_value} "
                                where_part_buff.append(where_column)
                            else:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value}{operator} ?.@{custom_value} "
                                where_part_buff.append(where_column)
                        elif query_option.upper() in ["F", "E"]:
                            if operator.lower() == "like":
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} '{value}'"
                                where_part_buff.append(where_column)
                            elif operator.lower() == "in":
                                final_chip_value = "','".join(chip_value_arr).strip()
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} ('{final_chip_value}')"
                                where_part_buff.append(where_column)
                            elif operator.lower() == "between":
                                from_value = chip_value_arr[0] if len(chip_value_arr) > 0 else ""
                                to_value = chip_value_arr[1] if len(chip_value_arr) > 1 else ""
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} '{from_value}' AND '{to_value}'"
                                where_part_buff.append(where_column)
                            else:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value}{operator}'{value}'"
                                where_part_buff.append(where_column)
                        elif query_option.upper() == "C":
                            expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                            where_column = f"{main_condition}{expression_value}{operator}{value}"
                            where_part_buff.append(where_column)
                        elif query_option.upper() == "P":
                            if operator.lower() in ["like", "in", "between"]:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} ?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(where_column)
                            else:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value}{operator} ?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(where_column)
                    else:
                        if custom_value.strip().lower() != "" and custom_value.lower() != "fixedvalue" and query_option.lower() == "f":
                            if operator.lower() in ["like", "in", "between"]:
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f" and {expressionValue} {operator} ?.@{custom_value} "
                                where_part_buff.append(whereColumn)
                            else:
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue}{operator} ?.@{custom_value} "
                                where_part_buff.append(whereColumn)
                        elif query_option.lower() == "f":
                            if operator.lower() == "like":
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} '{value}'"
                                where_part_buff.append(whereColumn)
                            elif operator.lower() == "in":
                                for k in range(len(chip_value_arr)):
                                    chip_value_a.append(f"{chip_value_arr[k]}','")
                                finalChipValue = chip_value_a.toString().strip()
                                if finalChipValue.endswith("','"):
                                    finalChipValue = finalChipValue[:-3]
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} ('{finalChipValue}')"
                                where_part_buff.append(whereColumn)
                            elif operator.lower() == "between":
                                toValue = []
                                fromValue = []
                                for k in range(len(chip_value_arr)):
                                    if k == 0:
                                        fromValue.append(chip_value_arr[k])
                                    elif k == 1:
                                        toValue.append(chip_value_arr[k])
                                        break
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} '{''.join(fromValue)}' AND '{''.join(toValue)}' "
                                where_part_buff.append(whereColumn)
                            else:
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue}{operator}'{value}'"
                                where_part_buff.append(whereColumn)
                        elif query_option.lower() == "c":
                            expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                            whereColumn = f"{expressionValue}{operator}{value}"
                            where_part_buff.append(whereColumn)
                        elif query_option.lower() == "p":
                            if operator.lower() in ["like", "in", "between"]:
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f" and {expressionValue} {operator} ?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(whereColumn)
                            else:
                                expressionValue = self.expressionForColumn(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue}{operator}?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(whereColumn)

                        
        except Exception as e:
            raise Exception(f"Exception in build_where_part: {str(e)}")
        
    def build_where_part(self, criteria_json_object, schema_xml, user_info, columns_array):
        where_part = ""
        where_part_buff = []

        try:
            query_json_obj = criteria_json_object["query"]
            rules_array = query_json_obj["rules"]
            main_condition = " and "
            if "condition" in query_json_obj:
                main_condition = query_json_obj["condition"]
                main_condition = f" {main_condition} "

            for i, column_json_object in enumerate(rules_array):
                logger.log(f'Condition ::: {"condition" in column_json_object}')
                if "condition" in column_json_object:
                    rule_set_condition = column_json_object["condition"]
                    rule_set_condition = f" {rule_set_condition} "
                    if i == 0 and not "".join(where_part_buff).strip():
                        where_part_buff.append(" ( ")
                    elif i == 0 and "".join(where_part_buff).strip():
                        where_part_buff.append(" AND ( ")
                    else:
                        where_part_buff.append(f" {main_condition} ( ")
                    self.build_where_part_conditions(where_part_buff, column_json_object, rule_set_condition, user_info, columns_array)
                    where_part_buff.append(" ) ")
                else:
                    col_name = column_json_object["DBNAME"]
                    table_name = column_json_object["tableName"]
                    operator = column_json_object["operator"]
                    query_option = column_json_object["queryOption"]
                    column_type = column_json_object["COLTYPE"] or column_json_object.get("COLUMN_TYPE")
                    where_str = "".join(where_part_buff)
                    value = ""
                    chip_value_arr = []
                    chip_value_a = []
                    chip_value_arr = column_json_object["chipValue"]
                    custom_value = column_json_object.get("customValue", "")
                    prompt_label = column_json_object.get("promptLabel", "")

                    column_name = ""
                    column_table = ""
                    expr_name = ""
                    col_function = ""

                    for json_object in columns_array:
                        selected_column_array = json_object["COLUMN"]
                        for col_json_object in selected_column_array:
                            if "NAME" in col_json_object:
                                column_name = col_json_object["NAME"]
                            if "DBTABLE" in col_json_object:
                                column_table = col_json_object["DBTABLE"]
                            if col_name.lower() == column_name.lower() and table_name.lower() == column_table.lower():
                                expr_name = col_json_object.get("expression", "")
                                col_function = col_json_object.get("FUNCTION", "")

                    # logger.log(f"column_name ::: {column_name}")
                    # logger.log(f"column_table ::: {column_table}")
                    # logger.log(f"expr_name ::: {expr_name}")
                    # logger.log(f"col_function ::: {col_function}")
                    if column_type.lower() == "number" and query_option.upper() != "P":
                        get_value = column_json_object.get("value", "")
                        if not get_value:
                            value = ""
                        else:
                            value = str(int(column_json_object["value"]))
                    elif column_type.upper() in ["DATE", "DATETIME"] and query_option.upper() not in ["C", "P"]:
                        date_obj = datetime.strptime(column_json_object["value"], "%Y-%m-%dT%H:%M:%S.%fZ")
                        value = date_obj.strftime("%d-%b-%Y")
                    elif query_option.upper() != "P":
                        value = column_json_object["value"]

                    logger.log(f"value ::: {value}")
                    logger.log(f"where_str ::: {where_str}")
                    if len(where_str) > 0 and not where_str.endswith(" ("):
                        if custom_value and custom_value.lower() != "fixedvalue" and query_option.upper() == "F":
                            if operator.lower() in ["like", "in", "between"]:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} ?.@{custom_value} "
                                where_part_buff.append(where_column)
                            else:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value}{operator} ?.@{custom_value} "
                                where_part_buff.append(where_column)
                        elif query_option.upper() in ["F", "E"]:
                            if operator.lower() == "like":
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} '{value}'"
                                where_part_buff.append(where_column)
                            elif operator.lower() == "in":
                                for chip_value in chip_value_arr:
                                    chip_value_a.append(f"{chip_value}','")
                                final_chip_value = "".join(chip_value_a).strip()
                                if final_chip_value.endswith("','"):
                                    final_chip_value = final_chip_value[:-3]
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} ('{final_chip_value}')"
                                where_part_buff.append(where_column)
                            elif operator.lower() == "between":
                                from_value, to_value = chip_value_arr[:2]
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} '{from_value}' AND '{to_value}'"
                                where_part_buff.append(where_column)
                            else:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value}{operator}'{value}'"
                                where_part_buff.append(where_column)
                        elif query_option.upper() == "C":
                            expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                            where_column = f"{main_condition}{expression_value}{operator}{value}"
                            where_part_buff.append(where_column)
                        elif query_option.upper() == "P":
                            if operator.lower() in ["like", "in", "between"]:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value} {operator} ?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(where_column)
                            else:
                                expression_value = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                where_column = f"{main_condition}{expression_value}{operator}?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(where_column)

                    else:
                        if custom_value.strip().lower() != "" and custom_value.lower() != "fixedvalue" and query_option.lower() == "f":
                            if operator.lower() in ["like", "in", "between"]:
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} ?.@{custom_value} "
                                where_part_buff.append(whereColumn)
                            else:
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue}{operator} ?.@{custom_value} "
                                where_part_buff.append(whereColumn)
                        elif query_option.lower() in ["f", "e"]:
                            if operator.lower() == "like":
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} '{value}'"
                                where_part_buff.append(whereColumn)
                            elif operator.lower() == "in":
                                for k in range(len(chip_value_arr)):
                                    chip_value_a.append(f"{chip_value_arr[k]}','")
                                finalChipValue = "".join(chip_value_a).strip()
                                if finalChipValue.endswith("','"):
                                    finalChipValue = finalChipValue[:-3]
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} ('{finalChipValue}')"
                                where_part_buff.append(whereColumn)
                            elif operator.lower() == "between":
                                toValue = []
                                fromValue = []
                                for k in range(len(chip_value_arr)):
                                    if k == 0:
                                        fromValue.append(chip_value_arr[k])
                                    elif k == 1:
                                        toValue.append(chip_value_arr[k])
                                        break
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} '{''.join(fromValue)}' AND '{''.join(toValue)}' "
                                where_part_buff.append(whereColumn)
                            else:
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue}{operator}'{value}'"
                                where_part_buff.append(whereColumn)
                        elif query_option.lower() == "c":
                            expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                            whereColumn = f"{expressionValue}{operator}{value}"
                            where_part_buff.append(whereColumn)
                        elif query_option.lower() == "p":
                            if operator.lower() in ["like", "in", "between"]:
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue} {operator} ?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(whereColumn)
                            else:
                                expressionValue = self.expression_for_column(table_name, col_name, expr_name, col_function, False)
                                whereColumn = f"{expressionValue}{operator}?.{prompt_label.replace(' ', '_').upper()}"
                                where_part_buff.append(whereColumn)

        except Exception as e:
            raise Exception(f"Exception in build_where_part: {str(e)}")
        
        if "".join(where_part_buff).strip():
            where_part = f" WHERE {''.join(where_part_buff)} "
        
        return where_part

    def updateFromPart(self, fromPart, databaseSchemaName, userInfo):
        try:
            logger.log(f"self.foreign_key_tables ::: {self.foreign_key_tables}")
            for i in range(len(self.foreign_key_tables)):
                if self.foreign_key_tables[i] not in self.get_from_table_names():
                    if self.foreign_key_tables[i] not in self.joins_table_names:
                        if E12GenericUtility.checkNull(databaseSchemaName) != "":
                            fromPart = fromPart + ", " + '"' + databaseSchemaName + '"' + "." + self.foreign_key_tables[i]
                        else:
                            fromPart = fromPart + ", " + self.foreign_key_tables[i]
        except Exception as e:
            logger.log(f"Exception ::: {e}")
            raise ITMException(e)

        if fromPart.endswith(","):
            fromPart = fromPart[:len(fromPart) - 1]

        return fromPart 

    def build_group_by(self, user_info):
        group_by_part = ""
        group_by_part_buff = []

        try:

            for column in self.selected_column_list:
                group_by_part_buff.append(column)

            if group_by_part_buff:
                group_by_part = " GROUP BY " + ", ".join(group_by_part_buff)

            if group_by_part.endswith(", "):
                group_by_part = group_by_part[:-2]

        except Exception as e:
            logger.log(f"Exception in build_group_by: {str(e)}")
            raise Exception(f"Error building GROUP BY part: {str(e)}") from e

        return group_by_part  

    def build_function_list(self, database, user_info):
        try:
            file_name = "Functions.json"
            file_path = f"/home/base/wildfly/resource/common/xml/{file_name}"

            with open(file_path, 'r') as f:
                function_data = f.read()
            function_json = json.loads(function_data)

            # Extract functions array
            functions_array = function_json.get("functions", [])
            for function_obj in functions_array:
                database_name = function_obj.get("database", "")
                if database.lower() == database_name.lower():
                    functions = function_obj.get("Function", [])
                    for function in functions:
                        aggregate_val = str(function.get("Aggregrate", "")).strip()
                        function_name = str(function.get("FunctionName", "")).strip()

                        if aggregate_val.lower() == "yes":
                            self.aggr_function.append(function_name)
                        elif aggregate_val.lower() == "no":
                            self.non_aggr_function.append(function_name)

        except Exception as e:
            logging.error(f"Exception in build_function_list: {str(e)}")
            raise e

        return ""    
    
    def generate_source_sql(self, sql_model, user_info, schema_sql):
        query = ""
        try:
            sql_model_json = json.loads(json.dumps(sql_model))
            logging.info(f"Sql Model JSON String: {sql_model_json}")

            if sql_model_json:
                sql_model_data = sql_model_json.get("SQLModel", {})
                columns_array = sql_model_data.get("COLUMNS", [])
                if columns_array:
                    logging.info(f"Columns Array: {columns_array}")
                    self.build_form_table_names_array(columns_array, user_info)

            file_path = f"/home/base/wildfly/resource/common/xml/{schema_sql}.xml"
            with open(file_path, 'r') as f:
                schema_xml = f.read()
            schema_json = self._xml_to_json(schema_xml)

            hr_master_json = schema_json.get("HR_Master", {})
            is_object = self.is_object_function(hr_master_json, user_info)
            logging.info(f"Is Object: {is_object}")

            if "JOIN_PREDICATES" in hr_master_json and is_object:
                join_predicate_json = hr_master_json["JOIN_PREDICATES"]
                join = join_predicate_json.get("JOIN")
                if isinstance(join, list):
                    for current_json in join:
                        if current_json.get("MAIN_TABLE") == "yes":
                            self.main_table_name = current_json.get("ID")
                            break
                elif isinstance(join, dict):
                    if join.get("MAIN_TABLE") == "yes":
                        self.main_table_name = join.get("ID")

            # logger.log(hr_master_json)
            if "DATABASE" in hr_master_json:
                # logger.log(f"Inside DATABASE")
                database_json = hr_master_json["DATABASE"]
                database_name = database_json.get("DATABASE_NAME", "")
                self.build_function_list(database_name, user_info)

            sql_query, select_part, from_part, where_part, group_by_part = "", "", "", "", ""

            if sql_model_json:
                sql_model_data = sql_model_json.get("SQLModel", {})
                columns_array = sql_model_data.get("COLUMNS", [])
                if columns_array:
                    select_part = self._build_select_part(columns_array, user_info)
                    from_part = self.build_from_part(columns_array, hr_master_json.get("DATABASE_SCHEMA", ""), schema_xml, user_info)

                    if self.is_aggregate_func:
                        group_by_part = self.build_group_by(user_info)

                criteria_json_object = sql_model_json.get("CRITERIA", {})
                if criteria_json_object:
                    where_part = self.build_where_part(criteria_json_object, schema_xml, user_info, columns_array)
                    fromPart = self.updateFromPart(from_part, schema_sql, user_info)
                    
                if len(E12GenericUtility.check_null(select_part)) > 0 and len(E12GenericUtility.check_null(fromPart)) > 0:
                    sql_query = select_part + fromPart + "" + where_part + group_by_part
                
                logger.log("-------------------------------------------")
                logger.log(f"select_part Query ::: {select_part}")
                logger.log("-------------------------------------------")
                logger.log(f"from_part Query ::: {from_part}")
                logger.log(f"from_part Query ::: {fromPart}")
                logger.log("-------------------------------------------")
                logger.log(f"where_part Query ::: {where_part}")
                logger.log("-------------------------------------------")
                logger.log(f"group_by_part Query ::: {group_by_part}")
                logger.log("-------------------------------------------")

            query = sql_query + ""
        except Exception as e:
            logging.error(f"Error occurred: {str(e)}")
            raise e

        # logger.log("-------------------------------------------")
        # logger.log(f"Final Query ::: {query.strip()}")
        return query.strip()

