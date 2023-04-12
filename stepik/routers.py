from django.contrib.auth.models import User
from django.db import OperationalError
import random

class DatabaseRouter:
   
    def db_for_read(self, model, **hints):
        
       
        return 'second_db' 
        # # return 'default'
        # return None
        return 'default'
    
    def db_for_write(self, model, **hints):
        from django.db import connections
        
        default_count = User.objects.using('default').count()
        
        second_count = User.objects.using('second_db').count()
        
        if second_count < default_count:
            return 'second_db'  
        else:
            return 'default'
        return 'default'
        #return 'default' if second_count > default_count else 'second_db'
    
        
    
    # def db_for_write(self, model, **hints):
    #     """
    #     Writes go to the database with fewer auth_user records.
    #     """   
    #     default_count = User.objects.using('default').count()
    #     second_count = User.objects.using('second_db').count()
    #     return 'second_db' if second_count < default_count else 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations between objects if they're both in the
        same database.
        """
        db1 = obj1._state.db
        db2 = obj2._state.db
        if db1 == 'default' and db2 == 'default':
            return True
        elif db1 == 'second_db' and db2 == 'second_db':
            return True
        else:
            return False
        
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the myapp2 app only appears in the 'myapp2'
        database.
        """
        # if app_label == 'myapp2':
        #     return db == 'second_db'
        # else:
        #     return True
        return None