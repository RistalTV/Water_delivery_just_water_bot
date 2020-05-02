import pymysql

conn = pymysql.connect('localhost', 'root', 'root', 'user_orders')


# def ensure_connection(func):
#     """ Декоратор для подключения к СУБД: открывает соединение,
#         выполняет переданную функцию и закрывает за собой соединение.
#         Потокобезопасно!
#     """
#
#     def inner(*args, **kwargs):
#
#             kwargs['conn'] = conn
#
#             res = func(*args, **kwargs)
#         return res
#         # with sqlite3.connect('data_users.db') as conn:
#         #     kwargs['conn'] = conn
#         #     res = func(*args, **kwargs)
#         # return res
#
#     return inner


# @ensure_connection

def add_info_of_user(user_id: int, username: str, company: str, address: str, address_city: str, mob_phone: str):
    with conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO `users` (`id`, `user_id`, `username`, `company`, `user_address`, `address_city`, `mob_phone`) values (NONE,'%d','%s','%s','%s','%s','%s')" %
            (user_id, username, company, address, address_city, mob_phone)
        )
        conn.commit()


# @ensure_connection
def add_order_of_user(user_id: int, order_1: int, order_2: int, order_3: int, ):
    with conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO `orders` (`id`, `user_id`, `data`, `order_1`, `order_2`, `order_3`) VALUES (NULL, {0}, CURRENT_TIMESTAMP, {1}, {2}, {3})".format(
                user_id, order_1, order_2, order_3))
        conn.commit()


def remove_info_of_user(us_id: int, user_id: int):
    with conn:
        c = conn.cursor()
        c.execute(
            "DELETE FROM `users` WHERE `users`.`id` = {0} AND `users`.`user_id`= {1}})".format(
                us_id, user_id))
        conn.commit()


def remove_order_of_user(us_id: int, user_id: int):
    with conn:
        c = conn.cursor()
        if us_id == 0:
            us_id = None
        c.execute(
            "DELETE FROM `order` WHERE `order`.`id` = {0} AND `order`.`user_id`= {1})".format(
                us_id, user_id))
        conn.commit()


# @ensure_connection
def exits_user(user_id: int):
    with conn:
        c = conn.cursor()
        c.execute("SELECT * FROM `users` WHERE user_id = {0} LIMIT 1".format(user_id))
        res = list(c.fetchall())
        print(res)
        if not res:
            return None
    return res
