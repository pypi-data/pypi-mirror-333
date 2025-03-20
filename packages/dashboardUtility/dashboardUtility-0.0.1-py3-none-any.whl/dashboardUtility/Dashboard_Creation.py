import json
import cx_Oracle
from typing import Dict, Any, Tuple
import loggerutility as logger
from DatabaseConnectionUtility import Oracle, Dremio, InMemory, MySql, MSSQLServer, SAPHANA, Postgress
from .Generate_Visual import Generate_Visual
from .Dashbrd_dgn import Dashbrd_dgn
import traceback
import commonutility as common

class Dashboard_Creation:

    connection           = None
    dbDetails            = ''
    
    def get_database_connection(self, dbDetails):
        try:
            if dbDetails['DB_VENDORE']:
                klass = globals().get(dbDetails['DB_VENDORE'])
                if klass:
                    dbObject = klass()
                    connection_obj = dbObject.getConnection(dbDetails)
                    return connection_obj
            logger.log("Invalid database vendor specified.")
            return None
        except Exception as e:
            logger.log(f"Error getting database connection: {str(e)}")
            return None

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

    def fetch_dashboard_data(self, proc_design_id, connection):
        try:
            if not connection:
                return '', '', '', {}, {}, ''

            cursor = connection.cursor()

            logger.log(f"Executing query for proc_design_id: {proc_design_id}")

            query = f"""
                SELECT DESCR, DET_DESCR, SCHEMA_NAME, SQLMODEL, LAYOUT_DATA, SOURCE_SQL
                FROM dashboard_definition 
                WHERE proc_design_id = :proc_design_id
            """
            cursor.execute(query,{'proc_design_id': proc_design_id})

            result = cursor.fetchone()
            logger.log(f"result for {proc_design_id} :: {result}")
            
            if result:
                desc = result[0]
                det_desc = result[1]
                schema_name = result[2]
                sql_model = result[3].read()
                layout_data = result[4].read()
                source_sql = result[5].read()

                return desc, det_desc, schema_name, sql_model, layout_data, source_sql

            else:
                logger.log(f"No data found for proc_design_id: {proc_design_id}")
                return '', '', '', {}, {}, ''
        
        except Exception as e:
            logger.log(f"Error fetching dashboard data: {str(e)}")
            return '', '', '', {}, {}, ''

    def generate_json(self, new_proc_design_id, cols, rows, x, y, visual_json, connection, line_no):

        desc, det_desc, schema_name, sql_model, layout_data, source_sql = self.fetch_dashboard_data(new_proc_design_id, connection)
        
        dashboard_layout = {
            "cols": cols,
            "rows": rows,
            "x": x,
            "y": y,
            "visual": {
                "sub_title": det_desc,
                "dashbrd_id": "",
                "line_no": line_no,  
                "title": desc,
                "visual_name": f"{visual_json['Visual_Name']}.svg",
                "visual_id": new_proc_design_id,
                "visual_data": [{
                    "DET_DESCR": det_desc,
                    "SCHEMA_NAME": schema_name,
                    "layoutData": layout_data,
                    "visualName": f"{visual_json['Visual_Name']}.svg",
                    "PROC_DESIGN_ID": new_proc_design_id,
                    "sourceSql": source_sql,
                    "sqlModel": sql_model,
                    "checked": True,
                    "DESCR": desc
                }]
            }
        }
        
        return dashboard_layout

    def process_data(self, dbDetails, dashboard_visual_json):

        self.connection = self.get_database_connection(dbDetails)
        if self.connection:

            try:

                cols = 16
                rows = 16
                x = 0
                y = 0
                line_no = 0
                layout_data_list = []
                for visual_json in dashboard_visual_json["visuals"]:
                    line_no = line_no + 1

                    generate_visual = Generate_Visual()
                    response = generate_visual.process_data(dbDetails, visual_json)
                    status = response['status']
                    data = response['data']

                    logger.log(f"new_proc_design_id ::: {data}")
                    if status == 'Success':
                        logger.log(f"Inside new_proc_design_id")
                        dashboard_layout = self.generate_json(data, cols, rows, x, y, visual_json, self.connection, line_no)
                        layout_data_list.append(dashboard_layout)
                    else:
                        raise Exception(f"Failed to create visual : {data}")

                    x = x + 16
                    y = y

                cursor = self.connection.cursor()
                cursor.execute(f"""
                    SELECT DASHBOARD_DGN_SEQ.NEXTVAL FROM DUAL
                """)
                dashbrd_id = cursor.fetchone()[0]
                cursor.close()
                logger.log(f"dashbrd_id ::: {dashbrd_id}")
                add_text = '00000000000000000000'
                new_dashbrd_id = add_text[:len(add_text) - len(str(dashbrd_id))] + str(dashbrd_id)
                logger.log(f"new_dashbrd_id ::: {new_dashbrd_id}")
                logger.log(f" len of new_dashbrd_id::: {len(new_dashbrd_id)}")

                dashbrd_dgn_data = {
                    "dashbrd_id": new_dashbrd_id, 
                    "title": 'Dashboard', 
                    "sub_title": 'Dashboard titile', 
                    "icon": None, 
                    "obj_name": None,
                    "dashbrd_type": None, 
                    "security_type": None, 
                    "obj_name__sec": None,
                    "application": None, 
                    "enterprise": None, 
                    "add_term": None,
                    "add_user": None, 
                    "add_date": None, 
                    "chg_term": None, 
                    "chg_user": None,
                    "chg_date": None, 
                    "layout_data": json.dumps(layout_data_list), 
                    "descr": None, 
                    "criteria": None,
                    "dashbrd_group": None, 
                    "dash_layout_data": None
                }
                dashbrd_dgn = Dashbrd_dgn()
                dashbrd_dgn.process_data(self.connection, dashbrd_dgn_data)

                self.commit()

                trace = traceback.format_exc()
                descr = str("Dashboard Created Successfully.")
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)

            except Exception as e:
                logger.log(f"Rollback successfully.")
                self.rollback()
                logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
                trace = traceback.format_exc()
                descr = str(e)
                returnErr = common.getErrorXml(descr, trace)
                logger.log(f'\n Exception ::: {returnErr}', "0")
                return str(returnErr)
                
            finally:
                logger.log('Closed connection successfully')
                self.close_connection()
        
        else:
            logger.log(f'\n In getInvokeIntent exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str("Connection fail")
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)
