!function(){"use strict";window.Misago=function(){var t=Object.getPrototypeOf(this),e=this;this.context={SETTINGS:{}},this._initServices=function(n){var r=new t.OrderedList(n).order(!1);r.forEach(function(t){var n=null;n=void 0!==t.item.factory?t.item.factory:t.item;var r=n(e);r&&(e[t.key]=r)})},this._destroyServices=function(n){var r=new t.OrderedList(n).order();r.reverse(),r.forEach(function(t){void 0!==t.destroy&&t.destroy(e)})},this.setup=!1,this.init=function(e){this.setup={fixture:t.get(e,"fixture",null),test:t.get(e,"test",!1),api:t.get(e,"api","/api/")},this._initServices(t._services)},this.destroy=function(){this._destroyServices(t._services)}};var t=window.Misago.prototype;t._services=[],t.addService=function(e,n,r){t._services.push({key:e,item:n,after:t.get(r,"after"),before:t.get(r,"before")})}}(),function(t){"use strict";t.has=function(t,e){return t?t.hasOwnProperty(e):!1},t.get=function(e,n,r){return t.has(e,n)?e[n]:void 0!==r?r:void 0},t.pop=function(e,n,r){var o=t.get(e,n,r);return t.has(e,n)&&(e[n]=null),o}}(Misago.prototype),function(t){"use strict";t.OrderedList=function(e){this.isOrdered=!1,this._items=e||[],this.add=function(e,n,r){this._items.push({key:e,item:n,after:t.get(r,"after"),before:t.get(r,"before")})},this.get=function(t,e){for(var n=0;n<this._items.length;n++)if(this._items[n].key===t)return this._items[n].item;return e},this.has=function(t){return void 0!==this.get(t)},this.values=function(){for(var t=[],e=0;e<this._items.length;e++)t.push(this._items[e].item);return t},this.order=function(t){return this.isOrdered||(this._items=this._order(this._items),this.isOrdered=!0),t||"undefined"==typeof t?this.values():this._items},this._order=function(t){function e(t){var e=-1;-1===o.indexOf(t.key)&&(t.after?(e=o.indexOf(t.after),-1!==e&&(e+=1)):t.before&&(e=o.indexOf(t.before)),-1!==e&&(r.splice(e,0,t),o.splice(e,0,t.key)))}var n=[];t.forEach(function(t){n.push(t.key)});var r=[],o=[];t.forEach(function(t){t.after||t.before||(r.push(t),o.push(t.key))}),t.forEach(function(t){"_end"===t.before&&(r.push(t),o.push(t.key))});for(var i=200;i>0&&n.length!==o.length;)i-=1,t.forEach(e);return r}}}(Misago.prototype),function(t){t.serializeDatetime=function(t){return t?t.format():null},t.deserializeDatetime=function(t){return t?moment(t):null}}(Misago.prototype),function(t){"use strict";t.startsWith=function(t,e){return 0===t.indexOf(e)},t.endsWith=function(t,e){return-1!==t.indexOf(e,t.length-e.length)}}(Misago.prototype),function(t){"use strict";t.UrlConfInvalidComponentError=function(t){this.message="route's "+t+" component should be an array or object",this.toString=function(){return this.message}},t.UrlConf=function(){var e=this;this._patterns=[],this.patterns=function(){return this._patterns};var n=function(t,e){return(t+e).replace("//","/")},r=function(t,r){for(var o=0;o<r.length;o++)e.url(n(t,r[o].pattern),r[o].component,r[o].name)};this.url=function(e,n,o){if("object"!=typeof n)throw new t.UrlConfInvalidComponentError(o);""===e&&(e="/"),n instanceof t.UrlConf?r(e,n.patterns()):this._patterns.push({pattern:e,component:n,name:o})}}}(Misago.prototype),function(t){"use strict";t.loadingPage=function(e){return m(".page.page-loading",e.component(t.Loader))}}(Misago.prototype),function(t){"use strict";var e=function(e){if(-1!==document.cookie.indexOf(e)){var n=new RegExp(e+"=([^;]*)"),r=t.get(document.cookie.match(n),0);return r.split("=")[1]}return null},n=function(n){this.csrfToken=e(n.context.CSRF_COOKIE_NAME);var r={};this.ajax=function(e,n,o,i){var s=m.deferred(),a={url:n,method:e,headers:{"X-CSRFToken":this.csrfToken},data:o|{},dataType:"json",success:function(o){"GET"===e&&t.pop(r,n),s.resolve(o)},error:function(o){"GET"===e&&t.pop(r,n);var i=o.responseJSON||{};i.status=o.status,i.statusText=o.statusText,s.reject(i)}};return i?void 0:($.ajax(a),s.promise)},this.get=function(e){var o=t.pop(n.context,e);if(o){var i=m.deferred();return i.resolve(o),i.promise}return void 0!==r[e]?r[e]:(r[e]=this.ajax("GET",e),r[e])},this.post=function(t,e){return this.ajax("POST",t,e)},this.patch=function(t,e){return this.ajax("PATCH",t,e)},this.put=function(t,e){return this.ajax("PUT",t,e)},this["delete"]=function(t){return this.ajax("DELETE",t)}};t.addService("ajax",function(t){return new n(t)})}(Misago.prototype),function(t){"use strict";var e=function(t){if("object"==typeof t){var e=[];for(var n in t)if(t.hasOwnProperty(n)){var r=encodeURIComponent(n),o=encodeURIComponent(t[n]);e.push(r+"="+o)}return"?"+e.join("&")}return t+"/"},n=function(t,r){this.url=r.url||t.setup.api,this.url+=r.path?r.path+"/":r.related?r.related+"/":r.model+"s/",r.filters&&(this.url+=e(r.filters)),!r.url&&r.filters&&(r.model&&(this.related=function(e,o){return new n(t,{url:this.url,relation:r.model,related:e,filters:o})}),this.endpoint=function(e,r){return new n(t,{url:this.url,path:e,filters:r})}),this.get=function(){var e=null;return r.related?e=r.relation+":"+r.related:r.model&&(e=r.model),t.ajax.get(this.url).then(function(n){return e?n.results?(n.results.map(function(n){return t.models["new"](e,n)}),n):t.models["new"](e,n):n})},this.post=function(e){return t.ajax.post(this.url,e)},this.patch=function(e){return t.ajax.patch(this.url,e)},this.put=function(e){return t.ajax.put(this.url,e)},this["delete"]=function(){return t.ajax["delete"](this.url)},this.then=function(t,e){return this.get().then(t,e)}},r=function(t){this.model=function(e,r){return new n(t,{model:e,filters:r})},this.endpoint=function(e,r){return new n(t,{path:e,filters:r})}};t.addService("api",function(t){return new r(t)})}(Misago.prototype),function(t){"use strict";t.addService("component-factory",function(t){t.component=function(){for(var e=[],n=0;n<arguments.length;n+=1)e.push(arguments[n]);return e.push(t),m.component.apply(void 0,e)}})}(Misago.prototype),function(t){"use strict";t.addService("conf",function(e){e.settings=t.get(e.context,"SETTINGS",{})})}(Misago.prototype),function(t){"use strict";t.addService("forum-layout",{factory:function(e){e.setup.fixture&&m.mount(document.getElementById(e.setup.fixture),e.component(t.ForumLayout))},destroy:function(t){t.setup.fixture&&m.mount(document.getElementById(t.setup.fixture),null)}},{before:"start-routing"})}(Misago.prototype),function(t){"use strict";var e=function(t){var e=this,n=document.getElementById("misago-modal"),r="click.misago-modal";$(n).on(r,"a",function(){e.hide()}),this.destroy=function(){$(n).off(r)};var o=$(n).modal({show:!1});this.open=!1,o.on("hidden.bs.modal",function(){e.open&&(m.mount(n,null),this.open=!1)}),this.show=function(e){this.open=!0,m.mount(n,t.component(e)),o.modal("show")},this.hide=function(){o.modal("hide")}};t.addService("modal",{factory:function(t){return new e(t)},destroy:function(t){t.modal.destroy()}},{after:"start-routing"})}(Misago.prototype),function(t){"use strict";var e=function(){this.classes={},this.deserializers={},this.relations={},this.add=function(t,e){if(e["class"]&&(this.classes[t]=e["class"]),e.deserialize&&(this.deserializers[t]=e.deserialize),e.relations)for(var n in e.relations)e.relations.hasOwnProperty(n)&&(this.relations[t+":"+n]=e.relations[n])},this["new"]=function(t,e){return this.classes[t]?new this.classes[t](e):e},this.deserialize=function(t,e){return this.relations[t]&&(t=this.relations[t]),this.deserializers[t]?this["new"](t,this.deserializers[t](e,this)):this["new"](t,e)}};t.addService("models",function(){return new e})}(Misago.prototype),function(t){"use strict";t.addService("set-momentjs-locale",function(){moment.locale($("html").attr("lang"))})}(Misago.prototype),function(t){"use strict";var e=function(){};t.route=function(n){n.isActive=!0;var r=n.controller||e;if(n.controller=function(){n.isActive=!0;var t=r.apply(n,arguments)||{},o=t.onunload||e;return t.onunload=function(){o.apply(n,arguments),n.isActive=!1},t},n.vm&&n.vm.init){var o=n.vm.init;n.vm.init=function(){var t=arguments,e=o.apply(n.vm,t);e&&e.then(function(){if(n.isActive&&n.vm.ondata){for(var e=[],r=0;r<arguments.length;r++)e.push(arguments[r]);for(var o=0;o<t.length;o++)e.push(t[o]);n.vm.ondata.apply(n.vm,e)}},function(t){n.isActive&&n.container.router.errorPage(t)})},n.loading||(n.loading=function(){var e=this.container;return m(".page.page-loading",e.component(t.Loader))});var i=n.view;n.view=function(){return n.vm.isReady?i.apply(n,arguments):n.loading.apply(n,arguments)}}return n}}(Misago.prototype),function(t){"use strict";var e=function(e){var n=this;this.baseUrl=$("base").attr("href");var r=t.get(e.context,"STATIC_URL","/"),o=t.get(e.context,"MEDIA_URL","/");this.urls={},this.reverses={};var i=function(t){return t.container=e,t},s=function(t){t.patterns().forEach(function(t){var e=n.baseUrl+t.pattern;e=e.replace("//","/"),n.urls[e]=i(t.component),n.reverses[t.name]=e})};this.startRouting=function(t,n){s(t),this.fixture=n,m.route.mode=e.setup.test?"search":"pathname",m.route(n,"/",this.urls)},this.url=function(t){return this.reverses[t]},this.delegateElement=null,this.cleanUrl=function(t){if(t){var e="/"===t.substr(0,1)&&"//"!==t.substr(0,2);if(!e){var n=window.location;if("//"!==t.substr(0,2)){var i=t.substr(0,n.protocol.length+2);if(i!==n.protocol+"//")return;t=t.substr(n.protocol.length+2)}else t=t.substr(2);if(t.substr(0,n.host.length)!==n.host)return;t=t.substr(n.host.length)}if(t.substr(0,this.baseUrl.length)===this.baseUrl&&t.substr(0,r.length)!==r&&t.substr(0,o.length)!==o){var s="/user-avatar/";if(t.substr(0,s.length)!==s)return t}}};var a="click.misago-router";this.delegateClicks=function(t){this.delegateElement=t,$(this.delegateElement).on(a,"a",function(t){var e=n.cleanUrl(t.target.href);e&&(e!=m.route()&&m.route(e),t.preventDefault())})},this.destroy=function(){$(this.delegateElement).off(a)};var u=function(t){return function(e){return t+e}};this.staticUrl=u(r),this.mediaUrl=u(o),this.error403=function(n){var r=null;n.ban?(r=i(t.ErrorBannedRoute),r.error={message:n.detail,ban:e.models.deserialize("ban",n.ban)}):(r=i(t.Error403Route),r.error=n.detail),m.mount(this.fixture,r)},this.error404=function(){m.mount(this.fixture,i(t.Error404Route))},this.error500=function(){m.mount(this.fixture,i(t.Error500Route))},this.error0=function(){m.mount(this.fixture,i(t.Error0Route))},this.errorPage=function(t){0===t.status&&this.error0(),500===t.status&&this.error500(),404===t.status&&this.error404(),403===t.status&&this.error403(t)}};t.addService("router",function(t){return new e(t)}),t.addService("start-routing",function(e){e.router.startRouting(t.urls,document.getElementById("router-fixture")),e.router.delegateClicks(document.getElementById(e.setup.fixture))},{before:"_end"})}(Misago.prototype),function(t){"use strict";var e=function(t){var e=this;this._intervals={};var n=function(t){e._intervals[t]&&(window.clearTimeout(e._intervals[t]),e._intervals[t]=null)};this.run=function(r,o,i){this._intervals[o]=window.setTimeout(function(){n(o);var s=r(t);s!==!1&&e.run(r,o,i)},i)},this.runOnce=function(e,r,o){this._intervals[r]=window.setTimeout(function(){n(r),e(t)},o)},this.stop=function(t){for(var e in this._intervals)t&&t!==e||n(e)}};t.addService("runloop",{factory:function(t){return new e(t)},destroy:function(t){t.runloop.stop()}})}(Misago.prototype),function(t){"use strict";t.addService("start-tick",function(t){var e=m.prop();t.runloop.run(function(){m.startComputation(),e(e()+1),m.endComputation()},"tick",6e4)})}(Misago.prototype),function(t){"use strict";var e=function(t){this.set=function(e){e?this._set_complex(e):document.title=t},this._set_complex=function(e){"string"==typeof e&&(e={title:e});var n=e.title;if("undefined"!=typeof e.page&&e.page>1){var r=interpolate(gettext("page %(page)s"),{page:e.page},!0);n+=" ("+r+")"}"undefined"!=typeof e.parent&&(n+=" | "+e.parent),document.title=n+" | "+t}};t.addService("page-title",function(t){t.title=new e(t.settings.forum_name)})}(Misago.prototype),function(t){"use strict";var e=function(t){this.message={html:t.message.html,plain:t.message.plain},this.expires_on=t.expires_on},n=function(e){return e.expires_on=t.deserializeDatetime(e.expires_on),e};t.addService("ban-model",function(t){t.models.add("ban",{"class":e,deserialize:n})},{after:"models"})}(Misago.prototype),function(t){"use strict";var e=function(t){this.title=t.title,this.body=t.body,this.link=t.link};t.addService("legal-page-model",function(t){t.models.add("legal-page",{"class":e})},{after:"models"})}(Misago.prototype),function(t){"use strict";var e=function(t){var e=[m("p.lead",t.message)];return t.help&&e.push(m("p.help",t.help)),m(".page.error-page.error-"+t.code+"-page",m(".container",m(".error-panel",[m(".error-icon",m("span.material-icon",t.icon)),m(".error-message",e)])))};t.ErrorBannedRoute=t.route({controller:function(){this.container.title.set(gettext("You are banned"))},error:null,view:function(){var t=[];t.push(this.error.ban.message.html?m(".lead",m.trust(this.error.ban.message.html)):m("p.lead",this.error.message));var e=null;return e=this.error.ban.expires_on?this.error.ban.expires_on.isAfter(moment())?interpolate(gettext("This ban expires %(expires_on)s."),{expires_on:this.error.ban.expires_on.fromNow()},!0):gettext("This ban has expired."):gettext("This ban is permanent."),t.push(m("p",e)),m(".page.error-page.error-banned-page",m(".container",m(".error-panel",[m(".error-icon",m("span.material-icon","highlight_off")),m(".error-message",t)])))}}),t.Error403Route=t.route({controller:function(){this.container.title.set(gettext("Page not available"))},error:null,view:function(){return"Permission denied"===this.error&&(this.error=gettext("You don't have permission to access this page.")),e({code:403,icon:"remove_circle_outline",message:gettext("This page is not available."),help:this.error})}}),t.Error404Route=t.route({controller:function(){this.container.title.set(gettext("Page not found"))},view:function(){return e({code:404,icon:"info_outline",message:gettext("Requested page could not be found."),help:gettext("The link you followed was incorrect or the page has been moved or deleted.")})}}),t.Error500Route=t.route({controller:function(){this.container.title.set(gettext("Application error occured"))},view:function(){return e({code:500,icon:"error_outline",message:gettext("Requested page could not be displayed due to an error."),help:gettext("Please try again later or contact site staff if error persists.")})}}),t.Error0Route=t.route({controller:function(){this.container.title.set(gettext("Lost connection with application"))},view:function(){return e({code:0,icon:"sync_problem",message:gettext("Could not connect to application."),help:gettext("This may be caused by problems with your connection or application server. Please check your internet connection and refresh page if problem persists.")})}})}(Misago.prototype),function(t){"use strict";t.IndexRoute=t.route({controller:function(){var t=this.container;document.title=t.settings.forum_index_title||t.settings.forum_name;var e=m.prop(0);return{count:e,increment:function(){console.log("increment()"),e(e()+1)}}},view:function(t){return m(".container",[m("h1",["Count: ",m("strong",t.count())]),m("p","Clicky click button to increase count!."),m("p",m("button.btn.btn-primary",{onclick:t.increment},"Clicky clicky!"))])}})}(Misago.prototype),function(t){"use strict";var e=function(e,n){var r=e.replace(/_/g,"-");return t.route({controller:function(){var n=this.container;t.get(n.settings,e+"_link")?window.location=t.get(n.settings,e+"_link"):this.vm.init(this,n)},vm:{page:null,isReady:!1,init:function(t,e){return this.isReady?void e.title.set(this.title):(e.title.set(),e.api.model("legal-page",r))},ondata:function(t,e,r){m.startComputation(),t.link?window.location=t.link:(t.title=t.title||n,this.page=t,this.isReady=!0,m.endComputation(),e.isActive&&r.title.set(this.page.title))}},view:function(){var e=this.container;return m(".page.legal-page."+r+"-page",[e.component(t.PageHeader,{title:this.vm.page.title}),m(".container",e.component(t.Markup,this.vm.page.body))])}})};t.TermsOfServiceRoute=e("terms_of_service",gettext("Terms of service")),t.PrivacyPolicyRoute=e("privacy_policy",gettext("Privacy policy"))}(Misago.prototype),function(t){"use strict";var e=function(e,n,r){var o=t.get(e.settings,n+"_link");return!o&&t.get(e.settings,n)&&(o=e.router.url(n)),o?m("li",m("a",{href:o},t.get(e.settings,n+"_title",r))):null};t.FooterNav={isVisible:function(t){return-1!==[!!t.forum_footnote,!!t.terms_of_service,!!t.terms_of_service_link,!!t.privacy_policy,!!t.privacy_policy_link].indexOf(!0)},view:function(t,n){var r=[];return n.settings.forum_footnote&&r.push(m("li.forum-footnote",m.trust(n.settings.forum_footnote))),r.push(e(n,"terms_of_service",gettext("Terms of service"))),r.push(e(n,"privacy_policy",gettext("Privacy policy"))),m("ul.list-inline.footer-nav",r)}}}(Misago.prototype),function(t){"use strict";t.ForumFooter={view:function(e,n){var r=null;return t.FooterNav.isVisible(n.settings)&&(r=n.component(t.FooterNav)),m("footer.forum-footer",[m(".container",m(".footer-content",[r,n.component(t.FooterMisagoBranding)]))])}}}(Misago.prototype),function(t){"use strict";t.FooterMisagoBranding={view:function(){return m("a.misago-branding[href=http://misago-project.org]",["powered by ",m("strong","misago")])}}}(Misago.prototype),function(t){"use strict";function e(t,e,n){n.retain=!0}t.RegisterModal={view:function(){return m('.modal-dialog.modal-lg[role="document"]',{config:e},m(".modal-content",[m(".modal-header",m("h4#misago-modal-label.modal-title","Register in modal!")),m(".modal-body",[m("p","Lorem ipsum dolor met sit amet elit."),m("p",["Si vis pacem ",m("a",{href:"/"},"bellum")," sequitat."])])]))}}}(Misago.prototype),function(t){"use strict";function e(t,e,n){n.retain=!0}t.SignInModal={view:function(){return m('.modal-dialog[role="document"]',{config:e},m(".modal-content",[m(".modal-header",m("h4#misago-modal-label.modal-title","Sign in modal!")),m(".modal-body",[m("p","Lorem ipsum dolor met sit amet elit."),m("p",["Si vis pacem ",m("a",{href:"/"},"bellum")," sequitat."])])]))}}}(Misago.prototype),function(t){"use strict";t.BrandFull={view:function(t,e,n){var r=[m("img",{src:n.router.staticUrl("misago/img/site-logo.png"),alt:n.settings.forum_name})];return e&&r.push(e),m("a.navbar-brand",{href:n.router.url("index")},r)}}}(Misago.prototype),function(t){"use strict";t.DesktopForumNavbar={view:function(e,n){var r=[];return n.settings.forum_branding_display&&r.push(n.component(t.BrandFull,n.settings.forum_branding_text)),r.push(m("ul.nav.navbar-nav",[m("li",m("a",{config:m.route,href:n.router.url("index")},"Index"))])),r.push(n.component(t.NavbarGuestMenu)),m(".container.navbar-full.hidden-xs.hidden-sm",r)}}}(Misago.prototype),function(t){"use strict";t.ForumNavbar={view:function(e,n){var r=".navbar.navbar-default.navbar-static-top";return m("nav"+r+'[role="navigation"]',[n.component(t.DesktopForumNavbar)])}}}(Misago.prototype),function(t){"use strict";t.NavbarGuestMenu={view:function(e,n){return m("div.nav.guest-nav",[m("button.navbar-btn.btn.btn-default",{onclick:function(){n.modal.show(t.SignInModal)}},gettext("Sign in")),m("button.navbar-btn.btn.btn-primary",{onclick:function(){n.modal.show(t.RegisterModal)}},gettext("Register"))])}}}(Misago.prototype),function(t){"use strict";var e=function(t,e,n){n.retain=!0};t.ForumLayout={view:function(n,r){return[r.component(t.ForumNavbar),m("#router-fixture",{config:e}),r.component(t.ForumFooter),m.component(t.ForumModal)]}}}(Misago.prototype),function(t){"use strict";t.Loader={view:function(){return m(".loader.sk-folding-cube",[m(".sk-cube1.sk-cube"),m(".sk-cube2.sk-cube"),m(".sk-cube4.sk-cube"),m(".sk-cube3.sk-cube")])}},t.LoadingPage={view:function(e,n){return m(".page.loading-page",n.component(t.Loader))}}}(Misago.prototype),function(t){"use strict";var e=function(t,e,n){n.retain=!0};t.Markup={view:function(t,n){return m("article.misago-markup",{config:e},m.trust(n))}}}(Misago.prototype),function(t){"use strict";function e(t,e,n){n.retain=!0}t.ForumModal={view:function(){return m('#misago-modal.modal.fade[role="dialog"]',{config:e,tabindex:"-1","aria-labelledby":"misago-modal-label"})}}}(Misago.prototype),function(t){"use strict";t.PageHeader={view:function(t,e){return m(".page-header",m(".container",[m("h1",e.title)]))}}}(Misago.prototype),function(t,e){"use strict";var n=new e;n.url("/",t.IndexRoute,"index"),n.url("/terms-of-service/",t.TermsOfServiceRoute,"terms_of_service"),n.url("/privacy-policy/",t.PrivacyPolicyRoute,"privacy_policy"),n.url("/:rest...",t.Error404Route,"not_found"),t.urls=n}(Misago.prototype,Misago.prototype.UrlConf);
//# sourceMappingURL=/misago.js.map