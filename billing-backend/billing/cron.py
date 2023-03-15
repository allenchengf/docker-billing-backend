import datetime
import tools.dbhelper as dbhelper
import json
import ast


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
        now_datetime, sdate, edate, year, month, monthName = self.get_last_month_start_end()

        mysql = dbhelper.DBHelper()
        sql = "select * from billing_billingsettingaggregates where permanent != 'manual-one-time'"
        bw_prefix_set_group = mysql.fetch(sql)

        for group in bw_prefix_set_group:
            self.save_aggregate_results(now_datetime, year, month, group)

        # send email

    def save_aggregate_results(self, now_datetime, year, month, group_row):
        mysql = dbhelper.DBHelper()
        group_name = group_row['group_name']
        group_ary = group_row['billing_list']
        group_pir = group_row['pir']
        permanent = group_row['permanent']

        sql = "select * from billing_billingsummaryaggregates where group_name = %s and year = %s and month = %s order by id desc"
        params = (group_name, year, month)
        last_row = mysql.fetchone(sql, params)
        sequence = 1

        if last_row is not None:
            sequence = last_row['sequence']
            sequence = sequence + 1

        billing_info = dict(
            group_name=group_name,
            year=year,
            month=month,
            billing_list=group_ary,
            percentile_98_h=0,
            percentile_98_hm=0,
            percentile_98=0,
            percentile_98_m=0,
            percentile_mbps_98=0,
            data_progress='1/' + str(len(ast.literal_eval(group_ary))),
            monthly_report_done=0,
            sequence=sequence,
            created_at=now_datetime,
            updated_at=now_datetime

        )

        sql = """
                INSERT INTO billing_billingsummaryaggregates(group_name, year, month, billing_list, percentile_98_h, percentile_98_hm, percentile_98, percentile_98_m, percentile_mbps_98, data_progress, monthly_report_done, sequence, created_at, updated_at) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        params = (billing_info['group_name'],
                  billing_info['year'],
                  billing_info['month'],
                  billing_info['billing_list'],
                  billing_info['percentile_98_h'],
                  billing_info['percentile_98_hm'],
                  billing_info['percentile_98'],
                  billing_info['percentile_98_m'],
                  billing_info['percentile_mbps_98'],
                  billing_info['data_progress'],
                  billing_info['monthly_report_done'],
                  billing_info['sequence'],
                  billing_info['created_at'],
                  billing_info['updated_at'],
                  )
        mysql.execute(sql, params)
        curr_id = mysql.cur.lastrowid

        sql = "select a.sensor_id, a.prefix_list, b.billing_id from billing_sensor as a left join billing_billingsetting as b on a.billing_settings_id = b.id where billing_id in " + str(group_ary).replace('[', '(').replace(']', ')')
        result = mysql.fetch(sql)

        sensor_list = []
        prefix_list = []
        for raw in result:
            sensor_list.append(raw['sensor_id'])
            prefix_list.append(raw['prefix_list'])

        bandwidth_charging_id = 'Aggregate-' + group_name

        if len(sensor_list) > 0 and len(prefix_list) > 0:
            percentile_98_h = 0;
            percentile_98_hm = 0;
            percentile_98 = 0;
            percentile_98_m = 0;

            percentile_98, percentile_98_h = self.get_multi_percentile(sensor_list, 98, None, prefix_list,bandwidth_charging_id)
            percentile_98_m, percentile_98_hm = self.get_multi_percentile(sensor_list, 98, None, prefix_list,bandwidth_charging_id)

    def get_multi_percentile(self, sensor_ids, percentile=98, time_list=None, prefixes_by_in_out=None, bandwidth_charging_id=None):
        multi_percentile = None
        incoming_percentile = None
        outgoing_percentile = None
        sampling_in_x_minute = 1
        historicData = None

        historicData = self.get_samples_by_month(sensor_ids, time_list, prefixes_by_in_out, table='historic')
        return 1, 2

    def get_samples_by_month(self,sensor_ids, time_list, prefixes_by_in_out, table='historic'):
        mysql = dbhelper.DBHelper()

        sql ='select ANY_VALUE(SUM(incoming)) as incoming, ANY_VALUE(SUM(outgoing)) as outgoing, datetime from ' + table + ' where sensor_id in ' + str(sensor_ids).replace('[', '(').replace(']', ')') + ' and prefix in ' + str(prefixes_by_in_out).replace('["', '').replace('"]', '').replace('[', '(').replace(']', ')') + ' group by datetime'
        result = mysql.fetch(sql)
        print(result)

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
