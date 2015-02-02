import Ember from 'ember';

export default Ember.Route.extend({
  actions: {
    didTransition: function() {
      document.title = this.get('settings.forum_index_title') || this.get('settings.forum_name');
    }
  }
});
