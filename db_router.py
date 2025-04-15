# project/db_router.py
class SchoolScoreRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'loginPage':
            return 'school_score'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'loginPage':
            return 'school_score'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'loginPage':
            return db == 'school_score'
        return None
