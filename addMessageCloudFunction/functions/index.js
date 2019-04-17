// Cloud functions for firebase SDK to create cloud functions and setup triggers
const functions = require('firebase-functions');

// Firebase Admin SDKD to access Firebase realtime database
const admin = require('firebase-admin');

admin.initializeApp();

// Take text paremeter passed to this endpoint and insert it into
// the realtime database under path /messages/:pushId/original
exports.addMessage = functions.https.onRequest((req, res) => {
    // Grab text param
    const original = req.query.text;

    // Push new message into realtime database using firebase admin sdk
    return admin.database().ref('/messages').push({original: original}).then((snapshot) => {
        //redirect with 303, (SEE OTHER to the URL of the pushed object in firebse console)
        return res.redirect(303, snapshot.ref.toString());
    });
});

// Listens for new messages added to /messages/:pushId/original and creates an
// uppercase version of the message to /messages/:pushId/uppercase
exports.makeUppercase = functions.database.ref('/messages/{pushId}/original')
    .onCreate((snapshot, context) => {
      // Grab the current value of what was written to the Realtime Database.
      const original = snapshot.val();
      console.log('Uppercasing', context.params.pushId, original);
      const uppercase = original.toUpperCase();
      // You must return a Promise when performing asynchronous tasks inside a Functions such as
      // writing to the Firebase Realtime Database.
      // Setting an "uppercase" sibling in the Realtime Database returns a Promise.
      return snapshot.ref.parent.child('uppercase').set(uppercase);
    });

