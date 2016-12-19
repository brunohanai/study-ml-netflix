import omdb
from data_manager import insert_data

title = raw_input('Nome do filme/seriado: ')

omdb_info = omdb.title(title)

if len(omdb_info) == 0:
    print 'Informacoes nao encontradas.'
    exit()

print "Informacoes encontradas:"
print omdb_info

who = raw_input('Quem assistiu a esse filme? ')

insert_data(who, omdb_info)
