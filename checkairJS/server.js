// Create express app
var express = require("express");
var app = express();
var observations = require("./routes/observations");

// Server port
var HTTP_PORT = 8000;
// Start server
app.listen(HTTP_PORT, () => {
  console.log("Server running on port %PORT%".replace("%PORT%", HTTP_PORT));
});

// Root endpoint
app.get("/", (req, res, next) => {
  res.json({ message: "Ok" });
});

app.get("/current/", observations.getCurrentObservations);
// app.get("/current/", (req, res) => {
//         res.json({ temp: 72 });
// });

// Default response for any other request
app.use(function (req, res) {
  res.status(404);
});
