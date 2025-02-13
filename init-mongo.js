// init-mongo.js

db = db.getSiblingDB(process.env.DATABASE_NAME || "entreprise");

// Création de l'utilisateur "consultant" avec accès en lecture
db.createUser({
  user: process.env.CONSULTANT_USERNAME,
  pwd: process.env.CONSULTANT_PASSWORD,
  roles: [
    {
      role: "read",
      db: process.env.DATABASE_NAME || "entreprise"
    }
  ]
});

// Création de l'utilisateur "devs" avec accès en lecture/écriture
db.createUser({
  user: process.env.DEVS_USERNAME,
  pwd: process.env.DEVS_PASSWORD,
  roles: [
    {
      role: "readWrite",
      db: process.env.DATABASE_NAME || "entreprise"
    }
  ]
});

// Création de l'utilisateur "admin" avec accès complet
db.createUser({
  user: process.env.ADMIN_USERNAME ,
  pwd: process.env.ADMIN_PASSWORD ,
  roles: [
    {
      role: "dbOwner",
      db: process.env.DATABASE_NAME || "entreprise"
    }
  ]
});

print("Utilisateurs créés avec succès !");
