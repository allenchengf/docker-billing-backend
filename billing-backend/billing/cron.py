import datetime
import tools.dbhelper as dbhelper
import json


class RunReport:

    def save_billings_progress(self):
        now_datetime, sdate, edate, year, month, monthName = self.get_last_month_start_end()

        save_billing_result = {}

        mysql = dbhelper.DBHelper()
        sql = "select * from billing_billingsetting"
        result = mysql.fetch(sql)
        for row in result:
            save_billing_result['customer_id'] = row['customer_id']
            save_billing_result['service_id'] = row['service_id']
            save_billing_result['billing_id'] = row['billing_id']
            save_billing_result['cir'] = row['cir']
            save_billing_result['pir'] = row['pir']
            save_billing_result['provisioned_at'] = row['provisioned_at']
            save_billing_result['terminated_at'] = row['terminated_at']
            save_billing_result['year'] = str(year)
            save_billing_result['month'] = str(month)
            save_billing_result['created_at'] = now_datetime
            save_billing_result['updated_at'] = now_datetime
            save_billing_result['order'] = ''
            save_billing_result['sales_tag'] = ''
            save_billing_result['prefixes_done'] = json.dumps([])
            save_billing_result['monthly_report_done'] = 0

            sql = "select prefix_list from billing_sensor where billing_settings_id=" + str(row['id'])
            result = mysql.fetch(sql)
            prefix_list = []
            for item in result:
                item = json.loads(item['prefix_list'])
                for i in item:
                    prefix_list.append(i)
            save_billing_result['prefixes'] = json.dumps(prefix_list)
            sql = """
                    INSERT INTO billing_billingsummary(billing_id, customer_id, service_id, `year`, `month`, prefixes, cir, pir, prefixes_done, monthly_report_done, `order`, sales_tag, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
            params = (save_billing_result['billing_id'],
                      save_billing_result['customer_id'],
                      save_billing_result['service_id'],
                      save_billing_result['year'],
                      save_billing_result['month'],
                      save_billing_result['prefixes'],
                      save_billing_result['cir'],
                      save_billing_result['pir'],
                      save_billing_result['prefixes_done'],
                      save_billing_result['monthly_report_done'],
                      save_billing_result['order'],
                      save_billing_result['sales_tag'],
                      save_billing_result['created_at'],
                      save_billing_result['updated_at']
                      )
            mysql.execute(sql, params)

    def save_aggregates_reports(self):
        print('save_aggregates_reports')

    def copy_historic_data(self):
        now_datetime, sdate, edate, year, month, monthName = self.get_last_month_start_end()
        last_month_table_name = 'historic_' + year + '_' + month
        if not self.check_table_exists(last_month_table_name):
            result = self.historic_table_rename(last_month_table_name)
            if result == 'success':
                self.create_new_historic_table()
            else:
                print(result)
        else:
            print('yes ' + last_month_table_name)

    def check_table_exists(self, last_month_table_name):
        mysql = dbhelper.DBHelper()
        sql = """select count(*) as count from information_schema.tables WHERE table_name = %s
        """
        result = mysql.fetchone(sql, last_month_table_name)
        return bool(result['count'])

    def historic_table_rename(self, last_month_table_name):
        mysql = dbhelper.DBHelper()
        sql = "ALTER TABLE historic RENAME TO " + str(last_month_table_name)
        try:
            mysql.execute(sql)
            message = 'success'
        except (ValueError, ZeroDivisionError):
            message = ValueError
        return message

    def create_new_historic_table(self):
        mysql = dbhelper.DBHelper()
        sql = """
        CREATE TABLE `historic` (
          `id` bigint unsigned NOT NULL AUTO_INCREMENT,
          `sensor_id` int NOT NULL,
          `prefix` varchar(255) NOT NULL,
          `reserve_prefix` varchar(255) DEFAULT NULL,
          `incoming` varchar(50) DEFAULT NULL,
          `outgoing` varchar(50) DEFAULT NULL,
          `raw_incoming` varchar(50) DEFAULT NULL,
          `raw_outgoing` varchar(50) DEFAULT NULL,
          `datetime` varchar(255) DEFAULT NULL,
          `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
          `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
          PRIMARY KEY (`id`,`sensor_id`),
          KEY `IDX_SENSOR_ID` (`sensor_id`),
          KEY `IDX_DATETIME` (`datetime`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """
        try:
            mysql.execute(sql)
            print('create historic table success')
        except (ValueError, ZeroDivisionError):
            print(ValueError)

    def get_last_month_start_end(self):
        today = datetime.date.today()
        edate = datetime.date(today.year, today.month, 1) - datetime.timedelta(1)
        sdate = datetime.date(edate.year, edate.month, 1)
        year = sdate.strftime("%Y")
        month = sdate.strftime("%-m")
        monthName = sdate.strftime("%B")
        sdate = sdate.strftime("%Y-%m-%d 00:00:00")
        edate = edate.strftime("%Y-%m-%d 23:59:00")
        now_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return now_datetime, sdate, edate, year, month, monthName


report = RunReport()

# 準備開始，將待產月報者新增資料於 Billings，並於以下二者完成時再次更新進度。
# report.save_billings_progress()

# 產Aggregates 報表
report.save_aggregates_reports()

# report.copy_historic_data()
