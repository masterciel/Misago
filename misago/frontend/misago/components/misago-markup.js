(function (Misago) {
  'use strict';

  var setupMarkup = function(el, isInit, context) {
    context.retain = true;
  };

  Misago.Markup = {
    view: function(ctrl, content) {
      return m('article.misago-markup', {config: setupMarkup},
        m.trust(content)
      );
    }
  };
}(Misago.prototype));
