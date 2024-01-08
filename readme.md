## Start

1. build db server
```
docker-compose up -d
```

2. create_table
```
cd app_server
python create_tables.py
```

3. build main server
```
cd app_server
streamlit run main_server.py --server.port 50000
```

4. build management server
```
cd app_server
streamlit run management_server.py --server.port 50001
```

## ReStart
```
execute Step 1, 3, 4  
```
