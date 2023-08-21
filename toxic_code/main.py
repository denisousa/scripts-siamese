from configurations import siamese_jar_path, properties_path, stackoverflow_path, qualitas_path
from ..siamese_indexing import execute_siamese_index

execute_siamese_index(siamese_jar_path, qualitas_path, properties_path)