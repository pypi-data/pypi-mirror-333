import cx_Oracle
import loggerutility as logger
from datetime import datetime

class Dashboard_Definition:

    def check_or_update_dashboard_definition(self, dashboard_data, connection):

        required_keys = ['proc_design_id', 'schema_name']
        missing_keys = [key for key in required_keys if key not in dashboard_data]
        
        if missing_keys:
            logger.log(f"Missing required keys for dashboard_definition table: {missing_keys}")
            raise KeyError(f"Missing required keys for dashboard_definition table: {', '.join(missing_keys)}")
        
        proc_design_id = dashboard_data.get('proc_design_id', '')
        logger.log(f"proc_design_id ::: {proc_design_id}")
        descr = dashboard_data.get('descr', '')
        det_descr = dashboard_data.get('det_descr', '')
        schema_name = dashboard_data.get('schema_name', '')
        persist_obj_name = dashboard_data.get('persist_obj_name', '')
        key_column = dashboard_data.get('key_column', '')
        conf_col = dashboard_data.get('conf_col', '')
        conf_val = dashboard_data.get('conf_val', '')
        update_mth = dashboard_data.get('update_mth', '')
        obj_name__deploy = dashboard_data.get('obj_name__deploy', '')
        add_term = dashboard_data.get('add_term', '') or 'Insight'
        add_user = dashboard_data.get('add_user', '') or 'Insight'
        add_date = datetime.strptime(dashboard_data.get('add_date', ''), '%Y-%m-%d').date() if dashboard_data.get('add_date') else datetime.now().date()
        chg_term = dashboard_data.get('chg_term', '') or 'Insight'
        chg_user = dashboard_data.get('chg_user', '') or 'Insight'
        chg_date = datetime.strptime(dashboard_data.get('chg_date', ''), '%Y-%m-%d').date() if dashboard_data.get('chg_date') else datetime.now().date()
        sql_model = dashboard_data.get('sql_model', '')
        layout_data = dashboard_data.get('layout_data', '')
        source_sql = dashboard_data.get('source_sql', '').replace('\n', ' ').replace('\\n', ' ').replace('"', ' ').strip()
        revision_no = dashboard_data.get('revision_no', 0)

        logger.log("insert")   
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO dashboard_definition (
            PROC_DESIGN_ID, DESCR, DET_DESCR, SCHEMA_NAME, PERSIST_OBJ_NAME, 
            KEY_COLUMN, CONF_COL, CONF_VAL, UPDATE_MTH, OBJ_NAME__DEPLOY, 
            ADD_TERM, ADD_USER, ADD_DATE, CHG_TERM, CHG_USER, CHG_DATE, 
            SQLMODEL, LAYOUT_DATA, SOURCE_SQL, REVISION_NO
            ) VALUES (
            :proc_design_id, :descr, :det_descr, :schema_name, :persist_obj_name, 
            :key_column, :conf_col, :conf_val, :update_mth, :obj_name__deploy, 
            :add_term, :add_user, :add_date, :chg_term, :chg_user, :chg_date, 
            :sql_model, :layout_data, :source_sql, :revision_no
            )
        """
        cursor.execute(insert_query, {
            'proc_design_id': proc_design_id,
            'descr': descr,
            'det_descr': det_descr,
            'schema_name': schema_name,
            'persist_obj_name': persist_obj_name,
            'key_column': key_column,
            'conf_col': conf_col,
            'conf_val': conf_val,
            'update_mth': update_mth,
            'obj_name__deploy': obj_name__deploy,
            'add_term': add_term,
            'add_user': add_user,
            'add_date': add_date,
            'chg_term': chg_term,
            'chg_user': chg_user,
            'chg_date': chg_date,
            'sql_model': sql_model,
            'layout_data': layout_data,
            'source_sql': source_sql,
            'revision_no': revision_no
        })
        return_response = "Success"        
        cursor.close()
        return return_response

    def process_data(self, conn, visual_json):
        logger.log("Start of DashboardDefinition Class")
        try:
            response = self.check_or_update_dashboard_definition(visual_json, conn)
            logger.log("End of DashboardDefinition Class")
            return response
        except:
            return "Fail"

