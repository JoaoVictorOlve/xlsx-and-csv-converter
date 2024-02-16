import datetime
import uuid

filename = "Base.-do-Excel.xlsx"

datetime_name = str(datetime.datetime.now().date()).replace('-', '_') + '_' + str(datetime.datetime.now().time()).replace(':', '_').replace('.', '_')
uuid_name = uuid.uuid4().hex
unique_filename = f"{datetime_name}_{uuid_name}-{filename}"

print(unique_filename.rsplit(".", 1))