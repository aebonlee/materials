docker exec -i pg psql -U postgres << 'EOF'
CREATE TABLE sensor (id serial PRIMARY KEY, name text, value numeric);
INSERT INTO sensor (name, value) VALUES ('temp', 21.5), ('humidity', 48.2);
SELECT * FROM sensor;
EOF
