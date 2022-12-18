import datetime
import hashlib
import typing

import psycopg2
import psycopg2.extras

import settings as setting


class Db:
    def __init__(self):
        self.connection = psycopg2.connect(user=setting.DATABASE['login'],
                                           password=setting.DATABASE['password'],
                                           host=setting.DATABASE['ip'],
                                           port=5432)
        self.cur = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def insert_user(self, fio, post, organization, status, email, password) -> str or None:
        sql = """INSERT INTO public."user"(fio, post, organization, status, email, password)
                 VALUES(%s, %s, %s, %s, %s, %s) RETURNING id"""

        self.cur.execute(sql, (fio, post, organization, status, email, password))

        id = self.cur.fetchone()['id']
        hash_id = hashlib.sha256(str(id).encode()).hexdigest()

        sql = """UPDATE public."user" SET hash_id=%s WHERE id=%s"""
        self.cur.execute(sql, (hash_id, id,))

        self.connection.commit()
        return hash_id

    def select_user(self, email, password) -> int or None:
        sql = """SELECT id FROM public."user" WHERE email=%s AND password=%s"""

        self.cur.execute(sql, (email, password,))
        result = self.cur.fetchone()
        return dict(result).get('id') if result else None

    def select_user_id(self, id) -> int or None:
        sql = """SELECT fio, post, organization, status, email FROM public."user" WHERE id=%s"""
        self.cur.execute(sql, (id,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def select_user_info(self, token) -> int or None:
        sql = """SELECT fio, post, organization, status, email, password FROM public."user" WHERE hash_id=%s"""

        self.cur.execute(sql, (token,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def select_user_all_info(self, token) -> int or None:
        sql = """SELECT * FROM public."user" WHERE hash_id=%s"""

        self.cur.execute(sql, (token,))
        result = self.cur.fetchone()
        return dict(result) if result else None

    def insert_event(self, date_start, header, text, url):
        sql = """INSERT INTO public.event(date_start, header, text, url) VALUES (%s, %s, %s, %s) RETURNING id;"""
        date1 = datetime.datetime.fromisoformat(date_start.replace('Z', ''))
        self.cur.execute(sql, (date1, header, text, url,))
        self.connection.commit()
        return dict(self.cur.fetchone()).get('id')

    def update_event(self, id: str, date_start: str, header: str, text: str, url: str) -> bool:
        sql = """UPDATE public.event SET date_start=%s, header=%s, text=%s, url=%s WHERE id=%s"""
        date1 = datetime.datetime.fromisoformat(date_start.replace('Z', ''))
        self.cur.execute(sql, (date1, header, text, url, int(id),))
        self.connection.commit()
        return True

    def select_event(self, id) -> dict:
        sql = """SELECT * FROM public.event WHERE id=%s"""
        self.cur.execute(sql, (id,))
        result = self.cur.fetchone()
        if result is not None:
            result = dict(result)
            result['date_start'] = str(result['date_start'].isoformat())
        return result

    def delete_event(self, event_id: str or int) -> bool:
        event_id = int(event_id)
        sql = """DELETE FROM public.event WHERE id=%s;"""
        self.cur.execute(sql, (event_id,))
        self.connection.commit()
        return True

    def select_all_event(self) -> list:
        sql = """SELECT * FROM public.event"""
        self.cur.execute(sql)
        result = self.cur.fetchall()
        if result is not None:
            result = list(result)
            result = list(map(lambda x: dict(x), result))
            for i in result:
                i['date_start'] = str(i['date_start'].isoformat())
        return result

    def insert_member_event(self, event_id, token):

        if self.select_event(event_id) is None:
            return None
        user_id = self.select_user_all_info(token)
        if user_id is None:
            return None
        user_id = user_id.get("id")

        sql = """INSERT INTO public.event_member(event_id, user_id)VALUES (%s, %s);"""
        self.cur.execute(sql, (event_id, user_id,))
        self.connection.commit()
        return True

    def insert_steps_event(self, event_id, date_start: str, date_end, header: str, text: str, url: str) -> dict:
        sql = """INSERT INTO public.steps_event(event_id, date_start, date_end, header, text, url)VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"""
        self.cur.execute(sql, (event_id, date_start, date_end, header, text, url,))
        self.connection.commit()
        return dict(self.cur.fetchone())

    def select_steps_event(self, event_id, token) -> dict:
        sql = """SELECT * FROM steps_event WHERE event_id=%s ORDER BY date_start ASC;"""
        self.cur.execute(sql, (int(event_id),))
        self.connection.commit()
        result = self.cur.fetchall()
        if result is not None:
            result = list(result)
            result = list(map(lambda x: dict(x), result))
            for i in result:
                i['date_start'] = str(i['date_start'].isoformat())
                i['date_end'] = str(i['date_end'].isoformat())
        return result

    def update_step_event(self, event_id, step_id, date_start: str, date_end, header: str, text: str, url: str) -> bool:
        sql = """UPDATE steps_event SET date_start=%s, date_end=%s,header=%s, text=%s, url=%s WHERE event_id=%s AND id=%s;"""
        self.cur.execute(sql, (date_start, date_end, header, text, url, int(event_id), int(step_id)))
        self.connection.commit()
        return True

    def delete_step_event(self, event_id, step_id) -> bool:
        sql = """DELETE FROM public.steps_event WHERE event_id=%s AND id=%s;"""
        self.cur.execute(sql, (int(event_id), int(step_id),))
        self.connection.commit()
        return True

    def select_event_members(self, event_id) -> bool:
        sql = """SELECT * FROM public.event_member WHERE event_id=%s;"""
        self.cur.execute(sql, (int(event_id),))

        result = []
        for i in self.cur.fetchall():
            i = dict(i)
            user_info = self.select_user_id(i['user_id'])
            del i['user_id']
            i.update({"user": user_info})
            result.append(i)

        return result

    def select_user_event(self, token) -> bool:
        user_id = self.select_user_all_info(token)['id']

        sql = """SELECT * FROM public.event_member WHERE user_id=%s;"""
        self.cur.execute(sql, (int(user_id),))

        result = []
        for i in self.cur.fetchall():
            i = dict(i)
            user_info = self.select_event(i['event_id'])
            del i['user_id']
            i.update({"event_info": user_info})
            result.append(i)

        return result

    def delete_truncate_member_event(self, event_id,) -> bool:
        sql = """DELETE FROM public.event_member WHERE event_id=%s;"""
        self.cur.execute(sql, (int(event_id),))
        self.connection.commit()
        return True

    def delete_member_self_remove(self, event_id, token) -> bool:
        user = self.select_user_all_info(token)
        sql = """DELETE FROM public.event_member WHERE event_id=%s AND user_id=%s;"""
        self.cur.execute(sql, (int(event_id), int(user['id']),))
        self.connection.commit()
        return True
