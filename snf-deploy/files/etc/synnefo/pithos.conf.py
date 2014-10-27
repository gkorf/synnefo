# -*- coding: utf-8 -
#
# Copyright (C) 2010-2014 GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import pickle
import os
from synnefo.pithos.workers import glue
from multiprocessing import Lock


def find_hole(WORKERS, FOLLOW_WORKERS):
    old_key = []
    old_age = []
    for key in FOLLOW_WORKERS:
        if key not in WORKERS.keys():
                old_age.append(FOLLOW_WORKERS[key])
                old_key.append(key)
                break
    if len(old_age) and len(old_key):
        for key in old_key:
            del FOLLOW_WORKERS[key]
        return old_age
    return old_age


def follow_workers(pid, wid, WORKERS):
    hole = None
    if os.path.isfile('/dev/shm/wid'):
        fd = open('/dev/shm/wid', 'rb')
        f = pickle.load(fd)
        hole = find_hole(WORKERS, f)
        if len(hole) > 0:
            k = {pid: int(hole[0])}
        else:
            k = {pid: wid}
        f.update(k)
        fd.close()
        fd = open('/dev/shm/wid', 'wb')
        pickle.dump(f, fd)
        fd.close()
    else:
        fd = open('/dev/shm/wid', 'wb')
        pickle.dump({pid: wid}, fd)
        fd.close()
    return hole


def allocate_wid(pid, wid, WORKERS):
    hole = None
    hole = follow_workers(pid, wid, WORKERS)
    return hole


def when_ready(server):
    server.lock = Lock()


def update_workers(pid, wid):
    if os.path.isfile('/dev/shm/wid'):
        fd = open('/dev/shm/wid', 'rb')
        f = pickle.load(fd)
        for k, v in f.items():
            if wid == v:
                del f[k]
                break
        k = {pid: wid}
        f.update(k)
        fd.close()
        fd = open('/dev/shm/wid', 'wb')
        pickle.dump(f, fd)
        fd.close()
    else:
        fd = open('/dev/shm/wid', 'wb')
        pickle.dump({pid: wid}, fd)
        fd.close()


def resize_workers(no_workers):
    if os.path.isfile('/dev/shm/wid'):
        fd = open('/dev/shm/wid', 'rb')
        f = pickle.load(fd)
        for k, v in f.items():
            if v > no_workers:
                del f[k]
        fd.close()
        fd = open('/dev/shm/wid', 'wb')
        pickle.dump(f, fd)
        fd.close()


def post_fork(server, worker):
    server.lock.acquire()
    if worker.worker_id <= server.num_workers:
        update_workers(worker.pid, worker.worker_id)
        glue.WorkerGlue.setmap(worker.pid, worker.worker_id)
    else:
        wid = allocate_wid(worker.pid, worker.worker_id, server.WORKERS)
        glue.WorkerGlue.setmap(worker.pid, wid[0])
    resize_workers(server.num_workers)
    server.lock.release()


def worker_exit(server, worker):
    if glue.WorkerGlue.ioctx_pool:
        glue.WorkerGlue.ioctx_pool._shutdown_pool()


def on_exit(server):
    os.unlink('/dev/shm/wid')
