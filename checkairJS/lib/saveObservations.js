/*
 *  This script is intended to be run by a cron job.
 *  It's purpose is to get a temperature value from a sensor and write it to a database.
 */
const db = require("./database");
const ds18b20 = require("./ds18b20");

module.exports.writeCurrentObstoDb = () => {
  let temp = ds18b20.getCurrentTemp();
  //console.log("temp: ", temp);
  //   var sql =
  //     "INSERT INTO observations ( type, sensor,location,value) VALUES ( 1, 1, 3, {temp})";
  var sql =
    "INSERT INTO observations (type, sensor,location,value) VALUES (?,?,?,?)";
  var params = [1, 1, 3, temp];
  db.run(sql, params, function (err, result) {
    if (err) {
      console.log("sql error ", err);
      return;
    }
    console.log("success");
  });

  return temp;
};

//export default writeCurrentObstoDb;
