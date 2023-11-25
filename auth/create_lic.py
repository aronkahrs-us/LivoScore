import base64
import json

class License:
    def __init__(self,encoding) -> None:
        self.encoding=encoding
        pass

    def create(self,user,token):
        test = {
            'user': user,
            'token': token
        }
        data_str=json.dumps(test).encode(self.encoding)
        data_b64=base64.b64encode(data_str)
        with open('auth/lic.lvs', 'w', encoding=self.encoding) as lic:
            lic.write(data_b64.decode(self.encoding))

    def read(self):
        with open('auth/lic.lvs', 'r', encoding=self.encoding) as lic:
            data = lic.read().encode(self.encoding)
            data = base64.b64decode(data).decode(self.encoding)
            data = json.loads(data)
            print(data)

lc=License('utf-16')
lc.create('Domovyk','Hz09eMQmv7j2e9LfxCkCwlYt10v8VHqW')
lc.read()