import sys
import pymysql
import redis

class Healthcheck:

    def __init__(self):
        self.type = None

    def run(self):
        raise NotImplementedError()


class MysqlHealthcheck(Healthcheck):

    def __init__(self, name, host='localhost', port=3306, user='root', password='', db='mysql'):
        super(Healthcheck, self).__init__()
        self.name = name
        self.type = "mysql"
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db

    def run(self):
        print("Name: {} - Type: {}".format(self.name, self.type))
        connection = pymysql.connect(host=self.host,
                                        port=self.port,
                                        user=self.user,
                                        password=self.password,
                                        db=self.db,
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                sql = 'SELECT COUNT(1)'
                cursor.execute(sql)
                result = cursor.fetchone()

        finally:
            connection.close()

        if result == 1:
            return True

        return False


class RedisHealthcheck(Healthcheck):

    def __init__(self, name, host='localhost', port=6379, password='', db='0'):
        super(Healthcheck, self).__init__()
        self.name = name
        self.type = "redis"
        self.host = host
        self.port = port
        self.password = password
        self.db = db

    def run(self):
        print("Name: {} - Type: {}".format(self.name, self.type))
        key = 'toto'
        value = 'toto42'
        try:
            r = redis.Redis(host=self.host, port=self.port, password=self.password, db=self.db, socket_timeout=3)
            r.set(key, value)
            result = r.get(key)
        except:
            # problem connecting to redis host
            return False

        if result == value:
            return True

        return False


class Healthchecks:

    def __init__(self, healthchecks):
        self.healthchecks = healthchecks

    def run(self):

        if len(self.healthchecks) == 0:
            return False

        result = True
        for check in self.healthchecks:
            result &= check.run()

        return result
            

if __name__ == '__main__':

    try:
        from settings import settings
    except:
        print("Error loading settings, exiting")
        sys.exit(1)

    checks = []

    redis_checks = settings.HEALTHCHECKS_REDIS
    for name, check in redis_checks.items():
        checks.append(RedisHealthcheck(check['name'],
                                        host=check['host'],
                                        port=check['port'],
                                        password=check['password'],
                                        db=check['db']))

    mysql_checks = settings.HEALTHCHECKS_MYSQL
    for name, check in mysql_checks.items():
        checks.append(MysqlHealthcheck(check['name'],
                                        host=check['host'],
                                        port=check['port'],
                                        user=check['username'],
                                        password=check['password'],
                                        db=check['db']))

    hc = Healthchecks(checks)
    hc.run()
