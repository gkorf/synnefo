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

from binascii import hexlify
import ctypes
import ConfigParser
import logging

from archipelago.common import (
    Request,
    xseg_reply_map,
    xseg_reply_map_scatterlist,
    string_at,
    XF_ASSUMEV0,
    XF_MAPFLAG_READONLY,
    )

from pithos.workers import (
    glue,
    monkey,
    )

monkey.patch_Request()

logger = logging.getLogger(__name__)


class ArchipelagoMapper(object):
    """Mapper.
       Required constructor parameters: namelen.
    """

    namelen = None

    def __init__(self, **params):
        self.params = params
        self.namelen = params['namelen']
        cfg = ConfigParser.ConfigParser()
        cfg.readfp(open(params['archipelago_cfile']))
        self.ioctx_pool = glue.WorkerGlue.ioctx_pool
        self.dst_port = int(cfg.getint('mapperd', 'blockerm_port'))
        self.mapperd_port = int(cfg.getint('vlmcd', 'mapper_port'))

    def map_retr(self, maphash, size):
        """Return as a list, part of the hashes map of an object
           at the given block offset.
           By default, return the whole hashes map.
        """
        hashes = ()
        ioctx = self.ioctx_pool.pool_get()
        req = Request.get_mapr_request(ioctx, self.mapperd_port,
                                       maphash, offset=0, size=size)
        flags = req.get_flags()
        flags |= XF_ASSUMEV0
        req.set_flags(flags)
        req.submit()
        req.wait()
        ret = req.success()
        if ret:
            data = req.get_data(xseg_reply_map)
            Segsarray = xseg_reply_map_scatterlist * data.contents.cnt
            segs = Segsarray.from_address(ctypes.addressof(data.contents.segs))
            hashes = [string_at(segs[idx].target, segs[idx].targetlen)
                      for idx in xrange(len(segs))]
            req.put()
        else:
            req.put()
            self.ioctx_pool.pool_put(ioctx)
            raise Exception("Could not retrieve Archipelago mapfile.")
        req = Request.get_close_request(ioctx, self.mapperd_port,
                                        maphash)
        req.submit()
        req.wait()
        ret = req.success()
        if ret is False:
            logger.warning("Could not close map %s" % maphash)
            pass
        req.put()
        self.ioctx_pool.pool_put(ioctx)
        return hashes


    def map_stor(self, maphash, hashes, size, block_size):
        """Store hashes in the given hashes map."""
        objects = list()
        for h in hashes:
            objects.append({'name': hexlify(h), 'flags': XF_MAPFLAG_READONLY})
        ioctx = self.ioctx_pool.pool_get()
        req = Request.get_create_request(ioctx, self.mapperd_port,
                                         maphash,
                                         mapflags=XF_MAPFLAG_READONLY,
                                         objects=objects, blocksize=block_size,
                                         size=size)
        req.submit()
        req.wait()
        ret = req.success()
        if ret is False:
            req.put()
            self.ioctx_pool.pool_put(ioctx)
            raise IOError("Could not write map %s" % maphash)
        req.put()
        self.ioctx_pool.pool_put(ioctx)
