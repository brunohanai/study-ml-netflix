import omdb
from data_manager import insert_data
from data_manager import title_is_in_database

title = raw_input('Nome do filme/seriado: ')

omdb_info = omdb.title(title)

if len(omdb_info) == 0:
    print 'Informacoes nao encontradas.'
    exit()

print "Informacoes encontradas:"
print omdb_info

if title_is_in_database(omdb_info['title']) == True:
    print "\nEsse filme/seriado ja esta no banco de dados. Saindo..."
    exit()

who = raw_input("\nQuem assistiu a esse filme? ")

insert_data(who, omdb_info)
