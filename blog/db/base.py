import queue
import threading

from django.db.backends.sqlite3.base import DatabaseWrapper as DB

_alias_2_pool = {}
_lock = threading.Lock()


class DatabaseWrapper(DB):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.alias not in _alias_2_pool:
            with _lock:
                if self.alias not in _alias_2_pool:
                    conn_params = self.get_connection_params()
                    pool_size = conn_params.pop("POOLSIZE", 10)
                    pool = queue.Queue(maxsize=pool_size)
                    while not pool.full():
                        # 创建connection使用原始的get_new_connection函数
                        conn = self.get_new_connection(conn_params)
                        pool.put(conn)
                    _alias_2_pool[self.alias] = pool
        self._pool = _alias_2_pool[self.alias]
        # 替换掉原始的get_new_connection函数
        self.get_new_connection = lambda conn_params: self._pool.get()

    def _close(self):
        if self.connection is not None:
            self._pool.put(self.connection)
