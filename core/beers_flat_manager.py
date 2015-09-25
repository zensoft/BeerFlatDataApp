import psycopg2
import time
from settings.db_settings import *
from utils.custom_logger import *
from utils.db_utils import *

custom_logger = CustomLogger()

class BeersFlatManager:

    def update_flat(self):
        start = time.time()
        conn = self._get_db_connection()
        if not type(conn) == str:
            self._clear_flat(conn)
            self._reload_flat_data(conn)
            conn.close()
        else:
            custom_logger.log(conn)
        end = time.time()
        custom_logger.log("Execution time in seconds: {0}".format(end - start))

    def _reload_flat_data(self, conn):
        cursor = conn.cursor()
        get_reload_flat_data_sql = """
            INSERT INTO app_beers_flat
            (brewery_name, descriptiion, www, picture, address_name,
            address_lat, address_lon, city, province, updated_at)
             (
        		SELECT b.brewery_name as bname, b.brewery_description as bdesc,
        		b.www as www, b.picture_path as bpicture,
        		a.address_name as aname, a.lat as lat, a.lon as lon,
        		c.city_name as cname, p.province_name as pname, b.updated_at as updated_at
        		FROM app_brewery b
        		LEFT JOIN app_address a on a.address_id = b.address_id
        		LEFT JOIN app_city c on c.city_id = a.city_id
        		LEFT JOIN app_province p on p.province_id = c.province_id
        		WHERE b.brewery_name in (select brewery_name from app_brewery where published)
        	)
                                    """
        cursor.execute(get_reload_flat_data_sql)
        conn.commit()

    def _clear_flat(self, conn):
        cursor = conn.cursor()
        clear_sql = "DELETE FROM app_beers_flat"
        cursor.execute(clear_sql)
        conn.commit()

    def _update_flat(self, conn):
        custom_logger.log("update flat")
        published_brewerys = self._get_published_brewerys(conn)
        flat_brewerys = self._get_flat_brewerys(conn)
        #get all published brewery name's from app_brewery and compare to app_beers_flat brewerys name's

    def _proccess_brewery(self, conn, brewery_name):
        brewery_data = self._get_brewery_data(conn, brewery_name)
        self._add_brewery_data(conn, brewery_data)

    def _add_brewery_data(self, conn, brewery_data):
        cursor = conn.cursor()
        add_brewery_data_sql = """
            INSERT INTO app_beers_flat(brewery_name, descriptiion, www, picture,
            address_name, address_lat, address_lon, city, province, updated_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                               """
        query_params = (brewery_data["bname"],brewery_data["bdesc"],brewery_data["www"],brewery_data["bpicture"]
                        ,brewery_data["aname"],brewery_data["lat"],brewery_data["lon"],brewery_data["cname"]
                        ,brewery_data["pname"],brewery_data["updated_at"])
        cursor.execute(add_brewery_data_sql,query_params)
        conn.commit()

    def _get_brewery_data(self, conn, brewery_name):
        cursor = conn.cursor()
        flat_brewery_data_select = """
            SELECT b.brewery_name as bname, b.brewery_description as bdesc,
        	b.picture_path as bpicture, b.www as www, b.updated_at as updated_at,
        	a.lon as lon, a.lat as lat, a.address_name as aname,
        	c.city_name as cname, p.province_name as pname
        	FROM app_brewery b
        	LEFT JOIN app_address a on a.address_id = b.address_id
        	LEFT JOIN app_city c on c.city_id = a.city_id
        	LEFT JOIN app_province p on p.province_id = c.province_id
        	WHERE b.brewery_name = %s
                                   """
        cursor.execute(flat_brewery_data_select,(brewery_name,))
        flat_brewery_data = dictfetchone(cursor)
        return flat_brewery_data

    def _get_all_brewerys(self, conn):
        cursor = conn.cursor()
        all_brewerys_select = "select brewery_name from app_brewery where published"
        cursor.execute(all_brewerys_select)
        records = dictfetchall(cursor)
        custom_logger.log("Fetch all published brewery: {0}".format(len(records)))
        custom_logger.log("Working...")
        return records

    def _is_flat_empty(self, conn):
        cursor = conn.cursor()
        beers_total_select = "SELECT count(*) as beers_total FROM app_beers_flat"
        cursor.execute(beers_total_select)
        records = cursor.fetchone()
        custom_logger.log("Records in app_beers_flat {0}".format(records[0]))
        return records[0] == 0

    def _get_db_connection(self):
        try:
            return psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        except Exception as e:
            return str(e)
