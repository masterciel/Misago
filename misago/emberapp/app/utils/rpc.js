import Ember from 'ember';
import getCsrfToken from 'misago/utils/csrf';
import {startsWith, endsWith} from 'misago/utils/strings';
import ENV from '../config/environment';

export function buildUrl(procedure, config) {
  if (typeof config === 'undefined') {
    config = ENV.APP;
  }

  var finalUrl = config.API_HOST;

  if (!startsWith(procedure, '/' + config.API_NAMESPACE + '/')) {
    finalUrl += '/' + config.API_NAMESPACE + '/';
  }

  finalUrl += procedure;

  if (config.API_ADD_TRAILING_SLASHES && !endsWith(procedure, '/')) {
    finalUrl += '/';
  }

  return finalUrl;
}

export function ajax(url, data) {
  return new Ember.RSVP.Promise(function(resolve, reject){
    function success(json) {
      Ember.run(null, resolve, json);
    }

    function error(jqXHR) {
      if (jqXHR.status === 200) {
        if (typeof jqXHR.responseJSON === 'undefined') {
          Ember.run(null, resolve, {});
        } else {
          Ember.run(null, resolve, jqXHR.responseJSON);
        }
      } else {
        Ember.run(null, reject, jqXHR.responseJSON);
      }
    }

    Ember.$.ajax(url, {
      type: 'POST',
      accepts: 'application/json',
      contentType: 'application/json;charset=UTF-8',
      data: JSON.stringify(data || {}),
      dataType: 'json',

      headers: {
        'X-CSRFToken': getCsrfToken()
      },

      error: error,
      success: success
    });
  }, 'RPC: ' + url);
}

export function rpc(procedure, data, config) {
  return ajax(buildUrl(procedure, config), data);
}
