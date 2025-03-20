import filelock


class Flock():
    map = None

    @staticmethod
    def init(lock_key, timeout=5):
        if(Flock.map is None): Flock.map = {}
        lock = filelock.FileLock(lock_key, timeout=timeout)
        Flock.map[lock_key] = lock

    @staticmethod
    def lock(lock_key, timeout = 5):
        """
        获取锁
        :param lock_key:
        :param timeout:
        :return:
        """
        return Flock.map[lock_key].acquire(timeout)

    @staticmethod
    def unlock(lock_key):
        return Flock.map[lock_key].release()
