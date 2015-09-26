(function (Misago) {
  'use strict';

  var Ban = function(data) {
    this.message = {
      html: data.message.html,
      plain: data.message.plain,
    };

    this.expires_on = data.expires_on;
  };

  var deserializeBan = function(data) {
    data.expires_on = Misago.deserializeDatetime(data.expires_on);

    return new Misago.Ban(data);
  };

  Misago.addService('ban-model', function(_) {
    _.models.add('ban', {
      class: Ban,
      deserialize: deserializeBan
    });
  }, {after: 'models'});
} (Misago.prototype));
