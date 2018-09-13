import sys

class Healthcheck:

    def __init__(self):
        self.type = None

    def run(self):
        raise NotImplementedError()


class MysqlHealthcheck(Healthcheck):

    def __init__(self, name):
        super(Healthcheck, self).__init__()
        self.name = name
        self.type = "mysql"

    def run(self):
        print("Name: {} - Type: {}".format(self.name, self.type))
        return True


class RedisHealthcheck(Healthcheck):

    def __init__(self, name):
        super(Healthcheck, self).__init__()
        self.name = name
        self.type = "redis"

    def run(self):
        print("Name: {} - Type: {}".format(self.name, self.type))
        return True


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
        checks.append(RedisHealthcheck(check['name']))

    mysql_checks = settings.HEALTHCHECKS_MYSQL
    for name, check in mysql_checks.items():
        checks.append(MysqlHealthcheck(check['name']))

    hc = Healthchecks(checks)
    hc.run()
