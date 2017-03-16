import MySQLdb

#ONE MUST DO THIS FIRST: mysql -u user -p < voldemortdb.sql
db = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="p@ssword", db="voldemortdb")

cur = db.cursor()

#insert cycle (idcycle, date_start(mm-dd-yyyy format), time_start (hh:mm military time), date_end, time_end)
cur.execute("INSERT INTO cycle VALUES (%s,%s, %s, %s)")
#insert flow (idflow, idcycle, src_ip, dest_ip, protocol, service, packetflg, datasaize)
cur.execute("INSERT INTO flow VALUES (%d, %d, %s, %s, %s, %s, %s, %d)")
db.commit()
#returns all from cycle
cur.execute("SELECT * FROM cycle")
#returns all from flows
cur.execute("SELECT * FROM flows")
#returns src_ip and its suspicion count
cur.excecute("SELECT src_ip, count(src_ip) suspicion_count FROM flow GROUP BY src_ip") 
#returns total data size per protocol denoted by %s per cycle
cur.execute("SELECT f.idcycle, sum(datasize) datasize FROM flow f, cycle c, WHERE f.idcycle = c.idcycle and protocol like '%s0'")


db.close()

