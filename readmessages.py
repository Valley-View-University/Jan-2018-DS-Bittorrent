import struct
from pkgutil import get_data

from pip._vendor.requests.packages.urllib3.filepost import writer

from src.util import REQUEST_SIZE, LOG


class Peer(object):
    async def download(self, reader=None, consume_buffer=None, bitfield=None):
    # Start exchanging messages

        buf = b''
        while True:
            resp = await reader.read(REQUEST_SIZE)  # Suspends here if there's nothing to be read
            buf += resp

            while True:
                if len(buf) < 4:
                    break

                msg_message_length = self.get_message_message_length(buf)

                if msg_message_length == 0:
                    LOG.info('[Message] Keep Alive')
                    consume_buffer(buf)
                    continue

                msg_id = struct.unpack('>b', buf[4:5])  # 5th byte is the ID

                if msg_id == 0:
                    LOG.info('[Message] CHOKE')
                    consume_buffer(buf)

                elif msg_id == 1:
                    LOG.info('[Message] UNCHOKE')
                    consume_buffer(buf)

                elif msg_id == 5:
                    LOG.info('[Message] BITFIELD: {}'.format(bitfield))
                    data = get_data(buf)
                    self.process_bitfield(data)
                    await self.send_interested(writer)
                    consume_buffer(buf)

                elif msg_id == 7:
                    LOG.info('[Message] PIECE'.format(bitfield))
                    data = get_data(buf)
                    self.file_queue.enque(data)
                    consume_buffer(buf)

                else:
                    LOG.info('unknown ID {}'.format(msg_id))

                await self.request_a_piece(writer)



class Peer(object):
    async def download(self, piece_data=None, reader=None):
    # Start exchanging messages

        buf = b''
        while True:
            resp = await reader.read(REQUEST_SIZE)  # Suspends here if there's nothing to be read
            buf += resp

            while True:
                if len(buf) < 4:
                    break

                msg_message_length = self.get_message_message_length(buf)

                if msg_message_length == 0:
                    # Handle Keep Alive
                    continue

                msg_id = struct.unpack('>b', buf[4:5])  # 5th byte is the ID

                if msg_id == 0:
                    # Handle Choke...

                elif msg_id == 1:
                    # Handle Unchoke...
                    await self.send_interested_message()

                elif msg_id == 5:
                    # Handle bitfield

                elif msg_id == 7:
                    # Handle Piece...
                    self.file_queue.enqueue(piece_data)

                await self.request_a_piece(writer)


