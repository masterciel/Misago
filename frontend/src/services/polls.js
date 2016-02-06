export class Polls {
  init(ajax, snackbar) {
    this._ajax = ajax;
    this._snackbar = snackbar;

    this._polls = {};
  }

  start(kwargs) {
    let poolServer = () => {
      this._ajax.get(kwargs.url, kwargs.data || null).then((data) => {
        kwargs.update(data);

        this._polls[kwargs.poll] = window.setTimeout(
          poolServer, kwargs.frequency);
      }, (rejection) => {
        if (kwargs.error) {
          kwargs.error(rejection);
        } else {
          this._snackbar.apiError(rejection);
        }
      });
    };

    poolServer();
  }

  stop(pollId) {
    if (this._polls[pollId]) {
      window.clearTimeout(this._polls[pollId]);
    }
  }
}

export default new Polls();
