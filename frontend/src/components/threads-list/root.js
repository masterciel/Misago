import React from 'react';
import ListEmpty from 'misago/components/threads-list/list-empty'; // jshint ignore:line
import ListReady from 'misago/components/threads-list/list-ready'; // jshint ignore:line
import ListPreview from 'misago/components/threads-list/list-preview'; // jshint ignore:line

export default class extends React.Component {
  render () {
    /* jshint ignore:start */
    if (this.props.isLoaded) {
      if (this.props.threads.length > 0) {
        return <ListReady threads={this.props.threads}
                          categories={this.props.categories}
                          list={this.props.list}
                          isBusy={this.props.isBusy} />;
      } else {
        return <ListEmpty>
          {this.props.children}
        </ListEmpty>;
      }
    } else {
      return <ListPreview />;
    }
    /* jshint ignore:end */
  }
}