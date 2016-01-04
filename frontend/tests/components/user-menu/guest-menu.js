import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import { GuestMenu, GuestNav, CompactGuestNav } from 'misago/components/user-menu/guest-nav'; // jshint ignore:line
import misago from 'misago/index';
import dropdown from 'misago/services/mobile-navbar-dropdown';
import modal from 'misago/services/modal';
import store from 'misago/services/store';

describe("GuestMenu", function() {
  beforeEach(function() {
    window.initEmptyStore(store);
    window.initDropdown(dropdown);
    window.initModal(modal);

    misago._context = {
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    ReactDOM.render(
      <GuestMenu />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount .dropdown-menu');
    assert.ok(element.length, "component renders");
  });

  it('opens sign in modal on click', function(done) {
    window.simulateClick('#test-mount .btn-default');

    window.onElement('#modal-mount .modal-sign-in', function() {
      assert.ok(true, "sign in modal was displayed");
      done();
    });
  });
});

describe("GuestNav", function() {
  beforeEach(function() {
    window.initEmptyStore(store);
    window.initDropdown(dropdown);
    window.initModal(modal);

    misago._context = {
      'FORGOTTEN_PASSWORD_URL': '/forgotten-password/'
    };

    /* jshint ignore:start */
    ReactDOM.render(
      <GuestNav />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount .nav-guest');
    assert.ok(element.length, "component renders");
  });

  it('opens sign in modal on click', function(done) {
    window.simulateClick('#test-mount .btn-default');

    window.onElement('#modal-mount .modal-sign-in', function() {
      assert.ok(true, "sign in modal was displayed");
      done();
    });
  });
});

describe("CompactGuestNav", function() {
  beforeEach(function() {
    window.initEmptyStore(store);
    window.initDropdown(dropdown);

    /* jshint ignore:start */
    ReactDOM.render(
      <CompactGuestNav />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */
  });

  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    let element = $('#test-mount img.user-avatar');
    assert.ok(element.length, "component renders");
  });

  it('opens dropdown on click', function() {
    window.simulateClick('#test-mount button');

    let element = $('#dropdown-mount>.dropdown-menu');
    assert.ok(element.length, "component opened dropdown");
  });
});
