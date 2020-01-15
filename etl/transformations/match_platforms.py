import py_stringsimjoin as ssj
import py_stringmatching as sm
import pandas as pd

from utilities import engine

with engine.connect() as connection:
  g_platforms = pd.read_sql_query(
    ''' 
    SELECT id, name FROM giantbomb.stage_platforms
    ''',
    connection
  )

  m_platforms = pd.read_sql_query(
    '''
    SELECT DISTINCT platform as name FROM metacritic.stage_games
    ''',
    connection
  )

  # create key attribute
  m_platforms['id'] = range(0, len(m_platforms))

  i_platforms = pd.read_sql_query(
    ''' 
    SELECT 
      id,
      TRIM(regexp_replace(name, '\(.*\)', '')) as name -- removes abbreviations in paranthesis
    FROM igdb.stage_platforms;
    ''',
    connection
  )

  ### Matching

  g_platforms['ws_name'] = g_platforms['name']
  i_platforms['ws_name'] = i_platforms['name']
  g_platforms['name'] = g_platforms['name'].str.replace(" ", "")
  i_platforms['name'] = i_platforms['name'].str.replace(" ", "")

  i_platforms.loc[i_platforms.name == 'NintendoGameCube', 'name'] = 'GameCube'
  i_platforms.loc[i_platforms.name == 'CommodorePET', 'name'] = 'CommodorePET/CBM'
  i_platforms.loc[i_platforms.name == 'PCDOS', 'name'] = 'PC' #multiple matches, drop_duplicates necessary!
  g_platforms.loc[g_platforms.name == 'Commodore64', 'name'] = 'CommodoreC64/128'
  g_platforms.loc[g_platforms.name == 'Commodore128', 'name'] = 'CommodoreC64/128'
  g_platforms.loc[g_platforms.name == 'Genesis', 'name'] = 'SegaMegaDrive/Genesis'
  g_platforms.loc[g_platforms.name == 'Saturn', 'name'] = 'SegaSaturn'
  g_platforms.loc[g_platforms.name == 'Nintendo3DSeShop', 'name'] = 'Nintendo3DS'
  g_platforms.loc[g_platforms.name == 'NintendoeShop', 'name'] = 'Nintendo'
  g_platforms.loc[g_platforms.name == 'Jaguar', 'name'] = 'AtariJaguar'
  g_platforms.loc[g_platforms.name == 'TurboGrafx-CD', 'name'] = 'Turbografx-16/PCEngineCD'
  g_platforms.loc[g_platforms.name == 'TurboGrafx-16', 'name'] = 'TurboGrafx-16/PCEngine'

  matching_pairs = ssj.edit_distance_join(
    g_platforms, i_platforms, 
    'id', 'id', 
    'name', 'name',
    0, 
    l_out_attrs=['ws_name'], r_out_attrs=['ws_name'],
    l_out_prefix='giantbomb_', r_out_prefix='igdb_'
  )

  matching_pairs.to_sql('platforms', engine, schema='matching', if_exists='replace', index=False)


  # ### Joining

  giantbomb_merged = matching_pairs.merge(
     g_platforms, left_on='giantbomb_id', right_on='id', how='outer'
  )
  giantbomb_merged['giantbomb_id'] = giantbomb_merged['id']
  giantbomb_merged['giantbomb_name'] = giantbomb_merged['name']

  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Commodore 64', 'ws_name'] = 'Commodore C64/128'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Commodore 128', 'ws_name'] = 'Commodore C64/128'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Genesis', 'ws_name'] = 'Sega Mega Drive/Genesis'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Saturn', 'ws_name'] = 'Sega Saturn'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Jaguar', 'ws_name'] = 'Atari Jaguar'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Nintendo 3DS eShop', 'ws_name'] = 'Nintendo 3DS'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'Nintendo eShop', 'ws_name'] = 'Nintendo'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'TurboGrafx-CD', 'ws_name'] = 'Turbografx-16/PC Engine CD'
  giantbomb_merged.loc[giantbomb_merged.ws_name == 'TurboGrafx-16', 'ws_name'] = 'Turbografx-16/PC Engine'
  #TODO: better manual matching?

  for i in giantbomb_merged['ws_name']:
    if i in "Nintendo 3DS eShop":
      print(i)

  igdb_merged = matching_pairs.merge(
     i_platforms, left_on='igdb_id', right_on='id', how='outer'
   )
  igdb_merged['igdb_id'] = igdb_merged['id']
  igdb_merged['igdb_name'] = igdb_merged['name']
  igdb_merged = igdb_merged[igdb_merged.giantbomb_id.isnull()]

  merged = pd.concat([giantbomb_merged, igdb_merged], sort=False, ignore_index=True)
  merged = merged[['ws_name', 'igdb_id', 'giantbomb_id']]

  merged.to_sql('platforms', engine, schema='lookup', if_exists='replace', index_label='id')
  
  # Integrate Metacritic dataset

  merged_platforms = pd.read_sql_query(
    ''' 
    SELECT * FROM lookup.platforms
    ''',
    connection
  )

  merged_platforms['name'] = merged_platforms['ws_name'].str.replace(" ", "")

  m_platforms.loc[m_platforms.name == 'DS', 'name'] = 'NintendoDS'
  m_platforms.loc[m_platforms.name == '3DS', 'name'] = 'Nintendo3DS'
  m_platforms.loc[m_platforms.name == 'PSP', 'name'] = 'PlayStationPortable'
  m_platforms.loc[m_platforms.name == 'Switch', 'name'] = 'NintendoSwitch'

  matching_pairs2 = ssj.edit_distance_join(
  merged_platforms,  m_platforms,
  'id', 'id', 
  'name', 'name', 
  0, 
  l_out_attrs=['name','ws_name', 'giantbomb_id', 'igdb_id'], r_out_attrs=['name'],
  l_out_prefix='lookup_', r_out_prefix='metacritic_'
  )

  matching_pairs2 = matching_pairs2[['_id', 'lookup_giantbomb_id', 'lookup_igdb_id', 'lookup_name', 'metacritic_name', 'lookup_ws_name', '_sim_score']]
  matching_pairs2 = matching_pairs2.rename({'lookup_giantbomb_id': 'giantbomb_id', 'lookup_igdb_id': 'igdb_id'}, axis=1)
  
  merged_matching = matching_pairs.merge(
    matching_pairs2, left_on='giantbomb_id', right_on='giantbomb_id', how='outer'
  )

  merged_matching = merged_matching[['_id_x', 'giantbomb_id', 'igdb_id_x', 'giantbomb_ws_name', 'igdb_ws_name', 'metacritic_name']]
  merged_matching = merged_matching.rename({'_id_x': 'id', 'igdb_id_x': 'igdb_id'}, axis=1)
  merged_matching = merged_matching.drop_duplicates()
  merged_matching.to_sql('platforms', engine, schema='matching', if_exists='replace', index=False)

  # Lookup Table

  merged_lookup = merged_platforms.merge(
   merged_matching, left_on='giantbomb_id', right_on='giantbomb_id', how='outer'
  )
  merged_lookup = merged_lookup[['id_x', 'ws_name', 'igdb_id_x', 'giantbomb_id', 'metacritic_name']]
  merged_lookup = merged_lookup.rename({'id_x': 'id', 'ws_name' : 'name', 'igdb_id_x': 'igdb_id'}, axis=1)
  merged_lookup = merged_lookup.drop_duplicates()

  duplicateRows = merged_lookup[merged_lookup.duplicated(['name'],keep=False)]

  merged_lookup = merged_lookup.drop_duplicates(['name'], keep='first')
 
  
  i_id = -1
  g_id = -1
  m_id = -1
  dic = dict()

  for name,igdb_id,giantbomb_id,metacritic_name in zip(duplicateRows['name'],duplicateRows['igdb_id'],duplicateRows['giantbomb_id'],duplicateRows['metacritic_name']):
    if igdb_id == i_id:
      dic[name] = 'igdb_id'
    if giantbomb_id == g_id:
      dic[name] = 'giantbomb_id'
    if metacritic_name == m_id:
      dic[name] = 'metacritic_name'
    i_id=igdb_id
    g_id=giantbomb_id
    m_id=metacritic_name
  
  for x,y in dic.items():
    duplicate = duplicateRows.loc[duplicateRows['name']==x]
    duplicate['igdb_id'] = duplicate['igdb_id'].astype(int)
    duplicate['giantbomb_id'] = duplicate['giantbomb_id'].astype(int)
    if x in "PC":
      duplicateAgg = duplicate.groupby('name').igdb_id
      duplicateAgg = pd.concat([duplicateAgg.apply(list), duplicateAgg.count()], axis=1, keys=['igdb_id', 'number'])
    if x in "Commodore C64/128":
      duplicateAgg2 = duplicate.groupby('name').giantbomb_id
      duplicateAgg2 = pd.concat([duplicateAgg2.apply(list), duplicateAgg2.count()], axis=1, keys=['giantbomb_id', 'number'])

  for id in duplicateAgg['igdb_id']:
    merged_lookup.loc[merged_lookup.name=='PC', 'igdb_id'] = ",".join(map(str, id))
  for id in duplicateAgg2['giantbomb_id']:
    merged_lookup.loc[merged_lookup.name=='Commodore C64/128', 'giantbomb_id'] = ",".join(map(str, id))

  merged_lookup.loc[merged_lookup.metacritic_name == 'NintendoDS', 'metacritic_name'] = 'DS'
  merged_lookup.loc[merged_lookup.metacritic_name == 'Nintendo3DS', 'metacritic_name'] = '3DS'
  merged_lookup.loc[merged_lookup.metacritic_name == 'PlayStationPortable', 'metacritic_name'] = 'PSP'
  merged_lookup.loc[merged_lookup.metacritic_name == 'NintendoSwitch', 'metacritic_name'] = 'Switch'
  print(merged_lookup)

  #Somehow doesn't work -> takes forever. Instead table is dropped first and then merged_lookup is inserted
  #merged_lookup.to_sql('platforms', engine, schema='lookup', if_exists='replace', index_label='id')
  connection.execute(
    """
    DROP TABLE IF EXISTS lookup.platforms;
    """
  )

  merged_lookup.to_sql('platforms', engine, schema='lookup', if_exists='replace', index=False)

  ### CREATE FACT TABLE

  connection.execute(
    """
    DROP TABLE IF EXISTS platforms;
    CREATE TABLE platforms (
      id int NOT NULL PRIMARY KEY,
      name varchar(255)
    );
    INSERT INTO platforms
    SELECT id, name
    FROM lookup.platforms;
    """
  )

  connection.close()