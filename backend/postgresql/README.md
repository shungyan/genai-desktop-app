## 🧩 Step 1. Switch to the PostgreSQL system user

When PostgreSQL is installed, it creates a special Linux user called **`postgres`**.

In your WSL terminal, run:

```
sudo -i -u postgres
```

You’ll notice your prompt changes to something like:

```
postgres@your-wsl:~$
```

✅ You are now the **PostgreSQL admin user** (at the Linux level).

---
- ## 🧠 Step 2. Enter the PostgreSQL interactive shell ( `psql` )
  
  Run:
  
  ```
  psql
  ```
  
  You should now see:
  
  ```
  psql (16.x)
  Type "help" for help.
  
  postgres=#
  ```
  
  This means you’re inside the **PostgreSQL shell** (ready to run SQL commands).
  
  ---
- ## 👤 Step 3. Create a new PostgreSQL user (role)
  
  Let’s make your own database user.
  
  Run this inside the `psql` shell:
  
  ```
  CREATE USER myuser WITH PASSWORD 'mypassword';
  ```
  
  You’ll see:
  
  ```
  CREATE ROLE
  ```
  
  ✅ You just created a PostgreSQL user named **`myuser`**.
  
  ---
- ## 🗃️ Step 4. Create a new database
  
  Now create your own database:
  
  ```
  CREATE DATABASE mydb OWNER myuser;
  ```
  
  This creates a new database called `mydb` and sets `myuser` as its owner.
  
  ---
- ## 🔁 Step 5. Connect (switch) to that database
  
  Run:
  
  ```
  \c mydb
  ```
  
  You should see:
  
  ```
  You are now connected to database "mydb" as user "postgres".
  mydb=#
  ```
  
  ✅ You’re now *inside* your new database.
  
  ---
- ## 🧱 Step 6. Create a table
  
  Let’s create a table to store chat messages.
  
  ```
  CREATE TABLE conversations (
  id SERIAL PRIMARY KEY,
  sender VARCHAR(50),
  message TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
  
  You’ll see:
  
  ```
  CREATE TABLE
  ```
  
  ✅ Table created successfully.
  
  ---
- ## 💬 Step 7. Insert sample data
  
  Add a few test messages:
  
  ```
  INSERT INTO conversations (sender, message)
  VALUES ('user', 'Hello!'), ('bot', 'Hi there! How can I help?');
  ```
  
  You’ll see:
  
  ```
  INSERT 0 2
  ```
  
  ✅ Two rows inserted.
  
  ---
- ## 🔍 Step 8. Query the table
  
  Now read (select) the data back:
  
  ```
  SELECT * FROM conversations;
  ```
  
  You’ll see something like:
  
  ```
  id | sender |          message           |         created_at
  ----+--------+----------------------------+----------------------------
  1 | user   | Hello!                     | 2025-10-14 15:10:21.123456
  2 | bot    | Hi there! How can I help?  | 2025-10-14 15:10:21.123456
  (2 rows)
  ```
  
  ---
- ## 🧾 Step 9. List tables (to confirm)
  
  ```
  \dt
  ```
  
  Output:
  
  ```
  List of relations
  Schema |     Name      | Type  |  Owner
  --------+---------------+-------+----------
  public | conversations | table | myuser
  (1 row)
  ```
  
  ---
- ## 🧠 Step 10. List all databases (optional)
  
  From anywhere in `psql`, run:
  
  ```
  \l
  ```
  
  You’ll see something like:
  
  ```
  Name   |  Owner   | Encoding | Collate | Ctype | Access privileges
  ----------+-----------+----------+---------+--------+-------------------
  mydb     | myuser    | UTF8     | ...     | ...   |
  postgres | postgres  | UTF8     | ...     | ...   |
  template1| postgres  | UTF8     | ...     | ...   |
  ```
  
  ---
- ## 🚪 Step 11. Exit  `psql`
  
  Type:
  
  ```
  \q
  ```
  
  You’ll return to your Linux shell.
  
  ---
- ## 🔙 Step 12. Exit from postgres user
  
  Type:
  
  ```
  exit
  ```
  
  Now you’re back to your normal WSL user.