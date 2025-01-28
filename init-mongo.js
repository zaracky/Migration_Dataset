// init-mongo.js

db = db.getSiblingDB(process.env.DATABASE_NAME || "entreprise");

// Création de l'utilisateur "consultant" avec accès en lecture
db.createUser({
  user: process.env.CONSULTANT_USERNAME || "consultant",
  pwd: process.env.CONSULTANT_PASSWORD || "consultantpassword",
  roles: [
    {
      role: "read",
      db: process.env.DATABASE_NAME || "entreprise"
    }
  ]
});

// Création de l'utilisateur "devs" avec accès en lecture/écriture
db.createUser({
  user: process.env.DEVS_USERNAME || "devs",
  pwd: process.env.DEVS_PASSWORD || "devspassword",
  roles: [
    {
      role: "readWrite",
      db: process.env.DATABASE_NAME || "entreprise"
    }
  ]
});

// Création de l'utilisateur "admin" avec accès complet
db.createUser({
  user: process.env.ADMIN_USERNAME || "adminuser",
  pwd: process.env.ADMIN_PASSWORD || "adminuserpassword",
  roles: [
    {
      role: "dbOwner",
      db: process.env.DATABASE_NAME || "entreprise"
    }
  ]
});

print("Utilisateurs créés avec succès !");