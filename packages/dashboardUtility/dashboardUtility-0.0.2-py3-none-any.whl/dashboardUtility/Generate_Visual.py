import cx_Oracle
import json
import loggerutility as logger
from .SQL_Model import SQL_Model
from .Visual_Model import Visual_Model
from .FreeHand_SQL_Model import FreeHand_SQL_Model
from .FreeHand_Visual_Model import FreeHand_Visual_Model
from .Source_SQL import Source_SQL
from .Dashboard_Definition import Dashboard_Definition
from DatabaseConnectionUtility import Oracle 
from DatabaseConnectionUtility import Dremio
from DatabaseConnectionUtility import InMemory 
from DatabaseConnectionUtility import Oracle
from DatabaseConnectionUtility import MySql
from DatabaseConnectionUtility import MSSQLServer 
from DatabaseConnectionUtility import SAPHANA
from DatabaseConnectionUtility import Postgress
import traceback
import commonutility as common
from flask import request

class Generate_Visual:

    connection           = None
    dbDetails            = ''
    menu_model           = ''
    token_id             = ''
    
    def get_database_connection(self, dbDetails):
        if dbDetails['DB_VENDORE'] != None:
            klass = globals()[dbDetails['DB_VENDORE']]
            dbObject = klass()
            connection_obj = dbObject.getConnection(dbDetails)
        return connection_obj

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
                logger.log("Transaction committed successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during commit: {error}")
        else:
            logger.log("No active connection to commit.")

    def rollback(self):
        if self.connection:
            try:
                self.connection.rollback()
                logger.log("Transaction rolled back successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during rollback: {error}")
        else:
            logger.log("No active connection to rollback.")

    def close_connection(self):
        if self.connection:
            try:
                self.connection.close()
                logger.log("Connection closed successfully.")
            except cx_Oracle.Error as error:
                logger.log(f"Error during close: {error}")
        else:
            logger.log("No active connection to close.")

    def process_data(self, dbDetails, visual_json):

        schema_xml_file_path = f"/home/base/wildfly/resource/common/xml/{visual_json['Schema_Name']}.xml"
        visual_json_file_path = "/home/base/wildfly/resource/common/xml/DashboardVisuals.json"

        self.connection = self.get_database_connection(dbDetails)
        if self.connection:
            try:

                source_sql_data = ""
                if "Sql" in visual_json:
                    logger.log(f"Create Free hand sql model class")

                    sql_model = FreeHand_SQL_Model(visual_json, schema_xml_file_path)
                    sql_model_json = sql_model.generate_sql_model()

                    visual_model = FreeHand_Visual_Model(schema_xml_file_path)
                    visual_json_list = visual_model.load_visuals_json(visual_json_file_path)
                    visual_model_json = visual_model.generate_visual_model(visual_json, visual_json_list)

                    source_sql_data = visual_json['Sql']
                else:
                    sql_model = SQL_Model(visual_json, schema_xml_file_path)
                    sql_model_json = sql_model.generate_sql_model()

                    visual_model = Visual_Model(schema_xml_file_path)
                    visual_json_list = visual_model.load_visuals_json(visual_json_file_path)
                    visual_model_json = visual_model.generate_visual_model(visual_json, visual_json_list)

                    source_sql = Source_SQL()
                    source_sql_data = source_sql.generate_source_sql(sql_model_json,{},visual_json['Schema_Name'])

                # ---------------------------------------------------------------------------------
                
                cursor = self.connection.cursor()
                cursor.execute(f"""
                    SELECT SEQ_NO FROM REFSEQ WHERE REF_SER='DASDEF'
                """)
                new_proc_design_id = cursor.fetchone()[0]
                new_proc_design_id = str(int(new_proc_design_id) + 1).zfill(10)
                cursor.close()
                logger.log(f"new_proc_design_id ::: {new_proc_design_id}")

                dashboard_data = {
                    "proc_design_id": new_proc_design_id,
                    "descr": "New Visual",
                    "det_descr": "New Visual Description",
                    "schema_name": visual_json['Schema_Name'],
                    "persist_obj_name": None,
                    "key_column": None,
                    "conf_col": None,
                    "conf_val": None,
                    "update_mth": None,
                    "obj_name__deploy": None,
                    "add_term": None,
                    "add_user": None,
                    "add_date": None,
                    "chg_term": None,
                    "chg_user": None,
                    "chg_date": None,
                    "sql_model": json.dumps(sql_model_json),
                    "layout_data": json.dumps(visual_model_json),
                    "source_sql": source_sql_data,
                    "revision_no": None
                }
                
                dashboard_definition_table = Dashboard_Definition()
                response = dashboard_definition_table.process_data(self.connection, dashboard_data)

                logger.log(f"dashboard response ::: {response}")
                if response == 'Success':
                    cursor = self.connection.cursor()
                    update_query = """
                        UPDATE REFSEQ SET SEQ_NO=:seq_no WHERE REF_SER='DASDEF'
                        """
                    values = {'seq_no': new_proc_design_id}
                    logger.log(f"update_query values :: {values}")
                    cursor.execute(update_query, values)
                    logger.log(f"REFSEQ UPDATED")
                    cursor.close()
                
                self.commit()

                return {"status":"Success", "data": new_proc_design_id}
                    
            except Exception as e:
                logger.log(f"Rollback successfully.")
                self.rollback()
                return {"status":"Fail", "data": str(e)}
                
            finally:
                logger.log('Closed connection successfully')
                self.close_connection()
        else:
            descr = str("Connection fail")
            return {"status":"Fail", "data": descr}
