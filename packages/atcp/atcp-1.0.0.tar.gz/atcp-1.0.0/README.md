# ATCP
The trick of this protocol is that its connection address has a path (atcp://example.com[:1614]/[...]) there are also several types of packages:
1. The PING server/client responds with PONG if the connection can be continued or CLOSE if it needs to be closed. It is sent every 10 seconds.
2. `PONG` - I've already told you.
3. `CLOSE` - also.
4. `MESSAGE <message>` - the message itself.
5. `PATH <The PATH STARTING FROM / >` is sent when the client connects.
6. `CONN <code>` is sent by the server after sending the PATH by the client (0 - successfully connected, 1 - connection error and connection closure) and by the opposite side when the other side is notified (0 - ok, -1 - error).
