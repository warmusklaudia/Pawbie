from .Database import Database


class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens

    @staticmethod
    def read_last_time_ate():
        sql = "SELECT dayname(Actiedatum) as Dag, Concat(hour(Actiedatum), ':', minute(Actiedatum)) as Uur FROM Historiek WHERE ActieID = 5 ORDER BY Volgnummer DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_last_time_drank():
        sql = "SELECT dayname(Actiedatum) as Dag, Concat(hour(Actiedatum), ':', minute(Actiedatum)) as Uur FROM Historiek WHERE ActieID = 4 ORDER BY Volgnummer DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_last_value_fsr_food():
        sql = "SELECT Waarde FROM Historiek WHERE ActieID = 3 ORDER BY Volgnummer DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def read_last_value_fsr_water():
        sql = "SELECT Waarde FROM Historiek WHERE ActieID = 2 ORDER BY Volgnummer DESC LIMIT 1"
        return Database.get_one_row(sql)

    @staticmethod
    def update_status_actuator(id, status):
        sql = "UPDATE Device SET Status = %s WHERE DeviceID = %s AND Type = 'Actuator'"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_voederschema_food():
        sql = "SELECT TIME_FORMAT(CONVERT(Uur, char), '%H:%i') as Uur, Hoeveelheid FROM Voederschema WHERE ActieID = 6"
        return Database.get_rows(sql)

    @staticmethod
    def read_voederschema_water():
        sql = "SELECT TIME_FORMAT(CONVERT(Uur, char), '%H:%i') as Uur, Hoeveelheid FROM Voederschema WHERE ActieID = 7"
        return Database.get_rows(sql)

    @staticmethod
    def read_voederschema(id):
        sql = "SELECT TIME_FORMAT(CONVERT(Uur, char), '%H:%i') as Uur, Hoeveelheid FROM Voederschema WHERE ActieID = 6 and Volgnr = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def read_drankschema(id):
        sql = "SELECT TIME_FORMAT(CONVERT(Uur, char), '%H:%i') as Uur, Hoeveelheid FROM Voederschema WHERE ActieID = 7 and Volgnr = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_schema(uur, hoeveelheid, volgnr):
        sql = "UPDATE Voederschema SET Uur = %s, Hoeveelheid = %s WHERE Volgnr = %s "
        params = [uur, hoeveelheid, volgnr]
        return Database.execute_sql(sql, params)

    @staticmethod
    def add_historiek(deviceid, actieid, actiedatum, waarde):
        sql = "INSERT INTO Historiek (DeviceID, ActieID, Actiedatum, Waarde) "
        sql += "VALUES (%s, %s, %s, %s)"
        params = [deviceid, actieid, actiedatum, waarde]
        return Database.execute_sql(sql, params)
