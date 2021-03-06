from flask_sqlalchemy import SQLAlchemy as SA


class SQLAlchemy(SA):
    def apply_pool_defaults(self, app, options):
        options["pool_pre_ping"] = True
        SA.apply_pool_defaults(self, app, options)


db = SQLAlchemy()
