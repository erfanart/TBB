from outline_vpn.outline_vpn import OutlineVPN
import urllib3,time
from make_db import DbHandler
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)








class keys(OutlineVPN):  
    def __init__(self,url,cert) -> None:
        super().__init__(api_url=url,cert_sha256 = cert) 
        self.vpn = self.vpn(self)
        self.db = self.db("outline.db")
        pass 
    






    class vpn:
        def __init__(self,server) -> None:
            self.all = server.get_keys()


        def info(self,mode,value):
            self.keyratt = [] 
            for attr in dir(self.all[0]):
                if not callable(getattr(self.all[0], attr)) and not attr.startswith("__"):
                    self.keyratt += [attr]
            type(self).attrs = self.keyratt
            for attr in self.attrs:
                setattr(type(self), attr, self.get_key(mode,value)[self.attrs.index(attr)] )


        def get_key(self,attr,value):
            for key in self.all :
                if getattr(key , attr) == value:
                    return [getattr(key, att) for att in self.attrs]


        def check_usage(self,key):
            att = [att for att in key.keys()]
            usage = round(float(key["used_bytes"])/pow(10,9),3)
            limit = round(float(key["data_limit"])/pow(10,9),3) 
            db = keys.db("outline")
            if limit - usage < 0:
                key["status"]="limited"
            return key
                

        def check_date(self,key):
            print(key)

        def update(self):
            data = self.db.db.list_all_record("keys")
            colmuns = self.db.db.list_columns("keys")
            for d in data:
                key = {}
                for c in colmuns:
                    key[c] = f"{d[colmuns.index(c)]}"
                key = self.vpn.check_usage(key)
                key = self.vpn.check_date(key)
                # print(key)
                
                      
                
                

                







    class db:
        def __init__(self, database) -> None:
            self.db = DbHandler(database)
            self.tables = {
                "users" : {
                            "uid" : "TEXT",
                            "teleid":"TEXT",
                            "baleid":"TEXT",
                            "phone":"TEXT",
                            "email":"TEXT",
                        },
                "keys" : {
                            "access_url":"TEXT",
                            "data_limit":"TEXT",
                            "key_id":"TEXT",
                            "method":"TEXT",
                            "name":"TEXT",
                            "password":"TEXT",
                            "port":"TEXT",
                            "used_bytes":"TEXT",
                            "expire_date":"TEXT",
                            "status":"TEXT",
                        },
                "ownership":{
                            "keyid":"TEXT",
                            "manager":"TEXT",
                            "consumer":"TEXT",
                        },
                "payment":{
                            "uid":"TEXT",
                            "date":"TEXT",
                            "amount":"TEXT",
                            "methode":"TEXT",
                            "request":"TEXT",
                        },
            }






        def info(self,mode,table,value):
            self.query = self.db.list_column_query.format(table)
            self.all = self.db.list_all_record(table)
            self.attrs = [column[1] for column in self.db.select(self.query).fetchall()]
            try: 
                for attr in self.attrs:
                    setattr(self, attr, self.get_object(mode,value)[self.attrs.index(attr)] ) 
            except Exception as e:
                print("FOR ERROR :",e)



        def update_key(self,table,key):
            self.db.update(table=table,condition={"key_id": f'{key["key_id"]}'},data=key)



        def get_object(self,attr,value):
            try:
                for user in self.all: 
                    ins = user[self.attrs.index(attr)]
                    if ins == value:
                        return [user[self.attrs.index(col)] for col in self.attrs]
            except Exception as e :
                print(e)





        def make_db(self):
            for table in self.tables.keys():
                self.db.add_table(table)
                for column,type in self.tables[table].items():
                    self.db.add_column(table=table,name=column,data_type=type)






        def update(self):
            # print(2)
            for k in self.vpn.all:
                self.vpn.info("access_url",k.access_url)
                self.db.info(mode="key_id",table="keys",value=k.key_id)
                for a in  self.vpn.attrs:
                    self.db.db.update(table="keys",condition={"key_id": self.db.key_id }, data={a:f"{getattr(self.vpn, a)}"})
            type(self).vpn.update(self)    



    def update(self):
        # print(1)
        self.db.make_db()
        for k in self.vpn.all:
            self.vpn.info("key_id",k.key_id)
            key = {}
            for a in self.vpn.attrs:
                    key[a]= f"{getattr(self.vpn, a)}"
            self.db.db.add_record("keys",key,{"key_id" : key["key_id"]})
        type(self).db.update(self)


        

            


key = keys("https://77.237.73.68:31019/zHg5N7vdpw-7o16CbxCNNg","EB959607D6FDCD91240B216AEB276E7DB757D32D8423DEF9D78159F709E7817C")
key.update()
