import cx_Oracle
import json
import loggerutility as logger
from datetime import datetime

class Dashbrd_dgn:

    def check_or_update_dashbrd_dgn(self, connection, dashboard_data):
            
        required_keys = ['dashbrd_id']
        missing_keys = [key for key in required_keys if key not in dashboard_data]
        
        if missing_keys:
            logger.log(f"Missing required keys for dashbrd_dgn table: {missing_keys}")
            raise KeyError(f"Missing required keys: {', '.join(missing_keys)}")

        dashbrd_id = dashboard_data.get('dashbrd_id', '') or None
        title = dashboard_data.get('title', '') or None
        sub_title = dashboard_data.get('sub_title', '') or None
        icon = dashboard_data.get('icon', '') or None
        obj_name = dashboard_data.get('obj_name', '') or None
        dashbrd_type = dashboard_data.get('dashbrd_type', '') or None
        security_type = dashboard_data.get('security_type', '') or None
        obj_name__sec = dashboard_data.get('obj_name__sec', '') or None
        application = dashboard_data.get('application', '') or None
        enterprise = dashboard_data.get('enterprise', '') or None
        add_term = dashboard_data.get('add_term','') or 'Insight'
        add_user = dashboard_data.get('add_user','') or 'Insight'
        add_date = datetime.strptime(dashboard_data.get('add_date', ''), '%Y-%m-%d').date() if dashboard_data.get('add_date') else datetime.now().date()
        chg_term = dashboard_data.get('chg_term','') or 'Insight'
        chg_user = dashboard_data.get('chg_user','') or 'Insight'
        chg_date = datetime.strptime(dashboard_data.get('chg_date', ''), '%Y-%m-%d').date() if dashboard_data.get('chg_date') else datetime.now().date()
        layout_data = dashboard_data.get('layout_data', '') or None  
        descr = dashboard_data.get('descr', '') or None
        criteria = dashboard_data.get('criteria', '') or None
        dashbrd_group = dashboard_data.get('dashbrd_group', '') or None
        dash_layout_data = dashboard_data.get('dash_layout_data', '') or None
        
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO dashbrd_dgn (
            DASHBRD_ID, TITLE, SUB_TITLE, ICON, OBJ_NAME, DASHBRD_TYPE, 
            SECURITY_TYPE, OBJ_NAME__SEC, APPLICATION, ENTERPRISE, ADD_TERM, 
            ADD_USER, ADD_DATE, CHG_TERM, CHG_USER, CHG_DATE, LAYOUT_DATA, 
            DESCR, CRITERIA, DASHBRD_GROUP, DASH_LAYOUT_DATA
            ) VALUES (
            :dashbrd_id, :title, :sub_title, :icon, :obj_name, :dashbrd_type, 
            :security_type, :obj_name__sec, :application, :enterprise, :add_term, 
            :add_user, :add_date, :chg_term, :chg_user, :chg_date, :layout_data, 
            :descr, :criteria, :dashbrd_group, :dash_layout_data
            )
        """
        values = {
            'dashbrd_id': dashbrd_id, 
            'title': title, 
            'sub_title': sub_title, 
            'icon': icon, 
            'obj_name': obj_name,
            'dashbrd_type': dashbrd_type, 
            'security_type': security_type, 
            'obj_name__sec': obj_name__sec,
            'application': application, 
            'enterprise': enterprise, 
            'add_term': add_term,
            'add_user': add_user, 
            'add_date': add_date, 
            'chg_term': chg_term, 
            'chg_user': chg_user,
            'chg_date': chg_date, 
            'layout_data': layout_data, 
            'descr': descr, 
            'criteria': criteria,
            'dashbrd_group': dashbrd_group, 
            'dash_layout_data': dash_layout_data
        }
        cursor.execute(insert_query, values)
        cursor.close()

    def process_data(self, conn, dashbrd_dgn_data):
        logger.log("Start of Dashbrd_dgn Class")
        self.check_or_update_dashbrd_dgn(conn, dashbrd_dgn_data)
        logger.log("End of Dashbrd_dgn Class")
