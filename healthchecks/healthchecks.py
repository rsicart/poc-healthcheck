import sys

class Healthcheck:

    def __init__(self, name):
        self.name = name

    def run(self):
        print(self.name)
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

    redis_checks = settings.HEALTHCHECKS_REDIS

    checks = []
    for name, check in redis_checks.items():
        checks.append(Healthcheck(check['name']))

    mysql_checks = settings.HEALTHCHECKS_MYSQL
    for name, check in mysql_checks.items():
        checks.append(Healthcheck(check['name']))

    hc = Healthchecks(checks)
    hc.run()
