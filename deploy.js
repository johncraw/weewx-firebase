var client = require('/usr/local/lib/node_modules/firebase-tools');
 
client.deploy({
  project: 'weewx-sanctuary',
  token: process.env.FIREBASE_TOKEN,
  cwd: '/srv/weewx/build'
}).then(function() {
  console.log('Site was deployed.');
  process.exit();
}).catch(function(err) {
  console.log('Error in deploy.');
});
