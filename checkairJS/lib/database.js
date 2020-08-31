var sqlite3 = require("sqlite3").verbose();

const DBSOURCE = "db.sqlite";

// observation
//  - id
//  - timestamp
//  - type
//  - sensor_location
//  - value

let db = new sqlite3.Database(DBSOURCE, (err) => {
  if (err) {
    // Cannot open database
    console.error(err.message);
    throw err;
  } else {
    console.log("Connected to the SQLite database.");
    db.run(
      `CREATE TABLE observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            type INT, 
            sensor INT,
            location INT,
            value NUM 
            )`,
      (err) => {
        if (err) {
          // Table already created
          console.log("Table already created");
          //   var insert =
          //     " INSERT INTO observations (type, sensor, location, value) VALUES (?,?,?,?,?)";
          //   db.run(insert, [1, 1, 1, 66]);
        } else {
          console.log("database good to go");
          // Table just created, creating some rows
          // var insert = 'INSERT INTO user (name, email, password) VALUES (?,?,?)'
          // db.run(insert, ["admin","admin@example.com",md5("admin123456")])
          // db.run(insert, ["user","user@example.com",md5("user123456")])
          //   var insert =
          //     " INSERT INTO observations (timestamp, type sensor, location, value) VALUES (?,?,?,?,?)";
          //   db.run(insert, [Date.now(), 1, 1, 1, 66]);
          // }
        }
      }
    );
  }
});

module.exports = db;
