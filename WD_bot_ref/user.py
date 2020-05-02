class user_from_bot():
    def __init__(self,
                 company='0',
                 name = '0',
                 mob_phone = '0',
                 number = '0',
                 type_face = '0',
                 address = '0',
                 final_settings = '0'):
        self.company = '0'
        self.name = '0'
        self.number = '0'
        self.type_face = '0'
        self.address = '0'
        self.final_settings = '0'

    def set_company(self, text):
        company = text

    def set_name(self, text):
        name = text

    def set_mob_phone(self, text):
        number = text

    def set_type_face(self, text):
        if text == '1':
            type_face = 'Юр.лицо'
        elif text == '2':
            type_face = 'Физ.лицо'
        else:
            type_face = ''

    def set_address(self, text):
        address = text

    def set_final_settings(self, text):
        final_settings = text

    def get_company(self, text):
        return self.company

    def get_name(self, text):
        return self.name

    def get_mob_phone(self, text):
        return self.number

    def get_type_face(self, text):
        return self.type_face

    def get_address(self, text):
        return self.address

    def get_final_settings(self, text):
        return self.final_settings

